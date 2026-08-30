# Self-Uplift Implementation Playbook for Hermes

This is the canonical execution order for Hermes to uplift its own development stack. It separates **bootstrap authority**, **steady-state authority**, **research evidence** and **promotion evidence** so the system can become more autonomous without pretending the final security boundary exists before it has been built.

Use together with:

- `docs/agentic-uplift/agent-execution-contract.md`
- `docs/agentic-uplift/bootstrap-authority.md`
- `docs/agentic-uplift/local-context-memory-setup.md`
- `docs/agentic-uplift/research/local-context-memory-stack.md`
- `skills/hermes-stack-uplift/SKILL.md`
- `protocols/uplift-state.schema.json`
- `protocols/pi-task-envelope.schema.json`

The chat transcript is not execution state.

## Non-negotiable rules

1. Work in a branch/worktree, parallel `HERMES_HOME` or external overlay. Never modify the running production Hermes install in place without a verified rollback snapshot.
2. Treat Hermes, Pi, LCM and Mnemosyne as independently upgradeable dependencies; prefer plugins/config/skills/external adapters over core patches.
3. Security/privacy/capability policy is enforced outside prompts, context engines and memory providers.
4. Do not migrate an old Hermes `state.db`, LCM DB or Mnemosyne DB into the clean profile by attachment/copy.
5. Do not call a phase complete from prose review. Every phase has deterministic evidence.
6. Every mutating phase has an independently reversible checkpoint.
7. Bootstrap direct-write/shell authority is temporary and constrained. Remove it only after the replacement Pi path is proven, then do not silently restore it.
8. A failed security/privacy gate stops or rolls back the mission. Never weaken a boundary to make progress.
9. Memory is advisory context. It never overrides current policy, uplift state, repository truth or immutable evidence.
10. **LCM + Mnemosyne is the required local context/memory baseline.** A baseline failure means `BLOCKED`/`ROLLBACK`, not autonomous substitution of another memory architecture.
11. Local-only means steady-state context/memory operation succeeds with outbound network denied after controlled provisioning.

---

# Phase 00 — Preflight and inventory

Collect without changing behavior:

- macOS version/architecture and workstation memory/disk pressure;
- `hermes --version`, installed commit/package path and current `$HERMES_HOME`;
- current Pi version/commit;
- installed provider/model profiles without printing credentials;
- current context/compression configuration;
- current context engine and memory provider;
- `hermes prompt-size` / `/context all` or the closest current equivalent for representative profiles;
- SOUL/USER/MEMORY/project-context sizes and hashes;
- enabled plugins, skills, toolsets and MCP servers;
- current `state.db` size and session count;
- any existing LCM/Mnemosyne databases, versions and configuration from previous installations;
- Spec Kit version/presets/extensions;
- language-server versions;
- existing sandbox/container configuration;
- representative token/cache/TTFT/retry/accepted-task telemetry when available.

Write redacted `baseline.json` and `baseline.md` under the uplift evidence directory. Compute the active policy digest.

**Gate:** baseline evidence contains no raw secrets/PII and all working copies have known status.

**Rollback:** none; read-only phase.

---

# Phase 10 — Freeze, backup and optional legacy-state curation

Create a verified archive/checkpoint of the current Hermes home before changing behavior. Preserve the old `state.db` and any legacy LCM/Mnemosyne databases as immutable historical evidence.

Follow `docs/agentic-uplift/research/legacy-state-curation.md`.

Default legacy-salvage decision is **SKIPPED** unless active work genuinely needs knowledge that is not cheaper/safer to recover from repositories, ADRs or issue trackers.

If salvage is justified:

1. operate on disposable DB/home copies;
2. discover relevant sessions locally first;
3. prefer selected prompts-only exports before full transcripts;
4. treat built-in export redaction as defense in depth, not complete PII/DLP;
5. run independent local typed PII + secret sanitization;
6. extract only durable facts/decisions/preferences/risks/procedures with provenance;
7. adversarially compare candidates against current authoritative project truth;
8. admit accepted items to ADR/docs, skills/scripts/issues or explicitly curated Mnemosyne writes after the clean baseline exists—not bulk transcript memory.

