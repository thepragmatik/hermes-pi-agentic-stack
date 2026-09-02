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

## Dogfood Gate A0 — use the first optimization before adding more subsystems

Do **not** immediately layer LCM/Mnemosyne and Spec Kit changes on top of an unproven prompt/skill diet.

After the context + skill diet is staged:

1. persist Phase 20 as `EXECUTING` and write evidence for the exact prompt/skill configuration;
2. checkpoint the pre-dogfood profile/configuration so rollback is trivial;
3. close the pre-slimming conversation and resume **Phase 20** in a fresh Hermes session using the slimmer T0/T1 + sliced-skill layout;
4. keep the same bootstrap model/gateway and do not introduce router authority or another unrelated variable;
5. run a small matched subset of the Phase 10 representative workload;
6. compare fixed/hot input, skill/tool-schema input, cached input, TTFT, accepted-task quality, wrong/missed skill loads and human intervention;
7. persist `phase20-dogfood-A0` evidence before continuing.

Continue to the LCM + Mnemosyne step only when the slimmer configuration shows non-inferior accepted-task quality and a measurable context/token improvement. If it regresses materially, roll back or repair the context/skill change **before** introducing the memory/context-engine baseline.

This is a **mid-phase dogfood gate**, not Phase 20 completion and not permission to start Phase 30. The point is to get an early benefit, isolate causality and make the next increment smaller.

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

Require non-inferior accepted-task quality, materially smaller hot context, initial >=30% lower skill-related input on skill-heavy representative missions, bounded T1 (normally <=8K), reliable exact recovery, low-noise durable recall, no unexpected context/memory network dependency, verified backups and acceptable host resource behaviour before production promotion.

Dogfood Gate A0 evidence must show that the prompt/skill improvement itself helped before LCM/Mnemosyne and Spec Kit were added. This preserves causal attribution and keeps the self-uplift incremental.

If a mandatory LCM/Mnemosyne gate fails, persist `BLOCKED`/`ROLLBACK`; do not silently switch memory architecture.

## Restart Checkpoint A — mandatory

After the full Phase 20 gate passes, persist Phase 20 complete and report:

> **The first token/context improvements are ready to use.**

Then **close the Phase-20 qualification session**. Phase 30 starts in a fresh Hermes session using the uplifted context/skill + LCM/Mnemosyne configuration. This prevents Phase-20 qualification context from contaminating router measurements.

Persist state/evidence, send the required phase-boundary report, and stop.
