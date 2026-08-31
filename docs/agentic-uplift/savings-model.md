# Savings and Accepted-Mission Economics

Planning baseline supplied: **3,888,531,773 logical tokens/month**.

## Measure four different things

1. **Logical token volume** — smaller prompts/specs/tool output/context.
2. **Fresh vs cached input** — stable prefixes/model/provider/session affinity may lower cost/TTFT even when logical tokens remain visible.
3. **Router/workflow overhead** — local CPU/RSS/latency, model/provider switches, context transfer and extra tool/agent setup.
4. **Accepted-mission economics** — retries, failed stages, bad tool calls, queue time, reviewer/human intervention and escaped defects.

Do not collapse these into one “token savings” percentage. The routing objective is much closer to **cost and minutes per accepted mission** than cost per million tokens.

## Token-volume targets are hypotheses

| Hypothesis | Logical token reduction | Monthly tokens avoided at supplied baseline |
|---|---:|---:|
| conservative | 20% | ~777.7M |
| strong | 35% | ~1.361B |
| aggressive | 50% | ~1.944B |

Likely levers are Phase-20 prompt/skill/tool-schema slimming, T2 retrieval instead of artifact replay, Spec Kit profile selection, bounded diagnostics/tool output and compaction/recovery behavior.

## Routing economics from first principles

For a mission profile `m`, candidate eligible workflow/model route `r`, estimate total expected loss rather than nominal token price:

```text
expected_loss(r | m) =
  expected_inference_cost
+ expected_retry/failure_cost
+ expected_latency_cost
+ expected_context/cache_switch_cost
+ expected_tool/workflow_overhead
+ expected_human_intervention_cost
+ penalty_if_quality_floor_or_risk_requirement_is_missed
```

Tier 0 removes ineligible routes before this optimization. Tier 1/2 determine the mission profile/workflow candidates. Tier 3 compares eligible model-role/model options. Tier 4/OpenRouter handles downstream provider execution subject to hard provider requirements.

A cheaper model/provider that causes more retries, tool failures, context degradation or review rejection can be more expensive per accepted mission.

## Cache and switching economics

If fraction `H` of input is served at cache-price fraction `R` of fresh input, input-cost multiplier is:

```text
(1 - H) + H * R
```

Actual `H`/`R` must come from the selected model/physical provider and observed metadata. Record model, provider where observable, cached tokens, workflow/model/provider switches and the reason for each switch.

Session/provider affinity is a routing requirement, not an assumption. If the installed Hermes/OpenRouter path cannot prove stable session identity or provider/model continuity, do not credit hypothetical sticky-cache savings.

## OpenRouter changes what we should maintain ourselves

OpenRouter is the default external gateway. Our stack should normally own mission semantics, workflow and model selection while reusing OpenRouter provider capabilities such as eligible provider filtering, parameter support, data/ZDR policy, routing by price/latency/throughput and provider failover where the actual integration proves them.

This avoids rebuilding a provider health/rate/failover layer. It does **not** eliminate the need to measure:

- actual selected model and provider where observable;
- cache-read share and continuity;
- provider/model fallback reason;
- retries/rate limits/queue delay;
- tool/structured-output compatibility;
- privacy/ZDR/parameter compliance;
- accepted-mission quality.

Raw OpenRouter capabilities that the installed Hermes path does not forward are not economic benefits until an account policy or qualified gateway adapter demonstrably provides them.

## Direct-provider/local adapters are challengers

Direct DeepSeek/Z.ai or local MLX adapters use the same routing contracts. Promote one only if matched-mission evidence justifies the additional credential/integration/monitoring/cache/privacy complexity. Mission semantics must not change merely because the gateway adapter changes.

## Router bake-off economics

Compare candidates on the same corpus and, where technically feasible, the same downstream model/workflow outcomes:

```text
A deterministic rules/state
B minimal embedding prototype
C Aurelio Semantic Router
D vLLM Semantic Router
E ModernBERT when data is sufficient
F LLMRouter research algorithms
G RouteLLM-style Tier-3 scorer
H OpenRouter Auto shadow/teacher
```

Include router startup/RSS/CPU/p50/p95/p99, operational process/dependency burden and failure recovery. A sophisticated router must earn its hot-path cost.

A simpler rules/embedding router is the correct production choice if it captures most of the accepted-mission economic benefit.

## Outcome telemetry

Privacy-minimized records should join:

```text
mission/profile digest
workflow/stage
router candidate + confidence/maturity
model role/model
provider when observable
fresh/cached/output tokens
TTFT/wall time
router latency/RSS
model/provider/workflow switches
tool calls/failures
retries
checks/tests/review outcome
human override
accepted/rejected + failure reason
actual/estimated cost
```

Raw sensitive prompts are not required for routine economic telemetry. Keep explicitly sampled training records local/redacted under separate retention policy.

## Phase-aligned economic evidence

### Phase 10 — baseline
Record logical/fresh/cached tokens, TTFT/wall time, provider/model, tool calls/retries, human intervention and accepted mission outcome using the single bootstrap model.

### Phase 20 — first self-benefit
Measure hot-prefix size, skill/tool-schema tokens, T1/T2 behavior, LCM compaction/recovery and Mnemosyne injection. Dogfood the prompt/skill increment before later layers.

### Phase 30 — routing shadow
Record mission-profile/task/workflow inference, eligibility violations, abstention, local router resource cost, hypothetical workflow/model choices, candidate disagreements, OpenRouter Auto shadow signal, route/model/provider switches and cache continuity. Shadow predictions receive no savings credit until they are tied to matched outcomes.

### Phase 40/50 — enforcement + Pi
Include security scan/containment overhead, worker startup, routing-decision provenance, retries, tests/LSP evidence and blocked invalid routes. Preventing an unsafe cheap request is success even if nominal cost rises.

### Phase 60 — promotion
Compare whole-system routes on representative matched missions. Primary metrics are accepted-mission quality, regret, cost/time per accepted mission, security invariants and operational resilience. Classification F1 is diagnostic, not the business objective.

## Top-line metrics

Promote on:

- accepted-mission success/quality;
- **cost per accepted mission**;
- **minutes per accepted mission**;
- routing regret vs best eligible observed route;
- retries/rework and human interventions per accepted mission;
- fresh/cached/logical token mix;
- TTFT/wall time;
- workflow/model/provider switch rate and cache continuity;
- router + memory/context/tool-schema overhead;
- workstation resource pressure;
- tool-capability failures;
- privacy/security violations — mandatory zero on prohibited paths.

A token-saving or classifier-accurate design that increases rejected missions, unsafe eligibility, workflow churn, stale-memory influence, tool failures or human recovery has failed.