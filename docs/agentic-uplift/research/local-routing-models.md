# Local Mission Routing Architecture and Framework Assessment — 2026

Snapshot: 2026-08-31. Re-verify releases and integration semantics during Phase 30.

## Decision

The old `research | coding | hybrid` framing was too narrow. Research and coding remain important task families, but they are not the routing ontology.

The routing problem is:

> Given a mission, deterministic constraints, current workflow/session state and measured model/provider performance, choose an eligible **workflow + agent + model role + model + provider policy** that maximizes probability of accepted completion while controlling total cost, latency, retries, switching overhead and risk.

Use two stable framework-neutral contracts:

- `protocols/routing-mission.schema.json` — mission profile, deterministic requirements/constraints, session state and optimization objective;
- `protocols/routing-decision.schema.json` — eligible set, selected workflow/stages, model role/model, gateway/provider policy and confidence.

Hermes, Pi and OpenRouter integration must depend on these contracts, not on Aurelio Semantic Router, vLLM Semantic Router, RouteLLM, LLMRouter or a future ModernBERT implementation.

---

# Primary, secondary and tertiary objectives

## Primary — capability and workflow

Infer what the mission is trying to accomplish. A mission may contain several task families and transition between them over time.

Canonical initial task-family vocabulary:

```text
research
synthesis
architecture_design
planning_decomposition
coding_implementation
debugging_diagnosis
refactoring
testing
code_review
security_review
devops_configuration
data_analysis
document_generation_transformation
retrieval_memory
agent_supervision_orchestration
long_running_tool_execution
multimodal_analysis
verification_fact_check
other
```

This vocabulary is deliberately **multi-label**. It is not one model role per label and not an exhaustive product taxonomy. Add/change task families only when real missions and routing consequences justify doing so.

Represent workflow progression explicitly:

```text
research -> architecture_design -> coding_implementation -> testing -> security_review
```

Do not flatten that into `hybrid` when ordered stages are operationally meaningful.

Useful inferred Tier-1 signals also include domain, current phase, complexity, uncertainty, reasoning intensity and tool intensity.

## Secondary — eligibility and hard constraints

These restrict the candidate set before economic optimization. Most must be deterministic or measured from authoritative state rather than guessed by a classifier.

Examples:

- privacy class / `LOCAL_ONLY`;
- secret and PII policy;
- cloud eligibility;
- required tools/capabilities;
- coding-agent/Pi requirement;
- required modality;
- minimum context window;
- structured-output requirement;
- sandbox/network permissions;
- ZDR/data-retention requirement;
- destructive/risk/approval policy;
- independent-review requirement;
- current available model/tool/provider capabilities;
- session/cache-affinity and switch budget.

A learned model may help *detect* a possible security concern for review, but it is never the authority for facts already known from policy/state. `LOCAL_ONLY`, tool availability, network permission, model context limits and required modality are examples of deterministic eligibility facts.

## Tertiary — execution economics

After removing ineligible routes, rank the remaining paths using measured outcome economics:

- expected accepted-task quality;
- token/cached-token cost;
- retry/failure cost;
- TTFT, throughput and wall time;
- prompt-cache/provider affinity;
- model/provider reliability and rate-limit risk;
- context degradation/switch cost;
- local router CPU/RAM;
- current provider availability;
- human intervention probability.

The principal economic metric is **cost per accepted mission**, not cost per million tokens.

---

# Five-tier routing architecture

```text
MISSION + durable state
        |
        v
Tier 0 — deterministic eligibility / policy
  privacy / secrets / PII
  LOCAL_ONLY / cloud eligibility / ZDR
  required capabilities/tools/modality/context
  risk / approval / review
  sandbox / network
        |
        v
Tier 1 — mission-profile inference
  task family/families
  domain + workflow phase
  complexity + uncertainty
  reasoning/tool intensity
        |
        v
Tier 2 — workflow / agent planning
  Hermes-only
  research executor
  Pi worker
  review worker
  local tool runner
  bounded multi-stage workflow
  abstain/escalate
        |
        v
Tier 3 — model-role/model optimization
  filter by capabilities/quality floor
  score quality/cost/latency/reliability/cache/switch cost
        |
        v
Tier 4 — gateway / physical execution
  OpenRouter-first provider routing
  or qualified direct/local adapter
        |
        v
OUTCOME TELEMETRY -> offline research/training plane
```

### Responsibility boundaries

- Tier 0 is our deterministic local security/eligibility boundary.
- Tier 1 may use rules, embeddings, vLLM signals or later ModernBERT.
- Tier 2 remains bounded workflow planning owned by Hermes/our routing policy. A router framework may propose a workflow but cannot gain arbitrary tool authority.
- Tier 3 selects model roles/models among the eligible set.
- Tier 4 normally delegates physical-provider routing to OpenRouter.
- Merge/approval authority remains outside all five routing tiers.

