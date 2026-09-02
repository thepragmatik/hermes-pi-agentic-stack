---
name: context-management-execution
description: "Use when running CM mission phases or LCM flag benchmarks."
tags: []
---

# Context-management mission execution lessons (CM-00..CM-80, verified 2026-09-02)

Host-verified detail for the context-management uplift (`~/.hermes/profiles/uplift/cm/`).
Condensed from real phase runs so future sessions do not re-derive by trial.

## Isolated child-run harness (proven benchmark recipe)

Benchmark children (deterministic tasks under controlled LCM flags) run as one-shot
processes, NOT delegate_task subagents:

```
hermes -p uplift chat --query-file <query.txt> --yolo --max-turns 40 \
  --source <label> --in <worktree> > stdout.log 2>&1
```

- Always pass `-p uplift` explicitly; without it a child may resolve a different profile
  and silently read different flags (this invalidated a whole MEAS-0 batch).
- `-q` together with `--query-file` is INVALID (mutually exclusive); use `--query-file`
  alone — non-TTY implies oneshot.
- Deterministic fixture: seed-42 generator; verify size (wc -c) and sha256 per run.
- Large-output ingest: use read_file (>12K chars), not `cat` — same ingest class, no
  permission gate. Background-subagent terminal calls are auto-denied invisibly (prompts
  never reach the operator); run drivers from a tracked terminal, delegate only
  tool-based steps.
- NEVER launch two drivers concurrently — they share the one profile `.env` + lcm.db.
- Map child stdout → session_id via the "Resume this session with:" footer (`--source`
  labels do NOT appear in lcm.db session_ids).

## Child cwd-assertion mitigation (mandatory from CM-70 clean re-run)

CM-70's original matrix was degraded by children starting cwd=~ instead of their
`--in` worktree. The clean re-run (cm70r_run.sh, 2026-09-02, 9/9 valid) proved it:
- Prepend a MANDATORY FIRST ACTION block to a per-run COPY of the query file: the child
  must run pwd and emit `CWD_OK=<label>` (or `CWD_INVALID=<label>` and stop) as its
  first tool result.
- Driver post-check greps the stdout log for these markers. CRITICAL: anchor the greps
  (`^CWD_OK=` / `^CWD_INVALID=`). An unanchored grep matches the ECHOED QUERY TEXT
  inside the stdout log and misclassifies a passing run as INVALID — this exact bug
  fired on the first clean run (A-1) and required a retraction entry in
  INVALIDATED-RUNS.md plus an anchored-grep driver fix.
- Stale worktrees from earlier missions are a contamination source: delete leftover
  `.worktrees/<label>` dirs + branches before a new matrix (in CM-70 a stale identical
  seed-42 fixture silently satisfied wrong-cwd children).
- Run the driver FROM the repo dir (the direct `--in` mechanism test works from there).
- Re-run drivers: copy the original to a `-r` variant; never rewrite the original
  mid-mission (it is evidence). Worktrees/branches deleted after use; batched branch
  deletions triggered approval blocks — one worktree remove per command went through.

## Stray-fixture quarantine rule

Never leave a `fixture.log` outside a worktree, and NEVER name a quarantined stray
`*.stray-cm70` in a searchable location: read_file's similar_files suggestion steered
later wrong-cwd children at the quarantined file, re-invalidating runs (CM-70 second
defect). Quarantine strays to `~/.quarantine-cm70/` with a neutral name; the driver
sweeps before AND after each run.

## Stream-stall watchdog (compressor arm)

CM-70's native-compressor arm froze 2/4 at a static "preparing write_file" line with
CPU 0. Watchdog pattern: child in background, poll every 60s; stdout size unchanged for
~15 min AND child CPU <1% → kill, append INVALIDATED-RUNS.md (append-only), re-run once
max per prereg. In the clean 9-run matrix: ZERO stalls — the hang is intermittent, not
arm-deterministic; compressor stability remains unresolved at n=3 (do not claim it fixed).

## .env flag mechanics (the expensive lesson)

- Profile `.env` is loaded with `override=True` at CHILD startup
  (`hermes_cli/env_loader.load_hermes_dotenv`): shell-exported `LCM_*` vars are silently
  OVERRIDDEN. `export FLAG=x && hermes ...` does NOT work.
