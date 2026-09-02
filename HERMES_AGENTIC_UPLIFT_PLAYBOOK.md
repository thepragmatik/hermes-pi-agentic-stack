# Hermes + Pi Agentic Stack — Compact Control Playbook

Snapshot: 2026-08-31.

This is the compact architecture/control document. Detailed execution lives in `docs/agentic-uplift/implementation-playbook.md`; Hermes should load only the current phase slice rather than ingesting the full research corpus.

## Mission

Build an upgrade-safe local-first development stack where:

- Hermes is the mission/control plane;
- LCM + Mnemosyne is the fixed local context/memory baseline;
- deterministic local policy/eligibility decides what routes are possible;
- a small replaceable local router infers mission capabilities and recommends bounded workflow/model decisions;
- research and coding are first-class task families, not the whole ontology;
- **OpenRouter is the default external inference gateway** and normally chooses the physical provider subject to our requirements;
- coding crosses a typed Hermes -> Pi boundary into disposable externally-contained workers;
- routing learns from accepted mission outcomes without storing sensitive raw prompts by default;
- every uplift phase is observable, restartable and reversible.

## One routing architecture

```text
MISSION + durable state
  |
  v
Tier 0 deterministic eligibility / security
  privacy, LOCAL_ONLY, secrets/PII, cloud eligibility,
  tools/capabilities, modality, context, network/sandbox, ZDR
  |
  v
Tier 1 multi-label mission profile
  task families, domain, phase, complexity, uncertainty,
  tool/reasoning intensity, expected context
  |
  v
Tier 2 bounded workflow / agent selection
  Hermes-only | research executor | Pi worker | reviewer |
  multi-stage workflow | local-only | abstain/escalate
  |
  v
Tier 3 model-role / model optimization
  quality floor, expected accepted-mission cost, latency,
  retry risk, cache affinity, reliability, switch cost
  |
  v
Tier 4 gateway adapter
  OpenRouter-first -> policy-compatible physical provider
```

`research -> architecture_design -> coding_implementation -> testing -> security_review` is represented as ordered stages, not collapsed into `hybrid`.

Two framework-neutral contracts prevent lock-in:

- `protocols/routing-mission.schema.json` — deterministic requirements + inferred mission profile;
- `protocols/routing-decision.schema.json` — workflow/stages + model/gateway/provider requirements.

Hermes/Pi depend on those contracts, not on Aurelio, vLLM Semantic Router, LLMRouter, RouteLLM or a future ModernBERT implementation.

## Routing objectives

**Primary:** required capability/workflow and ordered mission stages.

**Secondary:** hard constraints. Known privacy, cloud eligibility, tools, modality, context, network/sandbox and ZDR requirements are derived/enforced deterministically, not predicted by a learned classifier.

**Tertiary:** among eligible choices, optimize expected accepted-mission quality/economics: cost, retry cost, TTFT/wall time, cache affinity, reliability, rate-limit risk, switching/context degradation and local resource footprint.

The top economic metric is **cost/minutes/retries/human intervention per accepted mission**, not $/M tokens or classifier F1 alone.

## Router progression

Phase 30 begins with the smallest useful implementation:

```text
rules + explicit state + deterministic eligibility + abstention
 -> tiny embedding / Aurelio challenger if useful
 -> shadow vLLM Semantic Router and other candidates
 -> RouteLLM-style Tier-3 scoring only if useful
 -> representative redacted outcome learning
 -> ModernBERT multi-label/multi-head only if earned
```

Current framework posture:

- **Aurelio Semantic Router:** strong lightweight Tier-1 semantic challenger/component.
- **vLLM Semantic Router:** strongest medium-term adoption candidate for richer signal/session/model routing; prefer upstream/config/adapters before a fork, and measure its heavier operational footprint.
- **LLMRouter:** research/training/evaluation laboratory; keep its large dependency surface off the production hot path.
- **RouteLLM:** optional Tier-3 strong-vs-economical scorer, recalibrated on our model outcomes.
- **OpenRouter Auto:** bootstrap/shadow/teacher/fallback signal only after Tier-0 eligibility; never privacy/security authority.
- **ModernBERT:** later multi-label/multi-head classifier only after stable ontology, representative deduplicated redacted outcomes, temporal holdout and simpler-baseline plateau.

A fork is justified only when an unmet material requirement cannot reasonably be upstreamed/adapted, the patch stays small and isolated, conformance/security tests exist, rebase capacity is explicit, and measured benefit exceeds maintenance cost.

## OpenRouter ownership

OpenRouter is downstream of our semantics and policy. Reuse provider allow/deny/order, required-parameter filtering, data/ZDR policy, pricing/latency/throughput preferences, fallback and session/provider affinity where the actual installed adapter proves they are forwarded/enforced.

