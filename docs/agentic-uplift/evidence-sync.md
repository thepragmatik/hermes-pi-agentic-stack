# Evidence Sync Policy

## Goal
Keep the public blueprint docs truthful without ever publishing private evidence.

## Rules
1. Evidence (experiments, scores, transcripts) stays canonical in the private
   evidence bundle. Blueprints never become the system of record for results.
2. Blueprints receive ONLY milestone summaries: (a) a gate passes or fails,
   (b) a standing decision changes (e.g. router deployed at threshold X),
   (c) a new phase becomes executable. Nothing else.
3. Every milestone summary is PII-scrubbed (no usernames, real prompts,
   session content, keys, or person-linked costs) and cites evidence in
   relative form ("private evidence bundle, routing track") — never absolute
   private paths.
4. One milestone = one commit = one review. No bulk rewrites.
5. The GitHub Pages allowlist must include any new doc BEFORE publishing;
   Pages output is PUBLIC — treat every line accordingly.

## Sync triggers (checklist for the next maintainer)
- [x] Router v1 milestone: replace "ModernBERT deferred" framing in README.md
      with the trained-MF-router milestone + measured numbers (after PII sweep).
- [ ] After the judge-labeling retrain (if it passes its gate): update
      research/router-training-control.md graduation rules with the outcome.
- [ ] After route.py ships: add it to architecture.md's component list.

## When to update (the schedule)
- IMMEDIATELY (next execution session): router-v1 milestone into README.md
  (the current framing is stale — a gated router exists).
- AFTER each mission gate resolves: one-line status in README's roadmap table
  (Phases 30/50 rows) if the outcome changes what an implementer would do.
- AFTER the retrain mission: research/router-training-control.md graduation note.
- BEFORE any GitHub Pages deploy: re-run the PII sweep on changed files.
- NEVER: on every experiment. Experiments are cheap; doc churn is expensive.

## Program status (milestone view)

| # | Workstream | Status | Milestone result | Next step |
|---|------------|--------|------------------|-----------|
| 1 | Router v1 (embeddings + 52K-param factorization head) | DONE — gate PASS | Preregistered gate passed 2026-09-04 (APGR 0.6528 vs 0.55), $0 spend | Deployment threshold selection (done) |
| 2 | Deployment threshold | DONE | Threshold 0.30: ~56% projected savings, ~99% of strong-model accuracy gain retained | Ship the router as a local decision tool |
| 3 | Local decision tool (route.py) | IN PROGRESS | — | Build + val reproduction test |
| 4 | Own-session-corpus triage | IN PROGRESS | — | Preregistered GO/NO-GO on labelable rows |
| 5 | Judge-labeled training data | PLANNED — gated | — | Calibration gate against real outcomes before any label counts |
| 6 | Judge compute decision | DECIDED (staged) | Local judge default; API/GPU only behind explicit operator spend gates | Operator pilot choice |
| 7 | GPU training decision | DECIDED (staged) | Current router trains in CPU-minutes; GPU reserved for larger corpora/towers/sweeps | None now |
| 8 | Reasoning-mode probe | BLOCKED on operator go | Preregistration locked, not rebalanceable | Operator decision |
