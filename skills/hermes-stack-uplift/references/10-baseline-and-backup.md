# Phase 10 — Baseline, Backup and Optional Legacy Salvage

Use the single configured OpenRouter bootstrap model; do not introduce intelligent multi-model routing yet.

Snapshot current Hermes/Pi/profile configuration and preserve prior Hermes/LCM/Mnemosyne state as immutable evidence. Never attach or migrate an old database into the clean production profile.

Capture representative before-state telemetry: total/fresh/cached tokens, prompt/tool/skill/project-context contribution, TTFT/wall time, retries/tool errors, accepted-task quality, human intervention, provider continuity where observable, and workstation memory pressure. Do not optimize during baseline collection.

Create/check a rollback checkpoint and prove restore instructions are usable.

## Legacy-state decision

Legacy salvage is optional and defaults to `SKIPPED`. If historical knowledge is genuinely needed, follow `docs/agentic-uplift/research/legacy-state-curation.md`: immutable original, disposable copy, local discovery, selected prompts-first export, independent secret/typed-PII sanitization, separate raw/sanitized hashes, provenance-bearing extraction and adversarial current-truth reconciliation.

Sanitizer uncertainty or missing provenance means `BLOCKED`/`SKIPPED`, never cloud fallback. The clean uplift must work without salvaged context.

**Gate:** baseline is measurable, backup/checksum/restore evidence is durable, and any salvage is independently safe.

**Adoption:** baseline only; no optimization yet. Restart only if backup tooling required quiescing a component.

Persist evidence/state, send the required phase-boundary report, then stop before Phase 20.