---

# Thin contract, replaceable engines

A routing engine consumes `routing-mission` and emits `routing-decision`.

This permits:

```text
rules/state
  -> Aurelio semantic component
  -> vLLM Semantic Router sidecar/control-plane
  -> future ModernBERT multi-head model
```

without rewriting Hermes/Pi/OpenRouter semantics.

Every field that matters to security or capability eligibility should retain provenance (`deterministic`, `human`, `measured`, `inferred`, `default`). If a future learned engine outputs a value that conflicts with deterministic state, deterministic state wins and the conflict is logged.

---

# Framework assessment

| Candidate | Best role in this stack | Current decision | Why |
|---|---|---|---|
| deterministic rules/state | Tier 0 + simple Tier 1/2 baseline | **ADOPT** | tiny, auditable, zero model dependency; establishes whether semantics add value |
| Aurelio Semantic Router | local semantic Tier-1 component | **ADOPT AS CHALLENGER / possible small production component** | lightweight semantic routes, local encoders, threshold optimization; insufficient as complete policy/session/workflow optimizer |
| vLLM Semantic Router | medium-term routing control-plane / signal-policy engine | **STRONGEST ADOPTION CANDIDATE** | Apache-2.0, composable signals/projections/decisions, v0.3 stateful/session-aware routing, shadow switch gates, cache-aware switching, observability and rollback; full runtime is heavier and agent/workflow work is still evolving |
| RouteLLM | Tier-3 quality/difficulty scorer | **RESEARCH/OPTIONAL SECOND STAGE** | useful preference/MF/BERT machinery for strong-vs-economical selection; not a mission-type classifier |
| LLMRouter (UIUC) | research/training/evaluation laboratory | **ADOPT IN RESEARCH PLANE ONLY** | broad algorithm/dataset/evaluation surface; dependency footprint is too large for default hot path |
| OpenRouter Auto | external shadow teacher/bootstrap/fallback | **SHADOW ONLY** | current market-adaptive model routing and session stickiness can provide a useful comparison signal; not local, not privacy authority, objective differs from ours |
| custom ModernBERT | later learned Tier-1/maybe Tier-3 signals | **DEFER TRAINING** | attractive 149M encoder/multi-head architecture, but only after representative outcome data proves simpler routes plateau |

## Aurelio Semantic Router

Current local semantic-router releases support local HuggingFace/FastEmbed-style execution, semantic route thresholds/optimization and multimodal routing. It is a very good answer to:

> Which of these semantic capability clusters does this mission resemble?

It is not by itself an answer to:

- deterministic privacy/capability eligibility;
- multi-stage workflow planning;
- session switch budgets/cache costs;
- accepted-task economics;
- provider policy and rollback lifecycle.

Use it behind the routing contract as the first low-friction semantic challenger. If rules + Aurelio/local embeddings deliver most of the economic benefit, retaining that small solution is a valid production outcome.

## vLLM Semantic Router

Current vLLM Semantic Router v0.3 (`Themis`) is the strongest project to evaluate seriously for medium-term adoption.

Its stable architecture already includes a broad signal -> projection -> decision pipeline. Maintained signal families include authorization, context, keyword/language/structure, complexity, domain, embeddings/KB, modality, fact checking, jailbreak, PII, preference, re-ask and user feedback. Session-aware work in v0.3 includes safe stay-vs-switch policy seams, conversational routing momentum, cache-warmth/switch-cost evidence and shadow model-switch gates.

This maps unusually well onto our Tier 1/3 needs.

However:

- our deterministic Tier-0 boundary remains outside it; learned PII/jailbreak signals are defense-in-depth, not our final egress authority;
- its full Envoy/control-plane deployment is operationally heavier than a 5–50 ms local classifier;
- current agent selection/multi-agent composition and richer long-running workflow/context directions include active roadmap work, so do not claim every desired agent feature is stable today;
- Router Replay/body capture and semantic-cache isolation require explicit privacy review before production use;
- our Hermes/Pi typed workflow semantics and authority cutover are stack-specific.

### Adoption sequence

1. Phase 30: run vLLM Semantic Router **in shadow** through an adapter that emits our routing-decision contract.
2. Configure existing signals/projections before writing code.
3. Add a small upstream-compatible extension only where the contract cannot be expressed cleanly.
4. Prefer upstream contribution over a long-lived fork.
5. Grant production authority only if it beats the simpler hot-path baseline on accepted-task economics and operational reliability.

### Fork gate

Do **not** fork merely for convenience. A fork is justified only when all are true:

- a mandatory requirement cannot be represented by the stable config/plugin/adapter interfaces;
- the requirement is important enough to materially improve quality, security, cost, latency or resilience;
- an upstream issue/PR path is unavailable, rejected, or cannot meet our bounded timeline;
- the patch set is small, isolated and covered by upstream-plus-local conformance tests;
- we can continuously rebase against security/stable releases;
- measured savings/quality value exceeds estimated fork-maintenance cost.

