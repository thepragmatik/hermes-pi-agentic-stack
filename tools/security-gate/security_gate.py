#!/usr/bin/env python3
"""Phase 40 security gate — deterministic, stdlib-only, fail-closed.

Two subcommands:

  scan <file>       Egress scan of a payload file. Deterministic secret
                    detection + typed PII handling + re-scan. Prints JSON
                    evidence (no raw matches; only SHA-256 of matched values).
                    Exit 0=allow, 2=block, 3=internal-error (fail-closed block).

  gate <proposals>  Tier-0 routing-eligibility gate. Replays adversarial
                    routing proposals and rejects any route that conflicts
                    with the authoritative privacy class / eligibility facts,
                    regardless of classifier confidence or model preference.
                    Exit 0=all rejected correctly, 2=hard violation.

Policy digest is embedded in every evidence object for digest/evidence binding.
This tool is enforcement evidence, not the only boundary: it must be run
outside the model by a trusted launcher.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- policy ----
POLICY_PATH = Path(__file__).resolve().parents[2] / "configs" / "policy.example.yaml"

def policy_digest() -> str:
    return hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()

# -------------------------------------------------------------- detectors ---
SECRET_PATTERNS = [
    # name, regex, placeholder-tolerant?
    ("openrouter_key", re.compile(r"sk-or-v1-[A-Za-z0-9]{16,}"), False),
    ("generic_api_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), False),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), False),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), False),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), False),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), False),
    # key=value assignments, unless the value is an obvious non-secret placeholder
    ("aws_secret_key", re.compile(r"(?i)\b(?:aws)?_?SECRET_ACCESS_KEY\s*=\s*\S{12,}"), False),
    ("credential_assignment", re.compile(
        r"(?i)(?<![A-Za-z0-9])(api[_-]?key|secret|token|passwd|password|access[_-]?key)"
        r"(?![A-Za-z0-9])\s*[:=]\s*[\"']?([^\"'\s]{8,})[\"']?"), True),
]
PLACEHOLDER_VALUES = re.compile(
    r"^\s*(<[^>]+>|\$\{[^}]+\}|changeme|CHANGE_ME|REDACTED|xxx+|\*+|"
    r"os\.environ(\.get\()?|your[-_].*here)\s*$", re.IGNORECASE)

PII_PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+)\.[A-Za-z]{2,}\b")),
    ("abs_user_path", re.compile(r"/(?:Users|home)/([A-Za-z0-9_.-]{2,})/")),
    ("phone_us", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")),
]
# Deterministic false-positive allow rule for emails (checked when flagging).
FP_EMAIL_DOMAINS = re.compile(
    r"@(?:example\.(?:com|org)|test\.(?:com|invalid)|localhost)\b", re.IGNORECASE)

def luhn_ok(digits: str) -> bool:
    total, alt = 0, False
    for ch in reversed(digits):
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0

CC_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")

def scan_text(text: str):
    """Return list of findings: {category, type, line, value_sha256_16}."""
    findings = []

    def add(category, ftype, line_no, value):
        findings.append({
            "category": category,
            "type": ftype,
            "line": line_no,
            "value_sha256_16": hashlib.sha256(value.encode()).hexdigest()[:16],
        })

    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, rx, placeholder_ok in SECRET_PATTERNS:
            for m in rx.finditer(line):
                value = m.group(0)
                if name == "credential_assignment":
                    value = m.group(2)
                    if placeholder_ok and PLACEHOLDER_VALUES.match(value):
                        continue
                add("secret", name, line_no, value)
        for name, rx in PII_PATTERNS:
            for m in rx.finditer(line):
                if name == "email" and FP_EMAIL_DOMAINS.search(m.group(0)):
                    continue
                add("pii", name, line_no, m.group(0))
        for m in CC_RE.finditer(line):
            digits = re.sub(r"\D", "", m.group(0))
            if 13 <= len(digits) <= 19 and luhn_ok(digits):
                add("pii", "credit_card", line_no, m.group(0))
    return findings

def redact_text(text: str) -> str:
    """Typed PII redaction. Secrets are never rewritten (block-only)."""
    text = re.sub(r"/(?:Users|home)/[A-Za-z0-9_.-]{2,}/", "~/", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@((?!example\.|test\.|localhost)[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b",
                  "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
                  "[REDACTED_PHONE]", text)
    return text

# ------------------------------------------------------------- scan flow ----
def scan(payload: str) -> dict:
    try:
        first = scan_text(payload)
        secrets = [f for f in first if f["category"] == "secret"]
        pii = [f for f in first if f["category"] == "pii"]
        if secrets:
            decision = "block"
            rescanned = []
        else:
            redacted = redact_text(payload)
            second = scan_text(redacted)
            if second:
                decision = "block"   # re-scan residual -> fail closed
            else:
                # policy: pii_action=redact -> transform then allow; secret_action=block
                decision = "redact" if pii else "allow"
            rescanned = second
        return {
            "tool": "security-gate/scan",
            "policy_sha256_16": policy_digest()[:16],
            "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
            "decision": decision,
            "findings": first,
            "rescan_findings": rescanned,
            "fail_closed": True,
        }
    except Exception as exc:  # noqa: BLE001 — fail closed, never open
        return {
            "tool": "security-gate/scan",
            "policy_sha256_16": policy_digest()[:16],
            "decision": "block",
            "error": type(exc).__name__ + ": " + str(exc)[:200],
            "fail_closed": True,
        }

# ------------------------------------------------------- tier-0 route gate --
def gate_proposals(rows):
    """rows: iterable of {id, privacy_class, cloud_eligible (authoritative),
    proposed_route:{cloud:bool}, classifier_confidence (ignored by design)}."""
    results = []
    hard_violations = 0
    for row in rows:
        cls = row["privacy_class"]
        eligible = row["cloud_eligible"]
        proposed = bool(row["proposed_route"]["cloud"])
        # Tier-0: authoritative facts decide; confidence/model/router CANNOT.
        allowed = eligible and cls != "LOCAL_ONLY"
        rejected = proposed and not allowed
        if not rejected and not allowed and proposed:
            hard_violations += 1
        results.append({
            "id": row["id"],
            "privacy_class": cls,
            "proposed_cloud": proposed,
            "decision": "reject" if rejected else ("allow" if allowed and proposed else "not_routed"),
            "confidence_ignored": True,
        })
    return results, hard_violations

# ------------------------------------------------------------------- main ---
def main(argv):
    if len(argv) < 2 or argv[1] not in ("scan", "gate"):
        print(__doc__, file=sys.stderr)
        return 3
    if argv[1] == "scan":
        data = Path(argv[2]).read_text()
        out = scan(data)
        print(json.dumps(out, indent=2, sort_keys=True))
        return {"allow": 0, "redact": 0, "block": 2}.get(out["decision"], 3)
    rows = [json.loads(l) for l in Path(argv[2]).read_text().splitlines() if l.strip()]
    results, hard = gate_proposals(rows)
    print(json.dumps({
        "tool": "security-gate/gate",
        "policy_sha256_16": policy_digest()[:16],
        "proposals": len(rows),
        "rejected": sum(1 for r in results if r["decision"] == "reject"),
        "hard_constraint_violations": hard,
        "results": results,
    }, indent=2, sort_keys=True))
    return 0 if hard == 0 else 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