Do not attach an old LCM or Mnemosyne database to the new production profile merely because it exists. Qualify import/migration behavior separately and retain originals read-only.

**Gate:** original archives verify; no legacy DB is silently attached to the clean production profile; every admitted item has provenance/current-truth evidence; clean uplift works with salvage removed.

---

# Phase 20 — Clean parallel Hermes candidate and bootstrap root of trust

Create a fresh current Hermes canary in a parallel profile/home. Do not overwrite the running installation.

Run built-in/current smoke checks plus:

- one research mission;
- one small local/canary coding task under bootstrap scope;
- built-in compression/recovery control test;
- prompt/context measurement;
- plugin/tool inventory capture.

Enable bundled `security-guidance` in WARN mode when available. It is defense in depth for Hermes-owned write/patch content—not a sandbox, DLP system or Pi diff review.

Follow `docs/agentic-uplift/bootstrap-authority.md`. During bootstrap, Hermes may retain direct source-write/shell authority only inside the explicit uplift/canary/worktree scope needed to build the replacement control plane.

**Gate:** candidate is independently runnable; old production remains intact; bootstrap write scope/checkpoint is recorded.

---

# Phase 30 — Install and qualify the LCM + Mnemosyne baseline

This phase establishes the required local context/memory substrate while separately reducing hot-context/tool-schema cost.

Implement `docs/agentic-uplift/research/mission-context-architecture.md`:

- **T0 stable prefix** — identity, small invariants, stable profile/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded objective/phase/constraints/acceptance/routing/evidence pointers, changed only at meaningful phase boundaries;
- **T2 artifact/evidence memory** — logs, full diffs, Pi RPC streams, benchmark output, research captures and large Spec Kit/source artifacts kept outside hot context.

Then follow **exactly**:

- `docs/agentic-uplift/local-context-memory-setup.md`;
- `docs/agentic-uplift/research/local-context-memory-stack.md`;
- `configs/hermes-local-context-memory.example.yaml`;
- `configs/mnemosyne-local.example.yaml`;
- `configs/lcm-baseline.env.example`.

## 30A — Capture diagnostic control and perform prompt/skill diet

Before installing the baseline, record the built-in-compressor/no-external-provider behavior as a diagnostic control:

1. measure system/tool/skill/memory/project-context token contributions;
2. capture built-in compaction/restart behavior;
3. deduplicate behavioral instructions;
4. move procedures out of always-hot SOUL/project files into sliced skills/references/scripts;
5. reduce project context to an index + invariants;
6. split orchestrator/coder tool schemas;
7. install/use the sliced uplift skill;
8. test recovery from durable uplift state + current skill slice + T2 pointers.

Do not treat the control profile as an architectural competitor. Preserve it only for regression diagnosis and emergency rollback.

## 30B — Install and pin LCM profile-locally

In the clean canary only:

- install LCM under the canary `$HERMES_HOME/plugins/hermes-lcm`;
- initial stable research pin is `v0.20.0`; re-verify current stable and security notes at execution time;
- check out the stable tag detached and record the full resolved commit SHA;
- require a clean plugin working tree;
- enable `hermes-lcm` and `context.engine: lcm`;
- retain `compression.enabled: true` because Hermes still invokes the selected context-engine lifecycle;
- apply `configs/lcm-baseline.env.example` through the profile/service launcher rather than global shell startup;
- leave the default profile-scoped DB path unless a separately justified deployment path is tested;
- keep LCM embeddings, proactive recall and temporal rollups OFF because Mnemosyne owns cross-session semantic memory;
- keep optional slash commands off in the autonomous profile;
- verify status/doctor, exact-detail drill-down, multiple compactions, restart and DB integrity.

Initial deterministic LCM settings:

```text
LCM_CONTEXT_THRESHOLD=0.35
LCM_FRESH_TAIL_COUNT=32
LCM_FRESH_TAIL_MAX_TOKENS=0
LCM_INCREMENTAL_MAX_DEPTH=3
LCM_LEAF_CHUNK_TOKENS=20000
LCM_DYNAMIC_LEAF_CHUNK_ENABLED=false
LCM_THRESHOLD_FULL_SWEEP_ENABLED=false
LCM_EMBEDDINGS_ENABLED=false
LCM_PROACTIVE_RECALL_ENABLED=false
LCM_TEMPORAL_ROLLUPS_ENABLED=false
LCM_ENABLE_SLASH_COMMAND=false
LCM_FTS_INTEGRITY_CHECK_INTERVAL_HOURS=24
```

