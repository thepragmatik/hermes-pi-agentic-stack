# Self-Uplift Implementation Playbook for Hermes

This is the canonical execution order for Hermes to uplift its own development stack. It separates **bootstrap authority**, **steady-state authority**, **research evidence** and **promotion evidence** so the system can become more autonomous without pretending the final security boundary exists before it has been built.

Use together with:

- `docs/agentic-uplift/agent-execution-contract.md`
- `docs/agentic-uplift/bootstrap-authority.md`
- `docs/agentic-uplift/research/local-context-memory-stack.md`
- `skills/hermes-stack-uplift/SKILL.md`
- `protocols/uplift-state.schema.json`
- `protocols/pi-task-envelope.schema.json`

The chat transcript is not execution state.

## Non-negotiable rules

1. Work in a branch/worktree, parallel `HERMES_HOME` or external overlay. Never modify the running production Hermes install in place without a verified rollback snapshot.
2. Treat Hermes, Pi, LCM and Mnemosyne as independently upgradeable dependencies; prefer plugins/config/skills/external adapters over core patches.
3. Security/privacy/capability policy is enforced outside prompts, context engines and memory providers.
4. Do not migrate an old Hermes `state.db` into the clean profile.
5. Do not call a phase complete from prose review. Every phase has deterministic evidence.
6. Every mutating phase has an independently reversible checkpoint.
7. Bootstrap direct-write/shell authority is temporary and constrained. Remove it only after the replacement Pi path is proven, then do not silently restore it.
8. A failed security/privacy gate stops or rolls back the mission. Never weaken a boundary to make progress.
9. Memory is advisory context. It never overrides current policy, uplift state, repository truth or immutable evidence.
10. Local-only means steady-state context/memory operation succeeds with outbound network denied after controlled provisioning.

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

Default legacy-salvage decision is **SKIPPED** unless a current mission genuinely needs knowledge that is not cheaper/safer to recover from repositories, ADRs or issue trackers.

If salvage is justified:

1. operate on disposable DB/home copies;
2. discover relevant sessions locally first;
3. prefer selected prompts-only exports before full transcripts;
4. treat built-in export redaction as defense in depth, not complete PII/DLP;
5. run independent local typed PII + secret sanitization;
6. extract only durable facts/decisions/preferences/risks/procedures with provenance;
7. adversarially compare candidates against current authoritative project truth;
8. admit accepted items to ADR/docs, compact user memory, skills/scripts, issues or explicitly curated Mnemosyne writes—not bulk transcript memory.

Do not attach an old LCM or Mnemosyne database to the new production profile merely because it exists. Qualify import/migration behavior separately and retain the originals read-only.

**Gate:** original archives verify; no legacy DB is silently attached to the clean production profile; every admitted item has provenance/current-truth evidence; clean uplift works with salvage removed.

---

# Phase 20 — Clean parallel Hermes candidate and bootstrap root of trust

Create a fresh current Hermes canary in a parallel profile/home. Do not overwrite the running installation.

Run built-in/current smoke checks plus:

- one research mission;
- one small local/canary coding task under bootstrap scope;
- built-in compression/recovery test;
- prompt/context measurement;
- plugin/tool inventory capture.

Enable bundled `security-guidance` in WARN mode when available. It is only defense in depth for Hermes-owned write/patch content—not a sandbox, DLP system or Pi diff review.

Follow `docs/agentic-uplift/bootstrap-authority.md`. During bootstrap, Hermes may retain direct source-write/shell authority only inside the explicit uplift/canary/worktree scope needed to build the replacement control plane.

**Gate:** candidate is independently runnable; old production remains intact; bootstrap write scope/checkpoint is recorded.

---

# Phase 30 — Context, skills and local memory qualification

This phase has two goals that must be measured separately:

1. reduce hot-context/tool-schema/token cost;
2. improve long-horizon recovery without creating a second uncontrolled source of truth.

Implement `docs/agentic-uplift/research/mission-context-architecture.md`:

- **T0 stable prefix** — identity, small invariants, stable profile/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded objective/phase/constraints/acceptance/routing/evidence pointers, changed only at meaningful phase boundaries;
- **T2 artifact/evidence memory** — logs, full diffs, Pi RPC streams, benchmark output, research captures and large Spec Kit/source artifacts kept outside hot context.

Then follow `docs/agentic-uplift/research/local-context-memory-stack.md`.

## 30A — Prompt and skill diet on built-in baseline

1. measure system/tool/skill/memory/project-context token contributions;
2. deduplicate behavioral instructions;
3. move procedures out of always-hot SOUL/USER/project files into sliced skills/references/scripts;
4. reduce project context to an index + invariants;
5. split orchestrator/coder tool schemas;
6. install/use the sliced uplift skill;
7. test restart/compaction recovery from durable uplift state + current skill slice + T2 evidence pointers.

