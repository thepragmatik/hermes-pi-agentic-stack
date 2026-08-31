# OpenRouter Gateway, Model Roles and Provider Routing

Snapshot: 2026-08-31. Re-verify raw OpenRouter and installed Hermes capabilities at execution time.

## Decision

OpenRouter is the **default Tier-4 external inference gateway**, not the mission ontology and not the privacy/security boundary.

```text
MISSION
  -> Tier 0 deterministic eligibility/security
  -> Tier 1 mission-profile inference
  -> Tier 2 workflow/agent selection
  -> Tier 3 model-role/model optimization
  -> Tier 4 OpenRouter physical-provider execution
```

Our routing contracts choose mission semantics, workflow and model intent. OpenRouter normally chooses the physical provider for the already-approved model/request.

Direct DeepSeek, Z.ai, local MLX or another OpenAI-compatible/direct adapter is an alternate Tier-4 implementation. It must not change mission semantics.

---

# Why OpenRouter reduces infrastructure

For an explicitly selected model, OpenRouter's current provider-routing API can handle much of the infrastructure we would otherwise have to maintain ourselves:

- provider allow/deny/order;
- provider fallback;
- required-parameter support;
- data-collection filtering;
- per-request Zero Data Retention filtering;
- provider sorting by price, throughput or latency;
- maximum price constraints;
- preferred latency/throughput thresholds;
- model fallback chains;
- physical-provider health/failover;
- session/provider stickiness and prompt-cache reuse when a stable `session_id` is supplied.

Therefore our router should not implement its own provider load balancer unless measured requirements cannot be expressed through OpenRouter or a direct-provider adapter.

## Abstract provider requirements vs current Hermes keys

`protocols/routing-decision.schema.json` carries **abstract requirements** such as ZDR, data-collection policy, parameter support, performance/cost preferences, fallbacks and session affinity.

The adapter translates those requirements to the gateway actually used.

Current Hermes documentation exposes this OpenRouter subset under `provider_routing`:

```yaml
provider_routing:
  sort: price
  only: []
  ignore: []
  order: []
  require_parameters: true
  data_collection: deny
```

Do not put raw OpenRouter-only keys into Hermes config unless the installed Hermes release documents/supports them.

For requirements such as per-request `zdr`, max price/performance thresholds or stable OpenRouter `session_id`, the implementation must prove one of:

1. current Hermes forwards the required field;
2. an account/workspace guardrail enforces it;
3. a small audited gateway adapter injects it;
4. the request is blocked because the requirement cannot be guaranteed.

Never silently downgrade a requirement because the current client lacks a config field.

---

# Model roles are not task-family labels

Task families describe **what the mission needs**. Model roles describe **replaceable capability/economic pools**.

A small initial role set is preferable to one role per task family:

| Role | Intended characteristics | Likely task families |
|---|---|---|
| `bootstrap.default` | reliable tool-capable general agent for early uplift | most bootstrap work |
| `general.default` | balanced general-purpose execution | synthesis, documents, orchestration, retrieval |
| `reasoning.default` | stronger architecture/planning/analysis reasoning | design, planning, diagnosis, difficult analysis |
| `research.default` | strong information gathering/synthesis/verification | research, synthesis, fact checking |
| `coding.default` | strong tool/code behavior | implementation, debugging, refactoring, testing, DevOps |
| `review.default` | independent-family checking/judging | code/security/architecture review, verification |
| `multimodal.default` | required image/audio/video/file capability | multimodal missions |
| `local.default` | local model/tool path | LOCAL_ONLY or offline-eligible work |
| `auxiliary.cheap` | bounded low-risk cheap tasks | optional background/utility work |

One mission can use several roles over ordered stages. The router is not required to create a new role whenever the task taxonomy grows.

Snapshot model IDs belong in config/runtime locks, not in the task ontology.

---

# Bootstrap

Do not require an optimized router before Hermes can build it.

The fresh bootstrap profile still uses **one explicit OpenRouter model** through Phase 20. Research snapshot candidate: GLM-5.3-Flash-class (`z-ai/glm-5.3-flash` at the current snapshot), re-verified with the live Hermes/OpenRouter catalog during setup.

```text
fresh narrow Hermes
  -> OpenRouter
  -> one verified bootstrap model
  -> Phases 00 / 10 / 20
  -> Phase 30 rules/state router + shadow challengers
  -> later multi-role promotion only after gates
```

OpenRouter Auto may be an emergency bootstrap fallback only when explicit policy permits it; record the actual selected model.

---

# OpenRouter Auto

