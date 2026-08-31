import json
import pathlib
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools/security-gate"))
import security_gate as sg  # noqa: E402

FIX = REPO / "tools/security-gate/fixtures"

class TestScan(unittest.TestCase):
    def test_adversarial_payloads_never_allow_unsanitized(self):
        # secrets -> block; PII-only -> redact (transformed, never raw egress)
        # adv-8 (card): card redaction unimplemented -> re-scan residual -> block
        # (fail-closed on uncertain transformation, per policy doc)
        expect = {"adv-2": "redact", "adv-3": "redact", "adv-8": "block", "adv-6": "allow"}
        for line in FIX.joinpath("adversarial-payloads.jsonl").read_text().splitlines():
            row = json.loads(line)
            out = sg.scan(row["payload"])
            want = expect.get(row["id"], "block")
            self.assertEqual(out["decision"], want, row["id"])
            self.assertTrue(out["fail_closed"])
            for f in out["findings"]:
                self.assertNotIn("value", f)  # no raw match in evidence

    def test_technical_false_positives_allowed(self):
        for line in FIX.joinpath("technical-false-positives.jsonl").read_text().splitlines():
            row = json.loads(line)
            out = sg.scan(row["payload"])
            self.assertEqual(out["decision"], "allow", (row["id"], out["findings"]))

    def test_rescan_residual_blocks(self):
        # email redaction leaves a secret -> re-scan must fail closed
        out = sg.scan("mail me at bob@corp.io\nkey = \"sk-or-v1-abcdefghijklmnopq\"")
        self.assertEqual(out["decision"], "block")

    def test_pii_redaction_then_allow(self):
        out = sg.scan("user dir /Users/someuser/work and mail someuser@corp.io")
        self.assertEqual(out["decision"], "redact", out)  # transformed, not raw
        self.assertIn("~/", sg.redact_text("see /Users/someuser/work"))

    def test_fail_closed_on_internal_error(self):
        orig = sg.scan_text
        sg.scan_text = lambda *_: (_ for _ in ()).throw(RuntimeError("boom"))
        try:
            out = sg.scan("anything")
        finally:
            sg.scan_text = orig
        self.assertEqual(out["decision"], "block")
        self.assertTrue(out["fail_closed"])

    def test_no_raw_values_in_evidence(self):
        out = sg.scan("token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456")
        blob = json.dumps(out)
        self.assertNotIn("ghp_ABCD", blob)

class TestTier0Gate(unittest.TestCase):
    def test_hard_violations_zero(self):
        rows = [json.loads(l) for l in
                FIX.joinpath("routing-proposals.jsonl").read_text().splitlines() if l.strip()]
        results, hard = sg.gate_proposals(rows)
        self.assertEqual(hard, 0)
        decisions = {r["id"]: r["decision"] for r in results}
        self.assertEqual(decisions["t0-1"], "reject")
        self.assertEqual(decisions["t0-2"], "reject")
        self.assertEqual(decisions["t0-3"], "reject")
        self.assertEqual(decisions["t0-4"], "allow")
        self.assertEqual(decisions["t0-5"], "reject")
        self.assertEqual(decisions["t0-6"], "not_routed")

if __name__ == "__main__":
    unittest.main()
