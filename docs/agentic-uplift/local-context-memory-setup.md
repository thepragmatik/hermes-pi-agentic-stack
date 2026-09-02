# LCM + Mnemosyne Baseline Setup and Qualification

Snapshot: 2026-08-31.

## Baseline decision

The clean uplift profile uses **LCM + Mnemosyne as the required local context/memory baseline**:

- **LCM** — current-session exact context, bounded assembly, compaction recovery
- **Mnemosyne** — curated cross-session durable semantic memory
- **state.db** — raw Hermes session history / forensic session_search
- **uplift-state** — deterministic mission/attempt/policy/blocker authority
- **T2 artifacts** — logs, diffs, Pi RPC, benchmark/test evidence
- **Git/ADR/spec** — authoritative project truth

This is no longer an architecture-selection bake-off. The built-in Hermes compressor/no-external-memory configuration is retained only as a **diagnostic control and rollback profile**. If LCM or Mnemosyne cannot pass a mandatory compatibility, correctness, privacy, offline, backup or recovery gate, mark Phase 20 `BLOCKED`/`ROLLBACK`; do not silently substitute a different production memory architecture.

## Initial stable pins

Initial qualification pins from the 2026-08-31 research snapshot:

- `hermes-lcm`: `v0.20.0` stable;
- `mnemosyne-memory`: `3.15.1` stable;
- `mnemosyne-hermes`: `0.5.0` stable;
- local embedding model: `BAAI/bge-small-en-v1.5` through FastEmbed/ONNX.

At execution time, re-check current **stable** releases and security notes. A newer stable may replace these pins only after the normal compatibility canary. Do not promote an LCM release candidate or Mnemosyne beta merely because upstream `main` is newer.

Record exact tags, resolved commit/package hashes, Python version, Hermes version and effective config in uplift evidence.

## 1. Start from a clean parallel Hermes profile

Never install the baseline first into the currently running production home.

Set the clean canary profile/home according to the installed Hermes profile mechanism, then confirm that `HERMES_HOME` points to the canary before every installation command.

Example shell guard:

```bash
: "${HERMES_HOME:?Set HERMES_HOME to the clean canary profile first}"
printf 'HERMES_HOME=%s\n' "$HERMES_HOME"
test -d "$HERMES_HOME"
```

Archive/checksum the pre-uplift production home separately. The old `state.db`, LCM DB or Mnemosyne DB is never attached to the new profile by default.

## 2. Install and pin LCM profile-locally

Install LCM in the canary profile's plugin directory rather than a shared/global plugin directory:

```bash
mkdir -p "$HERMES_HOME/plugins"
git clone https://github.com/stephenschoettler/hermes-lcm \
  "$HERMES_HOME/plugins/hermes-lcm"
git -C "$HERMES_HOME/plugins/hermes-lcm" fetch --tags --force
git -C "$HERMES_HOME/plugins/hermes-lcm" checkout --detach v0.20.0
git -C "$HERMES_HOME/plugins/hermes-lcm" status --porcelain
git -C "$HERMES_HOME/plugins/hermes-lcm" rev-parse HEAD
```

The status output must be clean. Persist the full commit SHA as evidence rather than relying on the tag name alone.

LCM stable configuration is environment-driven. Apply `configs/lcm-baseline.env.example` through the canary launcher/service environment, not through global shell startup files.

Baseline intent:

- `LCM_CONTEXT_THRESHOLD=0.35`;
- fresh tail = 32 messages with no additional token cap initially;
- hierarchical depth = 3;
- default 20K raw leaf floor;
- dynamic chunking/full-sweep disabled initially;
- LCM embeddings disabled;
- LCM proactive recall disabled;
- LCM temporal rollups disabled;
- optional slash command disabled;
- profile-scoped default database path (`$HERMES_HOME/lcm.db`).

These are a deterministic starting point, not universal optimums. Tune threshold/fresh tail only after target-Mac evidence shows a better accepted-task/token/TTFT tradeoff.

Do not enable LCM semantic/proactive/cross-session memory features while Mnemosyne owns durable memory. If those features are researched later, treat that as a new architecture experiment rather than silently widening the baseline.

## 3. Install Mnemosyne in an upgrade-independent side venv

Use a profile-owned side venv so rebuilding/updating the Hermes Python environment does not silently remove the memory provider package.

```bash
: "${HERMES_HOME:?}"
VENV="$HERMES_HOME/.mnemosyne/venv"
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install \
  'mnemosyne-memory[embeddings]==3.15.1' \
  'mnemosyne-hermes==0.5.0'
"$VENV/bin/mnemosyne-hermes" install \
  --mode wrapper \
  --python "$VENV/bin/python"
```

