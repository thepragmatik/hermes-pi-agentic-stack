# Context-management corpus — reusable benchmark pattern

What this is: the deterministic benchmark corpus + zero-model-call harness pattern
proven in the CM mission (CM-10 onward), extractable for any future context-engine
benchmark. Load when building a new LCM/memory benchmark from scratch.

## Components

1. Synthetic canaries: 16 deterministic fixtures covering every mission-doc corpus
   category (exact-recall identifiers, deliberately planted bugs, buried FATAL
   markers, constraint-retention ADV-6 probes). Seed=42 for reproducibility.
2. Redacted real slices: exported from lcm.db with extractive exact-identifier
   probes; never raw transcripts.
3. Harness (`cm10_harness.py`, stdlib-only): checks live pipeline primitives —
   raw-history survival, summary-not-sole-source, FTS recall, supersession,
   LOCAL_ONLY flags, backup integrity — with zero model calls.
4. Scoring rule: non-observable dimensions are recorded `unknown`, never fabricated
   as pass.

## Provenance

Evidence: ~/.hermes/profiles/uplift/cm/evidence/CM-10/ (baseline CM10_BASELINE_PASS,
0 critical losses / 0 privacy violations). Corpus files:
~/.hermes/profiles/uplift/cm/corpus/ (sha256 pinned in evidence/CM-80/MANIFEST.md).
