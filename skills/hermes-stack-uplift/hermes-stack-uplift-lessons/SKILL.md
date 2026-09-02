---
name: hermes-stack-uplift-lessons
description: "Use when executing uplift phases on this host."
---

# Hermes Stack Uplift — Host Execution Lessons

Companion to the `hermes-stack-uplift` skill (whose slice references cover the generic phase design). This file holds concrete, host-verified execution notes from real phase runs so future sessions do not rediscover them by trial. For the context-management (CM) mission's own benchmark recipe — child-run harness, flag-matrix drivers, adversarial scoring — load the dedicated `context-management-execution` skill instead; this file keeps only the host-wide lessons that outlived that mission.

## Context Management (CM) mission specifics (verified 2026-09-01)

The CM mission (phases CM-00..CM-80) runs from its own durable dir `~/.hermes/profiles/uplift/cm/` with its own evidence + corpus tree. Lessons:

- **Schema-per-mission, not schema-fork.** The repo's `protocols/uplift-state.schema.json` is hard-locked to mission-1 phase ids (8-item prefixItems with const ids). Never weaken or edit it (repo is read-only during execution). Instead create a mission-specific schema (e.g. `cm-state.schema.json`) next to the state file, mirroring the repo schema's conventions (same enums for phaseStatus/adoption_state, required boundary_report on COMPLETE), and validate with the repo's `tools/validate_state.py <state> <schema>` — it takes any schema path.
- **Validate a generated schema immediately.** Building `prefixItems` programmatically (list-comprehension over phase ids) produced wrong const ids on the first try. Run the validator against the freshly written state right away, not after filling in all phases.
- **PII sweep hits generated artifacts too.** Absolute home paths (real username paths) leak into tool-output captures like `SHA256SUMS` files and version inventories, not just hand-written evidence. Sweep the whole new evidence tree (`grep -rI`), text-replace to `~/`, re-verify. After normalizing paths inside a SHA256SUMS file, re-verify checksums with relative paths (`cd <dir> && shasum -a 256 <files> | shasum -a 256 -c -`), not the mutated manifest.
- **sum() over a set of bools lies.** `sum({a in x, b in x, c in x})` collapses duplicate True to 1 — use a list/tuple for counted assertions in evidence scripts. Caught only because the detail output was re-checked against a direct probe.
- **execute_code kernel terminal(): the kwarg is `timeout=`, not `timeout_s`** (the browser helper's name). A TypeError here wastes a whole call batch.
- **lcm.db telemetry is the baseline goldmine.** The `metadata` table holds `compaction_telemetry:<conversation_id>` JSON rows (total_compactions, last_compaction_duration_ms, peak/last prompt tokens, cache_read, cache_state) and `lcm_lifecycle_state` proves maintenance never fired (debt_size_estimate=0). Query these directly for CM-00-style baselines instead of estimating. Schema v5: `messages(store_id, session_id, role, content, token_estimate, tool_name...)`, `summary_nodes(node_id, depth, token_count, source_token_count)`.
- **Version discovery:** LCM plugin version = `git describe --tags` in `~/.hermes/profiles/uplift/plugins/hermes-lcm` (v0.20.0 @ 49e99a2); Mnemosyne from `plugins/mnemosyne/plugin.yaml` (v0.4.0). Neither is pip-installed; `pip show` fails.
- **sqlite backup of a live db:** `con.backup(dst)` (online backup API), then verify by reopening and counting rows. Plain `cp` risks a torn WAL copy.

## CM-10 corpus + harness pattern

Reusable pattern (details in `references/context-management-corpus.md`): 16 deterministic synthetic canaries covering every mission-doc corpus category, plus redacted real slices exported from `lcm.db` with extractive exact-identifier probes, scored by a stdlib-only harness (`cm10_harness.py`) that checks live pipeline primitives (raw-history survival, summary-not-sole-source, FTS recall, supersession, LOCAL_ONLY flags, backup integrity) with zero model calls. Non-observable dimensions are recorded as `unknown` — never fabricated as pass. Baseline established `CM10_BASELINE_PASS` with 0 critical losses / 0 privacy violations; later phases re-run the same harness and must not regress it.

## Mnemosyne programmatic drill API (verified 2026-09-01)

Do NOT import `hermes_tools` or `mnemosyne_memory` — neither module exists. The side venv (`PROFILE_HOME/.mnemosyne/venv/bin/python`, py3.12) exposes:
- `mnemosyne_hermes.MnemosyneMemoryProvider` — no constructor args; `initialize(session_id=...)` REQUIRES a session_id; then `is_available()`, `handle_tool_call("mnemosyne_remember"|"mnemosyne_recall", {args})`, `shutdown()`.
- `remember` returns `{"status": "stored", "memory_id": ...}`; recall output is a JSON string containing results.
- Required env: `HERMES_HOME=<profile>` and `FASTEMBED_CACHE_PATH=<profile>/.mnemosyne/fastembed-cache`. The first vector op fetches model files if not cached — with the durable profile cache set, also set `HF_HUB_OFFLINE=1`.

## Offline-proof technique (§9)

Initialize the provider FIRST (model load happens then), then swap `socket.socket` for a raising stub plus `HF_HUB_OFFLINE=1`/`TRANSFORMERS_OFFLINE=1`, then run remember+exact-recall. This produced `OFFLINE_PROOF_OK` — remember/recall work with all sockets blocked.

## lcm.db backup gotchas

- Use absolute paths in scripts: a relative `uplift/evidence/...` path failed with `unable to open database file` even though the directory existed (session cwd drift between commands).
- sqlite3 online backup API (`src.backup(dst)`) on a read-only URI source is WAL-safe; verify the restore by reopening the backup and counting rows (297 messages at time of run).
- Write backups under `uplift/evidence/` with a `phaseNN-` prefix so they belong to the state evidence list.

## uplift-state.json schema strictness

- `checkpoints[]` items allow ONLY: `id`, `kind` (enum: baseline|dogfood-A0|restart-A|router-B|authority-C|worker-D|promotion-E|upgrade-F|rollback), `git_ref`, `created_at`, optional `evidence[]`.
- Phase objects do NOT accept `completed_at`.
- `boundary_report.adoption_state` enum: `observed|staged|active|shadow|canary|production-approved|control-only` — note `active`, not `activated`.
- Run `tools/validate_state.py <state> <schema>` after EVERY mutation and fix on the first validation error rather than batching fixes.

## hermes-mnemosyne enablement

The wrapper plugin can be installed yet show "not enabled": `plugins.enabled` must list BOTH `"hermes-lcm"` and `"hermes-mnemosyne"`. Set via `HERMES_PROFILE=uplift hermes config set plugins.enabled '["hermes-lcm","hermes-mnemosyne"]'` and verify both report enabled.

## PII sweep before closing a phase

Grep new evidence for `/Users/<name>` paths, key fragments (`sk-...`), and emails; normalize absolute paths to `~/...`; re-run the state validator after touching evidence. (One absolute path slipped into `phase30-router-shadow-bench.json` and was caught exactly this way.)

## Phase 40/50 security qualification

macOS sbpl canonical-path pitfalls, the B4 structural probe matrix, and secret-detector regex lessons live in `references/b4-containment-and-egress.md` — load it before touching sandbox profiles or egress scanners. (That reference file was not present in the re-registered copy; if missing, it must be restored from the repo blueprint `references/execution-lessons.md` or prior evidence.)

## Compaction-drill carry-forward (known open item)

`summary_nodes=0` persists until the live session naturally crosses the compaction threshold (0.35 in `.env.lcm`). Do not force or fabricate it; the §8 drill + mandatory irrelevant-memory-injection test ride on the first natural compaction, and Phase 30E telemetry fields carry the measurement.
