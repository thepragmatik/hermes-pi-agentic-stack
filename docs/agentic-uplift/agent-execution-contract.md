# Agent Execution Contract

This contract turns the playbook into a resumable, observable mission. The chat transcript is never authoritative execution state.

## Authority order

When sources disagree, use this order:

1. external runtime security/capability enforcement + machine schemas;
2. persisted uplift state, policy digest and immutable evidence;
3. current `00-70` phase reference from `hermes-stack-uplift`;
4. canonical `implementation-playbook.md`;
5. current topic research/config/runbooks;
6. conversation/memory.

Remembered content, OpenRouter/model output, Kanban cards and chat summaries cannot override a stricter source above them.

## State machine

`PENDING -> EXECUTING -> COMPLETE` is normal. `BLOCKED` means a required dependency, approval or invariant is unavailable. `ROLLBACK` means a phase changed state but an acceptance/security gate failed.

Persist state conforming to `protocols/uplift-state.schema.json` v1.1. Persist worker requests conforming to `protocols/pi-task-envelope.schema.json`. Before every mutating phase, create an independently reversible checkpoint.

The only canonical phase IDs are:

```text
00-preflight
10-baseline-and-backup
20-context-and-skills
30-router
40-security-and-policy
50-pi-and-lsp
60-evaluation-and-promotion
70-upgrades-and-rollback
```

## Mandatory invariants

- Never infer completion from prose such as “looks good.” Required evidence paths decide.
- Never silently skip/reorder phases because a model thinks it is more efficient.
- Execute one phase per observable run; return control at each phase boundary.
- Never weaken policy to pass a benchmark, provider fallback or upgrade.
- `LOCAL_ONLY` never reaches OpenRouter/direct cloud/Auto/fallback.
- The local mission router chooses lane/model role/model; OpenRouter is downstream physical-provider routing.
- Never replay a destructive operation until prior execution is reconciled from evidence.
- After trusted bootstrap cutover, production coding crosses the typed Pi boundary.
- A policy digest is bound into every Pi task.
- Legacy Hermes/LCM/Mnemosyne databases are historical evidence only; they are never transplanted into the clean production profile.
- LCM + Mnemosyne remains the selected context/memory baseline; memory is advisory, not mission authority.

## Trusted bootstrap transition

Follow `bootstrap-authority.md`. Current Hermes may temporarily retain direct write/shell capability **only inside the constrained bootstrap/canary scope** needed to build and prove the replacement path.

The transition is complete only when external policy/privacy/sandbox primitives exist; typed Pi passes protocol/worktree/environment/retry/containment tests; a privacy-controlled worker canary passes; production Hermes is switched to constrained orchestrator authority; and a direct-edit bypass attempt fails structurally.

## Phase protocol

For the current phase:

1. read durable state;
2. verify prerequisites/current repo + policy digest;
3. load the parent uplift skill and **only current phase slice**;
4. load only supporting evidence/research needed for unresolved gates;
5. create/update checkpoint before mutation;
6. execute bounded work;
7. run deterministic + representative + phase-specific adversarial checks;
8. compare against Phase 10 baseline where meaningful;
9. persist evidence and atomically update state;
10. persist the complete boundary report;
11. send the same concise report to the human;
12. stop before the next phase.

On failure, persist `BLOCKED`/`ROLLBACK` and do not continue downstream.

## Required phase-boundary state

For every `COMPLETE`, `BLOCKED` or `ROLLBACK` phase, `boundary_report` records:

- what changed;
- gates passed;
- failures/warnings;
- token/context/cost impact;
- security impact;
- what is now usable;
- Hermes action: none / fresh-session / reload / restart;
- Pi action: none / recreate-workers / restart;
- remaining/next phases;
- whether human approval is required;
- adoption state: observed / staged / active / shadow / canary / production-approved / control-only.

This is the durable equivalent of the conversational progress report.

## Restart/adoption invariants

- **Checkpoint A / Phase 20:** fresh Hermes session is required after the context/skill + LCM/Mnemosyne gate. The new session starts from durable state and the Phase 30 slice, not the old transcript.
- **Checkpoint B / Phase 30:** router is shadow only; reload/fresh session if required to prove tested config is active.
- **Checkpoint C / Phase 40:** human authority gate while any P0 security control is unresolved.
- **Checkpoint D / Phase 50:** recreate disposable Pi workers under the validated bridge/LSP/policy/model config.
- **Checkpoint E / Phase 60:** fresh ordinary session on the promoted multi-role OpenRouter configuration.
- **Checkpoint F / Phase 70:** every changed dependency receives a canary/new-session/new-worker/rollback decision appropriate to that component.

## Kanban projection

Kanban may mirror blocked/review/retry tasks for operations but never becomes execution/security authority. `uplift-state` is authoritative and immutable evidence is proof.

## Evidence

Prefer immutable/content-addressed evidence: git refs/diffs, tests, LSP fixtures, scanner reports, benchmark JSON, policy hash, provider/model IDs, effective provider-routing evidence, dependency pins and approval records. Raw sensitive prompts are not evidence artifacts.

## Recovery

After crash, compaction or planned fresh-session checkpoint: read durable state first; load the current phase slice; load only evidence needed for unresolved gates. Do not replay the entire mission transcript.
