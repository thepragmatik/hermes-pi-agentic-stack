# Hermes + Pi Agentic Stack — Architecture Summary

This directory is the canonical research/design source for a local-first Hermes control plane with isolated Pi coding workers.

## Read this in order

1. `architecture.md` — deterministic text architecture and invariants.
2. `artifact-usability-review.md` — what is actually ready vs merely designed.
3. `implementation-playbook.md` — staged autonomous uplift plan.
4. `agent-execution-contract.md` — resumability/evidence/state rules.
5. `bootstrap-authority.md` — temporary root-of-trust transition.
6. `research/mission-context-architecture.md` — T0/T1/T2 context ownership.
7. `research/local-context-memory-stack.md` — local LCM + Mnemosyne qualification, alternatives, setup and rollback.
8. `research/skill-slimming-slicing.md` — progressive-disclosure skill design.
9. `adversarial-review.md` — failure catalogue and kill criteria.
10. `validation-report.md` — checks and remaining evidence gaps.
11. `site-publishing.md` — human/agent Pages representation.

## Executive topology

Hermes is the mission/control plane, not an unrestricted coding shell. A deterministic policy/privacy gate precedes a tiny local mission router. Research uses a session-pinned research-model role. Coding crosses a typed Hermes→Pi boundary into an isolated worktree/sandbox using a coding-model role and LSP. Tests/scanners/review provide evidence before merge. Durable uplift state survives model context/session loss.

Context/memory is also split by authority: LCM is the preferred canary for exact current-session compaction recovery; Mnemosyne is the preferred canary for curated cross-session durable memory; Hermes `state.db/session_search` retains raw session history; `uplift-state` remains deterministic mission authority; Git/ADRs/specs remain project truth. The pair must beat simpler built-in controls before promotion.

## Maturity

The package is **fit for architecture review and controlled prototyping**, not yet for unattended production self-uplift. P0 gates are listed in `artifact-usability-review.md`, including real Pi/security enforcement and target-machine qualification of the selected local context/memory profile.