# Local Mission Routing Models and Frameworks — 2026 Assessment

## Router responsibility

The local router does **mission classification and model-role selection**, not cloud privacy and not physical-provider routing.

```text
Tier 0 deterministic local privacy/security policy
 -> local mission router
 -> model-role/model binding
 -> OpenRouter
 -> physical provider
```

OpenRouter Auto is not the primary mission classifier. A classic strong-vs-weak preference router is also not the same thing as research-vs-code mission classification.

## Recommended progression

### 0. Deterministic privacy/state gates — mandatory

Use deterministic code for `LOCAL_ONLY`, credential/PII/security constraints and operational state that Hermes already knows. Security/privacy is not learned preference.

Rules may also resolve obvious lane signals, but ambiguous work falls through to semantic classification.

### 1. Rules + explicit state baseline

Before adding embeddings, benchmark a compact deterministic baseline using features such as current phase/lane, write intent, active worker, test failure, research requirement, risk/security class and recent route switches.

This baseline is interpretable and establishes whether semantics are actually needed.

### 2. Frozen embedding encoder + calibrated lightweight head

Benchmark at minimum:

- `nomic-ai/modernbert-embed-base` at 256d and 768d;
- Qwen3-Embedding-0.6B as a larger embedding challenger;
- a smaller licensing-compatible encoder if it materially improves latency/RSS.

Use the same mission corpus, structured-state features and calibrated logistic/linear head for a fair comparison. The frozen ModernBERT embedding path is particularly attractive because it is much smaller than a generative router and can be retrained cheaply without changing the encoder.

Do **not** name one embedding model “best” before the target-Mac/representative-mission bake-off.

### 3. Fine-tuned ModernBERT-base — only after outcome data exists

ModernBERT-base is an encoder architecture well matched to mission classification, but fine-tuning is a later graduation step.

Promote encoder fine-tuning only when:

- the route ontology has stabilized;
- representative real missions have been locally redacted/deduplicated;
- labels include actual accepted-task outcomes, retries and human overrides rather than only LLM opinions;
- train/test separation is by mission/repository/session/time cohort;
- ambiguous/hybrid/security-vocabulary cases are represented;
- the frozen encoder + calibrated head has plateaued for reasons attributable to representation rather than label/design errors.

There is no magic fixed mission count or number of weeks that proves readiness; use learning curves, holdout stability and downstream regret.

### 4. RouteLLM-style difficulty/preference — optional second stage

RouteLLM's historical strong-vs-weak framing can be useful for **difficulty/escalation after the lane is known**. Its pretrained preference weights are not a research-vs-code classifier and must not be interpreted as coding probability.

Any such layer must be recalibrated on current role-model outcomes before it receives authority.

### 5. Semantic Router — useful prototype framework

Aurelio Semantic Router remains a practical local prototype/benchmark framework. Keep it behind our own adapter/interface so it does not become the architecture or policy boundary.

## Bootstrap paradox avoided

Do not wait for any of the above before starting the uplift. Bootstrap uses one explicit OpenRouter model through the early phases. Phase 30 builds the router and enters shadow mode; only Phase 60 can promote ordinary multi-role authority.

## Route phases, not micro-turns

A good router keeps a lane sticky within a meaningful phase and switches only on deliberate phase/state changes or calibrated confidence/margin.

Examples:

- active Pi repair loop -> remain coding;
- research source collection -> remain research;
- accepted research plan transitions into implementation -> phase boundary may switch coding;
- uncertainty -> abstain/hybrid rather than oscillate.

Use separate enter/leave thresholds/hysteresis and measure route switches per mission.

## Training data

Public datasets can seed coverage but must not become the final truth:

1. SWE-bench-family issue prompts — coding-positive examples;
2. CodeSearchNet query/doc language — code/search semantics, respecting per-sample licenses;
3. BFCL/tool-use examples — tool-action/coding-adjacent language;
4. RouteLLM preference data — difficulty/preference experiments, not direct mission labels;
5. broad public/gated chat distributions only after license/privacy review;
6. **locally redacted Hermes mission telemetry and matched role-model outcomes** — highest-value final data.

Maintain a dataset bill of materials and separate distributable vs internal-use recipes.

### Outcome labeling

```text
mission + state
 -> candidate lane/model role
 -> actual result
 -> accepted? tests? reviewer evidence? retries? cost? latency? human override?
```

For ambiguous samples, run candidate role models against the same frozen task/environment. The gateway may be OpenRouter, but record the actual model and physical provider when observable so provider effects are not mistaken for classifier quality.

### Active learning

Prioritize low margin, abstentions, route switches, human overrides, failures/retries, hybrid missions, long Spec Kit work and security vocabulary that contains no sensitive payload.

## Evaluation

Promotion hierarchy:

1. accepted-task utility/regret;
2. zero `LOCAL_ONLY -> cloud` violations (enforced upstream, measured here as an invariant);
3. high-severity wrong-lane errors;
4. retries/human overrides;
5. route-switch rate and OpenRouter physical-provider/model cache continuity;
6. wall time/TTFT/cost per accepted task;
7. calibration/abstention and macro-F1;
8. local router p50/p95 latency and RSS/memory pressure.

Split by mission/repository/session/time, not random near-duplicate turns.

## Final policy shape

```text
privacy_result = deterministic_policy(mission, state)
if privacy_result == LOCAL_ONLY:
    local_or_block()
else:
    lane = deterministic_state_gate(...) or semantic_router(...)
    if lane confidence is insufficient:
        abstain_or_hybrid()
    role_model = role_binding(lane)
    call OpenRouter(role_model, provider_policy)
```

For hybrid work, a typical pattern is a research artifact followed by a typed Pi coding task. The router never decides merge authority.
