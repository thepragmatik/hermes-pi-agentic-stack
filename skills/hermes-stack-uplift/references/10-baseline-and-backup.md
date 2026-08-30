# Phase 10 — Baseline, Backup and Optional Legacy Salvage

Snapshot current Hermes/Pi installs and configuration. Preserve the previous Hermes home and `state.db` as immutable evidence; never attach or migrate the old database into the clean production profile.

Capture representative mission telemetry: prompt/input/output/cache tokens, TTFT, retries, tool errors, accepted-task success, human intervention and workstation memory pressure. Create a rollback tag/checkpoint.

## Legacy-state decision

Legacy salvage is **optional**. Default to `SKIPPED` when current repositories/ADRs already contain the truth, old sessions are known to be noisy/context-corrupted, privacy sanitization is ambiguous, or rediscovery is cheaper than curation.

If historical context is genuinely valuable, follow `docs/agentic-uplift/research/legacy-state-curation.md`:

1. freeze and checksum the original old Hermes state;
2. work only from a disposable copy;
3. discover relevant sessions locally before export;
4. prefer selected `--only user-prompts` exports first;
5. treat Hermes `--redact` as secret-scrubbing defense in depth, not a complete PII boundary;
6. independently scan/sanitize locally before a clean Hermes agent sees candidate content;
7. extract only durable facts/decisions/preferences/risks/procedures with provenance;
8. adversarially compare every candidate to current authoritative project truth;
9. admit accepted knowledge to the correct durable surface (ADR/doc, compact `USER.md`, skill/script, issue), not a bulk `MEMORY.md` dump.

Sanitizer uncertainty or missing provenance produces `BLOCKED` or `SKIPPED`; it never triggers cloud fallback. The uplift must remain fully operable with no salvaged context.

Evidence: backup/archive location, SHA-256 manifest, baseline metrics, rollback rehearsal, salvage status (`SKIPPED`, `DISCOVERY_ONLY`, `CANDIDATES_REVIEWED`, or `ADMITTED`), selection manifest if used, sanitizer evidence, and provenance/truth-check records for every admitted item.
