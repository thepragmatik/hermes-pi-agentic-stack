# Hermes + Pi Agentic Stack — Compact Control Playbook

Snapshot: 2026-08-30.

This is the compact architecture/control document. Detailed execution lives in `docs/agentic-uplift/implementation-playbook.md`; Hermes should load only the current phase slice rather than ingesting the full research corpus.

## Mission

Build an upgrade-safe Apple-Silicon development stack where:

- Hermes is the mission/control plane;
- LCM + Mnemosyne is the fixed local context/memory baseline;
- deterministic local policy decides whether data may leave the machine;
- a small local mission router chooses research/coding/hybrid/review/auxiliary/abstain and the model role;
- **OpenRouter is the default external inference gateway** and chooses the physical provider subject to policy;
- coding crosses a typed Hermes -> Pi boundary into disposable externally-contained workers;
- LSP/tests/scanners/review provide evidence before merge;
- context, skills, specs and evidence use progressive disclosure;
- every uplift phase is observable, restartable and reversible.

## One routing architecture

```text
MISSION
  |
  v
Tier 0 deterministic local privacy/security/policy
  |-- LOCAL_ONLY --> local path / BLOCKED
  v
Tier 1 local mission router
  |  rules/state -> embeddings -> ModernBERT only if earned
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

Ownership is non-negotiable:

- local deterministic policy owns privacy/security routing;
- our local router owns mission classification;
- role config owns model selection;
- OpenRouter owns downstream physical-provider selection within constraints;
- OpenRouter Auto is bootstrap/shadow/fallback only, never privacy or final mission routing.

Direct Z.ai/DeepSeek access is a benchmarked exception, not default architecture. Additional provider credentials are justified only by material improvement in cost/minutes per accepted task, latency, caching, reliability, privacy or rate limits.

See `docs/agentic-uplift/research/openrouter-routing.md` and `configs/models.example.yaml`.

## Bootstrap Mode

Do not require the optimized router before Hermes can build it.

Fresh install:

```text
clean narrow Hermes profile
 -> OpenRouter
 -> one GLM-5.3-Flash-class bootstrap model
 -> Phases 00/10/20
 -> build router in Phase 30 shadow mode
 -> only later multi-role routing
```

The current model ID must be selected/verified with the installed Hermes `model` picker. Research snapshot only: `z-ai/glm-5.3-flash`.

The human bootstrap procedure is `docs/agentic-uplift/fresh-install-bootstrap.md`. The takeover action is:

```bash
uplift chat --query-file UPLIFT_MISSION.md
```

`UPLIFT_MISSION.md` requires one observable phase per run and phase-boundary reporting.

## Single 00–70 lifecycle

There is exactly one phase system:

| Phase | Objective | Adoption boundary |
|---|---|---|
| 00 | preflight/version/repo/provider/isolation truth | manual foundation verified |
| 10 | measurable baseline + backup + optional read-only legacy salvage | rollback evidence durable |
| 20 | context/skill diet + Spec Kit slicing + LCM/Mnemosyne | **A: first improvements usable; fresh session** |
| 30 | local router + OpenRouter roles | **B: shadow only** |
| 40 | external security/privacy/capability enforcement | **C: human authority gate** |
| 50 | typed Pi bridge + containment + LSP | **D: recreate disposable workers** |
| 60 | system evaluation + multi-role promotion | **E: ordinary role routing** |
| 70 | recurring upgrades/restart/rollback | **F: maintenance cycle** |

The old multi-dozen-phase execution ordering is superseded. Research topics remain supporting material, not extra phases.

## Phase-boundary contract

Every phase persists evidence + uplift-state first, then reports:

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

Do not start the next phase in the same uninterrupted run.

`protocols/uplift-state.schema.json` v1.1 persists the same report, adoption state, runtime gateway/router mode and restart/recreate decisions.

## First self-benefit boundary

Phase 20 is the first major payoff.

It must slim/deduplicate hot context, use a narrow skill catalogue, preserve stable prompt ordering, bound T1 mission context, keep T2 artifacts external, reduce tool-schema exposure, slice Spec Kit material, instrument prompt/cache size, and qualify the fixed LCM+Mnemosyne baseline.

When it passes Hermes says:

> **The first token/context improvements are ready to use.**

Then the pre-optimization session is closed. Phase 30 starts fresh on the uplifted profile. This prevents the uplift itself from carrying the very context decay it is trying to remove.

## Context architecture

```text
T0 = stable prefix / small invariants + skill/tool catalogue
T1 = bounded current mission/phase capsule
T2 = logs/diffs/research/specs/benchmarks/Pi RPC retrieved only on demand
```

Do not mirror the same state/output into conversation, memory, project context and artifacts.

## Skill architecture

```text
small eligible catalogue
 -> short class-level SKILL.md
 -> one current phase reference
 -> specific script/template/research only when required