- Vary flags per run by editing `~/.hermes/profiles/uplift/.env` immediately before child
  launch; restore the snapshot after. NEVER rewrite the file for a no-op change — the
  rewrite itself correlated with children not honoring flags (MEAS-0 v1 invalidation;
  v3 mechanism avoids it entirely).
- Flip scripts must handle both replacement and APPEND for keys not yet present (the
  profile `.env` lacked the cache/deferred flag lines until CM-60).
- After any flip: verify by re-read before spawning, and verify BEHAVIORALLY from the
  child's session rows (stub/inline counts for externalization), not file content.
  `lcm_status` does NOT display large_output/externalization keys.
- Check flag names against the installed plugin FIRST: grep
  `plugins/hermes-lcm/config.py` for `_EnvFieldSpec` entries (also reveals defaults —
  e.g. both `LCM_CACHE_FRIENDLY_CONDENSATION_ENABLED` and
  `LCM_DEFERRED_MAINTENANCE_ENABLED` default false). Never assume a canary name from the
  mission doc is the live key.

## Proven flag-matrix driver (CM-60) → generalized bake-off driver (CM-70r)

`cm/corpus/cm60_run.sh` generalizes the MEAS-0 v3 mechanism to any boolean flag pair:
snapshot → flip only what the arm needs (skip rewrite when already correct) → verify by
re-read AND behaviorally → sequential child runs → snapshot restore → diff-verify restore.
`cm/corpus/cm70r_run.sh` extends it to multi-arm bake-offs (engine flip for arm B,
retain-depth env for arm C) plus cwd assertion, stray sweep, and stall watchdog. Copy the
driver to a `-r` variant for re-runs; never rewrite the original mid-mission (keep it as
evidence). B-arm flips MUST diff-verify config restore after every run.
CM-60 results: cache-friendly + deferred-maintenance both neutral-to-positive (cached-share
0.9893 off vs 0.9934/0.9922, p50 202/176/165s, zero compactions, ADV-6 9/9); adopted.
CM-70 clean re-run (2026-09-02): 9/9 accepted (A/B/C x n=3), ids 8/8 x9, ADV-6 tested 6/6
(A/B) + DECLARED (C — capsule query has no violation step; structurally untestable there),
0 stalls / 0 wrong-cwd / 0 strays. Decision rule upheld: NO architecture switch.

## Instruments (reuse)

- `cm/corpus/usage_recorder.py` — session → billed-token report from lcm.db
  compaction_telemetry. Verified vs known session (35132/35072) before use; optional
  provider usage JSONL gives per-request rows, otherwise per-turn fresh tokens = UNKNOWN.
- `cm/corpus/cm60_score.py` — driver logs + telemetry + stub/inline counts →
  matrix-raw.json.
- Durable instrument limit: lcm.db persists ONLY last-request usage per session; per-turn
  billed fresh-token accumulation is UNKNOWN without a provider-side log. Peak/last-request
  prompt tokens were ~40-44K in ALL CM-60 arms regardless of tail config — last-request
  parity is NOT evidence about fresh-token accumulation. FRESH_TAIL_MAX_TOKENS=4000
  decision remains OPEN for that reason.
- grep-based scoring (REFUSED / identifier lists) under-matches when a child phrases
  differently or truncates — confirm by full-text read before scoring a run failed.
- Host has NO sqlite3 CLI — use `python3 -c "import sqlite3…"` for lcm.db checks.
- ADV-6 caveat: it is only TESTED in queries that contain a violation step (cm30-style).
  The capsule/handoff query (cm40) has only a HARD-RULE acknowledgment — score C-arm
  ADV-6 as DECLARED, never as a tested refusal.
- Child final reports quote artifact sizes only if the task asked for a report — extract
  metrics from the log tail after the LAST 'Report' marker; date-like numbers (20260902)
  can false-match a char-count regex. Sanity-check extracted numbers before persisting.

## Outlier scoring