Auto is a **model router with a different objective and trust boundary**.

Current Auto behavior is useful because it can choose among a changing model pool and exposes the resolved model. It also has best-effort multi-turn model/provider stickiness when session affinity is available.

Use it for policy-approved sanitized missions as:

- shadow comparator;
- weak teacher/labeling signal;
- bounded fallback;
- bootstrap fallback if an explicit model disappears.

Do not use it for:

- `LOCAL_ONLY` or cloud-eligibility decisions;
- secret/PII policy;
- tool/network/sandbox authorization;
- deciding whether Pi may receive production authority;
- replacing our workflow planner;
- hiding selected model/provider identity from telemetry.

A useful Phase-30/60 record is:

```text
mission profile + deterministic requirements
our workflow/model-role/model decision
Auto resolved model
actual physical provider when observable
accepted/rejected outcome
tokens + cached tokens
TTFT / total latency
retries/fallbacks
human override
cost
```

Auto disagreement is a feature for analysis, not an automatic correction.

---

# Session/provider stickiness and caching

For long-running Hermes/Pi work, model/provider switching has a real economic cost.

OpenRouter currently documents explicit sticky routing using a stable `session_id`. This can pin the resolved model/provider for a conversation or agent run on a best-effort basis and improve prompt-cache reuse.

Use a stable session/workflow key where supported and measure:

- actual provider continuity;
- actual model continuity;
- `cached_tokens` / cache-write tokens;
- cache discount/cost when exposed;
- TTFT changes;
- retry/failover events;
- behavior/tool correctness across a switch.

At the 2026-08-31 snapshot, an open Hermes issue reports that normal Hermes OpenRouter chat requests do not forward OpenRouter's `session_id`. Treat provider stickiness as an **integration gap to qualify**, not a capability we already receive automatically. Prefer an upstream fix; if necessary, a thin gateway adapter may inject the stable session key behind our routing contract.

Hysteresis and session switch budgets remain local Tier-1/3 responsibilities even when OpenRouter supplies physical-provider stickiness.

---

# Provider policy

Translate hard requirements before tertiary optimization.

Example abstract policy:

```yaml
zdr_required: true
data_collection: deny
require_parameters: true
allow_fallbacks: true
only: []
ignore: []
order: []
sort: price
max_price: null
preferred_min_throughput: null
preferred_max_latency: null
session_affinity:
  required: true
  key: <stable workflow/session id>
```

Ordering principle:

```text
hard privacy/capability filters
  -> eligible providers
  -> reliability/availability
  -> cache/session continuity
  -> quality/latency/throughput/cost preference
```

A cheap endpoint that violates ZDR, parameter or modality requirements is not eligible.

## Presets/account policy

Use OpenRouter account/workspace guardrails as defense in depth. Do not make an external preset the sole policy authority while Hermes also sends request-level provider preferences. Qualify the effective merged behavior and record the actual provider policy used.

---

# Model fallback

Separate two cases:

1. **physical-provider fallback for the same model** — normally OpenRouter's job;
2. **fallback to a different model** — a Tier-3 routing decision or explicit bounded model fallback.

Do not let a generic fallback silently cross a quality, context, tool, modality, privacy or review boundary. If the fallback model is not eligible under the routing mission contract, fail instead of falling back.

---

# Direct-provider-capable abstraction

OpenRouter-first does not mean OpenRouter-locked.

Every gateway adapter should implement the same conceptual interface:

```text
execute(
  selected_model,
  provider_requirements,
  stable_session_key,
  request
) -> response + actual model/provider/cost/usage metadata
```

Potential future adapters:

- OpenRouter;
- direct DeepSeek;
- direct Z.ai;
- local MLX/OpenAI-compatible endpoint;
- another aggregator.

A direct adapter is promoted only if matched outcomes show enough improvement in accepted-mission economics, latency, cache behavior, reliability, privacy or capabilities to justify an extra credential/integration/maintenance surface.

---

# Gateway benchmark

Measure the gateway separately from mission-profile classification so provider behavior is not blamed on the semantic router.

For each eligible model/gateway policy capture:

- accepted-task/mission success;
- actual model/provider;
- fresh/cached input and output;
- TTFT/wall time/throughput;
- cache-hit/read share;
- parameter/tool correctness;
- provider/model fallback count;
- rate limits/outages;
- ZDR/data-policy compliance;
- physical-provider switch rate;
- cost per accepted task/mission.

Periodically compare OpenRouter against direct-provider/local challengers on frozen matched tasks. Default remains OpenRouter until evidence earns an exception.