Do **not** assume raw OpenRouter features are valid Hermes YAML keys. If a hard requirement such as ZDR or stable `session_id` cannot be proven through the installed Hermes path/account policy/audited gateway adapter, block or use a qualified alternative.

Direct Z.ai/DeepSeek/local-MLX adapters remain replaceable challengers without changing mission semantics.

## Bootstrap Mode

Do not require the optimized router before Hermes can build it.

```text
clean narrow Hermes profile
 -> OpenRouter
 -> one verified GLM-Flash-class bootstrap model
 -> Phases 00/10/20
 -> Phase 30 rules/state router + shadow bake-off
 -> Phase 60 evidence-gated routing promotion
```

The human bootstrap procedure is `docs/agentic-uplift/fresh-install-bootstrap.md`. Takeover action:

```bash
uplift chat --query-file UPLIFT_MISSION.md
```

## Single 00–70 lifecycle

| Phase | Objective | Adoption boundary |
|---|---|---|
| 00 | preflight/version/repo/provider/isolation truth | manual foundation verified |
| 10 | measurable baseline + backup + optional read-only legacy salvage | rollback evidence durable |
| 20 | context/skill diet + Spec Kit slicing + LCM/Mnemosyne | **A: first improvements usable; fresh session** |
| 30 | routing contracts + simple router + candidate shadows + OpenRouter roles | **B: shadow only** |
| 40 | external security/privacy/capability enforcement | **C: human authority gate** |
| 50 | typed Pi bridge + routing provenance + containment + LSP | **D: recreate disposable workers** |
| 60 | whole-system/router bake-off + promotion | **E: ordinary multi-role/workflow routing** |
| 70 | recurring upgrades/restart/rollback | **F: maintenance cycle** |

Every phase persists evidence/uplift-state and stops before the next phase.

## First self-benefit boundary

Phase 20 first dogfoods prompt/context + skill slimming in a fresh same-phase session before LCM/Mnemosyne and Spec Kit are layered. Once the full Phase-20 gate passes Hermes says:

> **The first token/context improvements are ready to use.**

Then Phase 30 starts in a fresh optimized session.

## Context / memory ownership

```text
T0            = stable prefix / small invariants + skill/tool catalogue
T1            = bounded current mission/phase capsule
T2            = logs/diffs/research/specs/benchmarks/RPC on demand
LCM           = current-session exact context + compaction recovery
Mnemosyne     = curated cross-session durable memory
state.db      = raw Hermes session history / forensic search
uplift-state  = deterministic mission authority
Git/ADR/spec  = project truth
```

## Routing outcome telemetry

Store privacy-minimized joins rather than raw prompts by default:

```text
mission/profile digest
 -> workflow/stage + router recommendation
 -> model role/model + provider where observable
 -> tokens/cache/TTFT/wall time/tools/retries/switches
 -> tests/review/human override
 -> accepted/rejected + failure reason + actual cost
```

This is the dataset from which future routing should learn: **which eligible workflow/model maximizes probability of accepted completion under the mission constraints and budget?**

## Security/root of trust

A profile, SOUL file, memory, skill, YAML, learned routing score, vLLM signal or provider guardrail is not structural authorization.

Before stronger authority, implement external role/capability, filesystem/process/environment/credential/network enforcement, deterministic secret + typed PII scanning, policy digest/idempotency/evidence journal, sandbox/containment and independent review/merge authority.

Tier 0 runs before OpenRouter/Auto/direct cloud. Any learned/framework output conflicting with Tier 0 loses.

## Pi invariant

Pi has no assumed built-in permission boundary. Pi task envelope **v2.2** binds policy plus routing provenance (`mission_id`, `stage_id`, workflow and routing-decision digest) so outcomes can be joined back to the route without replaying chat/raw prompt data. Workers remain externally contained, disposable, non-self-merging and use `agent_settled` as final completion.

## Maturity labels

Use only:

`researched -> designed -> prototype -> smoke-tested -> host-validated -> shadow -> canary -> production-approved`

Current routing state: contracts/design + benchmark prototype + deterministic rules smoke; advanced candidates researched/designed, not production-approved.

## Canonical start order

1. `README.md`
2. `docs/agentic-uplift/fresh-install-bootstrap.md`
3. `UPLIFT_MISSION.md`
4. `docs/agentic-uplift/agent-execution-contract.md`
5. `docs/agentic-uplift/implementation-playbook.md`
6. `skills/hermes-stack-uplift/SKILL.md` + current phase only
7. `protocols/routing-mission.schema.json` + `routing-decision.schema.json` when Phase 30/route execution requires them
8. topic research only when the current gate requires it

Human Pages are generated from canonical source. Agents start at `llms.txt` / `agent/START.md` and fetch only the required slice.