# Evidence conventions — reusable templates

Conventions proven across uplift Phases 00–70, extracted so future missions
apply them without re-deriving. All paths below are relative to the profile's
`uplift/` directory unless noted.

## 1. PII normalization (SOUL.md hygiene, enforced)

- No absolute home paths in any persisted artifact: `/Users/<name>/...` → `~/...`
- No raw secrets, API keys, tokens, or raw prompts/transcripts in evidence.
- Grep sweep before closing a phase:

```bash
grep -rnE '/Users/[a-z]+|sk-[A-Za-z0-9]{8}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' \
  "$PROFILE_HOME/uplift/evidence" --include='phaseNN-*'
```

- Sweep result is recorded as a gate ("PII sweep clean"), never assumed.

## 2. Hash-pinning template

Pin every artifact that rollback or promotion depends on:

```json
{
  "artifact": "evidence/phaseNN-config-post.yaml",
  "sha256": "<64 hex>",
  "sha256_16": "<first 16 hex, for logs where full hash is too chatty>",
  "pinned_at": "<ISO8601 offset>"
}
```

Rules:
- `policy_sha256` in `uplift-state.json` must equal
  `sha256(configs/policy.example.yaml)` — verify every phase that touches policy.
- Model/provider pins are exact IDs (`z-ai/glm-5.3-flash`), never aliases
  (`latest`) — record the pin in run evidence, not just config.
- Worker diffs: store `diff_sha256`, not the diff body, when the body may carry
  unsanitized content; the egress-scanned payload stays in the evidence dir.

## 3. Compact+hashed evidence template

Evidence files are compact, structured, and self-describing:

```json
{
  "phase": "NN-slice-name",
  "what": "<one-line description>",
  "inputs": {"fixture_sha256": "<64 hex>"},
  "results": {"gate_name": {"pass": true, "metric": 0.0}},
  "notes": ["honest nulls live here: metric unmeasurable -> null, never estimated"]
}
```

Rules:
- Raw model/proxy response bodies are NEVER mirrored into evidence; store
  counts, hashes, event names, timings.
- Synthetic fixtures carry obvious markers (`FAKE_`, `«redacted:…»`,
  `f@example.invalid`) so a leaked fixture is identifiable as non-real.
- Every gate claim in a boundary report cites an evidence path — prose is not
  evidence.

## 4. Honest nulls template

```json
{
  "tokens_in": null,
  "tokens_out": null,
  "tokens_note": "not observable for local deterministic probes; null recorded, not estimated"
}
```

A gate that cannot be measured is recorded `null` with the reason, or the phase
records a documented handoff — never a fabricated number, never a silent skip.

## 5. Rollback-artifact naming

```
evidence/phaseNN-<thing>-pre.yaml        # pre-mutation snapshot + sha256
evidence/phaseNN-<thing>-post.yaml.sha   # post-mutation pin
evidence/phaseNN-rollback-runbook.md     # exact restore commands
checkpoints/phaseNN-checkpoint.json      # schema-valid checkpoint record
```

Restore proof = restore into a disposable copy and diff against the snapshot
(see `tools/phase70/rollback_drill.py`); never "prove" by editing the live
profile back and calling it identical.