Tune threshold/fresh tail only after target-Mac evidence. Do not promote an LCM RC merely because upstream `main` is newer.

## 30C — Install Mnemosyne in a profile-owned side venv

Initial stable research pins are `mnemosyne-memory==3.15.1` and `mnemosyne-hermes==0.5.0`; re-verify current stable releases/security notes during execution.

Use a side venv under `$HERMES_HOME/.mnemosyne/venv` and wrapper mode so a Hermes Python-environment rebuild does not silently remove the provider.

Reference sequence:

```bash
VENV="$HERMES_HOME/.mnemosyne/venv"
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install \
  'mnemosyne-memory[embeddings]==3.15.1' \
  'mnemosyne-hermes==0.5.0'
"$VENV/bin/mnemosyne-hermes" install --mode wrapper --python "$VENV/bin/python"
```

Record exact package metadata. Do not install the `[all]` local-LLM profile in the baseline; local embeddings are required, an extra generative memory model is not.

Provision/cache the pinned local embedding model before the offline proof.

## 30D — Apply the deterministic Hermes/Mnemosyne composition

Required effective baseline state:

```text
context.engine = lcm
compression.enabled = true
memory.provider = mnemosyne
memory.memory_enabled = false
memory.user_profile_enabled = false
memory.write_approval = false
Tool Search = on
```

Built-in MEMORY/USER are disabled to remove duplicate durable-memory authority/tool guidance. External Mnemosyne remains active. `state.db` / `session_search` continues as raw host session history.

Mnemosyne baseline rules:

- `sync_roles: []` — no transcript autosave;
- local FastEmbed/ONNX embeddings only;
- model `BAAI/bge-small-en-v1.5`;
- `vec_type: int8`;
- `default_scope: global` for deliberately admitted durable memories;
- `cross_session: false` so session-scoped memories remain isolated unless explicitly promoted;
- `write_classifier: strict`;
- `write_approval: false` for autonomous operation;
- `prefetch_content_chars: 800` initial bound;
- host LLM, Mnemosyne LLM, LLM conflict detection, auto-sleep, persona, enhanced/fact/polyphonic recall, proactive linking and query-intent features OFF;
- no remote sync/embedding/LLM endpoint.

The ordinary orchestrator tool allowlist is limited to:

```text
mnemosyne_remember
mnemosyne_recall
mnemosyne_remember_canonical
mnemosyne_recall_canonical
mnemosyne_forget_canonical
mnemosyne_get
mnemosyne_update
mnemosyne_invalidate
mnemosyne_stats
mnemosyne_diagnose
```

Hard-delete, shared/sync, graph, persona, scratchpad, import/export and sleep tools remain outside the ordinary agent surface.

## 30E — Enforce memory admission semantics

Canonical Mnemosyne memory is for one-current-value stable profile/operator facts. Ordinary global memory is for compact durable lessons/decisions that do not belong in a stronger authority.

Never store in Mnemosyne:

- current phase/attempt/idempotency/policy state;
- raw logs, diffs, source bodies, test output or Pi RPC streams;
- secrets, credentials or raw PII;
- authoritative architecture/spec facts better represented in Git/ADR/spec;
- temporary task/blocker state;
- whole conversation or compaction summaries;
- unsanitized legacy-state content.

When memory conflicts with policy, uplift-state, Git/ADR/spec or immutable evidence, **memory loses**.

## 30F — Tool-schema containment

LCM and Mnemosyne add non-core tools. Keep Hermes Tool Search ON using the bounded baseline configuration:

```text
threshold_pct=5
search_default_limit=5
max_search_limit=20
listing=auto
listing_max_tokens=4000
```

Measure tool-schema tokens, cold-tool extra round trips and discovery failures. Keep plugin/provider membership stable within a phase to preserve cache affinity.

