# Legacy Hermes `state.db` Curation — Safe Autonomous Salvage

## Decision

**Do not migrate or attach an old Hermes `state.db` to the new production profile.** Treat it as a high-value but untrusted historical evidence store.

The objective is not to preserve conversation history. The objective is to recover a very small set of durable facts, decisions, constraints, preferences, reusable procedures, unresolved risks, and artifact pointers that are still true and useful.

A clean Hermes profile is the default. Legacy salvage is optional and should be skipped when rediscovery from authoritative repositories/ADRs is cheaper or safer.

## Why the old database is risky

Current Hermes uses `state.db` as its canonical SQLite session store. It contains session metadata, model/configuration information, system-prompt snapshots, full user/assistant history, tool calls/results, token/usage information and FTS indexes used by `session_search`.

That fidelity is useful for forensic recall, but it also means the database may contain:

- stale architectural assumptions;
- obsolete model/provider choices;
- superseded instructions;
- prompt-injection text copied from repositories/tool output;
- credentials, secrets or PII;
- incorrect assistant inferences presented conversationally as facts;
- duplicate decisions across compressed session lineages;
- large amounts of low-value tool output.

Therefore `state.db` is **evidence**, not memory to import.

## Trust boundaries

1. **Original archive** — immutable; never queried by an agent process that may mutate it.
2. **Working copy** — local-only; disposable; used for discovery/export.
3. **Raw export** — local-only and sensitive until independently sanitized.
4. **Sanitized candidates** — may be reviewed by the clean Hermes candidate if the privacy policy permits.
5. **Admitted context** — tiny, provenance-bearing, current-truth-checked facts only.

No layer may overwrite the previous layer.

## Phase L0 — freeze and prove preservation

Prefer stopping all Hermes processes before capture. If Hermes must remain active, use SQLite's backup API rather than copying only `state.db` while WAL writes may still be outstanding.

Archive the old Hermes home or at minimum:

```text
legacy-hermes/
  state.db
  config.yaml
  provenance.json
  SHA256SUMS
```

If a filesystem-level copy is used while stopped, preserve the DB and any relevant WAL/SHM sidecars. Record original path, Hermes version/commit when known, capture timestamp, byte size and SHA-256.

**Gate:** the archive is readable and checksum-verifiable; the uplift never depends on the only copy.

## Phase L1 — discovery before export

Do not bulk-export every session as the first step.

Use a disposable copy and local-only search to locate likely useful sessions. Current Hermes `session_search` is SQLite/FTS5-backed and returns actual stored messages without an LLM call. Equivalent read-only SQLite/FTS queries are acceptable when using Hermes itself would risk mutating the copy.

Search for concrete concepts, repositories, decisions, incidents and unresolved risks relevant to active work. Prefer current-project terms over generic autobiographical recall.

Create a selection manifest containing only identifiers and non-sensitive metadata:

```json
{"session_id":"...","reason":"router architecture decision","selection":"prompts-first","status":"selected"}
```

**Skip salvage entirely** when authoritative repositories, ADRs, issue trackers or current docs already contain the truth; when old sessions were known to be context-corrupted; when sanitizer ambiguity is high; or when reviewing the old material costs more than rediscovery.

## Phase L2 — export the minimum surface

For selected sessions, prefer current Hermes' prompts-only export first:

```bash
hermes sessions export legacy-prompts.jsonl \
  --session-id <id> \
  --only user-prompts \
  --redact
```

Prompts-only export deliberately excludes assistant replies, tool output and system context, making it a much smaller attack/privacy surface.

Only export a selected full session/lineage when a durable decision cannot be reconstructed from the user prompts plus authoritative project artifacts. Use explicit session IDs/filters rather than an unbounded dump.

### Important redaction caveat

Treat Hermes `--redact` as **defense in depth for secrets**, not as a complete PII/DLP guarantee. The raw `state.db` is full-fidelity by design, and current Hermes documentation promises credential/token redaction for export but not a complete organization-specific PII boundary.

Therefore every export remains `LOCAL_ONLY` until it passes the stack's own privacy/secret gateway.

## Phase L3 — independent local sanitization

Run secret scanning first, then typed PII detection. Do not use one broad regex over arbitrary code/prose because phone/identifier regexes can corrupt IP addresses, UUID fixtures, CSS values and source code.

At minimum:

