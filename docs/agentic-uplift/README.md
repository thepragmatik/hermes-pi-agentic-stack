# Hermes + Pi Agentic Stack — Canonical Design Index

This directory is the canonical research/design source behind the human Pages manual and sliced agent execution surface.

**Mission outcome 2026-08-31 → 2026-09-01: 9/9 phases COMPLETE with persisted evidence.** The design below is no longer only designed — the bridge, containment, capability modes, LCM+Mnemosyne and rollback drill are proven (see `bootstrap-authority.md` and the readiness table in `artifact-usability-review.md`). Diagrams live in [`diagrams/`](diagrams/) — presentation views only; `architecture.md` remains canonical text.

## Read this in operating order

1. `../../README.md` — human start page, maturity and manual bootstrap summary.
2. `fresh-install-bootstrap.md` — verified fresh-install/manual foundation.
3. `../../UPLIFT_MISSION.md` — exact staged mission handed to Hermes.
4. `agent-execution-contract.md` — durable state/evidence/restart authority.
5. `implementation-playbook.md` — single canonical `00 -> 70` lifecycle.
6. `../../skills/hermes-stack-uplift/SKILL.md` — progressive-disclosure phase map; load only the current slice.
7. `architecture.md` / `architecture.graph.json` — deterministic architecture and trust boundaries.
8. `../../protocols/routing-mission.schema.json` + `routing-decision.schema.json` — stable internal routing interface.
9. `research/local-routing-models.md` — broad routing/framework assessment and bake-off.
10. `research/router-training-control.md` — outcome learning and ModernBERT graduation rules.
11. `research/openrouter-routing.md` — gateway/provider ownership and effective-policy requirements.
12. `local-context-memory-setup.md` — fixed LCM + Mnemosyne setup/verification/backup/rollback.
13. `artifact-usability-review.md`, `adversarial-review.md`, `validation-report.md` — readiness, failure catalogue and executed evidence.
14. `SOURCES.md` — current primary/upstream sources.

## Executive topology

```text
mission + durable state
 -> Tier 0 deterministic eligibility/security
 -> Tier 1 multi-label mission profile
 -> Tier 2 bounded workflow/agent selection
 -> Tier 3 model-role/model optimization
 -> Tier 4 OpenRouter-first provider execution
 -> evidence/outcomes -> offline router research/training
```

Research and coding are important first-class task families, not the complete routing ontology. A mission such as `research -> architecture_design -> coding_implementation -> testing -> review` remains an ordered workflow instead of becoming `hybrid`.

**OpenRouter is the default external inference gateway.** It is downstream of local eligibility/privacy/security and workflow/model decisions. OpenRouter Auto may be benchmarked for bounded bootstrap/shadow/teacher/fallback use only after Tier-0 approval; it never becomes the privacy boundary. Direct provider/local adapters remain measured exceptions behind the same contract.

## Router progression

Bootstrap avoids the router paradox: a clean narrow Hermes profile uses one verified OpenRouter model through Phases 00–20. Phase 30 first builds **rules + explicit state + abstention** and uses that only in shadow. Then the common benchmark may shadow minimal embeddings, Aurelio Semantic Router, vLLM Semantic Router, LLMRouter experiments, RouteLLM-style Tier-3 scoring and OpenRouter Auto. ModernBERT remains deferred until representative redacted outcomes justify it.

Current strategic posture:

- **initial router:** deterministic eligibility + rules/state + abstention;
- **lightweight semantic challenger:** Aurelio Semantic Router / small embedding path;
- **strongest medium-term adoption candidate:** vLLM Semantic Router behind our interface, if its measured benefit earns its heavier runtime;
- **research plane:** LLMRouter and RouteLLM experiments/training;
- **future learned model:** multi-label/multi-head ModernBERT only after stable ontology, temporal holdout and simpler-baseline plateau.

Prefer upstream/config/adapters over a fork. A fork requires a materially valuable unmet requirement, failed/unavailable upstream path, small isolated patch set, conformance/security tests, rebase capacity and measured benefit greater than maintenance cost.

## One lifecycle and adoption checkpoints

```text
00 preflight
10 baseline + backup
20 context + skills + LCM/Mnemosyne -> A0 dogfood + A fresh optimized session
30 routing contracts/simple router/bake-off -> B shadow only
40 security/policy enforcement             -> C human authority gate
50 Hermes->Pi + LSP + routing provenance   -> D recreate workers
60 evaluation/promotion                    -> E ordinary multi-role/workflow operation
70 upgrades/rollback                       -> F recurring canary cycle
```

Phase 20 remains the first self-benefit boundary. Phase 30 does not block the uplift on advanced routing infrastructure.

## Hard routing facts vs learned signals

Deterministic/runtime-derived facts include privacy class, `LOCAL_ONLY`, cloud eligibility, secret/PII policy, available tools/capabilities, required modality, actual context-window requirement, network/sandbox permissions and ZDR requirements. Learned/framework signals may infer task families, domain, complexity, uncertainty, tool/reasoning intensity and likely workflow—but cannot override hard facts.

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

## Maturity

**Post-mission (2026-09-01):** the controlled uplift executed end-to-end (9/9 phases). PROVEN: Pi bridge + Seatbelt containment, fail-closed egress scanning, bridge-level capability modes, parent-proxy cloud canary, disposable-copy rollback drill, LCM+Mnemosyne live. Still NOT production-approved: orchestrator-level tool removal (external, operator-owned), representative routing evidence for advanced routers, and whole-system target-Mac production qualification. Routing contracts and benchmark are smoke-tested; all advanced router candidates remain researched/designed or future shadow candidates.

Use only the maturity labels defined in the canonical playbook: `researched`, `designed`, `prototype`, `smoke-tested`, `target-Mac-validated`, `shadow`, `canary`, `production-approved`.