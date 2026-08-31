# Router Training, Outcome Learning and Control

Snapshot: 2026-08-31.

## Decision

Do not train a model to reproduce the old `research | coding | hybrid` labels.

The routing stack now separates:

```text
Tier 0 deterministic eligibility
  -> Tier 1 multi-label mission/profile inference
  -> Tier 2 bounded workflow/agent selection
  -> Tier 3 model-role/model economics
  -> Tier 4 gateway/provider execution
```

Training is allowed only for signals that benefit from learning. Known policy/capability facts remain deterministic.

The router should optimize **accepted completion under constraints and budget**, not classification accuracy in isolation.

---

# What may be learned

Useful learned/inferred outputs include:

- task families (multi-label);
- domain(s);
- workflow phase;
- complexity;
- uncertainty/abstention;
- reasoning intensity;
- tool intensity;
- expected context-need band;
- expected relative model/workflow quality.

Do **not** train the router to predict authoritative values already known from state/config, including:

- `LOCAL_ONLY` when policy has already classified the payload;
- whether a secret is permitted to leave the machine;
- tool availability;
- network/sandbox permission;
- actual modality supplied by the request;
- actual model context-window/tool/structured-output capabilities;
- policy-required human approval/review.

A learned signal may flag a possible issue for deterministic re-evaluation, but cannot override the hard result.

---

# Staged curriculum

## Stage 0 — deterministic baseline

Benchmark:

1. deterministic Tier-0 eligibility;
2. rules/state-only task-family inference;
3. rules/state-only workflow selection;
4. explicit abstention for unresolved cases.

The previous “always research / always coding” controls may remain in the research harness as deliberately poor controls, but they are no longer the production ontology.

## Stage 1 — simple semantic challengers

Compare on the same mission-profile corpus:

- a minimal embedding/prototype classifier;
- Aurelio Semantic Router with a local encoder;
- frozen `nomic-ai/modernbert-embed-base` at 256d and 768d;
- Qwen3-Embedding-0.6B or another measured local embedding challenger;
- vLLM Semantic Router signals/projections in shadow through our adapter.

Where a learned head is needed, fit the same calibrated logistic/linear heads to each embedding representation. Use one-vs-rest or another calibrated multi-label method rather than forcing one mutually exclusive label.

## Stage 2 — research-plane algorithm bake-off

Use LLMRouter and/or isolated experiment adapters to compare KNN, SVM, MLP, BERT-like, MF/graph and other relevant algorithms without putting the whole research framework in the production path.

Use RouteLLM-style preference/MF/BERT methods only for Tier-3 questions such as:

> Among these already eligible models, when is the stronger/more expensive one worth its cost?

## Stage 3 — active learning from real missions

Prioritize review/labeling of:

- low-confidence/low-margin multi-label predictions;
- abstentions;
- workflow transitions;
- human overrides;
- tool/capability failures;
- retries/fallbacks;
- missions where candidate workflows/models disagree materially;
- long-running/multi-stage missions;
- security vocabulary with no sensitive payload;
- new domains/modality combinations;
- model/provider switches that destroy cache affinity;
- expensive accepted or rejected missions.

## Stage 4 — matched outcome data

For a controlled subset, run eligible workflow/model candidates against the same frozen task/environment and capture:

```text
mission profile
constraints + session state
workflow/model/provider policy chosen
actual model + physical provider when observable
tokens + cached tokens
TTFT + wall time
tool calls + retries + fallbacks
tests/review evidence
human override
accepted/rejected
failure reason
actual/estimated cost
```

The final route target is based on these outcomes, not generic intent labels.

## Stage 5 — fine-tuned ModernBERT only if earned

A future ModernBERT should use a shared encoder with multiple calibrated heads rather than a single research/coding class head.

Candidate heads:

```text
task_family[]
domain[]
phase
complexity
reasoning_intensity
tool_intensity
context_need_band
uncertainty / out-of-distribution score
```

Model/workflow quality prediction may remain a separate Tier-3 scorer because its training target and refresh cadence differ from semantic mission inference.

---

# Frozen ModernBERT baseline

`nomic-ai/modernbert-embed-base` remains an attractive early challenger:

- ModernBERT-derived;
- Apache-2.0;
- 768-dimensional embeddings;
- supported 256-dimensional Matryoshka representation;
- local SentenceTransformers/ONNX-style deployment options;
- useful classification/retrieval benchmark characteristics.

Treat required query prefixes, truncation dimension, pooling/runtime and model revision as pinned configuration.

Fine-tune `answerdotai/ModernBERT-base` only after the evidence gate below. ModernBERT-base is a 149M encoder with 8,192-token context support and standard BERT-like downstream classification fine-tuning semantics.

