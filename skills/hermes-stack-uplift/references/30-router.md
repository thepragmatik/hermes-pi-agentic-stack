# Phase 30 — Routing Contracts + Small Router + Shadow Bake-off

Start in the **fresh optimized Hermes session required by Checkpoint A**.

The objective is not to build a sophisticated router immediately. Establish one replaceable routing seam, a tiny safe baseline, then shadow challengers.

## Stable seam

Use:

- `protocols/routing-mission.schema.json` for mission profile + deterministic requirements/session/optimization;
- `protocols/routing-decision.schema.json` for eligible paths + bounded workflow stages + model/gateway/provider requirements.

Router frameworks consume/emit these contracts. Hermes/Pi semantics must not depend on a framework-specific label/API.

## Routing order

```text
Tier 0 deterministic eligibility/security
 -> Tier 1 multi-label mission-profile inference
 -> Tier 2 bounded workflow/agent selection
 -> Tier 3 model-role/model economic optimization
 -> Tier 4 OpenRouter-first gateway/provider execution
```

Tier 0 owns `LOCAL_ONLY`, secret/PII/cloud policy, available/required tools, modality, context, Pi requirement, network/sandbox, ZDR/retention and required approval/review. A learned classifier cannot override these facts.

Tier 1 may infer task families such as research, synthesis, design, planning, implementation, diagnosis, refactor, test, review, security review, DevOps, data analysis, documents, retrieval, orchestration, long-running tools, multimodal and fact verification. Missions are multi-label and may transition stages; do not force `research -> design -> implementation -> test -> review` into `hybrid`.

## First router

Implement first:

```text
deterministic eligibility
 + deterministic agent/workflow state
 + simple multi-label capability rules
 + abstain
```

It should run locally with no heavy ML/runtime dependency.

## Shadow candidates

Use `research/local-routing-models.md`, `router-training-control.md` and `openrouter-routing.md`.

Compare where technically feasible:

A. rules/state;
B. minimal local embedding prototype;
C. Aurelio Semantic Router;
D. vLLM Semantic Router;
E. ModernBERT only after its data gate;
F. relevant LLMRouter algorithms in the research plane;
G. RouteLLM-style Tier-3 quality/difficulty scoring;
H. OpenRouter Auto on policy-approved sanitized missions only.

Current research hypothesis: vLLM Semantic Router is the strongest medium-term adoption candidate because its signal/projection/decision architecture and session-aware switching align with Tier 1/3. It remains shadow until evidence earns its heavier runtime. Prefer config/adapters/upstream contributions; do not fork merely for convenience.

Aurelio is the lighter semantic challenger. LLMRouter stays in the research/training plane. RouteLLM scores strong-vs-economical choices after eligibility/workflow. Auto is a weak teacher/comparator, never privacy or workflow authority.

## Roles and OpenRouter

Roles are reusable capability/economic pools such as general, reasoning, research, coding, review, multimodal, local and optional cheap auxiliary—not one role per task-family label.

Keep volatile model IDs in config/runtime evidence and re-verify current capability/availability before binding.

OpenRouter is Tier 4 and normally chooses the physical provider. Current Hermes exposes only a subset of raw OpenRouter provider policy; required ZDR/session-affinity/performance semantics must be enforced by the actual client/account/adapter or fail closed.

Measure provider/model stickiness and cached tokens. Do not assume current Hermes forwards OpenRouter `session_id` until tested.

## Shadow evidence

The existing explicit bootstrap/fixed path remains authoritative.

Default telemetry contains redacted feature summaries/hashes, not raw sensitive prompts. Record contract/engine version, profile/workflow/model/provider decision, actual model/provider when observable, fresh/cached tokens, TTFT/wall time, router latency/RSS, tool calls, retries/fallbacks/switches, tests/review, human override, accepted/rejected outcome, failure reason and cost.

Measure:

- zero hard-eligibility violations;
- multi-label task-family/profile metrics;
- uncertainty/abstention behavior;
- workflow/stage correctness where labels are meaningful;
- accepted-task/mission regret;
- cost per accepted mission;
- tool/capability failures;
- retries/human overrides;
- route/model/provider switch rate;
- cache continuity;
- TTFT/wall time;
- local p50/p95/p99 latency + RSS;
- operational/dependency complexity.

## ModernBERT

Do not train a `research|coding|hybrid` classifier. A future ModernBERT may use calibrated multi-label/multi-head outputs for task families/domain/phase/complexity/reasoning/tool/context-need/uncertainty only after representative redacted/deduplicated real Hermes missions, multi-stage outcomes, clean mission/repo/session/time holdouts and learning curves show simpler candidates have plateaued on routing regret/accepted-mission economics.

## Restart/Canary Checkpoint B

A passing Phase 30 remains **shadow only**. Reload/restart the routing integration if required and prefer a fresh shadow session so the tested contracts/engine/config are demonstrably active. Do not grant routing authority yet.

Persist state/evidence, send the required phase-boundary report, and stop before Phase 40.
