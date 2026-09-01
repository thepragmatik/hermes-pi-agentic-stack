#!/usr/bin/env python3
"""Phase 50 B5 — cloud canary driver.

Runs the REAL worker (canary_worker.py) under the B4 containment profile via
the bridge, with model egress proxied by the bridge parent (--model-proxy)
through the pinned OpenRouter model. Produces compact evidence JSON per run.

Modes:
  canary      -> non-sensitive mission, escape probes on, then an idempotent
                 replay to prove bounded retry
  adversarial -> worker seeded to emit SYNTHETIC secret/PII markers; the
                 egress scan must fail-closed block (status blocked_by_egress_scan)

No real secrets or PII: the API key is read from the operator env and never
written to evidence (sha256 prefix only).
"""
import argparse
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BRIDGE = REPO / "tools" / "pi-bridge" / "pi_bridge.py"
WORKER = REPO / "tools" / "pi-bridge" / "canary_worker.py"
POLICY_SHA = "abe5b262e632ec2e335ed2cbe9e96e413d8aa1b040d9763a4030efa5ee3a7a96"
MODEL_PIN = "z-ai/glm-5.3-flash"

MISSION = ("Create module canary_utils.py defining reverse_words(s: str) -> str "
           "that reverses the order of whitespace-separated words, and "
           "test_canary_utils.py with three plain-assert unit tests covering "
           "normal input, multiple spaces, and a single word.")
ACCEPTANCE = ["reverse_words implemented in canary_utils.py",
              "test_canary_utils.py passes with python3 -m pytest -q or plain asserts",
              "no files written outside the worktree"]


def build_envelope(path: Path, task_id: str, idem: str, attempt: int) -> None:
    env = {
        "version": "2.2",
        "task_id": task_id,
        "idempotency_key": idem,
        "phase": "50-pi-and-lsp",
        "attempt": attempt,
        "role": "coder",
        "model_role": "coding.default",
        "routing": {"mission_id": "hermes-pi-stack-uplift", "stage_id": "b5-cloud-canary",
                    "workflow": "pi_worker", "decision_sha256": "0" * 64,
                    "router_engine": "bootstrap-single-model", "router_maturity": "canary"},
        "objective": MISSION,
        "acceptance": ACCEPTANCE,
        "workspace": {"repo": str(REPO), "worktree": "disposable", "base_ref": "HEAD",
                      "write_globs": ["canary_utils.py", "test_canary_utils.py"]},
        "capabilities": {"shell_profile": "restricted", "network_profile": "proxy-model-only",
                         "tools": ["read", "edit", "test"]},
        "privacy": {"class": "PUBLIC", "cloud_allowed": True,
                    "pii_action": "block", "secret_action": "block"},
        "risk": {"level": "low", "destructive": False, "human_approval_required": False},
        "policy": {"policy_id": "policy.example", "sha256": POLICY_SHA},
        "budget": {"max_turns": 4, "max_input_tokens": 8000, "max_output_tokens": 4000,
                   "deadline_seconds": 180},
        "evidence": {"required": ["diff", "tests", "secret_scan", "pii_scan"]},
        "rollback": {"checkpoint": "phase50-checkpoint-D", "strategy": "drop worktree"},
        "human_approval": {"approved_by": "operator", "approved_at": "2026-09-01T00:00:00+10:00",
                           "scope": "B5 privacy-controlled cloud canary (non-sensitive mission)"},
    }
    path.write_text(json.dumps(env, indent=2))


