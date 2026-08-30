# Hermes + Pi Agentic Stack — Architecture Summary

This directory is the canonical research/design source for a local-first Hermes control plane with isolated Pi coding workers.

## Read this in order

1. `architecture.md` — deterministic text architecture and invariants.
2. `artifact-usability-review.md` — what is actually ready vs merely designed.
3. `implementation-playbook.md` — staged autonomous uplift plan.
4. `agent-execution-contract.md` — resumability/evidence/state rules.
5. `bootstrap-authority.md` — temporary root-of-trust transition.
6. `local-context-memory-setup.md` — clinical LCM + Mnemosyne installation/config/verification/backup/rollback procedure.
7. `research/mission-context-architecture.md` — T0/T1/T2 context ownership.
8. `research/local-context-memory-stack.md` — LCM + Mnemosyne baseline ownership, risks and qualification evidence.
9. `research/skill-slimming-slicing.md` — progressive-disclosure skill design.
10. `adversarial-review.md` — failure catalogue and kill criteria.
11. `validation-report.md` — checks and remaining evidence gaps.
12. `site-publishing.md` — human/agent Pages representation.

## Executive topology

Hermes is the mission/control plane, not an unrestricted coding shell. **LCM + Mnemosyne is the required local context/memory baseline**: LCM owns exact current-session context/compaction recovery, Mnemosyne owns curated cross-session durable memory, Hermes `state.db/session_search` retains raw session history, `uplift-state` remains deterministic mission authority, and Git/ADRs/specs remain project truth.

A deterministic policy/privacy gate precedes a tiny local mission router. Research uses a session-pinned research-model role. Coding crosses a typed Hermes→Pi boundary into an isolated worktree/sandbox using a coding-model role and LSP. Tests/scanners/review provide evidence before merge. Durable uplift state survives model context/session loss.

Built-in MEMORY/USER are disabled in the selected baseline to avoid duplicate durable-memory authority. Built-in-only, LCM-only and Mnemosyne-only profiles are retained only for diagnostic isolation/rollback. A failed required LCM/Mnemosyne gate produces `BLOCKED`/`ROLLBACK`, not autonomous selection of another memory architecture.

## Maturity

The package is **fit for architecture review and controlled prototyping**, not yet for unattended production self-uplift. The LCM + Mnemosyne architecture is selected and its configuration/runbook is execution-ready, but target-Mac runtime/local-only/recovery qualification has not yet been performed. P0 gates are listed in `artifact-usability-review.md`, including real Pi/security enforcement and target-machine qualification of the fixed local context/memory baseline.
