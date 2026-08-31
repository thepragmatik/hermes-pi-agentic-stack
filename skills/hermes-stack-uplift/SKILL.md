---
name: hermes-stack-uplift
description: "Execute or review the staged 00-70 Hermes + Pi uplift using progressive disclosure, durable state, OpenRouter role routing, local LCM+Mnemosyne, external security controls, typed Pi delegation, restart checkpoints, evidence gates, and rollback."
---

# Hermes Stack Uplift

Use this skill for installing, uplifting, validating or upgrading the stack defined by this repository. Keep this parent file in context; load **only the current phase reference** unless a dependency explicitly requires another slice.

## Invariants

- Security/privacy decisions are deterministic and local before cloud/model/provider routing.
- `LOCAL_ONLY` never goes to OpenRouter or another cloud model.
- Before Phase 30 authority, bootstrap uses the configured single OpenRouter bootstrap model; do not invent optimized routing early.
- The local stack derives the mission profile, selects a bounded workflow/agent path, then selects an eligible model role/model. OpenRouter is the default downstream gateway and may choose a physical provider subject to hard requirements.
- LCM + Mnemosyne is the selected local context/memory baseline; memory is advisory, never execution/security authority.
- Steady-state orchestrator mode does not code directly; coding uses the typed Pi boundary after authority cutover.
- Durable state conforms to `protocols/uplift-state.schema.json`; conversation memory is not execution state.
- Every mutating phase has a rollback checkpoint and evidence gate.
- Every phase ends with persisted state/evidence + a human-visible progress report, then stops before the next phase.
- Do not weaken policy to make an upgrade, benchmark or test pass.

## Phase map

| Phase | Slice | Adoption boundary |
|---|---|---|
| 00 | `references/00-preflight.md` | manual foundation verified |
| 10 | `references/10-baseline-and-backup.md` | baseline/checkpoint durable |
| 20 | `references/20-context-and-skills.md` | **Checkpoint A: fresh optimized Hermes session** |
| 30 | `references/30-router.md` | **Checkpoint B: router shadow only** |
| 40 | `references/40-security-and-policy.md` | **Checkpoint C: security authority gate** |
| 50 | `references/50-pi-and-lsp.md` | **Checkpoint D: recreate disposable Pi workers** |
| 60 | `references/60-evaluation-and-promotion.md` | **Checkpoint E: multi-role promotion** |
| 70 | `references/70-upgrades-and-rollback.md` | **Checkpoint F: recurring canary/rollback cycle** |

At session/recovery start: read durable state, identify the current phase, load that slice, then load only evidence necessary to resolve its gates. If required state/evidence is missing, mark `BLOCKED` rather than guessing.

## Phase-boundary report

After every phase persist state/evidence first, then report:

```text
Phase completed:
What changed:
Evidence/gates passed:
Failures/warnings:
Token/context/cost impact observed:
Security impact:
What is now usable:
Does Hermes need a fresh session/restart?:
Does Pi need to be recreated/restarted?:
Remaining phases:
Next phase:
Human approval required before continuing?: yes/no
```

Do not begin the next phase in the same uninterrupted run.