```

More micro-skills are not automatically better. Measure catalogue/parent/support tokens, unnecessary loads, post-compaction reloads, skill-selection errors, accepted-task quality and cached tokens. A pruned reference is unloaded until re-read.

## LCM + Mnemosyne baseline

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = large/raw evidence
Git/ADR/spec = project truth
Kanban       = optional operational projection
```

Initial research pins (re-verify before use): LCM stable v0.20.0, Mnemosyne core 3.15.1, Hermes wrapper 0.5.0.

Baseline posture:

- LCM owns compaction/recovery; overlapping semantic/proactive/temporal memory families off;
- Mnemosyne local FastEmbed/ONNX embeddings, strict curated writes, no transcript autosave, no remote/host LLM, no automatic persona/richer recall/sleep, narrow tool allowlist;
- built-in MEMORY/USER durable stores disabled to avoid duplicate authority;
- Tool Search enabled to progressively disclose non-core tools;
- after provisioning, context/memory must still work with outbound network denied.

If mandatory LCM/Mnemosyne gates fail, Phase 20 is `BLOCKED`/`ROLLBACK`; the agent does not redesign memory on its own.

See `docs/agentic-uplift/local-context-memory-setup.md`.

## Legacy state

Never transplant old `state.db`/LCM/Mnemosyne databases. If useful historical knowledge is genuinely missing from current repos/ADRs, use the read-only curation pipeline: immutable original -> disposable copy -> local discovery -> minimal export -> independent secret/PII sanitization -> provenance-bearing candidates -> adversarial current-truth reconciliation -> admit only durable accepted knowledge to its proper surface.

See `research/legacy-state-curation.md`.

## Router / ModernBERT

Progression:

```text
rules + explicit state
 -> frozen embedding classifier
 -> representative redacted real outcomes
 -> fine-tuned ModernBERT only if justified
```

ModernBERT classifies mission type; an optional RouteLLM-style model is a later difficulty/preference layer. Fine-tuning requires stable ontology, mission-level deduplicated/temporal holdout, ambiguous/hybrid examples and paired accepted-task outcomes.

Route phases, not micro-turns; use hysteresis and measure route-switch/provider-cache continuity.

## OpenRouter role intent

Snapshot candidates only:

```text
bootstrap.default -> GLM-5.3-Flash-class via OpenRouter
coding.default    -> GLM-5.3-Flash-class via OpenRouter
research.default  -> DeepSeek-V4-Flash-class via OpenRouter
review.default    -> independent family after benchmark
auxiliary.cheap   -> optional after benchmark
```

Runtime IDs/prices belong in config/locks/evidence, not policy prose. Current Hermes provider-routing config supports sort/only/ignore/order/required-parameters/data-collection controls; do not invent raw OpenRouter fields as Hermes YAML keys. Account/workspace privacy guardrails are additional defense.

Avoid per-request provider churn when it destroys prompt-cache affinity. Optimize cost/minutes/retries/human intervention **per accepted task**.

## Security/root of trust

A profile, SOUL file, memory, skill, YAML or provider guardrail is not structural authorization.

Before stronger authority, implement external:

- role/capability policy;
- filesystem/path/symlink scope;
- process/command policy;
- environment/credential minimization;
- network/egress default deny;
- deterministic secret + typed/context-aware PII scanning;
- re-scan after transformation;
- policy digest/idempotency/evidence journal;
- sandbox/containment launcher;
- independent review/merge authority.

Privacy is decided locally before OpenRouter, including Auto/fallback/retry. Human authority gate remains at Phase 40 while any P0 enforcement is unresolved.

## Pi invariant

Pi has no assumed built-in permission boundary. Coding tasks use validated v2 envelope + policy digest, ephemeral worktree, minimal env/credentials, external containment, local pipe RPC, bounded retries/idempotency, deterministic tests/LSP/security evidence and independent merge/review.

Treat `agent_settled` as fully-settled completion; never equate `agent_end` with final completion without current protocol evidence.

After a passing canary, ordinary Hermes direct source-write/arbitrary-shell authority is revoked and a “skip Pi and edit directly” attempt must fail structurally.

## Spec Kit and task graph

Use Micro/Patch, Lite, Standard and High-Assurance profiles. Policy can escalate; model cannot downgrade. Generated specs are T2 source; load only current slices.

Use bounded typed tasks, not uncontrolled swarms. Kanban can be a durable operational UI but never overrides uplift-state/evidence.

## Maturity labels

Use only:

`researched -> designed -> prototype -> smoke-tested -> target-Mac-validated -> shadow -> canary -> production-approved`

Never imply implementation/enforcement because a diagram/config/schema exists.

## Canonical start order

1. `README.md`
2. `docs/agentic-uplift/fresh-install-bootstrap.md`
3. `UPLIFT_MISSION.md`
4. `docs/agentic-uplift/agent-execution-contract.md`
5. `docs/agentic-uplift/implementation-playbook.md`
6. `skills/hermes-stack-uplift/SKILL.md` + current phase slice only
7. topic research only when the current gate requires it

Human Pages are generated from these sources. Agents start at `llms.txt` / `agent/START.md` and fetch only the required slice.