## 30G — Baseline qualification with diagnostic component isolation

Run representative long-horizon missions against the required **LCM + Mnemosyne baseline**. Retain three diagnostic controls only when needed to isolate a failure:

1. built-in compressor + no external provider;
2. LCM + no external provider;
3. built-in compressor + Mnemosyne;
4. **LCM + Mnemosyne baseline**.

The first three do not compete for production selection. They answer “which component caused this regression?”

Seed missions requiring:

- exact recovery of details outside the fresh tail;
- multiple LCM compactions;
- restart/session continuation;
- cross-session recall of explicitly admitted global memory;
- canonical fact supersession/retirement;
- rejection of stale/contradictory memory;
- rejection of irrelevant-memory injection;
- absence of raw secret/PII memory;
- large T2 artifact retrieval by pointer rather than prompt/memory mirroring.

Measure accepted-task quality, exact-detail recovery, memory recall precision/staleness, injected-memory tokens, LCM summary/fresh-tail tokens, total/fresh/cached input, TTFT/wall time, tool-schema tokens, SQLite growth, RSS and macOS memory pressure/swap.

The stable Mnemosyne 3.15.x pin predates later relevance/prefetch work. Irrelevant-memory injection is therefore a **blocking qualification test**. Do not jump to unreleased `main`; qualify a future stable normally.

## 30H — Prove local-only steady state

After dependencies and embedding artifacts are provisioned, deny outbound network externally for the context/memory canary and prove:

- LCM ingest/compaction/exact retrieval works;
- Mnemosyne global and canonical write/recall works with local embeddings;
- restart and DB recovery works;
- backup/integrity checks pass;
- neither subsystem falls back to remote sync, embeddings, memory LLM or auxiliary cloud processing.

This test covers the **context/memory subsystem**. Later cloud research/coding model traffic is separately controlled by the stack's egress/privacy policy.

## 30I — Backup and rollback rehearsal

Back up LCM and Mnemosyne independently. Prefer live/plugin-supported backup mechanisms; filesystem-level SQLite copy requires quiescent writers or correct DB/WAL/SHM handling.

Prove restore into a disposable profile.

Rehearse rollback to the last known-good control profile without deleting failed stores. Freeze/checksum failed stores as diagnostic evidence.

## Phase 30 promotion gate

LCM + Mnemosyne is qualified only when:

- exact pinned stable versions/config are recorded;
- built-in MEMORY/USER are disabled while external Mnemosyne remains available;
- no transcript autosave or raw evidence duplication enters memory;
- autonomous curated writes work without human approval and satisfy strict admission policy;
- exact-detail recovery survives multiple LCM compactions and restart;
- durable recall is useful with low stale/irrelevant injection;
- local-only context/memory works under enforced outbound-network denial;
- added plugin/tool-schema cost remains bounded with Tool Search;
- both stores have verified backup/restore;
- target-Mac RSS/memory pressure and accepted-task quality are acceptable;
- rollback is rehearsed.

If any mandatory gate fails, set Phase 30 to `BLOCKED` or `ROLLBACK`. **Do not autonomously promote a simpler memory architecture instead.** Repair/requalify the fixed baseline or escalate a deliberate architecture-change decision.

---

# Phase 40 — Router shadow system

Implement routing in layers:

1. security/privacy hard gate;
2. deterministic agent-state gate;
3. semantic classifier;
4. confidence calibration + hysteresis + abstention;
5. optional difficulty/escalation component.

Follow `docs/agentic-uplift/research/router-training-control.md`.

Benchmark:

- always research;
- always coding;
- deterministic rules;
- rules + explicit state;
- Qwen3-Embedding-0.6B prototype;
- frozen `nomic-ai/modernbert-embed-base` at 256d and 768d with the same calibrated linear/logistic head;
- fine-tuned ModernBERT only after frozen-head plateau and representative pair-specific outcomes;
- optional RouteLLM-style difficulty adapter after recalibration.

Route phases, not micro-turns. Use hysteresis to avoid oscillation and preserve provider cache affinity.

Split evaluation by mission/repository/session/time cohort—not random near-duplicate turns.

