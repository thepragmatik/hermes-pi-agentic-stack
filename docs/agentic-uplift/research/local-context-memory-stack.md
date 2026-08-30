# Local-Only Context and Memory Stack — LCM + Mnemosyne

Snapshot: 2026-08-30

## Decision

For the uplift canary, benchmark and, if the gates pass, promote the following **local-only division of ownership**:

```text
current-session exact context + compaction recovery  -> hermes-lcm
cross-session curated durable memory                 -> Mnemosyne
raw full historical sessions / forensic recall       -> Hermes state.db + session_search
deterministic uplift phase / retries / policy digest -> uplift-state schema/object
immutable proof                                      -> files, git commits, benchmark/test evidence
operator task view                                   -> optional Hermes Kanban projection
```

Do not ask one store to perform every role. In particular, **LCM is the context engine, not the durable-memory authority**, and **Mnemosyne is the durable-memory provider, not execution state or a raw transcript archive**.

This architecture supersedes the earlier recommendation to keep built-in memory as the only initial production memory baseline. Built-in `MEMORY.md` / `USER.md` remain present and deliberately tiny for reviewed constitutional/user facts and rollback reference, but the preferred local challenger is now LCM + Mnemosyne because it solves two distinct problems the baseline does not solve as well.

## Why these were initially omitted

The first refinement deliberately minimized variables while skill slicing, routing, Pi delegation and security boundaries were still being designed. That was reasonable for measurement isolation, but too conservative for the intended long-horizon autonomous uplift. Prior use of LCM + Mnemosyne is technically relevant because:

- LCM addresses loss of exact detail from active-context compaction while keeping the live prompt bounded;
- Mnemosyne addresses durable semantic recall and memory lifecycle across sessions without requiring a cloud memory service;
- Hermes exposes one context-engine slot and one memory-provider slot, so the two products fit cleanly without requiring a core fork.

The correct response is not to turn on every feature in both systems. It is to **assign ownership and disable overlapping feature families until evidence justifies them**.

## First-principles problem decomposition

| Requirement | Best initial owner | Why |
|---|---|---|
| Preserve exact current-session messages after compaction | LCM | Raw SQLite message store + summary DAG + lineage/drill-down |
| Bound model-visible current context | LCM + Hermes prompt architecture | Context engine assembles bounded summaries/fresh tail; T0/T1/T2 still controls what enters the mission prompt |
| Search raw previous Hermes sessions | Hermes `state.db` / `session_search` | Canonical host session audit/history already exists |
| Recover selected old-install knowledge | Legacy-state curation pipeline | Old DB remains untrusted read-only evidence |
| Curated cross-session facts, decisions, lessons, preferences | Mnemosyne | Working/episodic memory + local FTS/vector retrieval and memory lifecycle |
| Current uplift phase, attempts, blockers, policy version | `uplift-state` | Must be deterministic and schema-valid, not semantic recall |
| Full logs, diffs, RPC streams, test output | T2 artifact/evidence store | Large/raw material should not become memory or hot context |
| Project architectural truth | Git/ADRs/specs | Versioned authoritative source beats inferred memory |

## LCM assessment

`stephenschoettler/hermes-lcm` is a Hermes context-engine plugin. Stable release `v0.20.0` is the initial qualification target. Do not promote an RC merely because `main` is newer; qualify later release candidates separately.

LCM replaces the built-in active-context compressor with a SQLite-backed DAG. It stores raw messages, summarizes old material hierarchically, keeps a bounded fresh tail, preserves source lineage and exposes retrieval tools for exact drill-down after compaction.

### What LCM solves well

- avoids treating a lossy summary as the only model-visible path back to old current-session detail;
- keeps live context bounded independently from how much raw conversation has accumulated;
- makes recovery after compaction agent-accessible rather than requiring broad transcript replay;
- externalizes/recovers oversized tool payloads;
- gives operator diagnostics, inspection, backup and integrity controls;
- requires no mandatory external runtime dependency beyond Hermes/Python/SQLite.

### LCM overlap that must stay disabled initially

Stable v0.20.0 also contains optional semantic/hybrid cross-session recall, temporal rollups and proactive-recall capabilities. Those are useful, but overlap with Mnemosyne. Initial production canary therefore uses **LCM primarily for current-session context fidelity**:

