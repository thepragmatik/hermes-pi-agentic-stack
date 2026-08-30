# Hermes + Pi Agentic Stack — Control Playbook

Snapshot: 2026-08-30

This is the compact control document for a local-first, high-throughput agentic software-development stack using **NousResearch/hermes-agent** as the control-plane orchestrator and **earendil-works/pi** as the isolated coding-worker harness.

Detailed research and execution material is deliberately split under `docs/agentic-uplift/` and `skills/hermes-stack-uplift/` so Hermes does not ingest tens of thousands of tokens on every mission.

## Mission

Build a production workflow on Apple Silicon that:

- keeps Hermes as the single mission entry point and durable orchestrator;
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
2. it builds and proves the context/memory, policy/privacy/sandbox and Pi integration paths in parallel canaries;
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

## Local context and memory posture

The preferred target is **LCM + Mnemosyne**, but it is an evidence-gated canary target rather than a mandatory dependency.

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

### LCM

Qualify a pinned **stable** `hermes-lcm` release first. Initial research target is v0.20.0; re-verify at execution time rather than silently selecting an RC.

LCM replaces lossy active-context compression with a SQLite-backed summary DAG while preserving raw messages and source lineage. Use it primarily for **within-session fidelity and drill-down**. Keep optional temporal/proactive/cross-session semantic-memory features off initially while Mnemosyne owns durable memory.

### Mnemosyne

Qualify a pinned stable Mnemosyne core + Hermes wrapper; initial research targets are core v3.15.1 and wrapper v0.5.0, subject to re-verification.

Use **local embeddings**, explicit curated durable writes and conservative recall. Initial canary rules:

- no conversation autosave (`sync_roles: []`);
- no remote sync/embedding/LLM endpoint;
- no Hermes host LLM for memory;
- no tool-call auto logging;
- no automatic LLM-backed sleep;
- no persona/enhanced/fact/polyphonic/proactive recall until separately qualified;
- strict write classifier and bounded prefetch;
- memory write approval during the quality canary, deliberately removed only after precision/hygiene gates if autonomous writes are promoted.

### Built-in memory remains

Do **not** disable Hermes' memory toolset merely because Mnemosyne is active. Keep `MEMORY.md` / `USER.md` tiny for reviewed stable user/profile facts and rollback reference. `session_search` remains the host-level raw historical recall path.

### Tool Search is part of the design

LCM and Mnemosyne add non-core tools. Enable Hermes Tool Search in the uplift profile so plugin/provider schemas are progressively disclosed rather than injected eagerly on every turn. Measure the cold-tool round-trip cost against the static schema savings.

### Four-profile qualification

Compare the same long-horizon missions under:

1. built-in compressor + built-in memory/session_search;
2. LCM + built-in memory;
3. built-in compressor + Mnemosyne conservative mode;
4. **LCM + Mnemosyne conservative mode**.

Promote the simplest profile that passes accepted-task, exact-recovery, durable-recall, token/schema, restart/backup, RSS/storage and offline-operation gates. Do not force the pair if a simpler profile wins.

After dependencies/models are provisioned, block outbound network and prove context/memory operations still work. “Local primary path with cloud fallback” is not local-only.

Config examples:

- `configs/hermes-local-context-memory.example.yaml`
- `configs/mnemosyne-local.example.yaml`

Holographic remains the simpler local memory-provider fallback/challenger if Mnemosyne's richer lifecycle/tool surface does not justify itself.

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
4. context/skill/T0-T1-T2 diet + four-profile LCM/Mnemosyne qualification;
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
- selected context/memory profile proves exact recovery, useful low-noise durable recall, restart/backup and offline operation;
- context/memory ownership boundaries remain non-overlapping;
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
- rollback of Hermes/Pi plus context engine and memory provider is rehearsed;
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
4. run protocol/security/router/context/memory/LSP/coding smoke tests;
5. compare prompt/cache/recall/accepted-task metrics with prior pins;
6. inspect release/security/package changes;
7. promote only on pass;
8. otherwise keep previous pins and record an integration blocker.

Never upgrade production first and qualify second.

## Self-uplift mission

Give Hermes this mission from the bootstrap/canary profile:

> Implement the agentic uplift defined by this repository using the durable execution contract and sliced uplift skill. Treat each phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable state transition. Qualify the local context/memory stack by comparing the built-in control against LCM, Mnemosyne and their conservative combination; keep LCM as current-session context and Mnemosyne as curated durable memory unless evidence supports a simpler design. During trusted bootstrap use direct coding/shell capability only within the explicitly allowed canary/overlay/worktree scope; after the Pi/enforcement path passes its canary, revoke those capabilities from production Hermes and use typed Pi delegation for coding. Preserve upgradeability, keep old databases as read-only evidence rather than authority, collect deterministic evidence for every gate, and mark a phase `BLOCKED` or `ROLLBACK` rather than weakening a security/privacy/local-only boundary.

## Canonical index

Start with:

- `docs/agentic-uplift/implementation-playbook.md`
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

Keep this root document compact. Put detailed changing research in canonical topic documents and load it only when needed.