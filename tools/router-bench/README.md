# Router Bake-off Harness

This harness compares routing candidates behind the repository's framework-neutral contracts. It deliberately separates:

1. multi-label mission/task-profile inference;
2. deterministic hard eligibility;
3. workflow/stage selection;
4. runtime footprint;
5. optional real outcome economics.

It does **not** assume `research|coding|hybrid` is the routing ontology.

## Default smoke

The checked-in deterministic baseline uses only the Python standard library:

```bash
python tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --fail-on-hard-violations \
  --pretty
```

This is a regression fixture, not production evidence.

## Minimal embedding challenger

Install the model/runtime separately, then:

```bash
python tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules,prototype \
  --embedding-model nomic-ai/modernbert-embed-base
```

The prototype performs multi-label centroid matching. It is intentionally simple.

## External adapters

Aurelio Semantic Router, vLLM Semantic Router, custom ModernBERT, LLMRouter, RouteLLM-style scorers and OpenRouter Auto can be integrated without coupling the benchmark to their dependencies.

Register adapters:

```bash
python tools/router-bench/router_bench.py \
  --dataset missions-held-out.jsonl \
  --routers rules,aurelio,vllm \
  --external 'aurelio=python adapters/aurelio_adapter.py' \
  --external 'vllm=python adapters/vllm_adapter.py'
```

The adapter receives one JSON object on stdin:

```json
{
  "id": "mission-id",
  "text": "sanitized mission text",
  "constraints": {
    "privacy": {"class": "INTERNAL", "cloud_allowed": true}
  }
}
```

and returns:

```json
{
  "tasks": ["research", "architecture_design"],
  "phase": "discovery",
  "workflow": "multi_stage",
  "confidence": 0.84,
  "detail": {}
}
```

The harness applies the local Tier-0 `LOCAL_ONLY` gate before invoking any external adapter. Do not use a cloud adapter on unsanitized or policy-ineligible missions.

## Candidate roles

| Candidate | Benchmark role |
|---|---|
| deterministic rules/state | hard baseline + simple profile/workflow inference |
| minimal embedding prototype | cheap local semantic baseline |
| Aurelio Semantic Router | local semantic component |
| vLLM Semantic Router | richer signal/projection/session-aware routing candidate |
| ModernBERT | future multi-label/multi-head inference after data gate |
| LLMRouter algorithms | research-plane algorithm comparison |
| RouteLLM-style model | Tier-3 strong-vs-economical scoring |
| OpenRouter Auto | sanitized shadow teacher/model-routing comparator |

Not every candidate solves every tier. Do not compare a RouteLLM preference score to a PII hard gate as if they were the same task.

## Outcome economics

Classification/profile metrics are insufficient. Pass an optional outcome JSONL:

```json
{"id":"m1","candidate":"rules","accepted":true,"cost_usd":0.04,"total_latency_ms":4200,"retries":0,"human_override":false,"tool_failures":0,"model_switches":0,"provider_switches":0,"cache_hit_rate":0.62}
```

with:

```bash
--outcomes outcomes.jsonl
```

The harness reports accepted rate and cost per accepted mission plus retries, human overrides, switching, cache-hit rate and latency.

For meaningful economic comparison, outcomes must come from matched eligible workflow/model runs against the same frozen task/environment. Synthetic fixtures are not production evidence.

## What the harness reports

### Mission/profile inference

- multi-label task-family micro/macro F1;
- exact task-set accuracy;
- phase accuracy;
- uncertainty/abstention behavior.

### Hard eligibility

- `LOCAL_ONLY -> nonlocal` violations;
- false cloud eligibility.

The checked-in fixture covers privacy/cloud eligibility. Production evaluation must additionally test tool, modality, context, ZDR, network, sandbox and approval/review constraints at the routing-contract/policy layer.

### Workflow/runtime

- workflow accuracy where an adjudicated workflow target exists;
- p50/p95/p99 router latency;
- startup time/RSS;
- replay determinism;
- adapter failures.

### Real outcomes

- accepted rate;
- cost per accepted mission;
- retries/tool failures/human override;
- latency;
- model/provider switching;
- cache-hit rate.

## Splits

For training/evaluation corpora, split by mission/repository/session/time cohort. Never scatter near-duplicate turns from one trajectory across train/test.

Maintain separate clean held-out, boundary/adversarial and later temporal canary sets.

## Privacy

By default benchmark result rows contain SHA-256 of mission text, not text. `--include-text` is for explicitly approved local diagnostics only.

Outcome telemetry should contain only the minimum redacted/profile/decision/result facts needed for learning. Raw prompts are not the default training or evidence store.

## Promotion

No single F1 threshold is sufficient. Promotion hierarchy is hard-constraint safety, accepted-mission regret/quality, cost per accepted mission, capability failures/retries/human overrides, switching/cache behavior, latency, profile metrics, then router footprint/operational complexity.

A simpler router is allowed to win.