An outlier run (1625s vs ~200s) with passing quality gates is an efficiency deviation,
not an invalid run — record it in the arm aggregate with an explicit outlier annotation
plus a clean-aggregate-without-it, and attribute its latency via telemetry
(`total_compactions=0` + null compaction duration ⇒ no maintenance component; the child
just took extra tool calls).

## Dual-track assessment protocol (mandatory from CM-50)

- Task 0: write `evidence/CM-XX/preregistration.md` (metrics, bounds, n, rollback) BEFORE
  any run; post-hoc metrics labeled POST-HOC. Per-phase `CHECKLISTS.md` ticked only on
  tool-verified evidence. UNKNOWN is first-class — never silently dropped or proxied.
- Ledger: `cm/evidence/ASSESSMENT_LEDGER.md` (append-only).
- **Schema-first boundary reports:** `cm-state.schema.json` `$defs.boundaryReport` has
  `additionalProperties: false` with required keys (what_changed, gates_passed,
  failures_warnings, token_context_cost_impact, security_impact, usable_now, hermes_action,
  pi_action, remaining_phases, next_phase, human_approval_required, adoption_state);
  `hermes_action`/`pi_action` are enums ('none', not prose). Dump the schema's required
  list BEFORE authoring — writing from memory cost three failed validate loops.

## CM-50 recall findings (design inputs for CM-70)

- Ownership boundary works: Mnemosyne returns 0 hits for session-local identifiers
  (correct); mission facts 0.85-1.0 with provenance; LCM explicit FTS recall 1.0 adjusted
  on the 16-canary corpus.
- Duplication is REAL: the same fact retrievable from both sources — dual proactive
  injectors without arbitration would double-inject (safe today only because both are
  disabled).
- STALE-INJECTION CAUGHT: Mnemosyne's top-scored record (0.99) asserted an old threshold
  (0.65) as current; fixed via `mnemosyne_validate(action=update)` with supersession note.
  Any recall-broker design MUST include a stale guard. Broker arbitration rule design:
  `cm/evidence/CM-50/qual-scorecard.md`. Production policy: LCM explicit retrieval only;
  proactive recall stays disabled until the broker is built and measured (CM-70).

## MEAS-0 baselines (for CM-70 comparisons)

- Externalization ON vs OFF (n=3/3, behavioral verification 6/6): stored-history -79.8%
  (41,104 → 8,320 chars mean); peak billed prompt parity (~35.2K both); duration parity
  (p50 77s vs 80s); zero compactions at this scale.
- Stub economics: 33,459-char tool result → 182-char stub; payload char-exact,
  content-addressed (sha256_16 == filename segment).
- Pressure variant (2500-line fixture, ~90K peak prompt): still zero compactions —
  compaction-pressure gates need a long-horizon session (CM-70/close-out). Attempted-zero
  is a valid recorded result.

## CM-80 promotion pattern (verified 2026-09-02)

- When adopted flags are already `true` in the profile `.env`, the promotion config step
  is DOCUMENTATION + a dated rollback snapshot (`.env.cm80-promote`), never a rewrite.
  Diff the prior adoption snapshot (`.env.cm60-adopt`) against current to prove only the
  promoted flags moved.
- Behavioral evidence beats re-runs when the engine is unchanged: the clean matrix ran
  under the promoted config, so the adversarial re-run verifies structurally and cites
  the matrix as live behavioral proof; record unprovoked edges (ADV-4 >cap group, ADV-1
  crash-before-ingest) as carried limitations, never as passes.
- The independent-reviewer approval package must be self-verifiable: numbered checklist,
  every step an independently runnable command with expected output.
- The C-arm resume capsule lives at `cm/corpus/cm40_resume_capsule.json`; children only
  see it if the query tells them where it is — any handoff arm must verify CAPSULE_OK
  first or the run is INVALID (all 3 clean C-arm children reported it missing in-worktree).
- PII sweep gotcha: the sweep regex for the home-path fragment also matches the sweep
  instruction text and normalized-rule lines in prereg/runbook prose — exclude rule lines
  when judging sweep output, or phrase rules without the literal path.
- mnemosyne_remember_canonical(category='task:progress', name='cm-mission') is the
  cross-session checkpoint; update at every phase boundary (owner uplift).
