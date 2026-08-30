#!/usr/bin/env python3
"""Hermes local-router benchmark rig.

Designed for a Mac workstation where each router should be evaluated in a fresh
process so model/framework initialization, memory footprint, and warm routing
latency can be compared honestly.

Dataset JSONL format (one object per line):
  {"id":"r1", "text":"Investigate ...", "label":"deepseek"}

Labels used by the supplied policy:
  deepseek   research / ideation / architecture / broad synthesis
  glm        coding / terminal / implementation / tests / refactors
  hybrid     substantial planning + coding; caller should decompose
  local_only sensitive material that must not be sent to a cloud model
  abstain    router is insufficiently confident; caller escalates locally

No raw prompt text is written to result files unless --include-text is used.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import os
import platform
import re
import resource
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol

LABELS = ("deepseek", "glm", "hybrid", "local_only", "abstain")
CLOUD_LABELS = ("deepseek", "glm", "hybrid")


@dataclasses.dataclass(frozen=True)
class Sample:
    id: str
    text: str
    label: str


@dataclasses.dataclass(frozen=True)
class Prediction:
    label: str
    confidence: float | None = None
    detail: dict[str, Any] | None = None


class Router(Protocol):
    name: str

    def route(self, text: str) -> Prediction: ...


def _safe_confidence(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return max(0.0, min(1.0, float(x)))
    except (TypeError, ValueError):
        return None


def load_dataset(path: Path) -> list[Sample]:
    samples: list[Sample] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
        for key in ("id", "text", "label"):
            if key not in obj:
                raise SystemExit(f"{path}:{lineno}: missing {key!r}")
        label = str(obj["label"]).strip().lower()
        if label not in LABELS:
            raise SystemExit(f"{path}:{lineno}: unsupported label {label!r}; choose {LABELS}")
        samples.append(Sample(str(obj["id"]), str(obj["text"]), label))
    if not samples:
        raise SystemExit(f"dataset is empty: {path}")
    return samples


def _rss_mb() -> float:
    # macOS ru_maxrss is bytes; Linux is KiB.
    rss = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform == "darwin":
        return rss / (1024 * 1024)
    return rss / 1024


class RulesRouter:
    """Fast deterministic baseline and security override.

    Rules are deliberately conservative. The intended production stack runs
    these checks before any learned router, because privacy and explicit task
    declarations should not depend on probabilistic classification.
    """

    name = "rules"

    LOCAL_ONLY = re.compile(
        r"\b(local[- ]only|do not (?:upload|send|share)|never (?:upload|send|share)|"
        r"pii|personal data|passport|tax file number|tfn|ssn|private key|seed phrase|"
        r"client secret|access token|credential|production database dump)\b",
        re.I,
    )
    CODE = re.compile(
        r"\b(implement|code|fix|debug|refactor|compile|build|test|unit test|integration test|"
        r"rename symbol|edit (?:the )?file|patch|pull request|commit|typescript|javascript|"
        r"python|java|kotlin|gradle|maven|npm|pnpm|pytest|junit|stack trace|exception|"
        r"terminal|shell command|cli|api endpoint|migration)\b",
        re.I,
    )
    RESEARCH = re.compile(
        r"\b(research|investigate|compare|evaluate|architecture|strategy|ideat|brainstorm|"
        r"landscape|market|trade[- ]?off|design options|literature|survey|systems map|"
        r"root cause hypotheses|recommend|decision memo)\b",
        re.I,
    )

    def route(self, text: str) -> Prediction:
        if self.LOCAL_ONLY.search(text):
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        code = bool(self.CODE.search(text))
        research = bool(self.RESEARCH.search(text))
        if code and research:
            return Prediction("hybrid", 0.90, {"reason": "code + research indicators"})
        if code:
            return Prediction("glm", 0.93, {"reason": "coding/tool indicators"})
        if research:
            return Prediction("deepseek", 0.93, {"reason": "research/design indicators"})
        return Prediction("abstain", 0.0, {"reason": "no deterministic signal"})


PROTOTYPES: dict[str, list[str]] = {
    "deepseek": [
        "Research a technical topic deeply and synthesize competing evidence.",
        "Compare architectures, explore tradeoffs and recommend a strategy.",
        "Brainstorm product ideas and map an unfamiliar problem space.",
        "Investigate current libraries, standards, papers, vendors and approaches.",
    ],
    "glm": [
        "Implement a feature in the repository, edit files, run tests and fix failures.",
        "Debug this stack trace and patch the code using terminal tools.",
        "Refactor source code safely and use language-server diagnostics.",
        "Create tests, run the build and produce a verified code diff.",
    ],
    "hybrid": [
        "Research the right technical approach then implement and test it in the repository.",
        "Design an architecture and immediately build a production-ready implementation.",
        "Compare libraries, select one, integrate it and verify the code.",
    ],
}


class PrototypeEmbeddingRouter:
    """Cosine-to-prototypes baseline using SentenceTransformers.

    Recommended model for the target machine: Qwen/Qwen3-Embedding-0.6B.
    For a tiny smoke test, pass a smaller SentenceTransformers model.
    """

    name = "prototype"

    def __init__(self, model_name: str, threshold: float, margin: float):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "prototype router requires sentence-transformers; "
                "pip install 'sentence-transformers>=3'"
            ) from exc
        self.model_name = model_name
        self.threshold = threshold
        self.margin = margin
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
        labels, texts = [], []
        for label, examples in PROTOTYPES.items():
            for example in examples:
                labels.append(label)
                texts.append(example)
        vecs = self.model.encode(texts, normalize_embeddings=True)
        self.centroids: dict[str, Any] = {}
        for label in PROTOTYPES:
            members = [vecs[i] for i, value in enumerate(labels) if value == label]
            # avoid a mandatory numpy import in our own module; ST already returns ndarray.
            centroid = sum(members) / len(members)
            norm = math.sqrt(float((centroid * centroid).sum()))
            self.centroids[label] = centroid / max(norm, 1e-12)

    def route(self, text: str) -> Prediction:
        privacy = RulesRouter.LOCAL_ONLY.search(text)
        if privacy:
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        vec = self.model.encode([text], normalize_embeddings=True)[0]
        scores = {label: float(vec @ centroid) for label, centroid in self.centroids.items()}
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        label, score = ranked[0]
        second = ranked[1][1]
        # Cosine is not a calibrated probability. Keep the raw similarity in detail,
        # and expose a bounded confidence only for convenient threshold dashboards.
        conf = max(0.0, min(1.0, (score + 1.0) / 2.0))
        if score < self.threshold or (score - second) < self.margin:
            return Prediction("abstain", conf, {"scores": scores, "margin": score - second})
        return Prediction(label, conf, {"scores": scores, "margin": score - second})


class SemanticRouterAdapter:
    """Aurelio Semantic Router adapter with local Hugging Face encoder."""

    name = "semantic-router"

    def __init__(self, model_name: str, threshold: float):
        try:
            from semantic_router import Route
            from semantic_router.routers import SemanticRouter
            try:
                from semantic_router.encoders import HuggingFaceEncoder
            except ImportError:
                from semantic_router.encoders.huggingface import HuggingFaceEncoder  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "semantic-router adapter requires a patched/current local install; "
                "pip install 'semantic-router[local]>=0.1.16'"
            ) from exc

        try:
            encoder = HuggingFaceEncoder(name=model_name)
        except TypeError:
            encoder = HuggingFaceEncoder(model_name=model_name)
        routes = [Route(name=label, utterances=utterances) for label, utterances in PROTOTYPES.items()]
        # API names have changed across Semantic Router releases; support both common forms.
        try:
            self.router = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")
        except TypeError:
            self.router = SemanticRouter(encoder=encoder, routes=routes)
        self.threshold = threshold

    def route(self, text: str) -> Prediction:
        if RulesRouter.LOCAL_ONLY.search(text):
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        result = self.router(text)
        name = getattr(result, "name", None) or getattr(result, "route", None)
        score = getattr(result, "similarity_score", None)
        if score is None:
            score = getattr(result, "score", None)
        if not name:
            return Prediction("abstain", _safe_confidence(score), {"raw": str(result)[:500]})
        label = str(name)
        conf = _safe_confidence(score)
        if conf is not None and conf < self.threshold:
            return Prediction("abstain", conf, {"candidate": label})
        if label not in LABELS:
            return Prediction("abstain", conf, {"candidate": label})
        return Prediction(label, conf)


class ModernBERTRouter:
    """Fine-tuned local sequence-classification checkpoint adapter."""

    name = "modernbert"

    def __init__(self, checkpoint: str, threshold: float):
        if not checkpoint:
            raise RuntimeError("modernbert requires --modernbert-model PATH_OR_HF_ID")
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("modernbert requires transformers + torch") from exc
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
        self.model.eval()
        self.threshold = threshold
        self.id2label = {int(k): str(v).lower() for k, v in self.model.config.id2label.items()}

    def route(self, text: str) -> Prediction:
        if RulesRouter.LOCAL_ONLY.search(text):
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=2048)
        with self.torch.inference_mode():
            logits = self.model(**inputs).logits[0]
            probs = self.torch.softmax(logits, dim=-1)
        idx = int(probs.argmax().item())
        conf = float(probs[idx].item())
        label = self.id2label.get(idx, str(idx)).lower()
        if label not in LABELS or conf < self.threshold:
            return Prediction("abstain", conf, {"candidate": label})
        return Prediction(label, conf)


class RouteLLMDifficultyAdapter:
    """RouteLLM MF difficulty adapter.

    RouteLLM's pretrained routers are strong-vs-weak preference routers, *not*
    native research-vs-code classifiers. This adapter is intentionally exposed
    as an experiment: assign `strong_label` to the route that should receive
    high-difficulty cases, or retrain RouteLLM on actual DeepSeek-vs-GLM outcome
    pairs before production use.
    """

    name = "routellm"

    def __init__(
        self,
        strong_model: str,
        weak_model: str,
        strong_label: str,
        weak_label: str,
        threshold: float,
    ):
        try:
            from routellm.controller import Controller
        except ImportError as exc:
            raise RuntimeError("routellm adapter requires `pip install routellm`") from exc
        self.controller = Controller(
            routers=["mf"], strong_model=strong_model, weak_model=weak_model
        )
        self.strong_label = strong_label
        self.weak_label = weak_label
        self.threshold = threshold

    def route(self, text: str) -> Prediction:
        if RulesRouter.LOCAL_ONLY.search(text):
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        score = float(self.controller.calculate_strong_win_rate(prompt=text, router="mf"))
        label = self.strong_label if score >= self.threshold else self.weak_label
        confidence = score if label == self.strong_label else 1.0 - score
        return Prediction(label, confidence, {"strong_win_rate": score})


class ExternalJSONRouter:
    """Generic adapter for academic/custom routers.

    The command is invoked once per classification and receives the text on
    stdin. It must return one JSON object: {"label":"glm","confidence":0.9}.
    This intentionally makes it easy to test a Rust/Swift/ONNX daemon, a custom
    logic gate, or a RouteLLM service without coupling this benchmark to its API.
    """

    def __init__(self, name: str, command: str):
        self.name = name
        self.command = command

    def route(self, text: str) -> Prediction:
        if RulesRouter.LOCAL_ONLY.search(text):
            return Prediction("local_only", 1.0, {"reason": "privacy/security rule"})
        cp = subprocess.run(
            self.command,
            input=text,
            text=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
        if cp.returncode != 0:
            raise RuntimeError(f"external router failed ({cp.returncode}): {cp.stderr[-1000:]}")
        obj = json.loads(cp.stdout)
        label = str(obj["label"]).lower()
        if label not in LABELS:
            label = "abstain"
        return Prediction(label, _safe_confidence(obj.get("confidence")), obj.get("detail"))


def make_router(name: str, args: argparse.Namespace) -> Router:
    if name == "rules":
        return RulesRouter()
    if name == "prototype":
        return PrototypeEmbeddingRouter(args.embedding_model, args.embedding_threshold, args.embedding_margin)
    if name == "semantic-router":
        return SemanticRouterAdapter(args.semantic_model, args.semantic_threshold)
    if name == "modernbert":
        return ModernBERTRouter(args.modernbert_model, args.modernbert_threshold)
    if name == "routellm":
        return RouteLLMDifficultyAdapter(
            args.routellm_strong_model,
            args.routellm_weak_model,
            args.routellm_strong_label,
            args.routellm_weak_label,
            args.routellm_threshold,
        )
    for spec in args.external or []:
        ext_name, sep, command = spec.partition("=")
        if sep and ext_name == name:
            return ExternalJSONRouter(ext_name, command)
    raise RuntimeError(f"unknown router {name!r}")


def percentile(xs: list[float], p: float) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    k = (len(ys) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - k) + ys[hi] * (k - lo)


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    # Accuracy is on every repeated row. F1 is macro across expected production labels,
    # with abstain treated as an error unless the reference label itself is abstain.
    expected_labels = sorted({r["expected"] for r in rows})
    correct = sum(r["expected"] == r["predicted"] for r in rows)
    per_label: dict[str, dict[str, float]] = {}
    f1s: list[float] = []
    for label in expected_labels:
        tp = sum(r["expected"] == label and r["predicted"] == label for r in rows)
        fp = sum(r["expected"] != label and r["predicted"] == label for r in rows)
        fn = sum(r["expected"] == label and r["predicted"] != label for r in rows)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        f1s.append(f1)
        per_label[label] = {"precision": precision, "recall": recall, "f1": f1}

    lat = [float(r["latency_ms"]) for r in rows]
    by_id: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        by_id[row["id"]].append(row["predicted"])
    deterministic = sum(len(set(values)) == 1 for values in by_id.values()) / len(by_id)
    dangerous = sum(
        r["expected"] == "local_only" and r["predicted"] in CLOUD_LABELS for r in rows
    )
    code_to_research = sum(
        r["expected"] == "glm" and r["predicted"] == "deepseek" for r in rows
    )
    research_to_code = sum(
        r["expected"] == "deepseek" and r["predicted"] == "glm" for r in rows
    )
    return {
        "accuracy": correct / len(rows),
        "macro_f1": statistics.mean(f1s) if f1s else 0.0,
        "abstain_rate": sum(r["predicted"] == "abstain" for r in rows) / len(rows),
        "determinism_rate": deterministic,
        "latency_ms": {
            "mean": statistics.mean(lat),
            "p50": percentile(lat, 0.50),
            "p95": percentile(lat, 0.95),
            "p99": percentile(lat, 0.99),
        },
        "high_severity_errors": {
            "local_only_to_cloud": dangerous,
            "glm_to_deepseek": code_to_research,
            "deepseek_to_glm": research_to_code,
        },
        "per_label": per_label,
        "confusion": confusion(rows),
    }


def confusion(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for expected in LABELS:
        bucket = Counter(r["predicted"] for r in rows if r["expected"] == expected)
        if bucket:
            out[expected] = {label: int(bucket.get(label, 0)) for label in LABELS}
    return out


def benchmark_one(name: str, args: argparse.Namespace) -> dict[str, Any]:
    samples = load_dataset(Path(args.dataset))
    before_mb = _rss_mb()
    t0 = time.perf_counter()
    router = make_router(name, args)
    startup_ms = (time.perf_counter() - t0) * 1000
    after_load_mb = _rss_mb()

    # Warmup separate from measured passes.
    for sample in samples[: max(0, args.warmup)]:
        router.route(sample.text)

    rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for repeat in range(args.repeat):
        for sample in samples:
            started = time.perf_counter_ns()
            try:
                pred = router.route(sample.text)
            except Exception as exc:  # benchmark should report a broken adapter rather than silently die
                pred = Prediction("abstain", 0.0, {"error": f"{type(exc).__name__}: {exc}"})
                failures.append({"id": sample.id, "error": f"{type(exc).__name__}: {exc}"})
            elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
            row: dict[str, Any] = {
                "id": sample.id,
                "repeat": repeat,
                "expected": sample.label,
                "predicted": pred.label,
                "confidence": pred.confidence,
                "latency_ms": elapsed_ms,
                "text_sha256": hashlib.sha256(sample.text.encode()).hexdigest(),
            }
            if args.include_text:
                row["text"] = sample.text
            if args.include_detail and pred.detail is not None:
                row["detail"] = pred.detail
            rows.append(row)

    return {
        "router": name,
        "dataset": str(Path(args.dataset).resolve()),
        "samples": len(samples),
        "repeat": args.repeat,
        "startup_ms": startup_ms,
        "max_rss_mb_before": before_mb,
        "max_rss_mb_after_load": after_load_mb,
        "max_rss_mb_end": _rss_mb(),
        "metrics": metrics(rows),
        "failures": failures[:100],
        "rows": rows,
    }


def child_args(argv: list[str], router: str) -> list[str]:
    # Reconstruct all user options while stripping parent-only switches.
    out = [sys.executable, str(Path(__file__).resolve())]
    skip_next = False
    i = 0
    while i < len(argv):
        token = argv[i]
        if token in ("--routers", "--output", "--child-router"):
            i += 2
            continue
        if token in ("--in-process", "--pretty"):
            i += 1
            continue
        out.append(token)
        i += 1
    out += ["--child-router", router]
    return out


def run_isolated(router_names: list[str], args: argparse.Namespace, original_argv: list[str]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for name in router_names:
        started = time.perf_counter()
        cp = subprocess.run(
            child_args(original_argv, name),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        wall_ms = (time.perf_counter() - started) * 1000
        if cp.returncode != 0:
            results.append({
                "router": name,
                "fatal_error": cp.stderr.strip() or cp.stdout.strip(),
                "process_wall_ms": wall_ms,
            })
            continue
        try:
            result = json.loads(cp.stdout)
        except json.JSONDecodeError:
            results.append({
                "router": name,
                "fatal_error": "child did not emit JSON",
                "stdout": cp.stdout[-2000:],
                "stderr": cp.stderr[-2000:],
                "process_wall_ms": wall_ms,
            })
            continue
        result["process_wall_ms"] = wall_ms
        if cp.stderr.strip():
            result["child_stderr_tail"] = cp.stderr[-2000:]
        results.append(result)
    return envelope(results, args)


def envelope(results: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at_epoch": time.time(),
        "host": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "machine": platform.machine(),
        },
        "privacy": {
            "raw_text_included": bool(args.include_text),
            "note": "Result rows use prompt SHA-256 by default; do not use a sensitive dataset with third-party routers without the egress policy gate.",
        },
        "results": results,
    }


def print_summary(doc: dict[str, Any]) -> None:
    headers = ("router", "acc", "macro-F1", "abstain", "p50 ms", "p95 ms", "startup ms", "RSS MB", "fatal")
    print("\t".join(headers), file=sys.stderr)
    for r in doc["results"]:
        if "fatal_error" in r:
            print(f"{r['router']}\t-\t-\t-\t-\t-\t-\t-\t{r['fatal_error'][:80]}", file=sys.stderr)
            continue
        m = r["metrics"]
        print(
            "\t".join([
                r["router"],
                f"{m['accuracy']:.3f}",
                f"{m['macro_f1']:.3f}",
                f"{m['abstain_rate']:.3f}",
                f"{m['latency_ms']['p50']:.2f}",
                f"{m['latency_ms']['p95']:.2f}",
                f"{r['startup_ms']:.0f}",
                f"{r['max_rss_mb_end']:.1f}",
                "",
            ]),
            file=sys.stderr,
        )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dataset", required=True, help="JSONL benchmark dataset")
    p.add_argument("--routers", default="rules,prototype,semantic-router", help="comma-separated router names")
    p.add_argument("--repeat", type=int, default=5, help="measured repetitions")
    p.add_argument("--warmup", type=int, default=3, help="number of sample routes before measurement")
    p.add_argument("--output", help="write combined JSON results here")
    p.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    p.add_argument("--include-text", action="store_true", help="DANGEROUS: store raw prompt text in results")
    p.add_argument("--include-detail", action="store_true", help="include router score details")
    p.add_argument("--in-process", action="store_true", help="do not isolate routers in fresh processes")
    p.add_argument("--child-router", help=argparse.SUPPRESS)

    p.add_argument("--embedding-model", default=os.getenv("ROUTER_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B"))
    p.add_argument("--embedding-threshold", type=float, default=0.35)
    p.add_argument("--embedding-margin", type=float, default=0.03)
    p.add_argument("--semantic-model", default=os.getenv("SEMANTIC_ROUTER_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
    p.add_argument("--semantic-threshold", type=float, default=0.50)
    p.add_argument("--modernbert-model", default=os.getenv("MODERNBERT_ROUTER_MODEL", ""))
    p.add_argument("--modernbert-threshold", type=float, default=0.65)

    p.add_argument("--routellm-strong-model", default=os.getenv("ROUTELLM_STRONG_MODEL", "gpt-4-1106-preview"))
    p.add_argument("--routellm-weak-model", default=os.getenv("ROUTELLM_WEAK_MODEL", "mixtral-8x7b-instruct-v0.1"))
    p.add_argument("--routellm-strong-label", choices=LABELS, default="deepseek")
    p.add_argument("--routellm-weak-label", choices=LABELS, default="glm")
    p.add_argument("--routellm-threshold", type=float, default=0.5)
    p.add_argument(
        "--external",
        action="append",
        help="custom adapter NAME='command'; command reads prompt on stdin and returns JSON",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    p = parser()
    args = p.parse_args(argv)
    if args.repeat < 1:
        p.error("--repeat must be >= 1")

    if args.child_router:
        result = benchmark_one(args.child_router, args)
        print(json.dumps(result, separators=(",", ":"), default=str))
        return 0

    names = [x.strip() for x in args.routers.split(",") if x.strip()]
    if not names:
        p.error("--routers is empty")
    if args.in_process:
        doc = envelope([benchmark_one(name, args) for name in names], args)
    else:
        doc = run_isolated(names, args, argv)

    print_summary(doc)
    text = json.dumps(doc, indent=2 if args.pretty else None, default=str)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