---

# Input is text plus explicit state

Do not ask the semantic encoder to rediscover state Hermes already knows.

Useful structured features include:

```text
uplift/workflow phase
current workflow/stage
active agent/worker
file write requested
failing tests/diagnostics present
tool action pending
external information required
repo dirty
risk/review class
Spec Kit profile
available capability bitset
required modality/context band
recent model/workflow/provider switches
cache/read-token state
last route confidence
remaining session switch budget
```

Security/privacy fields enter the eligibility gate as hard facts, not soft features that can be voted away.

---

# Session-aware routing

Route **workflow stages and meaningful phases**, not isolated short turns.

Examples:

- a Pi worker repairing a failing test remains in the implementation/diagnosis workflow;
- a source-gathering session remains in research until a deliberate stage transition;
- an accepted design may transition into implementation;
- an implementation can transition into test and independent review without inventing a `hybrid` class;
- a short “continue” turn inherits session/stage state rather than being reclassified from text alone.

Use hysteresis/switch budgets. A model/workflow switch pays a real cost in cache warmth, context transfer, provider state and behavior continuity.

Conceptually:

```text
hard_eligibility = deterministic_filter(...)
profile = infer_profile(...)
candidates = eligible_workflows_models(hard_eligibility, profile)

if current_path remains eligible:
    switch_gain = expected_gain(best_candidate) - switch_cost(current_path)
    switch only when calibrated gain clears the stage-specific threshold
else:
    choose best eligible safe fallback
```

---

# ModernBERT training evidence gate

There is no fixed “10k examples” or “N weeks” threshold.

Fine-tuning is justified only when all are true:

- the task-family/workflow ontology has stabilized under real Hermes use;
- representative missions are locally redacted and deduplicated;
- multi-stage, ambiguous, long-running, multimodal/tool and new-domain cases are represented;
- labels include deterministic facts plus real execution outcomes rather than only LLM-generated intent labels;
- mission/repository/session/time cohort holdouts prevent leakage;
- learning curves and temporal holdouts are stable;
- simpler rules/embedding/Aurelio/vLLM-config baselines have plateaued on **routing regret and cost per accepted mission**;
- analysis shows the semantic representation is a bottleneck rather than poor policy/labels/workflow design;
- calibration and abstention remain reliable;
- training data has a reviewed provenance/license/privacy bill of materials.

If simpler routing delivers ~95% of the economic benefit, do not fine-tune merely to increase sophistication.

---

# OpenRouter Auto as teacher, never policy authority

For sanitized policy-approved missions, record Auto in shadow:

```text
our mission profile
our selected workflow/model
Auto-selected model
actual selected model/provider
outcome/cost/latency/retries
human override
```

Use this as a weak/teacher signal, not ground truth. Auto optimizes using OpenRouter's own market/task signals; our objective includes Hermes/Pi workflow semantics, security and accepted-mission economics that it does not own.

---

# Evaluation split

Never randomly split near-duplicate turns from one mission across train/test.

Use held-out **mission / repository / session / time cohorts**, with an additional later temporal canary for drift.

Evaluate both per-turn/profile inference and whole-mission routing outcomes. A classifier can be accurate per turn and still be a bad agent router if it thrashes models or picks the wrong workflow stage.

---

# Promotion hierarchy

1. hard-constraint/security violations — zero mandatory eligibility bypass;
2. accepted-task/mission utility and regret versus best eligible matched path;
3. cost per accepted mission;
4. tool/workflow capability failures;
5. retries/fallbacks/human overrides;
6. unnecessary workflow/model/provider switch rate;
7. cache-hit/read continuity;
8. TTFT/wall time/throughput;
9. multi-label task-family and phase/domain/intensity metrics;
10. calibration/abstention/OOD behavior;
11. router p50/p95/p99 latency, startup and RSS;
12. operational/dependency complexity.

A router with lower classification F1 can be superior if it abstains safely, avoids costly switches and improves accepted-mission economics.

---

# Outcome objective

The long-term learner should estimate something closer to:

```text
utility(route, mission) =
  P(accepted completion | mission, route)
  * quality_value
  - total_execution_cost
  - expected_retry_cost
  - latency_penalty
  - switch/cache_penalty
  - operational_risk_penalty
```

subject to hard eligibility constraints.

Do not collapse that into “which label does this sentence resemble?”

---

# Maturity and promotion

No learned router receives authority in Phase 30. Phase 30 is shadow.

A candidate progresses:

```text
researched -> designed -> prototype -> smoke-tested -> shadow -> canary -> production-approved
```

Production promotion occurs no earlier than Phase 60 and requires target-Mac operational evidence plus representative matched outcomes.