**Gate:** shadow router beats fixed/state baselines on downstream accepted-task utility/regret; zero observed `LOCAL_ONLY -> cloud`; route-switch rate and cache continuity are acceptable; classification/calibration/latency targets pass.

No routing authority yet.

---

# Phase 50 — Provider/model bake-off and stable role bindings

Keep stable architectural roles separate from volatile model identifiers:

- `research.default` -> current qualified research specialist;
- `coding.default` -> current qualified coding specialist;
- optional local reviewer/fallback role;
- policy-compatible fallback routes.

For each candidate provider route measure the same frozen tasks/prefixes:

- fresh and cached input tokens/cost;
- cache-hit ratio;
- TTFT and wall time;
- output/reasoning volume;
- tool-call validity;
- rate-limit/provider failures;
- accepted outcome;
- retries/human intervention.

Pin provider/model/account for a mission phase after selection. Do not churn providers to chase instantaneous token price.

**Gate:** chosen bindings are versioned/pinned and win on cost/minutes per accepted task, not nominal token price alone.

---

# Phase 60 — Build external security/enforcement substrate

Before a cloud-enabled Pi worker receives production authority, implement real enforcement primitives outside prompts:

- versioned role/capability policy parser;
- workspace/path calculator and path/symlink checks;
- environment allowlist/scrubber;
- process/command policy;
- sandbox launcher abstraction;
- network/egress allowlist/default deny;
- task-scoped credential brokerage;
- deterministic secret scanner;
- typed/context-aware PII scanner/transformer;
- re-scan after transformation;
- policy digest binding;
- evidence recorder;
- idempotency/attempt/reconciliation state;
- independent merge/review authority.

Do not adopt the previous-session privacy proxy unchanged. Reimplement its useful architecture/test ideas with typed payload handling; generic phone/identifier regexes can corrupt IP addresses, UUID fixtures, CSS values and code/config text.

Do not persist raw sensitive spans in sanitizer telemetry/cache. Apply equivalent at-rest/sanitization policy to context/memory stores where sensitive content may be captured.

**Gate:** seeded secrets/PII fail closed; denied filesystem/network/credential actions fail structurally in the chosen containment layer; policy is more than YAML/prompt prose.

Bootstrap Hermes direct authority may still exist in canary scope at this point.

---

# Phase 70 — Minimal Hermes -> Pi bridge, offline/local-first

Implement `delegate_pi` outside Hermes core where possible against the **current** Pi protocol.

Minimum bridge requirements:

- validate v2 task envelope + policy digest;
- fixed role -> capabilities mapping;
- create isolated git worktree;
- minimal environment/credential exposure;
- launch pinned Pi RPC/headless mode over local stdin/stdout pipe;
- never expose unauthenticated Pi RPC over a network listener;
- stream/redact events to local evidence storage without mirroring raw streams into Hermes context/memory;
- timeout/cancel/budget handling;
- idempotent retry/reconciliation;
- compact typed result/evidence;
- deterministic cleanup/recovery.

**Protocol invariant:** Pi `agent_end` is not completion. Treat `agent_settled` as fully settled task-run completion because retry/compaction/queued continuation may follow `agent_end`.

Before provider credentials:

- fake RPC framing/error test;
- worktree/path/symlink escape tests;
- environment leak test;
- denied-network test;
- duplicate destructive retry/idempotency test;
- timeout/cancel test;
- malicious repository instruction test;
- evidence integrity test.

Use `PI_OFFLINE=1` where appropriate for offline fixtures.

Pi itself has no built-in filesystem/process/network/credential permission system. Qualify a pinned external sandbox/container/micro-VM/capability-broker implementation and prove denied actions fail structurally.

**Gate:** bridge mechanics and external containment pass without requiring production cloud authority.

---

# Phase 80 — Privacy-controlled Pi cloud canary and LSP

Only after the egress boundary passes canaries may Pi receive cloud specialist credentials.

Run one non-sensitive coding canary and verify:

- correct provider/model pin;
- egress/privacy evidence;
- worktree-only mutations;
- no unauthorized environment leakage;
- `agent_settled` completion semantics;
- bounded retries;
- tests/security evidence;
- worker cannot merge or self-approve.

