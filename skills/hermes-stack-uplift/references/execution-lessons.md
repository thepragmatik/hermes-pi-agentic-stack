# Execution lessons (host-verified, curated from hermes-stack-uplift-lessons)

Concrete, host-verified notes from the 2026-08-31 → 2026-09-01 uplift mission so
future sessions do not rediscover them by trial. Companion to the phase slices.

## macOS Seatbelt (sbpl) containment (Phase 50 B4)

- **Canonical-path trap:** macOS resolves `/tmp` and `/var` to
  `/private/tmp` and `/private/var`. A deny written as `(deny file-write*
  (subpath "/tmp/x"))` does not match a process opening `/private/tmp/x`
  (and vice versa). Always deny BOTH spellings; allow subpaths explicitly.
- Probe structurally, in the SAME profile used for the real mission: fs write
  outside allowlist → `PermissionError`; network → `gaierror`; credential read
  (e.g. `~/.ssh`) → `PermissionError`. A probe under a different profile proves
  nothing.
- Worker rejects out-of-worktree paths itself (belt) in addition to sbpl
  (suspenders); test both.

## Delegation-brief patterns (B5 parent-proxy architecture)

- The worker keeps `deny network*`; its ONLY route to the cloud model is an
  inherited fd-pipe to the bridge parent (`--model-proxy`). Do NOT weaken the
  sandbox deny to get direct egress — the parent-proxy IS the sanctioned path.
- API key lives only in the parent env; never forwarded to the worker; masked
  in evidence as sha256_16.
- Reasoning models can return null content if the output budget is too small —
  set `max_tokens` high enough (Phase 50 used 6000) before blaming the model.
- Scope the worker's test command (e.g. `pytest tests/test_x.py`), or pytest
  collects the whole repo suite from the worktree root and fails spuriously.
- Bounded retry: cap in-worker model retries; bridge replays duplicates
  idempotently on `task_id`+`idempotency_key` without relaunching a worker.

## B6 external-enforcement boundary (Phase 60)

- This Hermes version exposes **no permissions/hooks config keys**; in-process
  removal of generic tools is not structurally provable from inside a running
  Hermes. Record enforcement as EXTERNAL/operator-owned with exact repro
  commands; never claim orchestrator-level zero-trust.
- Bridge-level structural rejection (`reject_direct_edit`, Phase 70
  `--capability-mode`) is the provable layer. See
  `references/session-capability-modes.md`.

## uplift-state schema gotchas

- `checkpoints[]` items allow ONLY: `id`, `kind` (enum: baseline|dogfood-A0|
  restart-A|router-B|authority-C|worker-D|promotion-E|upgrade-F|rollback),
  `git_ref`, `created_at`, optional `evidence[]`.
- Phase objects do NOT accept `completed_at`.
- `boundary_report.adoption_state` enum: `observed|staged|active|shadow|canary|
  production-approved|control-only` — note `active`, not `activated`.
- Run `tools/validate_state.py <state> <schema>` after EVERY mutation; fix on
  the first validation error rather than batching.

## Evidence conventions (extracted to templates)

See `references/evidence-conventions.md` for the reusable PII-normalization,
hash-pinning and compact-evidence templates. Key traps:

- sqlite3 online backup (`src.backup(dst)`) on a read-only URI source is
  WAL-safe; verify restores by reopening the backup and counting rows.
- Use absolute paths in scripts when touching sqlite — session cwd drift
  caused a spurious "unable to open database file".
- For WAL databases copied without `-wal`/`-shm`, open with
  `mode=ro&immutable=1`; plain `mode=ro` fails with "unable to open database
  file".
- PII sweep before closing a phase: grep new evidence for `/Users/<name>`
  paths, `sk-` fragments, emails; normalize to `~/...`; re-run the state
  validator after touching evidence. (One absolute path slipped into
  `phase30-router-shadow-bench.json` and was caught exactly this way.)

## Mnemosyne programmatic drill API (verified 2026-09-01)

- Do NOT import `hermes_tools` or `mnemosyne_memory` — neither module exists.
  Use the side venv (`PROFILE_HOME/.mnemosyne/venv/bin/python`, py3.12):
  `mnemosyne_hermes.MnemosyneMemoryProvider` — no constructor args;
  `initialize(session_id=...)` REQUIRES a session_id.
- Required env: `HERMES_HOME=<profile>` and
  `FASTEMBED_CACHE_PATH=<profile>/.mnemosyne/fastembed-cache`; with the durable
  cache present also set `HF_HUB_OFFLINE=1`.
- Offline-proof technique (§9): initialize FIRST (model load happens then),
  then swap `socket.socket` for a raising stub + offline env vars, then run
  remember+exact-recall → `OFFLINE_PROOF_OK`.

## hermes-mnemosyne enablement

`plugins.enabled` must list BOTH `"hermes-lcm"` and `"hermes-mnemosyne"`:
`HERMES_PROFILE=uplift hermes config set plugins.enabled '["hermes-lcm","hermes-mnemosyne"]'`.

## Compaction-drill carry-forward

`summary_nodes` stays 0 until the live session naturally crosses the
compaction threshold (0.35 in `.env.lcm`). Do not force or fabricate it. First
natural compaction observed 2026-09-01 (summary_nodes=1 at Phase 60; 2 at
Phase 70) — the §8 drill is now actionable; harness steps are recorded in
Phase 70 evidence.