If not, remain an adapter/config consumer.

## RouteLLM

RouteLLM should be treated as a Tier-3 scorer. Its MF, BERT and similarity-weighted preference approaches estimate when a stronger model is worth using relative to a weaker/economical model.

That is useful *after* the mission has an eligible workflow/model set. It should not decide `research vs coding`, privacy, Pi authority or tool eligibility.

Use its evaluation/training ideas or an adapter in the research plane. Recalibrate on our actual model portfolio and accepted-task outcomes before any authority; historical pretrained strong/weak pairs are not our truth.

## LLMRouter

UIUC LLMRouter is particularly useful as a **router laboratory**. Current `llmrouter-lib` exposes KNN, SVM, MLP, MF, Elo, BERT/causal/hybrid/graph approaches, multi-round/agentic routers, multimodal routing and dataset/evaluation pipelines.

Its default package pulls a substantial research stack including Torch, Transformers, Gradio, LiteLLM and torch-geometric. That is a feature for experimentation and a liability for an always-resident Hermes hot path.

Use it to benchmark algorithms against one converted Hermes mission/outcome corpus. Export the winning small model/artifact/logic behind our contract rather than embedding the whole lab in every request.

## OpenRouter Auto

OpenRouter Auto currently performs market-adaptive model selection and exposes the actual selected model. It respects configured privacy/guardrails and uses multi-turn model stickiness where the selected model remains a leading candidate.

Use only on policy-approved **sanitized** missions for:

- bootstrap fallback if an explicit model is unavailable;
- shadow comparison;
- teacher/weak-supervision signal;
- low-risk bounded fallback where explicitly allowed.

Record:

```text
our mission profile
our workflow/model decision
OpenRouter Auto selected model
the actual physical provider where observable
accepted/rejected outcome
cost + cached tokens
TTFT/wall time
retries/fallbacks
human override
```

Never let Auto decide whether data may leave the machine.

---

# OpenRouter changes what we should build

OpenRouter can own much of **Tier 4** so we do not recreate provider-health/load-balancing infrastructure.

Its raw provider policy currently supports, among other fields:

- provider `only` / `ignore` / `order`;
- fallbacks;
- `require_parameters`;
- `data_collection` filtering;
- per-request ZDR filtering;
- sorting by price, throughput or latency;
- max-price and preferred performance thresholds;
- model fallbacks;
- session/provider stickiness and prompt caching via stable `session_id`.

This means our internal router should normally choose **workflow + model role + model + abstract provider requirements**, then let OpenRouter choose the physical provider.

Do not couple the routing contract to what Hermes exposes today. Hermes' documented `provider_routing` currently covers a subset (`sort/only/ignore/order/require_parameters/data_collection`), while the raw OpenRouter API has additional fields such as ZDR and performance thresholds. The adapter must prove how each required field is enforced.

At this snapshot, an open Hermes issue reports that ordinary OpenRouter chat requests do not forward OpenRouter `session_id`; therefore session/provider stickiness must be **measured and qualified**, and may require an upstream Hermes fix or a thin gateway adapter before we rely on it for cache economics.

Direct DeepSeek, Z.ai, local MLX or another gateway implements the same Tier-4 adapter contract. Mission semantics do not change.

---

# Initial and medium-term router

## Bootstrap / early Phase 30

The fresh uplift remains single-model through Phase 20.

The first actual router in Phase 30 is deliberately small:

```text
Tier 0 deterministic eligibility
 + deterministic state/workflow rules
 + simple multi-label capability rules
 + abstain
```

Then shadow semantic challengers:

1. minimal frozen embedding prototype;
2. Aurelio Semantic Router with a local encoder;
3. vLLM Semantic Router configured as a shadow sidecar/control plane;
4. later research-plane algorithms/Auto comparisons.

Do not block the rest of the uplift on an advanced router.

## Likely medium term

Current hypothesis:

> **our thin contract + deterministic Tier 0 + vLLM Semantic Router (configured/upstream, not forked) for richer Tier 1/3 signals + Hermes-owned bounded workflow semantics + OpenRouter Tier 4**

This is a hypothesis to prove against the simpler baseline. If vLLM Semantic Router does not earn its runtime/operational footprint on the target Mac, use the smaller rules/embedding/Aurelio path instead.

---

# ModernBERT reconsidered

Do not train a single-head `research|coding|hybrid` classifier.

A future `answerdotai/ModernBERT-base` model can use shared encoder features with calibrated multi-label/multi-head outputs such as:

```text
task families (multi-label)
domain (multi-label/hierarchical)
workflow phase
complexity
reasoning intensity
tool intensity
context-need band
uncertainty / abstention score
```

