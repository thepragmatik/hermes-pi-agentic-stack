# Hermes + Pi Agentic Stack — Control Playbook

Snapshot: 2026-08-30

This is the compact control document for a local-first, high-throughput agentic software-development stack using **NousResearch/hermes-agent** as the control-plane orchestrator and **earendil-works/pi** as the isolated coding-worker harness.

Detailed research and execution material is deliberately split under `docs/agentic-uplift/` and `skills/hermes-stack-uplift/` so Hermes does not ingest tens of thousands of tokens on every mission.

## Mission

Build a production workflow on Apple Silicon that:

- keeps Hermes as the single mission entry point and durable orchestrator;
- uses **LCM + Mnemosyne as the local context/memory baseline**;
- routes research/synthesis and coding/tool work to qualified specialist roles;
- keeps the always-on local router small;
- delegates coding through a typed Hermes -> Pi boundary;
- enforces filesystem/process/network/credential/PII/secret/merge policy outside prompts;
- uses LSP selectively without workspace context floods;
- keeps context/memory local, recoverable and bounded;
- minimizes repeated prompt/spec/tool-schema prefill while preserving quality;
- uses mission-sensitive Spec Kit profiles;
- survives Hermes/Pi/LCM/Mnemosyne upgrades through canary qualification and rollback;
- measures accepted-task quality, latency, retries, cache behavior, recall quality, human intervention and spend before promotion.

## Execution authority

The desired steady state is strict at the agent boundary: production Hermes has no arbitrary shell/source-write authority and coding crosses the typed Pi path.

That state cannot exist before Hermes builds the Pi/enforcement path. The uplift therefore uses an explicit **trusted bootstrap authority**:

1. current Hermes may temporarily write/run shell only inside a constrained canary/overlay/worktree scope;
2. it installs/qualifies the required local context/memory baseline and builds the policy/privacy/sandbox substrate;
3. it builds/tests the Pi bridge offline/local-first;
4. it proves a privacy-controlled Pi cloud canary;
5. only then does it revoke direct coding/shell capability from production Hermes;
6. an instruction to “skip Pi and edit directly” must thereafter fail structurally.

See `docs/agentic-uplift/bootstrap-authority.md` and `docs/agentic-uplift/agent-execution-contract.md`.

## Router architecture

Use four routing/control layers:

1. **Tier 0 — deterministic security/privacy + state gate.** Resolve non-negotiable trust constraints and obvious operational state.
2. **Tier 1 — compact semantic classifier.** Benchmark Qwen3-Embedding-0.6B and frozen ModernBERT Embed challengers with a calibrated lightweight head.
3. **Tier 2 — confidence/hysteresis/abstention.** Route phases rather than micro-turns; optional RouteLLM-style difficulty escalation is separate.
4. **Tier 3 — specialist execution.** Pin provider/model/account within a phase/session to preserve cache affinity.

Security policy stays outside the learned classifier. Do not keep a 20B–100B+ generative model resident merely to classify mission intent.

### ModernBERT progression

Benchmark:

```text
rules
-> rules + structured agent state
-> Qwen3 embedding prototype
-> frozen nomic ModernBERT Embed 256d/768d + calibrated linear/logistic head
-> fine-tuned ModernBERT-base only after the frozen baseline plateaus
-> optional pairwise difficulty/escalation model
```

Primary promotion metrics are accepted-task utility/regret, high-severity wrong-lane errors, retries/human overrides, route-switch rate, cache continuity, time/cost per accepted task and then classification/calibration metrics.

See `docs/agentic-uplift/research/router-training-control.md`.

## Context and token architecture

Apply three operational temperatures:

- **T0 stable prefix** — identity, small invariants, stable role/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded objective/phase/constraints/acceptance/routing/evidence pointers, changed only at meaningful phase boundaries;
- **T2 artifact/evidence memory** — full logs/diffs/Pi RPC streams/benchmarks/research/large Spec Kit artifacts outside hot context, retrieved by slice.

