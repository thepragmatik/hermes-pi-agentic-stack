# Agent Execution Contract

This contract turns the playbook into a resumable mission. The chat transcript is never authoritative execution state.

## State machine

`PENDING -> EXECUTING -> COMPLETE` is the normal path. `BLOCKED` means a required dependency, approval or invariant is unavailable. `ROLLBACK` means the phase changed state but an acceptance/security gate failed. A phase may leave `BLOCKED` only after the blocker is recorded as resolved; retries increment `attempt` and preserve the same logical task id with a new idempotency key.

Persist state conforming to `protocols/uplift-state.schema.json`. Persist worker requests conforming to `protocols/pi-task-envelope.schema.json`. Before every mutating phase, create a checkpoint that is independently reversible.

## Mandatory invariants

- Never infer completion from prose such as “looks good.” Completion requires required evidence paths.
- Never silently skip a phase because a newer model considers it unnecessary.
- Never weaken policy to pass a benchmark or upgrade.
- Never replay a destructive task with the same uncertainty about whether it already executed; reconcile evidence first.
- The orchestrator does not become the coder as an optimization. Coding crosses the typed Pi boundary.
- A policy digest is bound into each Pi task so a worker cannot unknowingly run under stale rules.

## Phase protocol

For each phase: load only its skill slice; verify prerequisite phase states; snapshot/pin versions; create checkpoint; produce a typed task graph; execute bounded tasks; collect evidence; run the phase-specific adversarial checks; update durable state atomically; and emit a concise human-readable result. On failure, mark `BLOCKED` or `ROLLBACK` with reason and do not continue downstream.

## Evidence object

Evidence should reference immutable or content-addressed artifacts where practical: git commit/diff, test output, LSP diagnostics, scanner reports, benchmark JSON, policy hash, provider/model pins, and approval records. Raw prompts containing sensitive data are not evidence artifacts.

## Recovery

After process crash or context compaction, read durable uplift state first, then the current phase slice, then only evidence relevant to unresolved gates. Do not reload the entire historical mission transcript.
