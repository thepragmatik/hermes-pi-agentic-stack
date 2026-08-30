# Phase 20 — Context, Skills and Local Context/Memory

**First self-improvement boundary.** This phase must make the uplift start paying for itself in reduced hot context while preserving accepted-task quality.

**Architecture decision:** LCM + Mnemosyne is the required clean-profile baseline. Diagnostic controls isolate regressions only; Hermes must not autonomously substitute another production context/memory architecture if the pair fails a mandatory gate.

## Context + skill diet

Apply `research/mission-context-architecture.md`:

```text
T0 = stable identity/invariants + small skill/tool catalogue
T1 = bounded current mission/phase capsule
T2 = logs/diffs/research/spec/evidence retrieved only when needed
```

Measure and remove duplicate hot prose, irrelevant skills/tool schemas and whole-document replay. Preserve stable prompt order and current provider/session affinity where it improves cache continuity. Use prompt/context instrumentation; do not infer savings.

Use the sliced `hermes-stack-uplift` design:

```text
small catalogue -> short parent SKILL.md -> one phase slice -> support artifact only on demand
```

A pruned reference is unloaded; reload it before relying on it. Measure catalogue/parent/support tokens, unnecessary loads, reloads, wrong/missed skill choice, cached input and accepted-task quality.

## LCM + Mnemosyne baseline

Follow `docs/agentic-uplift/local-context-memory-setup.md` and `research/local-context-memory-stack.md`.

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw host session history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = raw logs/diffs/results
Git/ADR/spec = project truth
```

Initial LCM research pin: stable v0.20.0, re-verified before install. Keep LCM semantic/proactive/temporal cross-session memory features off while Mnemosyne owns durable memory. Prove multiple compactions, exact drill-down, restart, integrity and backup.

Initial Mnemosyne research pins: core 3.15.1 + Hermes wrapper 0.5.0, re-verified. Use the local embeddings profile, `sync_roles: []`, strict curated writes, no remote/host LLM, no auto-sleep/persona/richer recall, no remote sync, bounded prefetch and the narrow tool allowlist checked into `configs/`. Built-in MEMORY/USER durable stores remain disabled so Mnemosyne is the single durable-memory provider.

Tool Search is mandatory to progressively disclose LCM/Mnemosyne non-core schemas.

After dependencies/model artifacts are provisioned, deny outbound network and prove LCM + Mnemosyne still compacts/recalls/writes/restarts/backups locally. Any remote fallback fails the phase.

## Spec Kit projection

Validate Micro/Patch, Lite, Standard and High-Assurance profiles. Generated specs are T2 durable artifacts; T1 receives only current requirement/acceptance/task slices. Risk policy may escalate assurance; the model cannot downgrade it.

## Acceptance

Require non-inferior accepted-task quality, materially smaller hot context, initial >=30% lower skill-related input on skill-heavy representative missions, bounded T1 (normally <=8K), reliable exact recovery, low-noise durable recall, no unexpected context/memory network dependency, verified backups and acceptable target-Mac resource behaviour before production promotion.

If a mandatory LCM/Mnemosyne gate fails, persist `BLOCKED`/`ROLLBACK`; do not silently switch memory architecture.

## Restart Checkpoint A — mandatory

After the gate passes, persist Phase 20 complete and report:

> **The first token/context improvements are ready to use.**

Then **close the pre-optimization session**. Phase 30 starts in a fresh Hermes session using the uplifted context/skill + LCM/Mnemosyne configuration. This prevents old pre-optimization chat context from contaminating later measurements.

Persist state/evidence, send the required phase-boundary report, and stop.
