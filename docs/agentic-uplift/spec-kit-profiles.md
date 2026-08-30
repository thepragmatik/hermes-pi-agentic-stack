# Token-Aware Spec Kit Profiles

## Problem statement

Spec Kit's default workflow is intentionally artifact-rich: specification, clarification, plan, research/design artifacts, tasks, consistency analysis, implementation and convergence. That rigor is valuable for ambiguous/high-risk work, but using the full flow for every mission creates two costs:

1. generation cost for artifacts that are disproportionate to the change;
2. repeated prompt/context cost when multiple artifacts are re-read by an agent loop.

Modern Spec Kit now supports **presets, template overrides and extensions**, which is the correct customization mechanism. Do not maintain a private fork of core templates if a preset can express the change.

## Core principle: rigor proportional to change risk

Choose the profile *deterministically before execution* using mission size, ambiguity, blast radius, data/security class and reversibility. The model may recommend a higher profile; it cannot downgrade a policy-required profile.

## Profile 0 — Micro / Patch

Use for:

- small bug with known reproduction;
- typo/config tweak;
- localized test fix;
- dependency pin with clear acceptance criteria;
- low-risk UI copy or style adjustment.

Artifact:

```markdown
# Change contract
Goal:
Non-goals:
Files/area:
Acceptance:
Risk:
Rollback:
```

Skip full `specify -> plan -> tasks` unless ambiguity emerges. The Pi task envelope can consume this contract directly.

Target artifact budget: roughly 0.5–1.5k tokens.

## Profile 1 — Lite Feature

Use for a bounded feature/change with modest cross-file impact.

Artifacts:

- compact `spec.md`: user behavior, requirements, non-goals, acceptance;
- compact `plan.md`: architecture delta, affected components, migrations, tests;
- inline task checklist or `tasks.md` only if parallel/multi-stage.

Optional clarify only if unresolved questions materially affect design. Skip broad research/data-model/contracts files when they do not apply.

Target generated artifact budget: ~2–5k tokens before implementation.

## Profile 2 — Standard SDD

Use for:

- new feature spanning components;
- meaningful API/data-model changes;
- brownfield refactor;
- mobile/web/backend coordinated change;
- nontrivial migration.

Run:

```text
specify -> clarify (if needed) -> plan -> tasks -> analyze -> implement -> converge
```

Use checklists selectively. Preserve durable architecture decisions as ADRs.

## Profile 3 — High Assurance / Regulated

Use for:

- auth/permissions/PII/security controls;
- payment/financial/regulated data;
- destructive migration;
- major architecture/platform change;
- agent policy/sandbox/credential changes;
- public API compatibility with large blast radius.

Use the full flow plus security/privacy threat model, rollback, explicit evidence matrix, reviewer separation and adversarial tests.

## Brownfield profile

For existing enterprise code, modify templates so plans begin with **impact discovery** rather than greenfield design:

- affected modules/services;
- existing tests and contracts;
- dependency graph/API consumers;
- database/schema compatibility;
- rollout/rollback;
- observability;
- backwards compatibility.

Avoid spending tokens re-documenting architecture already indexed in stable project docs.

## Preset architecture

Create organization-owned Spec Kit presets instead of editing core:

```text
.specify/
  presets/
    pragmatik-micro/
    pragmatik-lite/
    pragmatik-standard/
    pragmatik-high-assurance/
  templates/
    overrides/        # only universal overrides
  extensions.yml
```

The current Spec Kit preset resolver supports layered resolution/priority. Keep the presets in a separate versioned overlay repository or uplift directory and install them into projects during bootstrap.

## Artifact retrieval contract

Generated Markdown is **durable source material, not mandatory prompt material**.

At runtime create a compact feature index:

```yaml
feature: 042-bulk-import
profile: standard
spec: specs/042-bulk-import/spec.md
plan: specs/042-bulk-import/plan.md
tasks: specs/042-bulk-import/tasks.md
active_tasks: [T07, T08]
acceptance_sections: [FR-03, FR-08, PERF-02]
architecture_refs: [ADR-017]
```

A coding worker receives only:

- relevant acceptance requirements;
- its task section;
- architecture decisions referenced by that task;
- required contract/data-model slices.

Do not concatenate `spec.md + research.md + plan.md + data-model.md + contracts + tasks.md` into every Pi turn.

## Content-addressed/digest caching

For stable specs, calculate a digest. Include only `spec_digest` and compact acceptance block in the hot session prefix. When a task requests a section, retrieve it from disk by heading/ID. This gives traceability without repeated prefill.

## Constitution handling

Spec Kit now favors a single live constitution source and runtime resolution rather than copying constitution policy into every governed template. Follow that model. Keep the constitution concise and point security enforcement to actual policy files/tools rather than duplicating lengthy prose.

## Auto-profile selection

A deterministic scorer can choose a minimum profile:

```text
+2 security/privacy/auth change
+2 destructive/non-backward-compatible migration
+2 >2 services/platforms
+1 public API/schema change
+1 ambiguous requirements
+1 new external dependency/integration
+1 expected >2 engineer-days / many implementation tasks

0-1  -> Micro
2-3  -> Lite
4-5  -> Standard
6+   -> High Assurance
```

Add hard rules: e.g. auth/PII policy changes cannot be Micro even if small.

## Token-budget gate

Before implementation, estimate:

- static prompt/tool schema;
- active spec slices;
- expected requests/turns;
- expected tool output;
- output/reasoning budget.

If the spec artifact budget itself exceeds a configurable fraction of expected implementation input (start with 20–25%), require a compaction/indexing pass before coding.

## Analyze/checklist frequency

These gates are valuable but should be risk-driven:

- Micro: deterministic tests only.
- Lite: lightweight consistency check at handoff.
- Standard: `analyze` before implementation and `converge` after.
- High Assurance: analyze + domain checklist + adversarial review + converge.

## Experiment to quantify the Spec Kit penalty

Run 50–100 representative tasks through both the current full flow and selected profile. Measure:

- total input/output tokens;
- cached input share;
- time-to-first-accepted-patch;
- retries;
- escaped defects;
- reviewer interventions;
- artifact size;
- acceptance rate.

Only keep a lighter profile if quality is non-inferior. Token reduction alone is not success.
