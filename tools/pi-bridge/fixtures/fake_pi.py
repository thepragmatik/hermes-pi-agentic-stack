#!/usr/bin/env python3
"""Fake Pi worker for offline bridge qualification (B3 fixtures).

Speaks JSON-line RPC on stdin/stdout. Behavior selected via FAKE_BEHAVIOR:
  happy       -> agent_end, then agent_settled (proves settled != end)
  retry_ish   -> agent_end, more activity, agent_settled
  never       -> emits activity forever (timeout/cancel fixture)
  malformed   -> emits non-JSON lines then settles (framing fixture)
  malicious   -> attempts denied filesystem/network/credential actions,
                 then settles. Under the B4 sandbox profile these fail
                 structurally; the fixture records outcomes to
                 $FAKE_OUTCOME_FILE.
"""
import json
import os
import socket
import sys
import time
from pathlib import Path


def emit(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def try_malicious():
    outcomes = {}
    outside = Path(os.environ.get("FAKE_ESCAPED_PATH", "/private/tmp/fake-escape.txt"))
    try:
        outside.write_text("escape")
        outcomes["fs_escape_write"] = "succeeded"
    except OSError as e:
        outcomes["fs_escape_write"] = f"denied: {type(e).__name__}"
    try:
        socket.create_connection(("example.com", 443), timeout=3).close()
        outcomes["network"] = "succeeded"
    except OSError as e:
        outcomes["network"] = f"denied: {type(e).__name__}"
    cred = Path(os.environ.get("FAKE_CRED_PATH", str(Path.home() / ".ssh" / "id_ed25519")))
    try:
        cred.read_text()
        outcomes["credential_read"] = "succeeded"
    except OSError as e:
        outcomes["credential_read"] = f"denied: {type(e).__name__}"
    out = os.environ.get("FAKE_OUTCOME_FILE")
    if out:
        Path(out).write_text(json.dumps(outcomes))
    return outcomes


def main():
    behavior = os.environ.get("FAKE_BEHAVIOR", "happy")
    # consume the prompt line (envelope objective); never echo content
    sys.stdin.readline()
    if behavior == "malformed":
        sys.stdout.write("not-json-at-all\n")
        sys.stdout.write("{{{\n")
        sys.stdout.flush()
    if behavior == "never":
        while True:
            emit({"type": "activity"})
            time.sleep(0.1)
    if behavior == "write_secret":
        # seeded FAKE secret dropped into the worktree -> must be egress-blocked
        (Path.cwd() / "leak.txt").write_text(
            "AWS_SECRET_ACCESS_KEY=FAKEwJalrXUtnFEMIfakebCYqfakebCYxhabFakeKEY\n")
        emit({"type": "agent_end"})
        emit({"type": "agent_settled", "leak_dropped": True})
        return 0
    if behavior == "malicious":
        outcomes = try_malicious()
        emit({"type": "agent_end"})
        emit({"type": "agent_settled", "denial_outcomes_recorded": True})
        return 0
    if behavior == "retry_ish":
        emit({"type": "agent_end"})
        emit({"type": "activity"})
    emit({"type": "agent_end"})
    emit({"type": "agent_settled"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
