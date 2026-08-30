# Hermes + Pi Agentic Stack — Canonical Design Index

This directory is the canonical research/design source behind the human Pages manual and sliced agent execution surface.

## Read this in operating order

1. `../../README.md` — human start page, maturity and manual bootstrap summary.
2. `fresh-install-bootstrap.md` — verified fresh-install/manual foundation.
3. `../../UPLIFT_MISSION.md` — exact staged mission handed to Hermes.
4. `agent-execution-contract.md` — durable state/evidence/restart authority.
5. `implementation-playbook.md` — the single canonical `00 -> 70` lifecycle.
6. `../../skills/hermes-stack-uplift/SKILL.md` — progressive-disclosure phase map; load only the current slice.
7. `architecture.md` / `architecture.graph.json` — deterministic architecture and trust boundaries.
8. `research/openrouter-routing.md` — privacy/mission/model/provider responsibility split.
9. `local-context-memory-setup.md` — fixed LCM + Mnemosyne installation/config/verification/backup/rollback path.
10. `artifact-usability-review.md` — what is actually ready vs merely designed.
11. `adversarial-review.md` — failure catalogue and kill criteria.
12. `validation-report.md` — executed checks and remaining evidence gaps.
13. `SOURCES.md` — current primary/upstream sources.

## Executive topology

```text
mission
 -> deterministic local privacy/security/policy
 -> local mission router
 -> model-role binding
 -> OpenRouter model ID
 -> policy-compatible physical provider
 -> {research/review | typed Pi coding worker}
 -> evidence/review/merge gate
```

**OpenRouter is the default external inference gateway.** It is downstream of local privacy/security and mission/model decisions. OpenRouter Auto may be benchmarked for bounded bootstrap/shadow/fallback use but never becomes the privacy boundary or final mission classifier. Direct Z.ai/DeepSeek access remains a measured exception only.

Bootstrap avoids the router paradox: a clean narrow Hermes profile uses one verified GLM-Flash-class OpenRouter model through Phases 00–20, then Phase 30 builds the local router in shadow mode. Exact model IDs are runtime config/lock evidence, not permanent architecture constants.

## One lifecycle and six adoption checkpoints

```text
00 preflight
10 baseline + backup
20 context + skills + LCM/Mnemosyne -> Checkpoint A fresh optimized session
30 local router/OpenRouter roles       -> Checkpoint B shadow
40 security/policy enforcement         -> Checkpoint C human authority gate
50 Hermes->Pi + LSP                    -> Checkpoint D recreate workers
60 evaluation/promotion                -> Checkpoint E multi-role operation
70 upgrades/rollback                   -> Checkpoint F recurring canary cycle
```

Phase 20 is the first self-benefit boundary. Once its acceptance gate passes, Hermes reports **“The first token/context improvements are ready to use.”** and closes the pre-optimization session before Phase 30.

Every phase persists its evidence and v1.1 `boundary_report`, sends the same concise progress report to the human, and stops before the next phase.

## Context/memory ownership

```text
LCM          = current-session exact context / compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission authority
T2 artifacts = raw logs/diffs/benchmarks/test evidence
Git/ADR/spec = project truth
Kanban       = optional operational projection
```

Built-in MEMORY/USER are disabled in the selected baseline to avoid duplicate durable-memory authority. Diagnostic one-component profiles may isolate faults but do not replace LCM + Mnemosyne autonomously.

## Maturity

The package is **designed/execution-ready for controlled Phase-00 startup**, not yet an unattended production self-uplift system. Repository/site/router fixtures are smoke-tested where stated; target-Mac runtime qualification, OpenRouter effective-policy evidence, external security/Pi containment and production promotion remain P0 gates.

Use only the maturity labels defined in the canonical playbook: `researched`, `designed`, `prototype`, `smoke-tested`, `target-Mac-validated`, `shadow`, `canary`, `production-approved`.