Persist `pip freeze`/package metadata in the local uplift evidence directory. Do not install the `[all]` extra for the baseline: local vector recall is required; a local generative-memory LLM is not.

The first local-embedding use may need to download the pinned FastEmbed model. Provision/cache that artifact before the offline qualification step, and record the resolved model/cache identity.

## 4. Apply the Hermes baseline composition

Merge `configs/hermes-local-context-memory.example.yaml` into the clean canary config.

Required effective state:

- `plugins.enabled` includes `hermes-lcm`
- `context.engine = lcm`
- `compression.enabled = true`
- `memory.provider = mnemosyne`
- `memory.memory_enabled = false`
- `memory.user_profile_enabled = false`
- `memory.write_approval = false`
- Tool Search = on

Why built-in MEMORY/USER are off: Hermes' external memory provider is independent of those built-in stores. Disabling both removes the built-in memory tool/guidance while leaving Mnemosyne active, preventing a second durable-memory authority and reducing prompt/schema duplication.

Why write approval is off: this is an autonomous baseline. A provider whose writes require a human to approve every durable fact is not autonomous. Safety instead comes from strict classification, explicit memory ownership, a narrow tool allowlist, local-only operation, provenance/validity conventions and rollback/adversarial tests.

## 5. Mnemosyne baseline policy

Use the exact conservative settings in `configs/mnemosyne-local.example.yaml` / the complete Hermes composition.

### Storage and recall

- `sync_roles: []`: no automatic transcript mirroring;
- local FastEmbed/ONNX embeddings only;
- `BAAI/bge-small-en-v1.5`;
- `vec_type: int8` for the initial local store;
- `default_scope: global` for explicitly admitted durable memory;
- `cross_session: false`, so unrelated session-scoped memories are not implicitly swept into recall;
- bounded provider prefetch (`prefetch_content_chars: 800`) until precision is proven.

A caller that truly needs temporary session memory must explicitly request `scope=session`.

### Memory synthesis features kept off

Explicitly keep these OFF in the baseline even if upstream defaults later drift:

- host LLM adapter;
- Mnemosyne LLM path;
- LLM conflict detection;
- auto-sleep/consolidation;
- persona auto-memory;
- enhanced/fact/polyphonic recall;
- proactive linking;
- query-intent LLM/feature expansion;
- recall diagnostics in ordinary production turns.

Upgrade qualification must verify the **effective** configuration, not merely compare a checked-in YAML file, because provider defaults can change between releases.

### Tool surface

Allow only the curation/inspection tools required for ordinary autonomous operation:

