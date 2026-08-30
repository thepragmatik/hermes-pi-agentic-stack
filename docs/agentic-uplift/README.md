# Hermes + Pi Agentic Stack — Architecture Summary

This directory is the canonical research/design source for a local-first Hermes control plane with isolated Pi coding workers.

## Read this in order

1. `architecture.md` — deterministic text architecture and invariants.
2. `artifact-usability-review.md` — what is actually ready vs merely designed.
3. `implementation-playbook.md` — staged uplift plan.
4. `agent-execution-contract.md` — resumability/evidence/state rules for autonomous execution.
5. `research/skill-slimming-slicing.md` — progressive-disclosure context design.
6. `adversarial-review.md` — failure catalogue and kill criteria.
7. `validation-report.md` — checks and remaining evidence gaps.
8. `site-publishing.md` — human/agent Pages representation.

## Executive topology

Hermes is the mission/control plane, not an unrestricted coding shell. A deterministic policy/privacy gate precedes a tiny local mission router. Research uses a session-pinned research-model role. Coding crosses a typed Hermes→Pi boundary into an isolated worktree/sandbox using a coding-model role and LSP. Tests/scanners/review provide evidence before merge. Durable uplift state survives model context/session loss.

## Maturity

The package is **fit for architecture review and controlled prototyping**, not yet for unattended production self-uplift. P0 gates are listed in `artifact-usability-review.md`.
