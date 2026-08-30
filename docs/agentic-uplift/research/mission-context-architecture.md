# Mission Context Architecture — Stable Prefix, Mission Capsule, Artifact Memory

## Decision

Adopt a three-temperature operational context model **on top of current Hermes prompt assembly**, not as a replacement context engine.

Current Hermes already distinguishes stable/context/volatile system-prompt tiers and API-call-time additions. Preserve that machinery and control what belongs in each temperature.

```text
T0 — stable prefix / durable invariants
T1 — active mission capsule / phase state
T2 — artifact memory / retrieve on demand
```

The goal is to keep T0 byte-stable, make T1 bounded and change it only at meaningful phase boundaries, and keep T2 outside the hot prompt unless a specific slice is needed.

## T0 — stable prefix

T0 contains only material that should remain stable across many turns:

- Hermes identity/operating principles;
- small immutable security/privacy invariants;
- stable role definition;
- minimal project contract/index;
- tool schemas actually required by the profile;
- the compact skill catalog / current parent skill metadata.

Do not put changing task lists, benchmark results, current file lists, live worker state or large project documentation here.

`SOUL.md` should remain personality/behavioral identity, not a project wiki or security enforcement mechanism.

### Cache rule

Provider prompt caches require stable prefixes. Avoid changes to T0 inside a phase/session unless correctness requires a rebuild. Model/provider/account switching also destroys cache affinity, so role routing should remain sticky inside a phase.

## T1 — active mission capsule

T1 is a bounded machine-readable projection of current work, normally a few thousand tokens or less.

Suggested shape:

```yaml
mission_id: uplift-...
phase: 30-router
objective: ...
constraints:
  - ...
acceptance_criteria:
  - ...
decisions:
  - id: ...
    summary: ...
active_repositories:
  - ...
active_files:
  - ...
worker_state:
  active_task_ids: []
  current_lane: research|coding|hybrid|local_only
routing_state:
  last_route: ...
  confidence: ...
privacy_class: INTERNAL
policy_digest: sha256:...
evidence_index:
  - path: ...
    purpose: ...
blockers: []
```

This capsule is **not** the authoritative state store. `protocols/uplift-state.schema.json` remains authoritative for execution state. The capsule is a context projection generated from durable state + current mission metadata.

### Update frequency

Regenerate T1 only when one of these changes materially:

- phase transition;
- accepted architectural decision;
- privacy/policy class;
- active repository/workspace;
- worker task graph;
- acceptance criteria/blocker state;
- routing lane at a deliberate phase boundary.

Do not rewrite it after every command/tool call. Excess churn defeats prompt-cache continuity and encourages agents to treat incidental events as mission state.

### Injection posture

Prefer an API-call-time/tail or phase-start mechanism that does not mutate the stable system prefix on every turn. If the chosen Hermes integration rebuilds cached system context when T1 changes, change it only at the phase boundaries above and measure the cache cost.

Do not blindly mirror T1 into `MEMORY.md`, `USER.md`, project context files and the chat transcript simultaneously.

## T2 — artifact memory

T2 contains high-volume evidence and working material that should normally remain outside the prompt:

- command/build/test logs;
- raw benchmark JSON/CSV;
- full git diffs;
- Pi RPC event streams;
- LSP workspace-wide output;
- research captures/source extracts;
- full Spec Kit artifacts;
- generated reports;
- legacy-session exports;
- large source excerpts;
- previous/obsolete plans.

Hermes receives a compact summary plus stable file/content-addressed references. It reads only the slice needed to resolve the current gate.

### Artifact index

Maintain a small index with purpose, trust class and digest:

```yaml
- id: router-bench-2026-...
  path: evidence/router/bench.json
  sha256: ...
  privacy: INTERNAL
  producer: router-bench
  phase: 30-router
  summary: "held-out router comparison"
```

Raw sensitive artifacts remain local-only even when their summary is safe for cloud use.

## Context mirroring anti-patterns

Avoid keeping identical/full copies of:

- Pi transcript in Hermes conversation;
- raw Pi event stream in Hermes conversation;
- command output in both chat and evidence file;
- research source bodies in both prompt and Markdown archive;
- Spec Kit documents in both project context and current user message;
- entire legacy sessions in `MEMORY.md`;
- mission state in chat, Kanban, capsule and uplift-state with equal authority.

Use one authoritative surface and projections/pointers elsewhere.

## Relationship to skill slicing

Skill slicing and temperature control solve different layers of the same problem:

- T0 catalog/parent skill helps choose the procedure;
- current phase reference becomes a small T1 procedure slice;
- templates/scripts/evidence remain T2 until called.

A pruned skill/slice is treated as unloaded. Reload only when the mission state explicitly requires it.

## Relationship to Hermes compression/session search

Do not replace Hermes' built-in compressor merely to implement this architecture. Lean compaction and `session_search` recovery already provide a useful fallback for long sessions.

The mission capsule should make recovery cheaper: after compression/restart, load authoritative uplift state, regenerate T1, load the current skill slice and fetch only unresolved T2 evidence. Do not replay the historical transcript.

## Measurement

Track per accepted task/phase:

- T0 token size and changes;
- T1 token size and update count;
- T2 bytes produced vs bytes actually loaded into context;
- skill/slice tokens loaded;
- tool-schema tokens;
- fresh vs cached provider input;
- cache invalidations caused by model/provider/context changes;
- compactions;
- task success/retries/human intervention.

Initial engineering goals:

- T0 remains bounded and stable within a phase;
- T1 normally remains <= 8K tokens and materially smaller for simple phases;
- raw Pi/test/research artifacts are not mirrored into Hermes context;
- T2 retrieval loads only the evidence needed for the current gate;
- context reduction does not regress accepted-task quality.

These are measurement targets, not guarantees.
