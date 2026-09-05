# Measurement-tail closeout lessons (CM closeout, verified 2026-09-02)

Session-specific detail from the CM measurement-tail closeout session (items 1-6).
Complements the main SKILL.md; the SKILL.md links here.

## Local billing telemetry: state.db `session_model_usage`

- Columns: session_id, model, billing_provider, task, api_call_count, input_tokens,
  output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens,
  estimated_cost_usd, cost_status ('estimated'), cost_source ('provider_models_api'),
  first_seen, last_seen.
- One row aggregates a whole session/task — per-TURN fresh vs cached split is UNKNOWN
  locally. Aggregate with GROUP BY session_id for mission totals.
- Verified closeout totals: 104 sessions, 6,262 calls, est $6.0789 vs OpenRouter actual
  $6.26296 (3.1% gap: estimator misses reasoning pricing + cache discounts).

## OpenRouter reconciliation (inference key)

- WORKS: `GET /api/v1/credits` (total_credits, total_usage USD) and
  `GET /api/v1/generation?id=<gen-id>` — per-request native_tokens_prompt /
  native_tokens_cached / native_tokens_completion / total_cost; stats lag ~5s after
  completion (retry at 5s then 15s).
- Verify per-generation recon with a live 1-token request ("usage":{"include":true});
  cost ~$0.0000012. Response `usage.prompt_tokens_details.cached_tokens` also present
  inline when usage.include=true.
- `GET /api/v1/activity` -> 403 with an inference key; needs a PROVISIONING key (operator
  must mint one in the OpenRouter dashboard).
- Generation ids (gen-XXXXXXXXXX-...) are NOT logged by Hermes anywhere (checked lcm.db
  messages, logs/agent.log, state.db, child stdout) — retroactive per-turn reconciliation
  is impossible; record UNKNOWN rather than proxy.
- Auth: read OPENROUTER_API_KEY from the profile .env; never print the value. Docs
  lookup: `urllib.request` with `User-Agent: Mozilla/5.0` against `.md` URLs listed in
  `https://openrouter.ai/docs/llms.txt` (analytics slug is /docs/api/api-reference/...).

## Multi-hop recall test recipe (3/3 verified)

1. CONTROL first: query the C-side term before planting — must be 0 results.
2. Plant three session-scope canaries, importance 0.6, nonce terms (A names codeword,
   B uses only the codeword, C uses only B's venue).
3. Hop queries carry ONLY the prior hop's distinctive term. Expected: top hit correct,
   first attempt, each hop. Note: ranking is FTS/keyword-driven; dense/vector score is
   0.0 on nonce terms — the chain depends on exact lexical match, not semantics.
4. Delete all canary ids after (mnemosyne_forget) and verify each delete returns.

## lcm.db backup/rotate integrity battery (copies only, never live)

1. Copy lcm.db (+ -wal/-shm if present) to a disposable dir; assert sha256 copy == live.
2. Battery: PRAGMA integrity_check, quick_check, foreign_key_check (0 violations),
   table counts (messages/metadata/summary_nodes), FTS canary smoke
   (`SELECT COUNT(*) FROM messages_fts WHERE messages_fts MATCH '<canary>'`).
3. Restore test: copy a real prior full-DB backup (e.g. cm/evidence/CM-00/backup/lcm.db.bak)
   and run the same battery; check all 16 LCM tables present.
4. Rotate code path: run the plugin's own suite from the plugin dir —
   `python -m pytest tests/test_lcm_rotate.py -q` (20 tests, all on tmp_path DBs, ~0.3s).
   No prior live /lcm rotate snapshot may exist — record restore-from-rotate-output as
   covered by backup restore test + suite, not as a live observation.
