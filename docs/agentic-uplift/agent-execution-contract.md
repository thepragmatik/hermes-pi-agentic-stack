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

Remembered content, routing-model output, OpenRouter/model output, Kanban cards and chat summaries cannot override a stricter source above them.

## State machine

`PENDING -> EXECUTING -> COMPLETE` is normal. `BLOCKED` means a required dependency, approval or invariant is unavailable. `ROLLBACK` means a phase changed state but an acceptance/security gate failed.

Persist state conforming to `protocols/uplift-state.schema.json` v1.1. Persist worker requests conforming to `protocols/pi-task-envelope.schema.json`. Routing integrations consume/emit the framework-neutral `protocols/routing-mission.schema.json` and `protocols/routing-decision.schema.json`. Before every mutating phase, create an independently reversible checkpoint.

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
- Deterministic privacy, secret/PII policy, cloud eligibility, required capabilities/tools/modalities/context, network/sandbox permissions and policy-required approval/review cannot be overridden by learned routing.
- Research and coding are task families, not a closed routing ontology. Multi-stage missions are represented as ordered workflow stages rather than a generic `hybrid` label when stage transitions matter.
- Hermes and Pi depend on the routing mission/decision contracts, not directly on a router framework.
- Hermes owns bounded workflow/agent authority; a routing framework may recommend/score but cannot grant arbitrary tools, coding authority or merge authority.
- The local stack selects workflow + model role/model among eligible candidates; OpenRouter is normally downstream physical-provider routing.
- OpenRouter Auto never becomes privacy/capability/final workflow authority.
- A hard gateway requirement such as ZDR/parameter support/session affinity must be enforced by the current gateway/account/adapter or the route fails closed; unsupported client fields are not silently ignored.
- Never replay a destructive operation until prior execution is reconciled from evidence.
- After trusted bootstrap cutover, production coding crosses the typed Pi boundary.
- A policy digest is bound into every Pi task; a production Pi task must also be attributable to the routing mission/stage/decision that selected it.
- Legacy Hermes/LCM/Mnemosyne databases are historical evidence only; they are never transplanted into the clean production profile.
- LCM + Mnemosyne remains the selected context/memory baseline; memory is advisory, not mission authority.
- Routing outcome telemetry minimizes sensitive raw prompt retention and never becomes project truth.

## Routing data contract

### Input

`routing-mission` carries three classes of routing objective:

1. **primary** — inferred task families/domain/phase/complexity/reasoning/tool intensity;
2. **secondary** — deterministic requirements and hard constraints such as privacy, capability, context, modality, risk, network/sandbox and ZDR;
3. **tertiary** — quality floor, latency/cost preference, provider reliability, cache/session affinity and switch budget.

Every security/capability-sensitive field should preserve derivation provenance. When an inferred value conflicts with deterministic/current state, deterministic state wins and the disagreement becomes evidence.

### Output

`routing-decision` records:

- eligible workflows/model roles/models;
- selected bounded workflow and ordered stages;
- stage agent/model role;
- selected model when known;
- gateway;
- abstract provider requirements;
- confidence/abstention;
- engine/version/maturity;
- concise reasons.

The routing engine is replaceable. Switching from rules/Aurelio to vLLM Semantic Router or a later ModernBERT artifact must not require changing Pi task semantics or OpenRouter policy semantics.

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

- **Dogfood A0 / inside Phase 20:** test prompt/skill slimming in a fresh continuation before layering LCM/Mnemosyne and Spec Kit changes.
- **Checkpoint A / Phase 20:** fresh Hermes session is required after the complete context/skill + LCM/Mnemosyne gate. The new session starts from durable state and the Phase 30 slice, not the old transcript.
- **Checkpoint B / Phase 30:** routing is shadow only; rules/state are the initial baseline and all semantic/framework/model candidates remain observational until later promotion.
- **Checkpoint C / Phase 40:** human authority gate while any P0 security control is unresolved.
- **Checkpoint D / Phase 50:** recreate disposable Pi workers under the validated bridge/LSP/policy/routing/model config.
- **Checkpoint E / Phase 60:** fresh ordinary session on the promoted workflow/router/model/provider configuration.
- **Checkpoint F / Phase 70:** every changed dependency receives a canary/new-session/new-worker/rollback decision appropriate to that component.

## Router research/training plane

Heavy experimentation such as LLMRouter, RouteLLM training/evaluation, OpenRouter Auto teacher comparisons, vLLM Semantic Router replay/simulation and ModernBERT fitting belongs outside the request hot path unless measured evidence promotes a bounded artifact/runtime.

Production routing must remain local-before-cloud, bounded in memory/latency, auditable, safe to abstain, independently replaceable and easy to roll back.

## Kanban projection

Kanban may mirror blocked/review/retry tasks for operations but never becomes execution/security authority. `uplift-state` is authoritative and immutable evidence is proof.

## Evidence

Prefer immutable/content-addressed evidence: git refs/diffs, tests, LSP fixtures, scanner reports, benchmark JSON, routing-contract versions/digests, routing engine/version, policy hash, model IDs, actual provider when observable, effective provider-routing evidence, dependency pins and approval records. Raw sensitive prompts are not evidence artifacts.

Outcome evidence may include accepted/rejected result, cost, tokens/cached tokens, TTFT/wall time, tool calls, retries/fallbacks, switches and human override, but default telemetry should keep only redacted feature summaries/hashes rather than reusable sensitive prompt text.

## Recovery

After crash, compaction or planned fresh-session checkpoint: read durable state first; load the current phase slice; load only evidence needed for unresolved gates. Do not replay the entire mission transcript.
