# OpenRouter Gateway, Model Roles and Provider Routing

Snapshot: 2026-08-30.

## Decision

OpenRouter is the **default external inference gateway** for the uplift. It is downstream of our local security and mission-routing decisions:

```text
MISSION
  |
  v
Tier 0: deterministic privacy / security / policy
  |-- LOCAL_ONLY --> local path or BLOCKED
  v
Tier 1: local mission router
  |  rules/state -> embedding prototype -> ModernBERT if earned
  v
research | coding | hybrid | review | auxiliary | abstain
  |
  v
model-role binding
  |
  v
OpenRouter model ID
  |
  v
OpenRouter physical-provider routing
```

The boundaries are deliberate:

- **privacy/security routing** is deterministic and local; it runs before any cloud request;
- **mission routing** is owned by our local router, ultimately a learned ModernBERT classifier only if evidence supports it;
- **model selection** is owned by our role-binding configuration;
- **physical provider selection** may be delegated to OpenRouter subject to our constraints;
- **OpenRouter Auto** may be benchmarked for bootstrap/shadow/fallback/ambiguous generic work but is never the privacy boundary or final mission classifier.

Direct Z.ai, DeepSeek or other provider APIs remain benchmarked alternatives. They are not the default architecture and do not receive credentials until direct access proves materially better on cost per accepted task, latency, cache behaviour, reliability, privacy, rate limits or parameter support.

## Bootstrap model

Do not require the optimized router before Hermes can build it.

The fresh bootstrap profile uses **one OpenRouter model** for early phases. Current research snapshot: `z-ai/glm-5.3-flash`. This ID is evidence, not a permanent constant: at installation time use current Hermes `hermes model` / profile alias model picker and record the exact resolved OpenRouter ID.

GLM-5.3-Flash is a pragmatic bootstrap candidate because the current OpenRouter listing describes it as an efficient coding/long-horizon agent model and it is inexpensive relative to larger reasoning models. The uplift must still measure tool correctness, accepted-task quality and provider behaviour rather than assuming capability from a model card.

Bootstrap flow:

```text
fresh narrow Hermes
  -> OpenRouter
  -> one GLM-Flash-class bootstrap model
  -> Phases 00-20
  -> build/validate local router in Phase 30
  -> shadow routing
  -> only later introduce multiple model roles
```

## Steady-state role intent

The role names are architecture; model IDs are replaceable bindings.

| Role | Research-snapshot candidate | Purpose |
|---|---|---|
| `bootstrap.default` | `z-ai/glm-5.3-flash` | initial single-model uplift |
| `coding.default` | `z-ai/glm-5.3-flash` | Pi coding/tool loop candidate |
| `research.default` | `deepseek/deepseek-v4-flash-0731` | research/synthesis candidate |
| `review.default` | unbound until benchmark | independent-family review for higher risk |
| `auxiliary.cheap` | unbound/optional | cheap bounded auxiliary work only if useful |

Never spread these snapshot IDs through multiple policy documents. Keep runtime IDs in config/locks/evidence and re-verify current stable availability before promotion.

## Hermes provider-routing controls

Current Hermes documents these OpenRouter `provider_routing` controls:

```yaml
provider_routing:
  sort: price             # price | throughput | latency
  only: []
  ignore: []
  order: []
  require_parameters: true
  data_collection: deny
```

Treat that as the request-level routing policy Hermes actually supports today. Do not invent unsupported Hermes YAML keys merely because OpenRouter's raw API supports a larger provider object.

Use OpenRouter account/workspace privacy guardrails as a second layer where available. In particular, privacy restrictions must fail closed rather than relax merely to reach a cheaper endpoint.

### Preset warning

Do not make an OpenRouter preset the sole provider-policy authority while Hermes also emits request-level `provider_routing`. A current Hermes issue reports that request-level provider fields can override preset provider policy. Until that interaction is explicitly qualified, keep one canonical request-level policy plus account-level guardrails and test the effective provider response.

## Provider stickiness and caching

Do not reroute the physical provider on every request merely to shave marginal price.

For a long phase/session, prefer provider/model affinity when it improves:

- prompt-cache hits;
- behavioural/tool consistency;
- TTFT stability;
- retry rate;
- accepted-task quality.

OpenRouter supports session-aware sticky routing/caching mechanisms, but the stack still measures actual cache-read tokens and effective provider continuity. A routing mode that constantly changes providers can be cheaper per nominal input token yet more expensive per accepted task.

## OpenRouter Auto

OpenRouter Auto is a **model router**, not our privacy boundary and not the final research-vs-code classifier.

Allowed experiments:

- first-day bootstrap when an exact bootstrap model is unavailable;
- shadow comparison against our local router;
- low-risk generic auxiliary work;
- bounded fallback when policy explicitly permits it.

Disallowed uses:

- deciding whether sensitive content may leave the machine;
- overriding `LOCAL_ONLY`;
- silently replacing stable role bindings;
- choosing the production research/coding lane after our router has authority;
- hiding the actual model/provider from evidence.

## Credential footprint

Preferred steady state:

```text
OPENROUTER_API_KEY
```

Additional direct-provider credentials are a measured exception, not a default. Store the key through Hermes' provider setup/.env mechanism; never commit it or put it in bootstrap prompts/evidence.

## Benchmark contract

Evaluate the gateway/provider layer on **cost and minutes per accepted task**, including:

- fresh/cached input and output cost;
- TTFT and wall time;
- throughput and queue delay;
- provider/model continuity;
- cache-hit/read share;
- tool-call correctness and parameter support;
- retries/fallbacks/rate-limit failures;
- privacy/provider-policy compliance;
- accepted-task quality.

Periodically compare OpenRouter against direct Z.ai/DeepSeek endpoints on the same frozen tasks. Direct access becomes a production exception only when the improvement is material enough to justify another credential and integration path.