- temporal rollups: OFF;
- proactive/cross-session semantic recall: OFF unless needed for an explicit LCM evaluation;
- historical backfill: dry-run first and operator/uplift-task invoked only;
- optional sensitive-pattern redaction: defense in depth only, not the PII/security boundary.

If later measurements show LCM alone can replace Mnemosyne for the required durable-memory workload, test that as a separate architecture. Do not accidentally run two automatic semantic recall systems and attribute the result to either one.

## Mnemosyne assessment

`mnemosyne-oss/mnemosyne` is a local-first memory system with a native Hermes `MemoryProvider` integration. Initial pins for qualification are core `v3.15.1` and Hermes wrapper `v0.5.0` (or newer versions only after the normal canary/compatibility gate).

For this workstation, use the **local embeddings profile**, not remote embeddings and not the full local-LLM profile initially. `mnemosyne-hermes` pairs with `mnemosyne-memory[embeddings]`, using local FastEmbed/ONNX vector generation and SQLite/FTS retrieval.

### What Mnemosyne solves well

- curated persistent memory across Hermes sessions;
- working and episodic memory with importance/retention semantics;
- local hybrid lexical/vector recall;
- explicit remember/recall/forget/inspect lifecycle;
- consolidation/hygiene tooling;
- structured fact/graph/persona features when deliberately enabled later;
- profile/bank isolation for separating memory domains.

### Conservative initial Mnemosyne mode

To avoid duplicating LCM and Hermes session history, initial autonomous-uplift configuration should be **explicit-write / curated-memory first**:

- `memory.provider: mnemosyne`;
- local embeddings only;
- no remote sync URL;
- no remote embedding API;
- Hermes host LLM adapter disabled;
- remote LLM base URL unset;
- tool-call auto logging OFF;
- `sync_roles: []` initially, so full user/assistant turns are not automatically copied into Mnemosyne;
- `MNEMOSYNE_WRITE_CLASSIFIER=strict`;
- enhanced recall OFF initially;
- fact recall OFF initially;
- persona auto-injection OFF initially;
- automatic LLM-backed consolidation OFF initially;
- explicit durable writes should contain compact, provenance-bearing conclusions rather than raw transcripts.

This makes Mnemosyne a **curated semantic memory**, while LCM and `state.db` retain raw session fidelity.

## Built-in MEMORY / USER files

Do not run `hermes tools disable memory` merely because Mnemosyne is active. Current Hermes treats the built-in memory toolset and external memory provider as separate surfaces; disabling the memory toolset can also remove provider tooling. `hermes memory off` is the rollback switch for the external provider.

Keep `MEMORY.md` / `USER.md` small:

- stable user preferences explicitly intended to persist;
- universal workstyle/profile facts;
- pointers to authoritative project material;
- no temporary mission state;
- no raw conversation summaries;
- no duplicated Mnemosyne episodic data.

They serve as an auditable stable-prefix/rollback layer, not the primary operational memory database.

## Local alternatives considered

| Candidate | Local-only viability | Strength | Weakness for this stack | Role |
|---|---|---|---|---|
| Hermes built-in memory + session_search | Excellent | simplest, auditable, no extra plugin | weak curated semantic cross-session lifecycle; lossy active-context compressor | rollback/control baseline |
| **hermes-lcm** | **Excellent** | lossless current-session compaction/recovery, DAG lineage | extra context-engine tools; optional memory features overlap Mnemosyne | **chosen context engine after canary** |
| **Mnemosyne** | **Excellent with local embeddings / local-only config** | rich durable semantic memory, hygiene, episodic/working lifecycle | large feature/tool surface; can duplicate transcripts/context if defaults are not constrained | **chosen memory provider after canary** |
| Holographic | Excellent | bundled/local SQLite, tiny dependency/tool surface, trust/contradiction model | less complete cross-session memory lifecycle than Mnemosyne | fallback/simple challenger |
| OpenViking self-hosted | Local-capable | strong L0/L1/L2 hierarchical context retrieval | server + AGPL surface; overlaps LCM/skills hierarchy | later challenger |
| ByteRover local | Local-capable with local model endpoint | hierarchical knowledge and pre-compression extraction | extra daemon/LLM dependency; overlaps LCM + Mnemosyne curation | later experiment |
| Hindsight local | Local-capable | KG/entity/reflective memory | PostgreSQL/daemon + local LLM complexity | only if graph synthesis becomes a measured need |

