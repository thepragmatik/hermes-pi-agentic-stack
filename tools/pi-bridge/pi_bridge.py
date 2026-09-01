#!/usr/bin/env python3
"""Phase 50 — Hermes -> Pi typed task bridge (B2/B3/B5).

Stdlib-only core (jsonschema used only for envelope validation, matching
tools/validate_state.py precedent). Local pipe/stdin/stdout RPC only — the
bridge never opens a network listener. Completion = `agent_settled`
(`agent_end` alone is insufficient). Evidence is compact and typed: event
names, hashes and exit codes only; raw RPC streams are never mirrored.

Subcommands:
  validate  --envelope E.json --policy-digest SHA
  run       --envelope E.json --policy-digest SHA --repo REPO
            --evidence-out OUT.json [--worker-cmd PATH] [--sandbox-profile P]
            [--timeout S] [--offline]

`--worker-cmd` points at a pinned Pi entrypoint (e.g. `pi`) or a fake-RPC
fixture for offline qualification. `--sandbox-profile` supplies the external
containment profile (B4); when given, the worker runs under
`sandbox-exec -f <profile>` so denied filesystem/network/credential actions
fail structurally outside the model.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
ENVELOPE_SCHEMA = REPO_ROOT / "protocols" / "pi-task-envelope.schema.json"
SECURITY_GATE = REPO_ROOT / "tools" / "security-gate" / "security_gate.py"

ENV_ALLOWLIST = ("PATH", "LANG", "LC_ALL", "TMPDIR", "SHELL", "TERM")


class BridgeError(Exception):
    pass


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_and_validate_envelope(path: Path, policy_digest: str) -> dict:
    from jsonschema import Draft202012Validator

    env = json.loads(path.read_text())
    schema = json.loads(ENVELOPE_SCHEMA.read_text())
    errs = sorted(Draft202012Validator(schema).iter_errors(env), key=lambda e: e.path)
    if errs:
        raise BridgeError("envelope invalid: " + "; ".join(
            f"{list(e.path)}: {e.message}" for e in errs[:5]))
    if env["policy"]["sha256"] != policy_digest:
        raise BridgeError(
            f"policy digest mismatch: envelope {env['policy']['sha256'][:12]} != live {policy_digest[:12]}")
    if env["privacy"]["class"] == "LOCAL_ONLY" and env["privacy"]["cloud_allowed"]:
        raise BridgeError("LOCAL_ONLY envelope claims cloud_allowed=true")
    return env


def scrub_env(offline: bool, passthrough=None) -> dict:
    """Environment minimization: allowlist only; never forward credentials.
    `passthrough` items (`NAME=VALUE`) are explicit, operator-controlled
    additions (fixture knobs), each recorded in evidence."""
    env = {k: os.environ[k] for k in ENV_ALLOWLIST if k in os.environ}
    env.setdefault("PATH", "/usr/bin:/bin")
    if offline:
        env["PI_OFFLINE"] = "1"
    for item in passthrough or []:
        k, _, v = item.partition("=")
        if k:
            env[k] = v
    return env


class IdempotencyLedger:
    """task_id + idempotency_key dedupe. Duplicate COMPLETED keys return the
    cached record without relaunching the worker (destructive-retry proof)."""

    def __init__(self, ledger_path: Path):
        self.path = ledger_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data = {}
        if self.path.exists():
            self.data = json.loads(self.path.read_text())

    def lookup(self, task_id: str, idem: str):
        return self.data.get(task_id) if self.data.get(task_id, {}).get("idempotency_key") == idem else None

    def record(self, task_id: str, idem: str, record: dict):
        self.data[task_id] = dict(record, idempotency_key=idem)
        self.path.write_text(json.dumps(self.data, indent=2, sort_keys=True))


def make_worktree(repo: Path, base_ref: str, wt_path: Path) -> None:
    wt_path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "-C", str(repo), "worktree", "add", "--detach",
                        str(wt_path), base_ref], capture_output=True, text=True)
    if r.returncode != 0:
        raise BridgeError(f"worktree creation failed: {r.stderr.strip()[:200]}")


def run_worker(env: dict, envelope: dict, wt: Path, worker_cmd: str,
               sandbox_profile: Optional[str], timeout: float) -> dict:
    """Launch worker with pipe stdin/stdout only; complete on agent_settled."""
    prompt = json.dumps({
        "type": "prompt",
        "objective": envelope["objective"],
        "acceptance": envelope["acceptance"],
        "workspace": {**envelope["workspace"], "worktree": str(wt)},
    })
    cmd = []
    if sandbox_profile:
        cmd += ["sandbox-exec", "-f", sandbox_profile]
    if os.access(worker_cmd, os.X_OK):
        cmd += [worker_cmd]
    else:  # pinned script entrypoint: run under the bridge's interpreter
        cmd += [sys.executable, worker_cmd]
    events: list[str] = []
    settled = False
    timed_out = False
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=env, cwd=str(wt), text=True)
    except OSError as e:
        raise BridgeError(f"worker launch failed: {e}")
    try:
        assert proc.stdin is not None and proc.stdout is not None  # pipes are wired above
        proc.stdin.write(prompt + "\n")
        proc.stdin.close()
        deadline = time.monotonic() + timeout
        while True:
            line = proc.stdout.readline()
            if line == "":  # worker exited without settling
                break
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                events.append("malformed_framing")
                continue
            t = evt.get("type")
            if t and t not in events:
                events.append(t)
            if t == "agent_settled":
                settled = True
                break
            if time.monotonic() > deadline:
                timed_out = True
                break
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=10)
    return {"events": events, "agent_settled": settled, "timed_out": timed_out,
            "worker_rc": proc.returncode,
            "stderr_tail": (proc.stderr.read() or "")[-400:] if proc.stderr else ""}


def egress_scan(diff_text: str, evidence_dir: Path) -> dict:
    """Fail-closed secret/PII scan of the worker diff via the Phase-40 gate."""
    payload = evidence_dir / "worker-diff-payload.txt"
    payload.write_text(diff_text)
    r = subprocess.run([sys.executable, str(SECURITY_GATE), "scan", str(payload)],
                       capture_output=True, text=True)
    try:
        detail = json.loads(r.stdout) if r.stdout.strip() else {}
    except json.JSONDecodeError:
        detail = {"raw_stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest()[:16]}
    return {"rc": r.returncode, "detail": detail}


def diff_worktree(wt: Path) -> str:
    r = subprocess.run(["git", "-C", str(wt), "diff"], capture_output=True, text=True)
    out = [r.stdout or ""]
    u = subprocess.run(["git", "-C", str(wt), "ls-files", "--others", "--exclude-standard"],
                       capture_output=True, text=True)
    for rel in u.stdout.split():
        f = wt / rel
        if f.is_file():
            out.append(f"\n--- untracked: {rel} ---\n" + f.read_text(errors="replace"))
    return "\n".join(out)


def cmd_run(args) -> int:
    env_path = Path(args.envelope)
    live_digest = args.policy_digest
    envelope = load_and_validate_envelope(env_path, live_digest)
    evidence_dir = Path(args.evidence_out).parent
    evidence_dir.mkdir(parents=True, exist_ok=True)
    ledger = IdempotencyLedger(evidence_dir / "bridge-ledger.json")

    task_id = envelope["task_id"]
    idem = envelope["idempotency_key"]
    cached = ledger.lookup(task_id, idem)
    if cached:
        record = {**cached, "cached": True, "status": "idempotent_replay"}
        Path(args.evidence_out).write_text(json.dumps(record, indent=2, sort_keys=True))
        print(json.dumps({"result": "idempotent_replay", "task_id": task_id}))
        return 0

    repo = Path(args.repo).resolve()
    wt = Path(args.workspace_dir).resolve()
    if wt.exists():
        raise BridgeError(f"workspace path already exists (must be disposable): {wt}")
    make_worktree(repo, envelope["workspace"]["base_ref"], wt)

    base_env = scrub_env(offline=args.offline or envelope["capabilities"]["network_profile"] == "none")
    worker_env = dict(base_env)
    for item in args.passthrough_env:
        k, _, v = item.partition("=")
        if k:
            worker_env[k] = v
    env_secret_candidates = sorted(
        k for k in os.environ
        if k not in ENV_ALLOWLIST and any(s in k.upper() for s in ("KEY", "TOKEN", "SECRET", "PASSWORD", "AUTH")))
    result = {
        "task_id": task_id, "attempt": envelope["attempt"],
        "policy_sha256": live_digest, "worktree": str(wt),
        "containment_profile": args.sandbox_profile or None,
        "env_keys_forwarded": sorted(base_env),
        "env_secret_candidates_blocked": env_secret_candidates,
        "passthrough_env_keys": sorted(i.partition("=")[0] for i in args.passthrough_env),
    }
    try:
        result["rpc"] = run_worker(worker_env, envelope, wt, args.worker_cmd,
                                   args.sandbox_profile, args.timeout)
        diff = diff_worktree(wt)
        result["diff_sha256"] = hashlib.sha256(diff.encode()).hexdigest() if diff else None
        result["egress_scan"] = egress_scan(diff, evidence_dir)
        result["merge_executed"] = False  # structural: bridge never merges; worker cannot merge or self-approve
        if not result["rpc"]["agent_settled"]:
            result["status"] = "timeout_or_unsettled" if result["rpc"]["timed_out"] else "not_settled"
        elif result["egress_scan"]["rc"] not in (0, 2):
            result["status"] = "egress_scan_internal_error"
        elif result["egress_scan"]["rc"] == 2:
            result["status"] = "blocked_by_egress_scan"
        else:
            result["status"] = "settled_clean"
    finally:
        ledger.record(task_id, idem, {"status": result.get("status", "incomplete"),
                                      "diff_sha256": result.get("diff_sha256")})
        Path(args.evidence_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"result": result["status"], "task_id": task_id}))
    return 0 if result["status"] in ("settled_clean", "idempotent_replay",
                                     "blocked_by_egress_scan", "timeout_or_unsettled") else 1


def cmd_validate(args) -> int:
    envelope = load_and_validate_envelope(Path(args.envelope), args.policy_digest)
    print(json.dumps({"envelope_valid": True, "task_id": envelope["task_id"]}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Hermes->Pi typed task bridge (Phase 50)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--envelope", required=True)
    v.add_argument("--policy-digest", required=True)
    v.set_defaults(fn=cmd_validate)
    r = sub.add_parser("run")
    r.add_argument("--envelope", required=True)
    r.add_argument("--policy-digest", required=True)
    r.add_argument("--repo", required=True)
    r.add_argument("--worker-cmd", required=True)
    r.add_argument("--evidence-out", required=True)
    r.add_argument("--workspace-dir", required=True)
    r.add_argument("--sandbox-profile")
    r.add_argument("--timeout", type=float, default=120.0)
    r.add_argument("--offline", action="store_true")
    r.add_argument("--passthrough-env", action="append", default=[],
                   metavar="NAME=VALUE", help="explicit operator-controlled worker env addition")
    r.set_defaults(fn=cmd_run)
    args = ap.parse_args()
    try:
        return args.fn(args)
    except BridgeError as e:
        print(json.dumps({"result": "bridge_error", "error": str(e)}))
        return 3


if __name__ == "__main__":
    sys.exit(main())