Retain built-in compressor + compact MEMORY/USER + `session_search` as the control profile. Do not erase this control configuration after the experiment.

## 30B — Pin and qualify LCM

In the clean canary only:

- install/pin the latest qualified **stable** `hermes-lcm` release; initial research pin is `v0.20.0`, but re-verify at execution time;
- record tag, commit, database location and config digest in `versions.lock`/evidence;
- enable plugin `hermes-lcm` and select runtime `context.engine: lcm`;
- leave Hermes' global compression gate enabled because it still gates plugin compaction;
- start from stable LCM defaults for the correctness run, then tune threshold/fresh-tail from the prompt budget actually worth paying;
- keep LCM temporal rollups, proactive recall and competing cross-session semantic-memory features OFF initially while Mnemosyne is evaluated as durable memory owner;
- verify `lcm_status`/doctor/backup and exact-detail drill-down after multiple compactions;
- verify restart recovery and DB integrity.

Do not upgrade the autonomous production profile to an LCM release candidate merely because the repository `main` is newer. RCs get a separate canary.

## 30C — Pin and qualify Mnemosyne in conservative local mode

Initial research pins are Mnemosyne core `v3.15.1` and Hermes integration `v0.5.0`; re-verify current stable releases and security notes at execution time.

Use the local embeddings profile and a side/persistent venv where practical. Apply `configs/mnemosyne-local.example.yaml` plus the Hermes fragment in `configs/hermes-local-context-memory.example.yaml`.

Ownership rules:

- no conversation transcript autosave initially (`sync_roles: []`);
- explicit curated durable writes only;
- no remote sync endpoint;
- no embedding API;
- no host/cloud LLM for memory;
- no automatic tool-call logging;
- no persona injection, enhanced recall, fact recall, polyphonic recall, proactive linking or automatic LLM-backed sleep during the first correctness/token canary;
- strict write classifier;
- bounded memory prefetch;
- built-in MEMORY/USER remain tiny rollback/audit facts, not duplicated episodic storage.

Enable Mnemosyne write approval during the initial memory-quality test so proposed writes can be inspected. After the precision/hygiene gate passes, autonomous operation may deliberately disable that approval gate; do not let the agent approve its own staged canary memories and call the test successful.

## 30D — Tool-schema containment

LCM and Mnemosyne add non-core plugin/provider tools. Enable current Hermes Tool Search in the uplift profile so those schemas are progressively disclosed rather than injected eagerly on every turn.

Measure:

- eager vs Tool Search system/tool-schema tokens;
- cold-tool extra round trips;
- tool discovery failures;
- prompt-cache invalidations caused by toolset changes.

Keep the provider/plugin set stable within a phase to preserve cache affinity.

## 30E — Four-profile context/memory benchmark

Run the same long-horizon corpus under:

1. built-in compressor + built-in memory/session_search;
2. LCM + built-in memory;
3. built-in compressor + Mnemosyne conservative mode;
4. **LCM + Mnemosyne conservative mode**.

Include missions that intentionally require:

- exact recovery of a detail that disappeared from the live tail;
- recovery after multiple compactions;
- restart/session continuation;
- cross-session recall of a reviewed durable decision;
- rejection of stale/contradictory remembered facts;
- no recall of a raw secret/PII canary;
- retrieval of a large T2 artifact by pointer rather than prompt mirroring.

Measure accepted-task quality, exact-detail recovery, cross-session recall precision/recall, stale/irrelevant recall, memory writes per accepted task, injected-memory tokens, LCM summary/fresh-tail tokens, total/fresh/cached input, TTFT/wall time, tool-schema tokens, compactions/recovery calls, SQLite growth, process RSS and workstation memory pressure.

## 30F — Prove local-only steady state

After dependencies/models are provisioned, deny outbound network for the context/memory canary and prove:

- LCM ingest/compaction/retrieval works;
- Mnemosyne write/recall works with local embeddings;
- restart and database backup checks pass;
- neither subsystem silently falls back to a remote endpoint or Hermes cloud auxiliary model.

A configuration is not local-only merely because its primary path is local.

## Phase 30 promotion gate

Promote LCM + Mnemosyne only when:

- fixed/hot context is materially smaller without accepted-task regression;
- exact-detail compaction recovery is better than the built-in control;
- cross-session durable recall improves real missions with low irrelevant/stale recall;
- no raw Pi/log/research artifact is mirrored into hot context or durable memory;
- no cloud dependency is observed for context/memory operations;
- added plugin/tool tokens do not erase the skill/context savings;
- backup/restart/recovery is proven;
- ownership remains: LCM=current-session context, Mnemosyne=curated durable memory, `state.db`=raw session history, uplift-state=mission authority;
- rollback to `context.engine: compressor` + `hermes memory off` is rehearsed.