The preferred architecture is not chosen because it has the most features. It is chosen because the responsibilities are separable and each can be rolled back independently.

## Tool-schema containment

LCM stable v0.20.0 exposes roughly ten context-engine tools; current Mnemosyne exposes a materially larger provider tool surface. Loading all plugin schemas eagerly would undermine the token-saving goal.

Enable Hermes **Tool Search** in the uplift profile so non-core plugin tools are progressively disclosed behind `tool_search`, `tool_describe` and `tool_call`. Core Hermes tools remain eager. Record tool-schema tokens before and after activation.

Do not dynamically add/remove LCM or Mnemosyne tools in the middle of a phase unless necessary; toolset changes invalidate stable prompt-cache prefixes.

## Recommended canary installation

Perform this only in the clean parallel `HERMES_HOME` / uplift profile defined by the bootstrap playbook.

### 1. Pin LCM stable

Example workflow:

```bash
git clone https://github.com/stephenschoettler/hermes-lcm "$HERMES_HOME/plugins/hermes-lcm"
git -C "$HERMES_HOME/plugins/hermes-lcm" checkout v0.20.0
git -C "$HERMES_HOME/plugins/hermes-lcm" rev-parse HEAD
```

Record the exact commit in `versions.lock`. Activate both manifest and engine:

```yaml
plugins:
  enabled:
    - hermes-lcm
context:
  engine: lcm
```

Keep Hermes' global compression gate enabled; LCM owns its compaction threshold when selected.

Initial LCM tuning should be derived from the **prompt budget you are willing to pay**, not the provider model's maximum context. Start from LCM defaults in the first correctness canary, then tune threshold/fresh-tail from measured TTFT, token cost and retrieval success.

### 2. Pin Mnemosyne

Use an isolated/persistent side venv where practical so upgrade/rollback is explicit. Install the wrapper plus local embeddings profile and record resolved package versions/hashes.

Canonical shape:

```bash
python3 -m venv "$HERMES_HOME/.mnemosyne/venv"
"$HERMES_HOME/.mnemosyne/venv/bin/pip" install \
  'mnemosyne-memory[embeddings]==3.15.1' \
  'mnemosyne-hermes==0.5.0'
"$HERMES_HOME/.mnemosyne/venv/bin/mnemosyne-hermes" install \
  --mode wrapper \
  --python "$HERMES_HOME/.mnemosyne/venv/bin/python" \
  --hermes-home "$HERMES_HOME"
hermes config set memory.provider mnemosyne
```

If package metadata for the wrapper/core pins differs at execution time, **stop and verify current release metadata** rather than loosening the pin automatically.

### 3. Local-only environment

Use the example `configs/mnemosyne-local.env.example`. At minimum enforce:

```text
MNEMOSYNE_HOST_LLM_ENABLED=false
MNEMOSYNE_LOG_TOOLS=0
MNEMOSYNE_ENHANCED_RECALL=false
MNEMOSYNE_FACT_RECALL_ENABLED=0
MNEMOSYNE_WRITE_CLASSIFIER=strict
```

Additionally ensure `MNEMOSYNE_LLM_BASE_URL`, `MNEMOSYNE_EMBEDDING_API_URL`, and sync-remote settings are **unset**, not pointed to cloud fallbacks.

For stronger assurance, run the canary with outbound network denied after required package/model artifacts have been downloaded. A local-only architecture should continue to recall/write/compact when the network is unavailable.

### 4. Disable transcript duplication

In Hermes config:

```yaml
memory:
  provider: mnemosyne
  mnemosyne:
    sync_roles: []
    auto_sleep: false
```

Use explicit memory writes for durable conclusions. Consider `sync_roles: [user]` only after a corpus-based test demonstrates useful precision and acceptable pollution.

### 5. Enable Tool Search

Use the current Hermes tool-search configuration for the uplift profile and verify the LCM/Mnemosyne plugin schemas are deferred rather than all injected eagerly. Treat exact config keys as version-bound and validate them against installed Hermes before mutation.