Do not mirror the same mission state, command output or worker transcript into chat, memory, project context and artifacts simultaneously.

See:

- `docs/agentic-uplift/research/mission-context-architecture.md`
- `docs/agentic-uplift/research/context-token-optimization.md`
- `docs/agentic-uplift/research/skill-slimming-slicing.md`
- `docs/agentic-uplift/research/local-context-memory-stack.md`

## Local context and memory baseline

**LCM + Mnemosyne is a fixed architecture decision for this playbook.** Runtime promotion remains evidence-gated, but Hermes does not choose a different production memory architecture on its own when the pair fails a gate.

Assign exactly one owner to each class of state:

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission phase, attempt, blocker and policy authority
T2 evidence  = raw logs, diffs, benchmark/test outputs
Git/ADR/spec = current project truth
Kanban       = optional operational projection/UI
```

Memory is advisory. Policy, uplift-state, current repository truth and immutable evidence win every conflict.

### LCM baseline

Initial stable research pin is `hermes-lcm v0.20.0`, re-verified during execution. Install it profile-locally and record the full resolved commit.

Use LCM for **within-session fidelity and drill-down**, with the versioned baseline environment:

```text
threshold=0.35
fresh tail=32
incremental depth=3
leaf floor=20000
embeddings=off
proactive recall=off
temporal rollups=off
```

LCM's optional semantic/proactive/temporal memory families stay OFF because Mnemosyne owns durable semantic memory. Do not promote an RC merely because upstream `main` is newer.

### Mnemosyne baseline

Initial stable research pins are core `3.15.1` and Hermes wrapper `0.5.0`, re-verified during execution.

Install Mnemosyne in a profile-owned side venv/wrapper with the local embeddings extra. Baseline behavior:

- no transcript autosave (`sync_roles: []`);
- local FastEmbed/ONNX `BAAI/bge-small-en-v1.5` only;
- `vec_type: int8`;
- explicit durable writes default to global scope;
- strict write classifier;
- autonomous writes (`write_approval: false`);
- bounded prefetch;
- no remote sync/embedding/LLM endpoint;
- no Hermes host LLM for memory;
- no auto-sleep, persona, enhanced/fact/polyphonic/proactive/query-intent features;
- narrow curation/inspection tool allowlist only.

### Built-in MEMORY/USER are disabled

The baseline sets:

```text
memory.memory_enabled = false
memory.user_profile_enabled = false
memory.provider = mnemosyne
```

This removes duplicate built-in durable-memory guidance/tooling while preserving the external provider. `state.db/session_search` remains the raw host session-history path.

### Tool Search is mandatory

LCM and Mnemosyne add non-core tools. Enable Hermes Tool Search so provider/plugin schemas are progressively disclosed rather than injected eagerly. Baseline listing budget is 4000 tokens; measure actual static/cold-tool cost.

### Qualification is not architecture selection

Keep built-in-only, LCM-only and Mnemosyne-only profiles reproducible **for diagnostic component isolation**. They do not compete for production selection.

LCM + Mnemosyne must prove:

- exact-detail recovery after multiple compactions and restart;
- useful low-noise durable recall;
- canonical fact lifecycle;
- no transcript/evidence duplication into durable memory;
- no irrelevant/stale memory influencing acceptance/security decisions;
- no unexpected context/memory network egress after provisioning;
- bounded tool-schema/context overhead;
- verified backup/restore of both stores;
- acceptable target-Mac RSS/memory pressure and accepted-task quality.

If a mandatory gate fails, Phase 30 becomes `BLOCKED`/`ROLLBACK`. Hermes does **not** autonomously switch to Holographic, OpenViking or another architecture.

Config/setup:

- `docs/agentic-uplift/local-context-memory-setup.md`
- `configs/hermes-local-context-memory.example.yaml`
- `configs/mnemosyne-local.example.yaml`
- `configs/lcm-baseline.env.example`

Alternatives remain contingency research only unless the operator deliberately reopens the architecture decision.

## Skill slicing

Treat skills as progressive disclosure:

1. profile/catalog metadata routes to an eligible skill;
2. `SKILL.md` contains only invariants and phase map;
3. current phase detail lives in one `references/` slice;
4. deterministic mechanics belong in scripts/templates;
5. large evidence remains external until needed.

The repository includes `skills/hermes-stack-uplift/` with phase slices. More micro-skills are not automatically better; measure tokens per accepted task.

## Legacy Hermes `state.db`

The old database is historical evidence, not memory to transplant.

Default legacy status is **SKIPPED**. If active work genuinely needs historical context:

1. freeze/checksum the original home/DB;
2. operate only on a disposable copy;
3. discover relevant sessions locally before export;
4. prefer selected prompts-only export first;
5. treat built-in redaction as defense in depth, not complete PII/DLP;
6. independently sanitize locally;
7. extract only durable provenance-bearing candidates;
8. adversarially compare them with current repository truth;
9. admit accepted items to the correct durable surface—not a bulk transcript or DB transplant.

The clean uplift must work identically without salvaged context.

See `docs/agentic-uplift/research/legacy-state-curation.md`.

## Hermes built-ins

Two built-ins are useful without becoming security authority:

- **`security-guidance` WARN mode** — defense in depth for Hermes-owned write/patch content; not sandbox/DLP/Pi diff review.
- **Kanban** — optional durable mission ledger/human UI for blocked/review/retry state. `uplift-state` remains authoritative; Kanban is a projection.

## Zero-trust Pi invariant

Pi has no built-in filesystem/process/network/credential permission system. Final worker authority therefore requires external containment.

Each coding task must use:

- validated v2 task envelope + policy digest;
- fixed role -> capability mapping;
- isolated git worktree;
- minimal environment/credential exposure;
- external sandbox/container/micro-VM/capability broker;
- network default deny/allowlist;
- local secret + typed-PII egress checks;
- bounded retry/idempotency semantics;
- deterministic test/LSP/security evidence;
- independent review/merge gate.

Pi RPC remains a local pipe. Treat `agent_settled` as fully settled completion; `agent_end` may still be followed by retry/compaction/queued continuation.

## Spec Kit

Use deterministic profiles: **Micro/Patch**, **Lite**, **Standard**, **High Assurance**. Policy may escalate; a model cannot downgrade a required high-assurance profile.

Generated Markdown is durable source material, not mandatory hot context. Index and retrieve current acceptance/plan/task slices only.

## Autonomous execution order

Canonical detail is `docs/agentic-uplift/implementation-playbook.md`. High-level order:

1. preflight/inventory;
2. freeze/backup and optional legacy-state curation;
3. clean parallel Hermes candidate + bootstrap checkpoint;
4. install/qualify **LCM + Mnemosyne baseline** plus context/skill/T0-T1-T2 diet;
5. router shadow evaluation;
6. provider/model bake-off;
7. external security/privacy/enforcement substrate;
8. minimal Pi bridge offline/local-first + containment qualification;
9. privacy-controlled Pi cloud canary + LSP;
10. **authority cutover** — revoke direct production Hermes coding/shell capability;
11. Spec Kit mission profiles;
12. bounded task graph + optional Kanban projection;
13. adversarial suite including memory poisoning/context recovery/offline tests;
14. canary comparison and gradual promotion;
15. continuous Hermes/Pi/LCM/Mnemosyne canary-upgrade discipline.

## Acceptance gates

Before production promotion:

- old production/legacy archives remain recoverable;
- no old DB is migrated into clean production;
- fixed/hot context shrinks without accepted-task regression;
- LCM + Mnemosyne proves exact recovery, useful low-noise durable recall, restart/backup and offline operation;
- built-in MEMORY/USER are disabled in the production baseline;
- context/memory ownership boundaries remain non-overlapping;
- autonomous curated memory writes pass admission/poisoning/staleness tests;
- no raw secrets/PII are automatically admitted to durable memory in seeded tests;
- plugin/provider tool-schema overhead does not erase slimming gains;
- routing beats fixed/state baselines on held-out mission outcomes;
- no observed `LOCAL_ONLY -> cloud` path exists;
- external Pi containment structurally denies disallowed actions;
- every coding task crosses the typed Pi boundary after cutover;
- direct Hermes bypass after cutover fails structurally;
- required test/LSP/security evidence is represented in task results;
- lighter Spec Kit profiles materially reduce eligible-task input tokens without quality regression;
- representative Mac memory pressure/swap remains acceptable;
- rollback of Hermes/Pi plus LCM/Mnemosyne is rehearsed;
- accepted-task quality is non-inferior within the chosen confidence interval.

## Economics

Planning baseline: **3,888,531,773 logical tokens/month**.

Treat savings as measured outcomes, not promises. Optimize **cost + minutes + retries + human intervention per accepted task**, while separately tracking context/memory/tool-schema tokens and cache-hit continuity.

## Upgrade discipline

This repository is an overlay/control repository, not a permanent fork.

For every Hermes/Pi/LCM/Mnemosyne update:

1. install/update a disposable canary;
2. take a plugin-supported/quiescent backup before database/schema-affecting changes;
3. apply pinned uplift integration;
4. diff effective defaults/config/tool surface;
5. run protocol/security/router/context/memory/LSP/coding smoke tests;
6. rerun exact-recovery, memory relevance/poisoning and offline/no-network tests;
7. compare prompt/cache/recall/accepted-task metrics with prior pins;
8. inspect release/security/package changes;
9. promote only on pass;
10. otherwise keep previous pins and record an integration blocker.

Never upgrade production first and qualify second.

## Self-uplift mission

Give Hermes this mission from the bootstrap/canary profile:

> Implement the agentic uplift defined by this repository using the durable execution contract and sliced uplift skill. Treat each phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable state transition. Install and qualify **LCM + Mnemosyne as the required local context/memory baseline** using `docs/agentic-uplift/local-context-memory-setup.md`; keep LCM as current-session context/compaction recovery and Mnemosyne as curated durable memory, with built-in MEMORY/USER disabled. Do not substitute another memory architecture when a mandatory baseline gate fails—mark the phase `BLOCKED`/`ROLLBACK` and repair/requalify or escalate a deliberate architecture change. During trusted bootstrap use direct coding/shell capability only within the explicitly allowed canary/overlay/worktree scope; after the Pi/enforcement path passes its canary, revoke those capabilities from production Hermes and use typed Pi delegation for coding. Preserve upgradeability, keep old databases as read-only evidence rather than authority, collect deterministic evidence for every gate, and never weaken a security/privacy/local-only boundary to make progress.

## Canonical index

Start with:

- `docs/agentic-uplift/implementation-playbook.md`
- `docs/agentic-uplift/local-context-memory-setup.md`
- `docs/agentic-uplift/agent-execution-contract.md`
- `docs/agentic-uplift/bootstrap-authority.md`
- `skills/hermes-stack-uplift/SKILL.md`
- `docs/agentic-uplift/artifact-usability-review.md`
- `docs/agentic-uplift/adversarial-review.md`
- `docs/agentic-uplift/research/local-context-memory-stack.md`
- `docs/agentic-uplift/research/legacy-state-curation.md`
- `docs/agentic-uplift/research/router-training-control.md`
- `docs/agentic-uplift/research/mission-context-architecture.md`
- `docs/agentic-uplift/research/security-zero-trust-pii.md`
- `docs/agentic-uplift/research/hermes-pi-lsp.md`

Keep this root document compact. Put detailed changing research/configuration in canonical topic documents and load it only when needed.