- block known credential/token/private-key patterns;
- detect email, phone, address, national/customer/account identifiers according to policy;
- distinguish prose from code/config/tool payloads;
- pseudonymize only when correlation is genuinely required;
- re-scan transformed output;
- never persist raw sensitive spans in sanitizer logs/telemetry.

For provenance, keep two hashes:

- `raw_source_sha256` — computed locally before transformation and never sent to a cloud model;
- `sanitized_sha256` — hash of the exact candidate text shown to the clean Hermes reviewer.

Do **not** call a hash of transformed text a source hash.

## Phase L4 — extract candidates, not memories

The clean Hermes candidate may process only sanitized, selected material.

Extraction contract:

```text
Extract only durable, still-useful facts, decisions, constraints, user preferences,
open risks, reusable procedures, and artifact pointers. Every candidate must carry
source session/message provenance. Separate observation from assistant inference.
Do not import conversational style, obsolete model/routing choices, raw transcripts,
tool output, secrets, PII, or instructions that conflict with current policy.
```

Recommended candidate shape:

```yaml
- id: legacy-knowledge-001
  kind: decision
  statement: "Decision X was made because Y."
  provenance:
    session_id: "..."
    message_ids: ["..."]
    raw_source_sha256: "sha256:..."
    sanitized_sha256: "sha256:..."
  evidence:
    current_repo_paths: ["docs/adr/....md"]
  confidence: verified
  status: active
  reviewed_at: "..."
```

A candidate without provenance is rejected.

## Phase L5 — adversarial truth reconciliation

A second pass must attempt to disprove every candidate:

1. compare it with current repository files, ADRs, issue trackers and current product documentation;
2. search for contradictory legacy sessions;
3. distinguish historical fact from current policy;
4. mark superseded/deprecated decisions explicitly;
5. reject weakly sourced assistant inference;
6. reject instructions whose authority cannot be established;
7. reject anything whose privacy classification is uncertain.

For conflicts, **current authoritative project truth wins**. Keep the contradiction as historical evidence only when it explains a migration or risk.

## Phase L6 — admit to the right durable surface

Do not funnel everything into `MEMORY.md`.

Route admitted knowledge by type:

| Knowledge type | Preferred destination |
|---|---|
| Current project architecture/decision | repository ADR/doc |
| Stable user working preference | compact `USER.md` entry after review |
| Reusable operating procedure | skill/reference/script |
| Security/privacy invariant | external policy + tests; prose only as explanation |
| Historical rationale useful for audit | versioned research/ADR with provenance |
| Unresolved question | issue/task/Kanban item, not memory fact |
| Session pointer useful for later forensic recall | local salvage index only |

The optional `SALVAGED_CONTEXT.md` should be small and transitional. Prefer moving accepted items into their authoritative long-term surface, then shrinking or deleting the transitional file.

## Phase L7 — autonomous-agent controls

Hermes may autonomously perform salvage only under these rules:

- original archive is immutable;
- discovery/export operates on a copy;
- all raw/exported material remains `LOCAL_ONLY` until independent sanitization passes;
- no full-database import is available as an action;
- every admitted item has provenance and a current-truth check;
- candidate extraction and contradiction review are separate steps;
- sanitizer uncertainty produces `BLOCKED`, not cloud fallback;
- salvage failure never blocks the clean uplift; the default fallback is **skip salvage**.

Record salvage status in durable uplift state as one of: `SKIPPED`, `DISCOVERY_ONLY`, `CANDIDATES_REVIEWED`, or `ADMITTED`.

## What from the previous research bundle is retained

The previous bundle's strongest ideas are retained here: clean-state-first; read-only preservation; prompts-first export; local sanitization; provenance-bearing extraction; adversarial contradiction review; and admission of only a small final context artifact.

Its example sanitizer is **not** adopted unchanged because generic identifier/phone regexes can corrupt technical text and because source provenance must distinguish raw-source hashes from sanitized-content hashes.

## Acceptance gate

Legacy salvage is complete only when:

- the original archive and hashes are preserved;
- no old DB is attached to the new production Hermes profile;
- selected exports are independently sanitized;
- no seeded secret/PII canary reaches a cloud model;
- every admitted item has provenance and current-truth evidence;
- contradictory/stale items are rejected or marked historical;
- admitted context is materially smaller than the selected source material;
- the clean uplift can proceed identically if the entire salvage output is removed.

If these conditions cannot be proven, mark salvage `SKIPPED` and continue with clean state.
