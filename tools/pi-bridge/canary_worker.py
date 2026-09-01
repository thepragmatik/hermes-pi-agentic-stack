#!/usr/bin/env python3
"""Phase 50 B5 — REAL Pi-style worker for the cloud canary (not fake_pi).

Speaks the same JSON-line RPC protocol as the bridge: prompt in on stdin,
typed events out on stdout, completion only on `agent_settled`.

Runs under the B4 containment profile (deny network*, deny fs escape, deny
credential reads). The cloud-model call is proxied: the worker writes a model
request to the inherited MODEL_REQ_FD and reads the response from
MODEL_RESP_FD — the bridge parent performs the actual HTTPS egress to the
pinned OpenRouter model. No API key or other credential is ever present in
the worker's environment.

Behaviors via env:
  CANARY_PROBES=1       -> also run containment escape probes, record outcomes
                           to $CANARY_OUTCOME_FILE (inside the worktree)
  CANARY_ADVERSARIAL=1  -> write a file seeded with SYNTHETIC (fake) secrets
                           and PII markers into the worktree; the bridge
                           egress scan must fail-closed block it
  CANARY_TEST_CMD       -> optional command run in the worktree after the
                           model-produced files are written (record rc only)
"""
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path


def emit(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def run_probes():
    outcomes = {}
    outside = Path(os.environ.get("CANARY_ESCAPED_PATH", "/private/tmp/canary-escape.txt"))
    try:
        outside.write_text("escape")
        outcomes["fs_escape_write"] = "succeeded"
    except OSError as e:
        outcomes["fs_escape_write"] = f"denied: {type(e).__name__}"
    try:
        socket.create_connection(("example.com", 443), timeout=3).close()
        outcomes["network_egress"] = "succeeded"
    except OSError as e:
        outcomes["network_egress"] = f"denied: {type(e).__name__}"
    cred = Path(os.environ.get("CANARY_CRED_PATH", str(Path.home() / ".ssh" / "id_ed25519")))
    try:
        cred.read_text()
        outcomes["credential_read"] = "succeeded"
    except OSError as e:
        outcomes["credential_read"] = f"denied: {type(e).__name__}"
    out = os.environ.get("CANARY_OUTCOME_FILE")
    if out:
        Path(out).write_text(json.dumps(outcomes, indent=2))
    return outcomes


def call_model(messages: list, max_tokens: int = 6000) -> dict:
    req_fd = int(os.environ["MODEL_REQ_FD"])
    resp_fd = int(os.environ["MODEL_RESP_FD"])
    with os.fdopen(os.dup(req_fd), "w") as w:
        w.write(json.dumps({"messages": messages, "max_tokens": max_tokens}) + "\n")
    with os.fdopen(os.dup(resp_fd)) as r:
        line = r.readline()
    if not line:
        return {"_proxy_error": "no_response"}
    return json.loads(line)


def extract_files(content: str) -> dict:
    """Model returns strict JSON {\"files\": {path: content}}; tolerate code fences."""
    text = content.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fence:
        text = fence.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    data = json.loads(text)
    files = data.get("files", {})
    if not isinstance(files, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in files.items()):
        raise ValueError("model output missing valid files map")
    return files


def main() -> int:
    prompt = json.loads(sys.stdin.readline() or "{}")
    objective = prompt.get("objective", "")
    acceptance = prompt.get("acceptance", [])
    emit({"type": "agent_start"})

    if os.environ.get("CANARY_PROBES") == "1":
        run_probes()

    if os.environ.get("CANARY_ADVERSARIAL") == "1":
        # SYNTHETIC markers only — these are fake values, never real credentials
        (Path.cwd() / "adversarial-payload.txt").write_text(
            "AWS_SECRET_ACCESS_KEY=FAKEwJalrXUtnFEMIfakebCYqfakebCYxhabFakeKEY\n"
            "api_key = \"sk-fake-canary-000000000000000000000000\"\n"
            "email: synthetic.canary.user@example.invalid\n"
            "ssn: 000-00-0000\n"
            "phone: +1-555-0100\n")
        emit({"type": "agent_end"})
        emit({"type": "agent_settled", "adversarial_payload_dropped": True})
        return 0

    user_msg = (
        "You are a coding worker. Mission (non-sensitive):\n"
        f"{objective}\n\nAcceptance criteria:\n" +
        "\n".join(f"- {a}" for a in acceptance) +
        '\n\nReply with STRICT JSON only, no prose: {"files": {"<relative/path>": "<full file content>"}} '
        "covering the mission and its tests. Keep paths inside the worktree.")
    files = None
    model_calls = 0
    last_err = "no_content"
    for _attempt in range(2):  # bounded: at most one model retry
        resp = call_model([{"role": "user", "content": user_msg}])
        model_calls += 1
        if resp.get("_proxy_error"):
            emit({"type": "agent_end"})
            emit({"type": "agent_settled", "model_error": resp["_proxy_error"],
                  "model_calls": model_calls, "files_written": []})
            return 1
        content = (resp.get("choices") or [{}])[0].get("message", {}).get("content")
        if not content:
            continue  # e.g. reasoning consumed the budget; bounded retry
        try:
            files = extract_files(content)
            break
        except (ValueError, json.JSONDecodeError) as e:
            last_err = type(e).__name__
    if files is None:
        emit({"type": "agent_end"})
        emit({"type": "agent_settled", "model_output_unparseable": last_err,
              "model_calls": model_calls, "files_written": []})
        return 1

    written = []
    for rel, body in files.items():
        p = (Path.cwd() / rel).resolve()
        cwd = Path.cwd().resolve()
        if cwd not in p.parents and p != cwd:  # worktree-only mutations
            emit({"type": "agent_settled", "rejected_path_escape": rel})
            return 2
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
        written.append(rel)

    test_rc = None
    test_tail = None
    cmd = os.environ.get("CANARY_TEST_CMD")
    if cmd:
        import shlex
        r = subprocess.run(shlex.split(cmd), shell=False, capture_output=True, text=True, timeout=120)
        test_rc = r.returncode
        test_tail = (r.stderr or "")[-300:]

    emit({"type": "agent_end"})
    emit({"type": "agent_settled", "files_written": written, "test_rc": test_rc,
          "model_calls": model_calls})
    rec = os.environ.get("CANARY_OUTCOME_FILE")
    if rec and Path(rec).exists():
        d = json.loads(Path(rec).read_text())
        d.update({"test_rc": test_rc, "files_written": written, "model_calls": model_calls,
                  "test_stderr_tail": test_tail})
        Path(rec).write_text(json.dumps(d, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
