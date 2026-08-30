---
name: hermes-stack-uplift
description: "Execute or review the staged Hermes + Pi stack uplift using progressive disclosure, durable state, external security controls, typed Pi delegation, evidence gates, and rollback checkpoints."
---

# Hermes Stack Uplift

Use this skill for installing, upgrading, validating or reviewing the stack defined by this repository. Keep this parent file in context; load **only the current phase reference** unless a dependency explicitly requires another slice.

## Invariants

- Security controls are external to prompts/skills.
- `LOCAL_ONLY` never goes to a cloud model.
- Orchestrator mode does not code directly; coding uses the typed Pi boundary.
- Durable state conforms to `protocols/uplift-state.schema.json`; conversation memory is not execution state.
- Every mutating phase has a rollback checkpoint and evidence gate.
- Do not weaken policy to make an upgrade, benchmark or test pass.

## Phase map

| Phase | Slice |
|---|---|
| 00 | `references/00-preflight.md` |
| 10 | `references/10-baseline-and-backup.md` |
| 20 | `references/20-context-and-skills.md` |
| 30 | `references/30-router.md` |
| 40 | `references/40-security-and-policy.md` |
| 50 | `references/50-pi-and-lsp.md` |
| 60 | `references/60-evaluation-and-promotion.md` |
| 70 | `references/70-upgrades-and-rollback.md` |

At session/recovery start: read durable state, identify current phase, load that slice, then load only evidence necessary to resolve its gates. If required state/evidence is missing, mark `BLOCKED` rather than guessing.