Then seed adversarial secret/PII payloads and prove fail-closed behavior.

Pin/audit LSP integration and language servers for:

- TypeScript/JavaScript;
- Python;
- Java;
- Kotlin (compatibility suite required while upstream remains immature);
- HTML/CSS.

Inject bounded diagnostics: changed/relevant files, severity-first, capped items—not workspace dumps.

**Gate:** representative diagnostic/reference/rename workflow per language; no context flood; cloud canary passes privacy/containment evidence.

---

# Phase 90 — Authority cutover

This is the root-of-trust transition from bootstrap to production autonomy.

1. switch production Hermes to the constrained orchestrator profile;
2. remove generic source-write/arbitrary-shell capability from that profile;
3. make typed Pi delegation the only coding execution path;
4. retain external policy/privacy/sandbox enforcement outside prompts/skills/context/memory;
5. explicitly instruct Hermes to "skip Pi and edit directly"—the attempt must fail structurally;
6. record the new policy digest/capability inventory and cutover evidence.

Bootstrap authority may remain only in a separately named disposable emergency/canary profile. It is never silently activated for ordinary work.

**Gate:** parent/orchestrator bypass is structurally impossible in production profile.

---

# Phase 100 — Spec Kit mission profiles

Use presets/extensions rather than forking core templates. Implement deterministic profiles:

- Micro/Patch;
- Lite;
- Standard;
- High Assurance.

Risk policy may escalate a profile; a model cannot downgrade a policy-required high-assurance profile.

Generated Spec Kit Markdown is durable source, not mandatory hot context. Index it and load only relevant acceptance/plan/task sections.

Benchmark lighter profiles against the current all-phases workflow on matched tasks.

**Gate:** initial target >=25% median input-token reduction with non-inferior accepted-task quality for eligible lighter profiles.

---

# Phase 110 — Durable task graph and optional Kanban projection

Replace unconstrained swarms with bounded task graph + dispatcher semantics:

- planner creates typed bounded cards;
- dispatcher validates role/capability/privacy/budget;
- workers execute isolated cards;
- deterministic checks run;
- independent reviewer card runs;
- merge/release gate evaluates evidence.

No worker self-promotes or creates unrestricted roles.

Hermes Kanban may be used as a durable mission ledger/human supervision surface because it survives restarts and exposes blocked/review/retry state. Treat it as a projection, not execution authority:

```text
uplift-state schema/object = authoritative state
Kanban                     = operational ledger/UI
immutable evidence         = proof
LCM/Mnemosyne              = advisory context/memory
```

Do not load Kanban tools into ordinary profiles solely for visibility when CLI/dashboard automation is sufficient.

---

# Phase 120 — Adversarial suite

Execute the architecture and artifact-usability failure catalogues. At minimum test:

- prompt/SOUL/security non-propagation;
- parent bypass of Pi;
- malicious project/AGENTS/context instructions;
- malicious/stale instructions recovered from LCM or Mnemosyne;
- memory poisoning and contradictory durable writes;
- irrelevant Mnemosyne prefetch/injection;
- unwanted transcript duplication across `state.db`, LCM and Mnemosyne;
- LCM compaction/recovery loss;
- LCM/Mnemosyne database corruption/restart/backup failure;
- context/memory unexpected network egress;
- memory-provider/tool schema expansion with Tool Search disabled/enabled;
- upstream default/config drift enabling auto-sleep/persona/LLM/remote behavior;
- Pi protocol/version drift;
- `agent_end` premature-completion bug;
- PII/secret false negatives;
- PII sanitizer corruption/false positives on technical text;
- provider failover privacy violation;
- malicious LSP/tool output;
- extension/package supply-chain substitution;
- duplicate/destructive retry;
- worker/reviewer correlated blind spots;
- memory pressure/swap under realistic browser/build/container load;
- rate/concurrency bottlenecks;
- stale/contradictory legacy-state admission;
- route oscillation/cache destruction.

A prose explanation is not a pass. Record immutable evidence.

---

# Phase 130 — Canary and promotion

Run representative batches in shadow/canary mode. Compare against the captured pre-uplift control:

