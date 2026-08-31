# Local-Only Context and Memory Stack — LCM + Mnemosyne

Snapshot: 2026-08-30.

## Decision

**LCM + Mnemosyne is the baseline architecture for the clean Hermes uplift profile.** It is no longer a challenger competing for architectural selection.

```text
current-session exact context + compaction recovery  -> hermes-lcm
cross-session curated durable memory                 -> Mnemosyne
raw full Hermes session history / forensic recall    -> state.db + session_search
deterministic uplift phase/retry/policy/blockers      -> uplift-state schema/object
large raw proof                                       -> T2 files/git/test/benchmark evidence
operator task view                                    -> optional Kanban projection
project truth                                         -> Git/ADR/specs
```

The built-in Hermes compressor with no external memory provider remains a diagnostic/control and emergency rollback profile. It is not an automatic production substitute. If the LCM + Mnemosyne baseline cannot pass a mandatory compatibility, correctness, local-only, privacy, backup or recovery gate, Phase 20 becomes `BLOCKED` or `ROLLBACK` until the baseline is repaired or the architecture is deliberately reconsidered.

Detailed installation and operation are canonical in `docs/agentic-uplift/local-context-memory-setup.md`.

## Why the pair is coherent

The products solve different layers:

- **LCM** is a Hermes context engine. It bounds current-session model-visible context while preserving exact raw messages and lineage for later drill-down.
- **Mnemosyne** is a Hermes memory provider. It stores deliberately admitted durable information across sessions and retrieves it semantically.

Hermes has a single selected context-engine slot and a single selected external memory-provider slot, so the pair maps cleanly to host architecture without a core fork.

The design only stays coherent if overlap is prevented. Do not let LCM become a second automatic cross-session semantic-memory provider while Mnemosyne is active, and do not let Mnemosyne become a raw transcript archive that duplicates LCM/state.db.

## Baseline version posture

Initial stable qualification pins from this research snapshot:

| Component | Initial stable pin | Baseline posture |
|---|---:|---|
| `hermes-lcm` | `v0.20.0` | pin stable tag + resolved commit; no RC promotion |
| `mnemosyne-memory` | `3.15.1` | local embeddings extra; exact package pin |
| `mnemosyne-hermes` | `0.5.0` | wrapper integration; exact package pin |
| embedding model | `BAAI/bge-small-en-v1.5` | local FastEmbed/ONNX |

Re-verify current stable releases and security notes during Phase 00/20. New stable releases are canary-upgraded; upstream `main`, LCM release candidates and Mnemosyne betas are not silently selected.

A stable pin is not proof of fitness. The target-Mac qualification still decides whether the baseline may be production-promoted.

## LCM ownership and configuration

Stable LCM stores raw messages in profile-local SQLite, builds a hierarchical summary DAG, assembles a bounded fresh tail/summary frontier and provides source-aware drill-down after compaction.

Baseline LCM settings are versioned in `configs/lcm-baseline.env.example`:

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

Keep Hermes `compression.enabled: true`; with `context.engine: lcm`, LCM owns plugin compaction and `LCM_CONTEXT_THRESHOLD` is the principal baseline trigger. Do not tune Hermes' built-in compressor threshold as though it controlled LCM.

Do not set `LCM_DATABASE_PATH` by default. Stable LCM resolves its empty path inside the active `HERMES_HOME`, preserving profile isolation.

### Why LCM semantic memory is off

LCM v0.20.0 also offers opt-in semantic/hybrid cross-session recall, temporal rollups and proactive recall. Those are intentionally disabled because Mnemosyne is the durable semantic-memory owner.

Enabling them later is an architecture experiment requiring a separate benchmark; it is not routine tuning.

## Mnemosyne ownership and configuration

Mnemosyne is the sole external durable-memory provider in the baseline. The complete effective composition is in `configs/hermes-local-context-memory.example.yaml`; the Mnemosyne subconfiguration is mirrored for inspection in `configs/mnemosyne-local.example.yaml`.

### Built-in Hermes memory is disabled

Set:

```yaml
memory:
  provider: mnemosyne
  memory_enabled: false
  user_profile_enabled: false
  write_approval: false
```

Hermes keeps an external provider active when the two built-in stores are disabled. This removes the built-in MEMORY/USER tool/guidance from the hot prompt and prevents a second durable-memory authority.

`state.db` / `session_search` remains the raw host session-history surface; disabling built-in MEMORY/USER does not mean deleting session history.

### Autonomous write posture

The production baseline uses `write_approval: false`. Human approval of each durable write would defeat autonomous operation and would not be a meaningful model-side security boundary.

Instead, durable-write safety is enforced by:

- `sync_roles: []` — no full-turn transcript autosave;
- `write_classifier: strict`;
- explicit store-ownership/admission rules;
- a narrow Mnemosyne tool allowlist;
- local-only operation;
- validity/provenance conventions;
- poisoning/staleness tests;
- independent project/execution authorities that memory cannot override.

### Local-only Mnemosyne path

Baseline configuration uses:

- `embeddings_via_api: false`;
- `embedding_model: BAAI/bge-small-en-v1.5`;
- `vec_type: int8`;
- no remote sync target;
- no host LLM;
- no Mnemosyne remote/local generative-memory LLM path initially;
- no LLM conflict detection;
- no auto-sleep;
- no persona auto-memory;
- no enhanced/fact/polyphonic/proactive/query-intent recall features;
- `prefetch_content_chars: 800` as an intentionally bounded initial budget;
- `default_scope: global` for explicitly admitted durable memory;
- `cross_session: false` so unrelated session-scoped memories are not implicitly swept into recall.