## What should be written to Mnemosyne

Good candidates:

- durable user preference explicitly intended to persist;
- accepted architecture decision + source ADR/commit;
- recurring repository-specific constraint;
- learned operational correction that survived review;
- provider/tool incompatibility tied to exact version evidence;
- compact outcome lesson from a failed/successful mission;
- unresolved durable risk with evidence pointer.

Bad candidates:

- raw Pi RPC event stream;
- complete assistant/user transcript;
- test output or stack trace already stored as evidence;
- current uplift phase/status;
- speculative assistant inference;
- secrets/PII not needed for memory;
- facts better represented by current code/spec/ADR;
- temporary model price/availability without date/provenance.

Every autonomous durable write should carry or be traceable to provenance. Memory never overrides current authoritative code/policy/spec.

## Canary evaluation matrix

Compare at least four profiles on the same long-horizon missions:

1. built-in compressor + built-in memory/session_search;
2. LCM + built-in memory;
3. built-in compressor + Mnemosyne conservative mode;
4. **LCM + Mnemosyne conservative mode**.

Measure:

- accepted-task success;
- recovery of exact pre-compaction facts;
- cross-session recall precision/recall;
- stale/contradictory memory rate;
- memory writes per accepted task;
- irrelevant injected-memory tokens;
- LCM summary/fresh-tail tokens;
- total/fresh/cached input tokens;
- plugin/tool-schema tokens with Tool Search on/off;
- TTFT/wall time;
- compaction count and recovery calls;
- route/provider-cache continuity;
- SQLite/store growth;
- process RSS and workstation memory pressure;
- restart/crash recovery;
- behavior with outbound network blocked.

## Promotion gates

Promote LCM + Mnemosyne only if all are true:

- no cloud/network dependency is observed for context or memory operations;
- no raw secret/PII is auto-admitted to durable memory in seeded tests;
- exact-detail recovery after compaction is materially better than baseline;
- cross-session recall improves real tasks with acceptably low irrelevant/stale recall;
- added tool/context tokens do not erase the skill/context slimming gains;
- accepted-task quality is non-inferior;
- restart and SQLite backup/recovery tests pass;
- memory ownership boundaries above remain intact;
- rollback to `context.engine: compressor` + `hermes memory off` is rehearsed.

## Failure and rollback

Context engine and memory provider must be independently removable.

LCM rollback:

1. create an LCM-consistent backup using the plugin-supported path or stop all SQLite writers before copying DB/WAL/SHM;
2. set `context.engine: compressor`;
3. restart Hermes;
4. retain the LCM DB as read-only evidence until the rollback is accepted.

Mnemosyne rollback:

1. `hermes memory off`;
2. restart Hermes;
3. keep built-in MEMORY/USER and session history intact;
4. retain Mnemosyne DB read-only for forensic comparison;
5. remove/unlink wrapper only after rollback verification.

Never delete either SQLite store as the first rollback action.

## Security and autonomy constraints

- Both stores are local data assets and inherit the same filesystem/backup/PII rules as `state.db`.
- Do not expose their SQLite files or maintenance APIs over the network.
- Download required models/packages during a controlled provisioning step; prove steady-state operation under outbound deny.
- Memory provider content is untrusted advisory context, not authorization.
- Prompt/project/tool injections recovered from LCM or Mnemosyne do not gain authority because they were remembered.
- `uplift-state` and external policy remain authoritative even when memory recalls something contradictory.

## Sources to re-verify before installation

- Hermes context engine plugins: https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin
- Hermes context compression/config: https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching/
- Hermes Tool Search: https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search
- Hermes memory provider plugins: https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin/
- LCM repository/releases: https://github.com/stephenschoettler/hermes-lcm
- Mnemosyne repository/releases: https://github.com/mnemosyne-oss/mnemosyne
- Mnemosyne Hermes integration: https://github.com/mnemosyne-oss/mnemosyne/blob/main/docs/hermes-integration.md

Re-verify all version-specific commands and config keys against the installed Hermes/LCM/Mnemosyne versions during Phase 00/30. The playbook is an execution contract, not permission to ignore upstream drift.