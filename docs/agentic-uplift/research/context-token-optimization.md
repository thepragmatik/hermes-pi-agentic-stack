# Hermes/Pi Context, Prefill and Token Optimization

## First principle: separate costs

1. **Logical input tokens** — what the harness serializes/sends.
2. **Billable fresh input** — provider tokens that miss prompt cache.
3. **Billable cached input** — discounted but still visible tokens.
4. **Prefill/TTFT compute** — latency cost of uncached prefixes.
5. **Workflow/model/provider switch cost** — lost cache/context continuity, transfer/summarization, new tool schemas and behavior/retry risk.

A provider cache can reduce billable fresh input/TTFT while telemetry still shows large logical input. Context pruning reduces more dimensions. Routing should therefore preserve useful session/stage affinity when its measured benefit exceeds staying on a degraded model/provider.

## Current Hermes behavior worth preserving

A clean current install should be measured/tuned before replacing its context engine. Preserve bounded context discovery, security scanning, tool-output pruning, searchable history, model-specific compression and stable session-prefix behavior where supported.

## Prompt layout: optimize for cacheable prefix

```text
[stable provider/model system framing]
[stable behavioral invariants; security authority lives outside prompt]
[stable minimal tool definitions]
[stable compact project identity/invariants]
---------------- CACHE STABILITY BOUNDARY ----------------
[mission/routing stage contract]
[small retrieved spec/code/context slices]
[conversation/tool events]
[current tool result]
[user turn]
```

Keep volatile IDs/timestamps/telemetry out of the stable prefix where possible. The routing decision/durable state should carry traceability rather than rewriting the full model prompt every turn.

## SOUL / durable memory / project context

SOUL contains personality/universal working style, not security policy, permissions, provider routing or the operating manual. Durable memory stores stable accepted facts/preferences, not mission execution state. Project context is an index/invariants surface; large research/spec/code artifacts remain retrievable T2 material.

## Tool-schema minimization

- Hermes orchestrator sees only coordination/read/delegate/review capabilities needed for the current workflow stage.
- Pi sees only task-scoped code/LSP/test tools.
- Do not advertise every MCP/plugin/tool to every stage.
- Progressive disclosure/Tool Search should keep niche schemas cold.
- Required tools are a deterministic Tier-0 routing fact; semantic inference does not invent unavailable tools.
- Measure schema tokens and cold-tool lookup cost.

## Provider-side caching and routing

OpenRouter can benefit from upstream prompt caching, but provider/model switching can destroy locality. Treat `cache_affinity`/`session_affinity` as explicit routing optimization fields, not an unconditional rule.

For long stages/sessions:

- keep stable model/provider/session identity when the actual integration proves it and the route remains healthy/eligible;
- benchmark provider `price`, `throughput`, `latency` and explicit order/allowlist policies against accepted-mission outcomes;
- measure cached-token share and TTFT before crediting cache economics;
- record every model/provider/workflow switch and reason;
- permit reliability/failure escape only to another Tier-0/Tier-3 eligible route.

Raw OpenRouter `session_id`/sticky behavior or ZDR/provider controls are not assumed available through Hermes merely because OpenRouter supports them. Prove forwarding/account policy/audited adapter behavior first.

A nominally cheaper endpoint can be more expensive if it destroys a warm prefix or raises retry/tool-failure rate.

## Local model caching

MLX-LM remains a sensible Apple-Silicon local-serving challenger where local model/reviewer use earns its memory footprint. Validate prompt/KV cache, quantization and persistence against the exact deployed version.

Do not assume standard CUDA-vLLM runtime behavior on macOS; vLLM Semantic Router as a routing control-plane candidate is a separate evaluation from local vLLM inference serving.

## Context compaction policy

Use compaction as loss-managed archival:

- `must_preserve`: mission goal, acceptance, authoritative Tier-0 constraints, current routing stage, blockers;
- `active`: current plan/files/failures/tests;
- `retrievable`: older tool/research/evidence with pointers;
- `discardable`: duplicate acknowledgements/listings/verbose superseded output.

At compaction, refresh deterministic `must_preserve` state first, archive retrievable evidence, then verify mission + acceptance + security/eligibility + current stage survived. Free-form summary is not security/state authority.

## Pi context policy

A Pi worker is ephemeral per bounded coding/diagnostic/test stage by default. It receives:

- Pi task envelope v2.2 with `mission_id`, `stage_id`, workflow and routing-decision digest;
- small project invariants/index;
- relevant spec/context slices;
- isolated worktree;
- explicit tools/LSP/capabilities.

It does not inherit the full Hermes conversation or durable memory. Return compact typed diff/tests/diagnostics/assumptions/evidence.

## Spec artifacts: pointers over replay

Keep feature indexes and active acceptance criteria compact; retrieve only the stage-relevant spec/research sections. Completed rationale moves to durable ADR/change record rather than remaining hot prompt context.

## Routing-aware measurement protocol

For representative missions, persist redacted structured telemetry such as:

```json
{
  "mission_id_hash": "...",
  "task_families": ["debugging_diagnosis", "coding_implementation", "testing"],
  "workflow": "multi_stage",
  "stage_id": "implement-fix",
  "router": "rules",
  "model_role": "coding.default",
  "model": "...",
  "provider": "unknown-or-observed",
  "input_tokens": 12345,
  "cached_input_tokens": 10000,
  "output_tokens": 800,
  "ttft_ms": 450,
  "total_ms": 8300,
  "tool_schema_tokens_est": 1200,
  "context_file_tokens_est": 1600,
  "spec_tokens_est": 2200,
  "compaction_count": 1,
  "workflow_switches": 1,
  "model_switches": 0,
  "provider_switches": 0,
  "retries": 0,
  "accepted": true
}
```

Do not persist sensitive raw prompts merely to optimize routing/context. Training samples are separately sampled, redacted and governed.

## High-leverage experiments in order

1. Remove duplicated policy/procedural prompt content.
2. Split orchestrator/Pi/reviewer tool surfaces by workflow stage.
3. Use Spec Kit/T2 on-demand retrieval.
4. Stabilize cacheable prefixes and measure real session/model/provider affinity.
5. Tune LCM/compaction using accepted-mission quality.
6. Move verbose outputs to indexed artifacts.
7. In Phase 30, compare simple routing against semantic/advanced challengers while including switch/cache costs.

The production router does not need to be sophisticated to exploit these savings; the simplest router that preserves correct capabilities/workflows and most accepted-mission economics should win.