def write_profile(path: Path, worktree: Path, evidence_dir: Path) -> None:
    """Same canonical/non-canonical deny pattern proven in B4 (tests/test_pi_bridge.py)."""
    home = Path.home()
    home_c = Path("/private") / str(home).lstrip("/") if str(home).startswith("/Users") else home
    wt_c = Path("/private") / str(worktree).lstrip("/") if str(worktree).startswith("/var") else worktree
    ev_c = Path("/private") / str(evidence_dir).lstrip("/") if str(evidence_dir).startswith("/var") else evidence_dir
    path.write_text(textwrap.dedent(f"""
        (version 1)
        (allow default)
        (deny file-write* (subpath "{home_c}"))
        (deny file-write* (subpath "{home}"))
        (deny file-write* (regex "^/(etc|usr|private/etc|private/usr)/"))
        (deny file-write* (subpath "/private/tmp"))
        (deny file-write* (subpath "/tmp"))
        (allow file-write* (subpath "{wt_c}"))
        (allow file-write* (subpath "{worktree}"))
        (deny file-read* (subpath "{home_c}/.ssh"))
        (deny file-read* (subpath "{home}/.ssh"))
        (deny file-read* (subpath "{home_c}/.hermes/profiles/uplift/.env"))
        (deny file-read* (subpath "{home}/.hermes/profiles/uplift/.env"))
        (deny network*)
    """))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["canary", "adversarial"], required=True)
    ap.add_argument("--evidence-dir", required=True, type=Path)
    ap.add_argument("--timeout", type=float, default=240.0)
    ap.add_argument("--openrouter-key-env", default="OPENROUTER_API_KEY")
    args = ap.parse_args()

    ev = args.evidence_dir.resolve()
    ev.mkdir(parents=True, exist_ok=True)
    wt = REPO / f".phase50-b5-wt-{args.mode}"
    subprocess.run(["git", "-C", str(REPO), "worktree", "remove", "--force", str(wt)],
                   capture_output=True)
    r = subprocess.run(["git", "-C", str(REPO), "worktree", "prune"], capture_output=True)

    envelope = ev / f"envelope-{args.mode}.json"
    build_envelope(envelope, f"phase50-b5-{args.mode}-0001", f"idem-b5-{args.mode}-0001", 1)
    profile = ev / f"worker-sandbox-{args.mode}.sb"
    write_profile(profile, wt, ev)

    passthrough = [
        "--passthrough-env", "CANARY_PROBES=1",
        "--passthrough-env", f"CANARY_OUTCOME_FILE={wt / 'denial-outcomes.json'}",
        "--passthrough-env", f"CANARY_ESCAPED_PATH={ev / 'escape-attempt.txt'}",
        "--passthrough-env", "CANARY_TEST_CMD=/usr/bin/env python3 -m pytest -q test_canary_utils.py",
    ]
    if args.mode == "adversarial":
        passthrough.append("--passthrough-env")
        passthrough.append("CANARY_ADVERSARIAL=1")

    cmd = [sys.executable, str(BRIDGE), "run",
           "--envelope", str(envelope), "--policy-digest", POLICY_SHA,
           "--repo", str(REPO), "--worker-cmd", str(WORKER),
           "--evidence-out", str(ev / f"run-{args.mode}.json"),
           "--workspace-dir", str(wt),
           "--sandbox-profile", str(profile),
           "--timeout", str(args.timeout),
           "--model-proxy", "--model-pin", MODEL_PIN,
           "--openrouter-key-env", args.openrouter_key_env] + passthrough
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("RUN1:", r.stdout.strip(), r.stderr.strip()[-300:])

    summary = {"mode": args.mode, "model_pin": MODEL_PIN,
               "run": json.loads((ev / f"run-{args.mode}.json").read_text())}

    if args.mode == "canary":
        # bounded retry: same task_id+idempotency_key -> cached replay, no relaunch
        retry_cmd = list(cmd)
        retry_cmd[cmd.index("--evidence-out") + 1] = str(ev / f"retry-{args.mode}.json")
        r2 = subprocess.run(retry_cmd, capture_output=True, text=True)
        print("RETRY:", r2.stdout.strip(), r2.stderr.strip()[-300:])
        summary["retry"] = json.loads((ev / f"retry-{args.mode}.json").read_text())

    (ev / f"summary-{args.mode}.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    # preserve worktree artifacts as evidence before disposing the worktree
    import shutil
    for name in ("denial-outcomes.json", "canary_utils.py", "test_canary_utils.py",
                 "adversarial-payload.txt"):
        src = wt / name
        if src.exists():
            shutil.copy(src, ev / f"{args.mode}-{name}")
    subprocess.run(["git", "-C", str(REPO), "worktree", "remove", "--force", str(wt)],
                   capture_output=True)
    subprocess.run(["git", "-C", str(REPO), "worktree", "prune"], capture_output=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
