---
name: hermes-stack-uplift-lessons
description: "Use when executing uplift phases 20C+ on this host."
---

# Hermes Stack Uplift — Host Execution Lessons

Companion to the `hermes-stack-uplift` skill (whose slice references cover the generic phase design). This file holds concrete, host-verified execution notes from real phase runs so future sessions do not rediscover them by trial.

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

macOS sbpl canonical-path pitfalls, the B4 structural probe matrix, and secret-detector regex lessons live in `references/b4-containment-and-egress.md` — load it before touching sandbox profiles or egress scanners.

## Compaction-drill carry-forward (known open item)

`summary_nodes=0` persists until the live session naturally crosses the compaction threshold (0.35 in `.env.lcm`). Do not force or fabricate it; the §8 drill + mandatory irrelevant-memory-injection test ride on the first natural compaction, and Phase 30E telemetry fields carry the measurement.
