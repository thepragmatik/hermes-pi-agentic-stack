# Hermes/Pi Context, Prefill and Token Optimization

## First principle: separate four different costs

1. **Logical input tokens** — what the harness serializes/sends.
2. **Billable fresh input** — provider tokens that miss prompt cache.
3. **Billable cached input** — often strongly discounted but still reported as tokens.
4. **Prefill/TTFT compute** — latency cost of processing uncached prefixes.

A provider cache can dramatically reduce #2 and #4 while your telemetry still shows a large #1. Spec/context pruning reduces all four. This distinction is essential when evaluating whether an optimization worked.

## Current Hermes behavior that should be preserved

Recent Hermes documentation/source indicates several good modern choices:

- USER/MEMORY-style persistent context can be frozen at session start so the system prefix remains stable.
- Context-file discovery is bounded and security-scanned.
- The context engine can prune old tool output before expensive summarization.
- Lean compaction keeps a small tail and searchable historical material rather than replaying everything.
- Compression thresholds can be model-specific.
- In-place compaction allows old material to remain discoverable through session search rather than injected on every turn.

A clean current install should therefore be tuned before replacing its context engine.

## Prompt layout: optimize for cacheable prefix

Use this conceptual order for model calls:

```text
[stable provider/model system framing]
[stable security/behavioral policy]
[stable minimal tool definitions]
[stable compact project identity/invariants]
[session-start durable-memory snapshot]
---------------- CACHE STABILITY BOUNDARY ----------------
[mission/task contract]
[small retrieved spec/code/context slices]
[conversation/tool events]
[current tool result]
[user turn]
```

Do not put timestamps, random nonces, mutable counters, dynamic directory listings or telemetry before stable material. If a request identifier is needed for tracing, put it in metadata/headers where possible or after the reusable prefix.

## SOUL.md / USER.md / project context design

### SOUL.md

Keep personality and universal working style only. **Do not put security policy, role permissions, provider routing logic or procedural manuals here.** Security needs code enforcement; procedural knowledge belongs in skills/explicit task artifacts.

Target: small enough that humans can audit the entire file quickly. Remove duplicated mission rules already represented in tools/policy.

### USER.md / durable memory

Persist stable preferences/facts only. Avoid accumulating temporary mission state or imperative instructions. Session-specific requirements belong in the mission contract/spec.

### Project context (`HERMES.md`, `.hermes.md`, AGENTS.md etc.)

Keep an index and invariants, not a repository encyclopedia. Example:

```markdown
# Project context
- Architecture map: docs/architecture/index.md
- Build/test commands: docs/dev/commands.md
- Security constraints: policy/security.yaml (enforced by launcher)
- Coding conventions: docs/dev/style.md
- Current feature specs: specs/ (retrieve only active feature)
- Never assume generated files are authoritative; regenerate from source.
```

Retrieval should materialize the relevant referenced sections only when a task needs them.

## Tool-schema minimization

Agentic harnesses often pay more for tool definitions than expected because the same schemas are repeated in every model request.

- In orchestrator mode expose only coordination/read/delegate tools.
- In Pi coding mode expose only task-scoped code/LSP/test tools.
- Do not advertise every MCP server to every turn.
- Lazy-register niche tools after a classifier or explicit user intent requests them.
- Prefer compact typed schemas and stable descriptions.
- Measure prompt-size before/after each toolset change.

This also improves zero-trust behavior: fewer tools means fewer accidental capabilities.

## Provider-side caching strategy

### DeepSeek V4 Flash

DeepSeek documents automatic disk/context caching for repeated prefixes. Exact overlapping prefixes are the key. Therefore:

- pin model + provider for a session;
- keep stable prefix exact;
- append new turns rather than rewriting earlier blocks;
- avoid reserializing semantically identical JSON/tool schemas with different key/order/whitespace if the API cache is byte/token-prefix sensitive;
- measure cached-token counters rather than assuming hits.

Native DeepSeek uses peak/off-peak pricing and very cheap cached input relative to fresh input. This creates a strong incentive to stabilize prefixes even if OpenRouter is used for other reasons.

### GLM-5.3-Flash / Z.ai