The last two are complementary: global durable memories are explicitly cross-session by nature; session memories remain local to their session unless intentionally queried/promoted.

## Mnemosyne memory classes

### Canonical facts

Use canonical memory only for one-current-value profile facts such as stable operator preferences or identity/profile properties. Canonical replacement preserves history; canonical retirement should retire rather than hard-delete.

### Ordinary global durable memory

Use ordinary global memory for compact lessons/decisions likely to help future sessions when Git/ADR/spec is not the better authority. Prefer source/provenance metadata and explicit validity horizons for time-sensitive facts.

### Forbidden memory content

Do not use Mnemosyne for:

- uplift phase/attempt/idempotency/policy digest;
- raw logs, diffs, source bodies, Pi RPC streams or benchmark corpora;
- secrets, credentials or unsanitized PII;
- authoritative project architecture/specification that belongs in Git;
- temporary task/blocker state;
- wholesale conversation/compaction summaries;
- unsanitized legacy database material.

Memory is advisory context. Current policy, `uplift-state`, authoritative repository content and immutable evidence win every conflict.

## Tool surface and Tool Search

Mnemosyne exposes a broad tool family upstream. The baseline intentionally exposes only:

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

Hard-delete, sync/shared-bank, graph, persona, scratchpad, import/export and sleep tools are not part of the ordinary autonomous profile.

Hermes Tool Search is ON with a bounded listing budget so non-core plugin/provider schemas are progressively disclosed. This prevents a richer memory stack from undoing skill/context token savings through eagerly injected tool schemas.

## Install isolation

Install LCM profile-locally under the clean `HERMES_HOME/plugins/hermes-lcm` and pin the stable tag/commit.

Install Mnemosyne in a profile-owned side venv under `$HERMES_HOME/.mnemosyne/venv` and use its wrapper integration. This keeps the provider independently upgradeable from the rebuildable Hermes Python environment and reduces the chance that a Hermes repair/update silently removes the memory package.

Exact commands and verification gates are in `local-context-memory-setup.md`.

## Known risk posture

### Mnemosyne relevance/prefetch

The stable 3.15.x research pin predates later upstream work on relevance/prefetch behavior. Do not jump to unreleased `main` to obtain a fix. Instead:

- keep the durable corpus curated (`sync_roles: []`);
- keep optional richer recall systems off;
- bound `prefetch_content_chars`;
- seed irrelevant/stale memories in qualification;
- make irrelevant-memory injection a blocking gate;
- canary-upgrade to the next stable release normally when its fixes are available.

### Auto-sleep/concurrency/default drift

`auto_sleep_enabled`, persona and LLM-backed features are set explicitly OFF because effective defaults can change between releases and some historical issues involved autonomous maintenance paths. Qualification checks **effective runtime config**, not only checked-in YAML.

### SQLite durability

LCM and Mnemosyne are independent SQLite-backed stores. Backup/restore both separately and verify restore rather than assuming copying one live `.db` file is sufficient. LCM live backup should use its operator facility; filesystem copy requires quiescent writers or correct WAL/SHM handling.

## Diagnostic controls, not alternative architecture selection

Keep these profiles reproducible for diagnosis/regression:

1. built-in compressor + no external provider;
2. LCM + no external provider;
3. built-in compressor + Mnemosyne;
4. **LCM + Mnemosyne baseline**.

Their purpose is component isolation: if token cost, recall or recovery regresses, determine which layer caused it. They do **not** form a winner-take-all production bake-off anymore.

If the required baseline fails a mandatory gate, retain the last known-good production profile and mark Phase 20 `BLOCKED`/`ROLLBACK`. Do not let Hermes autonomously switch to Holographic, OpenViking, ByteRover or another memory provider as an architectural workaround.

## Local-only proof

After package and embedding-model artifacts are provisioned, deny outbound network externally and repeat:

- LCM ingest/compaction/exact recovery;
- Mnemosyne global memory write/recall;
- canonical fact write/read/retire;
- restart/recovery;
- backup/integrity tests.

Any unexpected remote embedding, sync, auxiliary-memory LLM or other network attempt fails the context/memory baseline. This is separate from the wider stack's deliberately policy-controlled cloud research/coding model traffic.

## Promotion metrics

Record on representative long-horizon missions:

- accepted-task quality;
- exact-detail recovery after multiple compactions;
- recovery after restart;
- durable-memory precision, stale/irrelevant injection and contradiction behavior;
- memory writes per accepted task;
- injected memory tokens;
- LCM summary/fresh-tail tokens;
- non-core tool-schema tokens with Tool Search;
- total/fresh/cached input;
- TTFT and wall time;
- SQLite growth;
- process RSS, macOS memory pressure and swap;
- backup/restore outcome;
- offline/no-network outcome.

The baseline may be production-promoted only when these gates are acceptable on the target Mac. The architecture decision is fixed; runtime qualification is not assumed.

## Alternatives retained for contingency research

Holographic, OpenViking, ByteRover, Hindsight and other local/self-hostable systems remain documented research alternatives. They are useful if the architecture is deliberately reopened later, but they are not part of ordinary autonomous fallback logic.

This keeps the playbook decisive while preserving reversibility and future evidence-based redesign.