Never train heads for deterministic facts such as `LOCAL_ONLY`, actual tool availability, network permission or known model context length.

Nomic `modernbert-embed-base` remains a useful **frozen embedding** challenger: Apache-2.0, ModernBERT-derived, 768d with 256d Matryoshka support. It can provide a cheap intermediate step before any encoder fine-tuning.

### Evidence gate for ModernBERT training

Fine-tuning is justified only when:

- mission/task vocabulary has stabilized under real use;
- representative Hermes missions are locally redacted and deduplicated;
- labels/outcomes cover more than research/coding and include multi-stage missions;
- mission/repository/session/time holdouts prevent trajectory leakage;
- actual matched outcomes exist across eligible workflows/models/providers;
- learning curves show more data still improves the relevant heads;
- simpler rules/embedding/vLLM-config baselines plateau on **routing regret / accepted-task economics**, not merely F1;
- calibration/abstention is measurable and stable;
- privacy review approves every training field.

There is no magic sample count. Data sufficiency is an empirical learning-curve and temporal-holdout question.

---

# Research/training plane vs production hot path

## Research / training plane

May use:

- LLMRouter algorithms and data/evaluation utilities;
- RouteLLM preference experiments;
- vLLM Semantic Router simulation/replay where privacy permits;
- OpenRouter Auto shadow labels on sanitized missions;
- notebooks/training pipelines;
- ModernBERT fitting/fine-tuning;
- large outcome joins.

It is offline/non-critical and may be comparatively heavy.

## Production hot path

Must remain:

- local before cloud;
- deterministic for eligibility/security;
- bounded in CPU/RAM/latency;
- auditable/explainable enough to troubleshoot;
- session-aware without model thrashing;
- replaceable behind the routing contracts;
- safe to abstain;
- easy to roll back.

Every added runtime layer must earn its place through measured improvement.

---

# Outcome learning

Record a privacy-minimized event per decision/stage, not raw prompt replay by default:

```text
mission/profile hash + redacted feature summary
contract/schema + router engine/version
candidate/selected workflow
model role + model ID
physical provider when observable
provider policy + session-affinity key hash
input/output/cached tokens
TTFT + total latency
router latency/RSS
number/type of tool calls
retries/fallbacks/model/provider switches
tests/review outcome
human override
accepted/rejected
failure reason
estimated/actual cost
```

The eventual optimization target is:

> `P(accepted completion | mission profile, constraints, workflow, model, provider state) / expected total cost`

with hard constraints applied before optimization.

---

# Bake-off

Run every candidate against the same versioned mission corpus and, where applicable, matched execution outcomes.

Required candidates:

A. deterministic rules/state;
B. minimal local embedding prototype;
C. Aurelio Semantic Router;
D. vLLM Semantic Router;
E. ModernBERT only once its data gate passes;
F. relevant LLMRouter algorithms;
G. RouteLLM-style Tier-3 preference scoring;
H. OpenRouter Auto in sanitized shadow mode.

Evaluate separately:

### Mission/profile inference

- multi-label task-family precision/recall/F1;
- phase/domain/complexity/intensity calibration where labels are meaningful;
- uncertainty/abstention quality.

### Deterministic eligibility

- zero false `LOCAL_ONLY -> cloud`;
- zero secret-policy bypass;
- zero required-tool/modality/context/sandbox/network eligibility bypass;
- ZDR/data-policy compliance.

### Workflow/model economics

- accepted-task success;
- regret versus best eligible matched route;
- cost per accepted mission;
- retry/failure cost;
- TTFT/wall time/throughput;
- model/provider/cache switches;
- prompt-cache hit/read share;
- tool-capability failures;
- human overrides.

### Router operations

- p50/p95/p99 decision latency;
- startup time;
- RSS/memory pressure;
- determinism/replayability;
- dependency/runtime complexity;
- failure/fallback behavior.

Use mission/repository/session/time cohort splits. Do not randomly scatter turns from one trajectory across train/test.

---

# Promotion and maturity

Use the repository maturity vocabulary accurately:

- `researched` — current upstream evidence supports the candidate/idea;
- `designed` — contract/config/evaluation plan exists;
- `prototype` — runnable implementation exists;
- `smoke-tested` — narrow deterministic fixture passes;
- `shadow` — observes/recommends without authority;
- `canary` — bounded real traffic/authority;
- `production-approved` — representative outcome, security, rollback and human gates passed.

Current default posture:

- deterministic rules/state: prototype/smoke baseline;
- Aurelio/vLLM/LLMRouter/RouteLLM/OpenRouter Auto: researched/designed challengers until executed in our harness;
- ModernBERT fine-tuned router: researched only; not trained;
- Phase 30: shadow only;
- Phase 60: earliest ordinary routing promotion.
