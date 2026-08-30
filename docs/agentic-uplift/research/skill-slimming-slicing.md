# Skill Slimming / Skill Slicing for Hermes

## Decision

Adopt **progressive-disclosure skill slicing** as a first-class context-management mechanism. The goal is not to create hundreds of tiny skills. The goal is to keep the always-visible skill catalogue compact, keep each `SKILL.md` focused on routing/decision logic, and move phase-specific procedures, reference material, templates and scripts into support files loaded only when needed.

Hermes already has the primitives for this pattern: a compact skill catalogue plus on-demand skill viewing and support-file loading. The correct optimization is therefore mostly **information architecture**, not a new retrieval engine.

## First principles

Every token included in every turn has three costs: provider input cost, prefill/TTFT cost, and attention competition with task-relevant information. A skill that contains every procedure “just in case” pays all three costs on every use. Conversely, a catalogue of hundreds of micro-skills increases selection entropy and can cause the agent to load multiple overlapping skills.

The optimum is hierarchical:

```text
Level 0: tiny catalogue metadata
    -> Level 1: one broad class-level SKILL.md
        -> Level 2: one or two task/phase slices
            -> Level 3: concrete script/template only when execution needs it
```

## What to slice

Good slice boundaries correspond to **state transitions or capability changes**, not arbitrary document length. For this stack the natural slices are preflight, baseline/backup, context/skills, router, security/policy, Pi/LSP, evaluation/promotion, and upgrades/rollback. The files under `skills/hermes-stack-uplift/references/` implement this model.

Keep in the parent `SKILL.md` only: applicability, non-negotiable invariants, phase map, state-file rules, and how to load the next slice. Move commands, checklists, detailed failure handling and evidence requirements to the relevant slice.

## Anti-patterns

- **Micro-skill explosion:** one skill per command/tool. This bloats the catalogue and makes selection probabilistic.
- **Hidden policy:** security requirements only inside an optional skill slice. Security enforcement must exist outside the model; the parent skill should also repeat the invariant.
- **Slice ping-pong:** splitting mutually dependent instructions so the agent repeatedly reloads files. Co-locate instructions used in the same execution phase.
- **Monolithic support file:** replacing one huge `SKILL.md` with one huge `references/all.md` gains little.
- **Semantic duplication:** copying the same policy paragraphs into every slice creates cache churn and inconsistency.

## Measurement

Instrument skill-heavy sessions with: catalogue tokens, parent-skill tokens, support-file tokens, number of slice loads, unnecessary slice loads, reloads after compaction, cache-hit tokens, accepted-task success, and human corrections. Compare against the current unsliced baseline on the same mission set.

An initial experimental target is **>=30% lower skill-related input tokens** with non-inferior accepted-task quality. Do not promote slicing merely because token counts fall; a wrong or repeatedly reloaded slice can cost more than a compact monolith.

## Second-order effects

Slicing improves more than token spend. It lowers the probability that obsolete procedures remain salient after an upgrade, makes phase ownership auditable, and makes deterministic state recovery easier because the state file can point to the exact phase slice. The downside is a new failure class—missing or stale slice loading—so every slice needs a version/phase contract and the evaluator must test transitions, not only steady-state execution.

## Implementation rule

Treat the skill tree as **operational code**: version it, validate links/frontmatter, keep slices independently readable, add regression missions for selection, and fail closed if a required slice is missing. Never use a skill as the sole security boundary.

## Primary references

- Hermes documentation: https://hermes-agent.nousresearch.com/docs/reference/tools-reference/
- Hermes Curator: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
- Anthropic, agent skills progressive disclosure: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