If the pair fails, promote the best simpler profile rather than forcing the preferred architecture.

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

Do not adopt the previous-session privacy proxy unchanged. Its useful architecture/test ideas should be reimplemented with typed payload handling; generic phone/identifier regexes can corrupt IP addresses, UUID fixtures, CSS values and code/config text.

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
- never expose unauthenticated Pi RPC over the network;
- stream/redact events to local evidence storage without mirroring raw streams into Hermes context;
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

Risk policy may escalate a profile; a model cannot downgrade a policy-required high-assurance mission.

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

Hermes Kanban may be used as a durable mission ledger/human supervision surface because it survives restarts and exposes blocked/review/retry state. Treat it as a **projection**, not execution authority:

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
- unwanted transcript duplication across `state.db`, LCM and Mnemosyne;
- LCM compaction/recovery loss;
- LCM/Mnemosyne database corruption/restart/backup failure;
- context/memory unexpected network egress;
- memory-provider schema/token explosion with Tool Search disabled/enabled;
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

Run representative batches in shadow/canary mode. Compare against the captured baseline:

- accepted-task rate/quality;
- total/fresh/cached tokens;
- cache-hit continuity;
- TTFT/wall time;
- route-switch rate;
- context recovery success;
- durable-memory recall precision/staleness;
- memory/context/tool-schema token overhead;
- retries;
- human intervention;
- security events;
- crashes/update failures;
- workstation memory pressure/swap;
- cost and minutes per accepted task.

Promote gradually. Keep one-operation rollback for the previous Hermes/Pi versions **and independent context/memory rollback** (`context.engine: compressor`, `hermes memory off`).

**Gate:** accepted-task quality is non-inferior within the chosen confidence interval and every mandatory security/authority/context-memory gate remains green.

---

# Phase 140 — Daily/continuous upgrade discipline

For each upstream Hermes/Pi/LCM/Mnemosyne update:

1. fetch current trusted metadata in a disposable canary;
2. back up any SQLite store using a quiescent/plugin-supported method before schema-affecting upgrades;
3. apply the versioned uplift overlay without overwriting upstream-owned files;
4. run protocol/security/router/context/memory/LSP/representative coding smoke tests;
5. compare prompt/cache/recall/accepted-task metrics to previous pins;
6. check plugin/package changes and security notes;
7. promote new pins only on pass;
8. otherwise retain prior pins and file an integration issue.

Never update the production installation or its only context/memory database first and test afterward.

Any unavoidable upstream patch must be feature-flagged, integration-tested, documented and tracked for upstreaming/removal.

---

# Self-uplift mission brief

Give Hermes this mission from the bootstrap/canary profile:

> Implement the agentic uplift defined by this repository using the durable execution contract and sliced uplift skill. Treat every phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable state transition. During trusted bootstrap, use direct coding/shell capability only inside the explicitly allowed canary/overlay/worktree scope. Qualify the local context/memory stack by comparing the built-in control against LCM, Mnemosyne and their conservative combination; do not enable overlapping automatic memory features merely to claim success. After the Pi/enforcement path passes its canary, revoke direct coding/shell capability from the production orchestrator and use typed Pi delegation for coding. Preserve upstream upgradeability, keep old databases as read-only evidence rather than migrated authority, collect deterministic evidence for every gate, and mark a phase `BLOCKED` or `ROLLBACK` rather than weakening a security/privacy boundary. Verify assumptions against actually installed versions before implementation.

## Autonomous stop conditions

Hermes must stop rather than improvise when:

- original backup/checkpoint cannot be verified;
- raw legacy state would need cloud exposure to continue;
- LCM/Mnemosyne installation resolves to an unreviewed release or incompatible schema;
- a supposedly local context/memory path attempts unexpected network egress;
- context/memory rollback cannot be demonstrated;
- memory poisoning/stale recall materially influences an acceptance or security decision;
- sanitizer/security scanner fails or privacy classification is uncertain;
- external Pi containment is unproven;
- provider credentials would be exposed outside the allowed worker boundary;
- destructive retry state cannot be reconciled;
- current Pi/Hermes protocol differs from the pinned/tested contract;
- bypass of Pi remains possible after intended cutover;
- accepted-task quality materially regresses;
- promotion would require disabling a mandatory control.

A blocked optional feature or failed preferred challenger does **not** block the clean uplift when a simpler qualified path exists. Prefer the simplest profile that passes the gates rather than forcing LCM, Mnemosyne, Holographic, a local reviewer or an experimental router into production.