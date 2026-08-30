# Savings and Accepted-Task Economics

Planning baseline supplied: **3,888,531,773 logical tokens/month**.

## Measure three different things

Prompt/context work affects different metrics:

1. **logical token volume** — smaller prompts/specs/tool output/context;
2. **fresh vs cached input** — stable prefixes/provider affinity may lower input cost/TTFT even when logical tokens remain visible;
3. **accepted-task economics** — retries, bad tool calls, queue time, reviewer/human intervention and escaped defects can dominate nominal token price.

Do not collapse these into one “token savings” percentage.

## Token-volume targets are hypotheses

Reasonable experiment bands, not promises:

| Hypothesis | Logical token reduction | Monthly tokens avoided at supplied baseline |
|---|---:|---:|
| conservative | 20% | ~777.7M |
| strong | 35% | ~1.361B |
| aggressive | 50% | ~1.944B |

The likely levers are Phase-20 prompt/skill/tool-schema slimming, T2 retrieval instead of artifact replay, Spec Kit profile selection, bounded diagnostics/tool output and compaction/recovery behaviour.

## Cache economics

If fraction `H` of input is served at cache-price fraction `R` of fresh input, the input-cost multiplier is:

```text
(1 - H) + H * R
```

This is only an accounting identity. The actual `H` and `R` must come from the selected model/physical provider and measured OpenRouter/provider response metadata. Do not assume one provider's cache pricing applies after a provider switch.

Provider churn can reduce nominal price while destroying cache affinity. Therefore record model + physical provider continuity alongside cache-read tokens.

## OpenRouter-first price snapshot

OpenRouter is the default external gateway, so the primary economic comparison is **model role + effective OpenRouter physical provider**, not a direct-provider rate card.

At the 2026-08-30 research snapshot, OpenRouter's comparison page lists approximately:

- `z-ai/glm-5.3-flash`: **$0.075/M input, $0.25/M output**;
- `deepseek/deepseek-v4-flash-0731`: **$0.03/M input, $0.10/M output**.

These are volatile headline rates and may differ by physical provider, cache behaviour, routing policy, time or future model revision. They are not budget constants and are deliberately not embedded into security/routing policy.

Use the live OpenRouter/Hermes model/provider view at execution time and persist the actual tested model/provider/rate snapshot in evidence.

## Why there is no hard monthly-dollar promise

The supplied baseline does not contain the real input/output/reasoning mix, cache-read share, provider distribution, retries or accepted-task outcomes. A single monthly-dollar number would therefore be false precision.

Compute actual cost from captured telemetry:

```text
cost =
  fresh_input_tokens * fresh_input_rate
+ cached_input_tokens * cached_input_rate_if_applicable
+ output_or_reasoning_tokens * output_rate
+ retry/fallback costs
```

Then compare **matched tasks**, not different workloads.

## Direct provider economics are a challenger

Direct Z.ai/DeepSeek APIs are not the default architecture. Periodically run matched benchmarks only if useful and include the operational cost of:

- another credential;
- another client/integration path;
- different cache semantics;
- different privacy/data controls;
- rate-limit/failover logic;
- monitoring/reconciliation complexity.

A direct provider is promoted only when its material advantage on accepted-task cost/latency/reliability/privacy justifies that added surface.

## Phase-aligned economic evidence

### Phase 10 — baseline
Record current logical/fresh/cached tokens, TTFT/wall time, provider/model, tool calls/retries, human intervention and accepted outcome.

### Phase 20 — first self-benefit
Measure hot-prefix size, skill/tool-schema tokens, T1 size/update count, T2 bytes produced vs loaded, LCM compaction/recovery and Mnemosyne injection. This is where token/context savings should first become real.

### Phase 30 — routing shadow
Record router decision cost/RSS/latency, route switches, hypothetical role selection and OpenRouter model/physical-provider cache continuity. Shadow predictions do not get credited as savings until authority is promoted.

### Phase 40/50 — enforcement + Pi
Include security scan/containment overhead, worker startup, retries, test/LSP evidence and invalid/blocked attempts. A security control that prevents an unsafe cheap request is a success even if it increases nominal cost.

### Phase 60 — promotion
Compare the whole system on matched representative tasks and bootstrap confidence intervals for accepted-task quality, cost and time.

## Top-line metrics

Promote on:

- accepted-task quality/success;
- **cost per accepted task**;
- **minutes per accepted task**;
- retries/rework per accepted task;
- human interventions per accepted task;
- fresh/cached/logical token mix;
- TTFT/wall time;
- cache/provider continuity;
- memory/context/tool-schema overhead;
- workstation resource pressure;
- security/privacy incidents (mandatory zero for prohibited paths).

A token-saving design that increases rework, stale-memory influence, tool failures or human recovery has failed.
