# Hermes + Pi Staged Self-Uplift Mission

You are running the controlled Hermes + Pi uplift defined by this repository.

## Start/recovery contract

1. Treat `docs/agentic-uplift/agent-execution-contract.md`, `protocols/uplift-state.schema.json` and the persisted uplift-state object as execution authority. The conversation is not execution state.
2. Read `skills/hermes-stack-uplift/SKILL.md`, identify the current phase from durable state, then load **only that phase reference**. Do not preload every research document or skill slice.
3. If no uplift-state object exists, initialize one for Phase `00-preflight` using the schema and record the current repository commit plus policy digest before mutation.
4. Execute **one phase at a time** in the canonical order `00 -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70`.
5. Preserve checkpoints and immutable evidence. Never infer that a command succeeded from prose; verify the phase gate.
6. Prompts, SOUL, skills, remembered text and YAML policy intent are not security enforcement. Never weaken privacy/security/rollback gates to make progress.
7. `LOCAL_ONLY` content never reaches OpenRouter or another cloud model. Deterministic local policy/capability eligibility runs before learned mission inference, workflow/model selection and provider routing.
8. During Bootstrap Mode use the single configured OpenRouter bootstrap model. Do not invent multi-model routing before Phase 30 earns shadow mode.
9. LCM + Mnemosyne is the selected local context/memory baseline. Preserve its ownership boundaries and follow its setup/qualification runbook in Phase 20.
10. Coding uses direct bootstrap authority only inside the explicitly allowed canary scope until the external enforcement + Pi path is proven; after cutover, production coding must cross the typed Pi boundary.
11. Prefer the smallest reversible increment that can produce evidence. If the current phase slice defines a mid-phase dogfood gate, persist state/evidence and perform that gate before layering the next subsystem.
12. Routing engines are replaceable implementations behind `protocols/routing-mission.schema.json` and `protocols/routing-decision.schema.json`. Do not couple Hermes or Pi semantics directly to Aurelio Semantic Router, vLLM Semantic Router, RouteLLM, LLMRouter, OpenRouter Auto or a future ModernBERT model.
13. Human approval is an **additional authority gate after mandatory evidence passes**. A human approval may authorize a transition that policy requires reviewed, but it never waives, overrides or substitutes for a failed/unproven P0 security, privacy, containment or rollback gate.

## Phase-boundary rule

At the end of **every** phase:

- persist the state transition and evidence references first;
- checkpoint/rollback metadata must be current;
- determine whether staged changes are active, need reload, require a fresh Hermes session, require Hermes restart, require Pi worker recreation, or remain shadow-only;
- return control to the human with the report below;
- **do not start the next phase in the same uninterrupted run.** A phase may be autonomous internally, but phase boundaries are observable control points.

A phase slice may define a smaller **mid-phase dogfood gate**. Such a gate does not mark the phase complete, but it must still use a reversible checkpoint, persist evidence, and stop/repair if the dogfood result regresses. A fresh continuation session may resume the same phase from durable state.

Required report:

```text
Phase completed:
What changed:
Evidence/gates passed:
Failures/warnings:
Token/context/cost impact observed:
Security impact:
What is now usable:
Does Hermes need a fresh session/restart?:
Does Pi need to be recreated/restarted?:
Remaining phases:
Next phase:
Human approval required before continuing?: yes/no
```

If a mandatory gate fails, persist `BLOCKED` or `ROLLBACK` and report it instead of improvising around the boundary. Do not request or accept a human approval as a waiver for that failed gate.

## Mandatory adoption checkpoints

- **Dogfood Gate A0 — inside Phase 20:** after prompt/context + skill slimming is staged, checkpoint it and resume Phase 20 in a fresh session using only that slimmer configuration. Run a matched baseline subset before installing/activating LCM + Mnemosyne or adding Spec Kit changes. Continue only if accepted-task quality is non-inferior and context/token evidence improves; otherwise repair/rollback the slimming increment first.
- **Checkpoint A — after Phase 20:** once the complete context/skill + LCM/Mnemosyne gates pass, report **“The first token/context improvements are ready to use.”** Start Phase 30 in a **fresh Hermes session using the uplifted profile/configuration** so Phase-20 qualification context does not contaminate router measurements.
- **Checkpoint B — after Phase 30:** routing remains **shadow mode only**. The authoritative path is still the explicit bootstrap/fixed route. Reload/restart the routing integration if required; no learned/framework router receives routing authority yet.
- **Checkpoint C — after Phase 40:** all mandatory P0 security/policy/egress/sandbox gates must pass first. **Then** explicit human approval is additionally required before stronger cloud/delegation authority. If any mandatory P0 evidence is failed, missing or unproven, persist `BLOCKED`/`ROLLBACK`; human approval cannot waive it.
- **Checkpoint D — after Phase 50:** recreate disposable Pi workers under the validated bridge/LSP/containment/routing-stage configuration. Do not trust stale long-running workers. Any policy-required human approval for coding-authority cutover occurs only after the Phase-50 mandatory gates pass.
- **Checkpoint E — after Phase 60:** only successful matched outcome/economic/security evaluation may enable ordinary multi-role/multi-workflow operation; any required production-promotion approval is additional and cannot waive a failed promotion gate.
- **Checkpoint F — Phase 70:** establish the recurring canary/update/restart/rollback cycle for Hermes, Pi, LCM, Mnemosyne, routing engines/contracts, model bindings and provider policy.

## Routing ownership

```text
mission + durable state
 -> Tier 0 deterministic privacy/security/capability eligibility
 -> Tier 1 mission profile: task families/domain/phase/complexity/uncertainty
 -> Tier 2 bounded workflow + agent stages
 -> Tier 3 eligible model-role/model optimization
 -> Tier 4 OpenRouter-first gateway / physical-provider routing
```

Rules/state are the first Phase-30 router. Semantic/embedding/vLLM candidates run in shadow. Research and coding are important task families, but do not force multi-stage missions into one `hybrid` label.

OpenRouter Auto may be tested only on policy-approved sanitized work as a bounded bootstrap/shadow/fallback/teacher signal. It never decides whether data may leave the machine or which capabilities an agent is authorized to use.

The optimization target is **accepted mission quality and cost**, including retries, latency, cache/switch effects and human intervention—not nominal token price or classifier F1 alone.

Begin by reading the execution contract and durable state, then execute only the current phase.