Current Z.ai pricing infrastructure supports cached-input billing in its model families; 5.3-Flash launch pricing is especially aggressive. Treat launch discounts as temporary. The architecture should remain viable at list price.

### OpenRouter

OpenRouter can automatically benefit from upstream prompt caching and exposes cached-token accounting, but provider routing can hurt cache locality. For long agent loops:

- pin or strongly prefer a provider after the first successful request;
- disable/avoid routing modes that freely switch providers if cache reuse matters more than tiny per-request price differences;
- benchmark `price`, `throughput`, `latency` routing and explicit provider order separately;
- include cache-hit ratio and p95 TTFT in the provider score, not just $/M token.

A nominally cheaper endpoint can be more expensive/slower if it destroys a 90% cache-hit prefix.

## Local model prompt/KV caching

### MLX-LM

Use MLX-LM as the first local serving experiment on Apple Silicon. Relevant capabilities include saved/loaded prompt caches, server prefix-cache behavior, rotating/bounded KV caches, KV quantization and speculative decoding. For a local reviewer that repeatedly sees the same policy/repository prefix, persisted prompt caches can make a material difference.

### vLLM-Metal

Apple Silicon support is provided through the vLLM-Metal path rather than assuming the standard CUDA vLLM stack. Validate each feature needed (prefix cache, quantization, offload/tiering) against the exact deployed release. Do not copy Linux GPU flags blindly into a macOS runbook.

## Context compaction policy

Use compaction as a *loss-managed archival process*, not just summarization.

Recommended state classes:

- `must_preserve`: mission goal, non-negotiable constraints, acceptance criteria, security/privacy class, unresolved blockers;
- `active`: current implementation plan, open files, current failures, latest test results;
- `retrievable`: earlier tool outputs, research evidence, superseded attempts, detailed logs;
- `discardable`: duplicated acknowledgements, old directory listings, redundant test successes, verbose command output.

At compaction:

1. deterministically extract/refresh the `must_preserve` state object;
2. prune discardable and superseded tool output;
3. summarize active state with source pointers;
4. archive retrievable material in session history/artifacts;
5. verify the new context still contains mission + acceptance + security class.

Add a post-compaction invariant test. Do not trust a free-form summary to remember security constraints.

## Pi context policy

A Pi worker should be **ephemeral per coding task** by default. It receives:

- a typed task envelope;
- a small project invariant/index file;
- relevant spec slices;
- a worktree path;
- explicit tool/LSP capabilities.

It should *not* inherit the full Hermes conversation or durable memory. Return a structured handoff containing patch/diff, tests, diagnostics, assumptions and unresolved items. This prevents parent-context bloat and child mission drift.

## Spec artifacts: pointers over replay

Spec Kit generates useful durable Markdown. The expensive pattern is replaying every artifact on every loop. Treat specs like a queryable local knowledge base:

- active feature index: <= ~1–2k tokens;
- retrieve headings/sections by task ID;
- cache stable spec digest and acceptance criteria in the session prefix;
- keep research/data-model/contracts on disk and load on demand;
- when a task is complete, compact its detailed rationale into an ADR/change record, not the active prompt.

## Measurement protocol

For every representative mission, log:

```json
{
  "mission_class": "coding",
  "model": "...",
  "provider": "...",
  "request": 12,
  "input_tokens": 12345,
  "cached_input_tokens": 10000,
  "output_tokens": 800,
  "ttft_ms": 450,
  "total_ms": 8300,
  "tool_schema_tokens_est": 1200,
  "context_file_tokens_est": 1600,
  "spec_tokens_est": 2200,
  "compaction_count": 1,
  "accepted": true
}
```

Redact before persistence. Never store raw PII merely to optimize tokens.

## High-leverage experiments in order

1. Remove duplicated policy/procedural prompt content.
2. Split orchestrator/coder toolsets.
3. Introduce Spec Kit mission profiles and on-demand artifact retrieval.
4. Stabilize provider/model/system prefix and pin provider per session.
5. Tune Hermes compression thresholds and lean mode using accepted-task quality.
6. Move verbose tool outputs to artifacts with short indexed summaries.
7. Only then evaluate alternate context engines or local long-context models.

The first four are lower-risk and often deliver most of the savings.