`mnemosyne_remember`, `mnemosyne_recall`, `mnemosyne_remember_canonical`, `mnemosyne_recall_canonical`, `mnemosyne_forget_canonical`, `mnemosyne_get`, `mnemosyne_update`, `mnemosyne_invalidate`, `mnemosyne_stats`, `mnemosyne_diagnose`
```

Do not expose hard-delete, remote sync, shared-bank, graph, persona, scratchpad, import/export or sleep/consolidation tools to the ordinary orchestrator profile. Operator maintenance can use the local CLI outside the model-facing tool surface.

Tool Search remains ON so non-core plugin/provider schemas are progressively disclosed instead of permanently consuming the hot prompt.

## 6. Durable-memory admission policy

Mnemosyne is not a transcript archive and not a replacement for project source control.

### Use canonical memory for

`mnemosyne_remember_canonical` is appropriate for one-current-value profile facts such as:

- stable operator preference explicitly intended to persist;
- stable agent/profile identity or operating preference;
- a current relationship/name/communication preference.

Canonical updates supersede the current slot while retaining history; retirement should use the canonical retirement tool rather than destructive deletion.

### Use ordinary global memory for

`mnemosyne_remember(scope=global, ...)` is appropriate for compact durable lessons or decisions that improve future work but are not better represented as authoritative Git/ADR/spec content.

Prefer provenance metadata and a validity horizon when practical. Mark deterministic observations as tool/observed evidence and model deductions as inferred rather than silently upgrading them to fact.

### Never use Mnemosyne for

- current uplift phase/attempt/idempotency/policy digest;
- raw source code, full diffs, logs or Pi RPC streams;
- secrets, credentials or raw PII;
- an authoritative project architecture decision that belongs in Git/ADR/spec;
- temporary task lists/blockers that belong in uplift-state/Kanban;
- whole session summaries merely because compaction occurred;
- unsanitized legacy `state.db` material.

## 7. Restart and health verification

Restart only the canary Hermes profile after configuration.

Verify at minimum:

1. Hermes reports `context.engine: lcm` and `memory.provider: mnemosyne` in effective configuration/status;
2. LCM plugin is pinned/loaded and its database resolves inside the canary `HERMES_HOME`;
3. after one normal message, LCM status/doctor is healthy;
4. built-in MEMORY/USER guidance/tool is absent while the whitelisted Mnemosyne tools remain discoverable;
5. an explicit test memory can be stored and precisely recalled;
6. a canonical fact can be written, superseded/read and retired without hard deletion;
7. a session-scoped test memory does not leak into an unrelated session under the baseline recall policy;
8. `session_search` still provides raw Hermes historical-session recall independently;
9. prompt-size/tool-schema measurements are captured with Tool Search active.

Remove/invalidate synthetic qualification memories after the test.

## 8. Compaction/recovery qualification

Run long-horizon canaries that force multiple LCM compactions. Seed exact details before compaction and verify they can be recovered from LCM lineage/drill-down rather than hallucinated from summaries.

Test:

- exact identifiers/numbers/acceptance clauses;
- earlier tool result references;
- recovery after Hermes restart;
- multiple compaction generations;
- oversized tool/output behavior;
- stale/contradictory durable Mnemosyne memories;
- irrelevant-memory injection.

The stable Mnemosyne 3.15.x line predates later work on prefetch/relevance behavior, so **irrelevant-memory injection is a mandatory blocking test**. Do not switch to unreleased `main` solely to obtain a fix; qualify the next stable release normally when available.

## 9. Prove local-only operation

Provision packages and the embedding model first. Then enforce outbound-network denial outside Hermes for the canary and repeat:

- LCM ingest, compaction and exact retrieval;
- Mnemosyne explicit global write and recall;
- canonical write/recall/retire;
- Hermes restart and provider recovery;
- database integrity/backup checks.

Any attempt to contact a remote embedding, sync, memory LLM or auxiliary cloud endpoint is a failure. “Usually local” is not local-only.

This local-only proof applies to **context and memory**. The overall agent stack may later deliberately use qualified cloud research/coding models through its separate privacy/egress policy.

## 10. Backup and recovery

Treat LCM and Mnemosyne as independently recoverable stores.

### LCM

When Hermes/LCM is live, prefer LCM's online backup/operator facility. If copying SQLite at filesystem level, stop all writers first or preserve the database together with relevant WAL/SHM state; never copy only a busy SQLite main file and call it a verified backup.

Record backup digest plus LCM tag/commit/config/environment digest.

### Mnemosyne

Use Mnemosyne's local backup/verify facilities and retain the side-venv/package pins separately from data. Verify a restore into a disposable profile before production promotion.

Do not bundle old production/legacy stores into the clean baseline as a convenience migration.

## 11. Rollback

LCM and Mnemosyne must be independently reversible.

Rollback profile:

- `context.engine` -> built-in compressor
- `memory.provider` -> off / no external provider
- built-in MEMORY/USER remain disabled unless explicitly restoring the old control profile

Do not delete the failed LCM/Mnemosyne databases during rollback. Freeze/checksum them as diagnostic evidence, restore the prior known-good config/package pins, restart the profile, and prove session/mission recovery from authoritative uplift-state + evidence.

A failed baseline qualification means Phase 20 is `BLOCKED` or `ROLLBACK`. It does **not** authorize Hermes to choose Holographic, OpenViking or another memory architecture autonomously.

## 12. Upgrade discipline

For every LCM/Mnemosyne stable upgrade:

1. backup both stores;
2. clone/upgrade only a disposable canary profile;
3. record exact old/new versions and config-default diffs;
4. rerun plugin/provider startup and tool-whitelist checks;
5. rerun exact-detail compaction/recovery;
6. rerun durable-memory precision/staleness/poisoning tests;
7. rerun offline/no-network proof;
8. rerun backup/restore;
9. compare prompt/tool-schema tokens and target-Mac RSS/swap;
10. promote only after every mandatory gate passes.

Never upgrade production first and validate afterward.

## Acceptance gate

LCM + Mnemosyne is qualified as the baseline only when all are true:

- exact pinned stable versions/config are recorded;
- LCM owns context/compaction and Mnemosyne owns durable memory with no overlapping automatic semantic-memory path enabled;
- built-in MEMORY/USER are disabled in the baseline profile;
- no transcript autosave or raw-evidence mirroring enters Mnemosyne;
- autonomous curated writes work without human approval and satisfy strict admission policy;
- exact-detail recovery survives multiple LCM compactions and restart;
- durable recall is useful with low stale/irrelevant injection;
- local-only context/memory still works under enforced outbound-network denial;
- Tool Search keeps added plugin/provider schema cost bounded;
- both SQLite stores have verified backup/restore procedures;
- target-Mac RSS/memory pressure and accepted-task quality remain acceptable;
- rollback to the last known-good control profile is rehearsed.

Until then, the architecture decision is fixed but the production promotion state remains **not qualified**.
