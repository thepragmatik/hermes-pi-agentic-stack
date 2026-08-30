# Projected Savings Model

Baseline supplied: **3,888,531,773 logical tokens/month**.

## Important distinction

Prompt caching often discounts cached input but does **not** remove it from logical token counts. Therefore there are two savings dimensions:

- **token-volume reduction** from smaller prompts/specs/tool output/context;
- **bill reduction and TTFT reduction** from cached repeated prefixes.

## Token-volume opportunity

Reasonable targets to validate experimentally rather than promise:

| Optimization maturity | Logical token reduction target | Monthly tokens avoided at baseline |
|---|---:|---:|
| Conservative | 20% | ~777.7M |
| Strong | 35% | ~1.361B |
| Aggressive but plausible | 50% | ~1.944B |
| Stretch | 55% | ~2.138B |

The largest volume levers are Spec Kit profile selection, tool-schema separation, retrieval instead of artifact replay, bounded tool output and earlier compaction.

## Cache opportunity

If a fraction `H` of *input* tokens hits a cache priced at fraction `R` of fresh input, the input-cost multiplier before volume reduction is:

```text
(1 - H) + H * R
```

Example: 70% input cache hit at 20% cached-input price => `0.30 + 0.70*0.20 = 0.44`, a **56% input-cost reduction** even though those cached tokens may still appear in usage.

At a 10% cache-read price, 70% hits => 63% input-cost reduction.

## Current model-price observations (snapshot, verify before purchasing)

### GLM-5.3-Flash

Public 2026 launch listings show approximately:

- current promotion: **$0.075/M input, $0.015/M cached input, $0.25/M output**;
- published list/reversion around **$0.15/M input, $0.03/M cached, $0.50/M output**.

The promotion has a short published end date in September 2026, so use **list price** for steady-state planning.

### DeepSeek V4 Flash

DeepSeek native pricing currently uses peak/off-peak bands and automatic context caching. For DeepSeek-V4-Flash-0731, the official rate card observed on 2026-08-30 is **$0.44/M fresh input, $0.014/M cache-hit input, $1.32/M output at peak**, with off-peak rates exactly half.

OpenRouter's current `deepseek/deepseek-v4-flash-0731` page is materially cheaper at **$0.03/M input, $0.007/M cache read and $0.10/M output** on the cheapest displayed route. This is an unusually large provider spread. Do not choose from price alone: benchmark exact provider, p95 TTFT/throughput, tool-call correctness, cache behavior, data policy, rate limits and failure/fallback semantics. Pin the serving provider for a session when cache affinity and determinism matter.

## Worked cost examples

Because the exact input/output split was not supplied, the examples assume **85% input / 15% output**, typical of a context-heavy agent loop but not a claim about your actual telemetry.

### GLM-5.3-Flash at list price

No input caching:

- estimated monthly cost at 3.888B tokens: **~$787**.

With 70% of input hitting cached-input price:

- estimated cost: **~$510**.

With the same 70% input-cache hit plus 40% logical-token reduction:

- estimated cost: **~$306**.

That is roughly **61% lower** than the uncached/unoptimized list-price example.

### DeepSeek V4 Flash — current OpenRouter low-cost route

Using the current OpenRouter 0731 headline route at $0.03/M fresh input, $0.007/M cache read and $0.10/M output, at the same 85/15 split:

- no caching: **~$157/month**;
- with 70% of input hitting the $0.007/M cache-read rate: **~$104/month**;
- plus 40% logical-token reduction: **~$63/month**.

For comparison, the current DeepSeek **native peak** card at $0.44/M fresh input and $1.32/M output is about **~$2,224/month** without cache on the same assumed token mix; running entirely off-peak halves that. Native may still win on official serving guarantees, concurrency or consistency, so the provider bake-off must measure accepted-task economics rather than blindly selecting the cheapest token rate.

These surprisingly small OpenRouter totals are a consequence of extraordinary 2026 Flash-provider pricing, not an error in the token baseline. At these prices, engineering time and reliability can be worth more than the raw API bill.

## Expected overall range

A defensible target for the uplift is:

- **25–50% logical token reduction** after Spec Kit/context/tool optimization;
- **60–90% cache-hit rate on the stable repeated input prefix** for long sequential sessions, where the provider supports it and routing remains sticky;
- **45–75% reduction in input-side spend/compute** versus an uncached, prompt-heavy baseline;
- **30–65% overall API spend reduction** as an initial planning band when output/reasoning remains a meaningful share.

An aggressive workload with very high repeated-input share can exceed this; a workload dominated by generated reasoning/output will save less.

## More valuable than raw API dollars

At Flash-model pricing, the economic win may come primarily from:

- lower TTFT and faster agent loops;
- fewer retries and invalid tool calls;
- less workstation memory pressure;
- higher concurrency before provider quotas;
- reduced context-decay defects;
- less human supervision;
- predictable security behavior.

Track **cost per accepted task**, **minutes per accepted task**, and **human interventions per accepted task** as the top-line measures.

## Savings experiment

For a statistically useful mission sample, record baseline and uplift variants. Stratify by research/coding/hybrid and task size. Do not compare different tasks.

Report:

```text
logical input/output tokens
fresh vs cached input
provider/model
TTFT and total wall time
number of model requests
number of tool calls/retries
accepted outcome
reviewer interventions
escaped defects within observation window
```

Calculate bootstrap confidence intervals for the median/mean cost and time deltas. Promote the uplift only if quality is non-inferior.