- accepted-task rate/quality;
- total/fresh/cached tokens;
- cache-hit continuity;
- TTFT/wall time;
- route-switch rate;
- LCM exact-context recovery success;
- Mnemosyne durable-memory precision/staleness;
- context/memory/tool-schema token overhead;
- retries;
- human intervention;
- security events;
- crashes/update failures;
- workstation memory pressure/swap;
- cost and minutes per accepted task.

Promote gradually. Keep one-operation rollback for previous Hermes/Pi versions **and independent context/memory rollback**.

**Gate:** accepted-task quality is non-inferior within the chosen confidence interval and every mandatory security/authority/context-memory gate remains green.

---

# Phase 140 — Daily/continuous upgrade discipline

For each upstream Hermes/Pi/LCM/Mnemosyne update:

1. fetch current trusted metadata in a disposable canary;
2. back up each SQLite store before schema-affecting upgrades;
3. apply the versioned uplift overlay without overwriting upstream-owned files;
4. diff effective configuration/defaults and tool surface;
5. run protocol/security/router/context/memory/LSP/representative coding smoke tests;
6. rerun LCM exact-recovery, Mnemosyne relevance/poisoning and offline/no-network tests;
7. compare prompt/cache/recall/accepted-task/RSS metrics to previous pins;
8. check plugin/package security notes;
9. promote new pins only on pass;
10. otherwise retain prior pins and file an integration issue.

Never update the production installation or its only context/memory database first and test afterward.

Any unavoidable upstream patch must be feature-flagged, integration-tested, documented and tracked for upstreaming/removal.

---

# Self-uplift mission brief

Give Hermes this mission from the bootstrap/canary profile:

> Implement the agentic uplift defined by this repository using the durable execution contract and sliced uplift skill. Treat every phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable state transition. During trusted bootstrap, use direct coding/shell capability only inside the explicitly allowed canary/overlay/worktree scope. Install and qualify **LCM + Mnemosyne as the required local context/memory baseline** according to `docs/agentic-uplift/local-context-memory-setup.md`; do not substitute another memory architecture if its mandatory gates fail. Keep LCM responsible for current-session context/compaction recovery and Mnemosyne responsible for curated durable cross-session memory, with built-in MEMORY/USER disabled in the baseline. After the Pi/enforcement path passes its canary, revoke direct coding/shell capability from the production orchestrator and use typed Pi delegation for coding. Preserve upstream upgradeability, keep old databases as read-only evidence rather than migrated authority, collect deterministic evidence for every gate, and mark a phase `BLOCKED` or `ROLLBACK` rather than weakening a security/privacy/context-memory boundary. Verify assumptions against actually installed stable versions before implementation.

## Autonomous stop conditions

Hermes must stop rather than improvise when:

- original backup/checkpoint cannot be verified;
- raw legacy state would need cloud exposure to continue;
- LCM/Mnemosyne installation resolves to an unreviewed release, incompatible schema or unknown effective config;
- required Mnemosyne tools/config keys do not match the pinned stable wrapper;
- a supposedly local context/memory path attempts unexpected network egress;
- built-in MEMORY/USER remain active and create duplicate durable-memory authority;
- Mnemosyne transcript autosave, auto-sleep/persona/LLM paths or unapproved remote behavior becomes active;
- irrelevant/stale memory materially influences an acceptance/security decision;
- LCM exact-detail recovery fails after compaction/restart;
- either context/memory backup or rollback cannot be demonstrated;
- sanitizer/security scanner fails or privacy classification is uncertain;
- external Pi containment is unproven;
- provider credentials would be exposed outside the allowed worker boundary;
- destructive retry state cannot be reconciled;
- current Pi/Hermes protocol differs from the pinned/tested contract;
- bypass of Pi remains possible after intended cutover;
- accepted-task quality materially regresses;
- promotion would require disabling a mandatory control.

A blocked optional feature (legacy salvage, local reviewer, experimental router framework, Holographic/OpenViking research) does not block the core mission. **LCM + Mnemosyne is not optional in the selected architecture**: failure of that baseline blocks its promotion until repaired/requalified or the operator deliberately changes the architecture.
