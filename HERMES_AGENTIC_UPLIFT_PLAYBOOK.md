# Hermes + Pi Agentic Stack — Control Playbook

Snapshot: 2026-08-30

This is the compact control document for a local-first, high-throughput agentic software-development stack using **NousResearch/hermes-agent** as the control-plane orchestrator and **earendil-works/pi** as the isolated coding-worker harness.

Detailed research and execution material is deliberately split under `docs/agentic-uplift/` and `skills/hermes-stack-uplift/` so Hermes does not ingest tens of thousands of tokens on every mission.

## Mission

Build a production workflow on Apple Silicon that:

- keeps Hermes as the single mission entry point and durable orchestrator;
- routes research/synthesis to the qualified research specialist and coding/tool work to the qualified coding specialist;
- keeps the always-on local router small;
- delegates coding through a typed Hermes -> Pi boundary;
- enforces filesystem/process/network/credential/PII/secret/merge policy outside prompts;
- uses LSP selectively for code intelligence without workspace context floods;
- minimizes repeated prompt/spec/tool-schema prefill while preserving quality;
- uses mission-sensitive Spec Kit profiles;
- survives Hermes/Pi upgrades through canary qualification and rollback;
- measures accepted-task quality, latency, retries, cache behavior, human intervention and spend before promotion.

## Execution authority

The desired steady state is zero-trust-ish at the agent boundary: the production Hermes orchestrator has no arbitrary shell/source-write authority and coding crosses the typed Pi path.

That state cannot exist before Hermes builds the Pi/enforcement path. Therefore the uplift uses an explicit **trusted bootstrap authority**:

1. current Hermes may temporarily write/run shell only inside a constrained canary/overlay/worktree scope;
2. it builds the external policy/privacy/sandbox substrate;
3. it builds and tests the Pi bridge offline/local-first;
4. it proves a privacy-controlled Pi cloud canary;
5. only then does it revoke direct coding/shell capability from production Hermes;
6. an instruction to “skip Pi and edit directly” must thereafter fail structurally.

See `docs/agentic-uplift/bootstrap-authority.md` and `docs/agentic-uplift/agent-execution-contract.md`.

## Architecture

Use four routing/control layers:

1. **Tier 0 — deterministic security/privacy + state gate.** Resolve non-negotiable trust constraints and obvious operational state.
2. **Tier 1 — compact semantic classifier.** Benchmark Qwen3-Embedding-0.6B and frozen ModernBERT Embed challengers with a calibrated lightweight head.
3. **Tier 2 — confidence/hysteresis/abstention.** Route phases rather than micro-turns; optional RouteLLM-style difficulty escalation is separate.
4. **Tier 3 — specialist execution.** Pin provider/model/account within the phase/session to preserve cache affinity.

Security policy stays outside the learned classifier.

Do not keep a 20B–100B+ generative model permanently resident merely to classify mission intent on a 128 GB developer workstation.

## ModernBERT progression

Do **not** start by fine-tuning ModernBERT.

Benchmark this progression:

```text
rules
-> rules + structured agent state
-> Qwen3 embedding prototype
-> frozen nomic ModernBERT Embed 256d/768d + calibrated linear/logistic head
-> fine-tuned ModernBERT-base only after the frozen baseline plateaus
-> optional pairwise difficulty/escalation model
```

Explicit state features include current phase/lane, write request, failing tests, pending tool action, active worker, repo state, research requirement, privacy class and recent route switches.

Primary promotion metrics are accepted-task utility/regret, high-severity wrong-lane errors, retries/human overrides, route-switch rate, cache continuity, time/cost per accepted task and then classification/calibration metrics.

See `docs/agentic-uplift/research/router-training-control.md`.

## Context and token architecture

Preserve current Hermes prompt assembly/compression. Apply three operational temperatures:

- **T0 stable prefix** — identity, small invariants, stable role/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded current objective/phase/constraints/acceptance/routing/evidence pointers, changed only at meaningful phase boundaries;
- **T2 artifact memory** — full logs/diffs/Pi RPC streams/benchmarks/research/large Spec Kit artifacts kept outside hot context and retrieved by slice.

Do not mirror the same mission state, command output or worker transcript into chat, MEMORY, project context and artifacts simultaneously.

Use current Hermes compression/`session_search` as recovery machinery; after restart/compaction, reload durable uplift state, regenerate T1, load the current skill slice and fetch only unresolved T2 evidence.

See:

- `docs/agentic-uplift/research/mission-context-architecture.md`
- `docs/agentic-uplift/research/context-token-optimization.md`
- `docs/agentic-uplift/research/skill-slimming-slicing.md`

## Skill slicing

Treat skills as progressive disclosure:

1. profile/catalog metadata routes to an eligible skill;
2. `SKILL.md` contains only invariants and phase map;
3. current phase details live in one `references/` slice;
4. deterministic mechanics belong in scripts/templates;
5. large evidence remains external until needed.

The repository includes `skills/hermes-stack-uplift/` with eight phase slices.

More micro-skills are not automatically better. Excess catalog entries increase selection cost and inconsistency. Slice by stable phase/concern boundaries and measure tokens per accepted task.

## Legacy Hermes `state.db`

The old database is historical evidence, not memory to transplant.

Current Hermes `state.db` is full-fidelity session storage used for resume/search, so it can contain stale decisions, raw tool output, secrets/PII and old model assumptions.

Default legacy status is **SKIPPED**. If active work genuinely needs historical context:

1. freeze/checksum the original old home/DB;
2. operate only on a disposable copy;
3. discover relevant sessions locally before export;
4. prefer selected prompts-only export first;
5. treat Hermes `--redact` as secret-scrubbing defense in depth, not complete PII/DLP;
6. independently sanitize locally;
7. extract only durable provenance-bearing candidates;
8. adversarially compare them with current repository truth;
9. admit facts to the correct durable surface—not a bulk MEMORY transcript.

The clean uplift must work identically without salvaged context.

See `docs/agentic-uplift/research/legacy-state-curation.md`.

## Memory posture

Baseline memory is deliberately simple:

- built-in `MEMORY.md` / `USER.md` for compact reviewed durable state;
- local `session_search` for historical recall;
- project ADR/docs for project truth.

Do not turn on another memory provider during the baseline just because it is available. Holographic memory is a later local canary if baseline recall proves insufficient; start with `auto_extract: false` and measure added schema/context cost, stale-fact risk and retrieval quality before promotion.

## Hermes built-ins

Two current built-ins are useful without becoming security authority:

- **`security-guidance` WARN mode** — cheap pattern-based defense in depth for Hermes-owned write/patch content; not a sandbox/DLP/Pi diff reviewer.
- **Kanban** — optional durable mission ledger/human UI for blocked/review/retry state. `uplift-state` remains authoritative execution/security state; Kanban is a projection.

Keep unnecessary toolsets out of ordinary profile schemas.

## Zero-trust Pi invariant

Pi has no built-in filesystem/process/network/credential permission system. Final worker authority therefore requires external containment.

Each coding task must use:

- validated v2 task envelope + policy digest;
- fixed role -> capability mapping;
- isolated git worktree;
- minimal environment/credential exposure;
- external sandbox/container/micro-VM/capability broker;
- network default deny/allowlist;
- local secret + typed-PII egress checks;
- bounded retry/idempotency semantics;
- deterministic test/LSP/security evidence;
- independent review/merge gate.

Pi RPC remains a local pipe. Treat `agent_settled` as fully settled completion; `agent_end` may still be followed by retry/compaction/queued continuation.

## Spec Kit

Use deterministic profiles:

- **Micro/Patch** — localized low-risk change;
- **Lite** — bounded feature;
- **Standard** — cross-component feature/refactor;
- **High Assurance** — security/auth/PII/destructive migration/large blast radius.

Policy may escalate; a model cannot downgrade a required high-assurance profile.

Generated Markdown is durable source material, not mandatory hot context. Index and retrieve only current acceptance/plan/task slices.

## Autonomous execution order

Canonical detail is `docs/agentic-uplift/implementation-playbook.md`. High-level order:

1. preflight/inventory;
2. freeze/backup and optional legacy-state curation;
3. clean parallel Hermes candidate + bootstrap checkpoint;
4. context/skill/T0-T1-T2 diet;
5. router shadow evaluation;
6. provider/model bake-off;
7. external security/privacy/enforcement substrate;
8. minimal Pi bridge offline/local-first + containment qualification;
9. privacy-controlled Pi cloud canary + LSP;
10. **authority cutover** — revoke direct production Hermes coding/shell capability;
11. Spec Kit mission profiles;
12. bounded task graph + optional Kanban projection;
13. adversarial suite;
14. canary comparison and gradual promotion;
15. continuous Hermes/Pi canary-upgrade discipline.

This order intentionally builds enforcement **before** cloud Pi authority while retaining only the minimum temporary bootstrap capability needed to construct the replacement path.

## Acceptance gates

Before production promotion:

- old production/legacy archive remains recoverable;
- no old DB is migrated into clean production;
- fixed/hot context shrinks without accepted-task quality regression;
- routing beats fixed/state baselines on held-out mission-level outcomes;
- no observed `LOCAL_ONLY -> cloud` path exists;
- external Pi containment structurally denies disallowed filesystem/network/credential actions;
- every coding task crosses the typed Pi boundary after cutover;
- direct Hermes bypass after cutover fails structurally;
- seeded secrets/PII fail closed and sanitizer does not corrupt common technical fixtures;
- required test/LSP/security evidence is represented in task results;
- lighter Spec Kit profiles materially reduce eligible-task input tokens without quality regression;
- representative Mac memory pressure/swap remains acceptable;
- daily upstream canary qualification does not overwrite uplift-owned controls;
- rollback to the previous pins/overlay is documented and rehearsed;
- accepted-task quality is non-inferior within the chosen confidence interval.

## Economics

Planning baseline: **3,888,531,773 logical tokens/month**.

Treat savings as measured outcomes, not promises. A sensible initial architecture target remains roughly **25–50% logical-token reduction** from prompt/spec/tool/context optimization plus materially higher cached-input share on long sequential work.

Optimize **cost + minutes + retries + human intervention per accepted task**, not token price in isolation.

## Upgrade discipline

This repository is an overlay/control repository, not a permanent fork of Hermes or Pi.

For every upstream update:

1. install/update a disposable canary;
2. apply pinned uplift overlay/integration;
3. run protocol/security/router/context/LSP/coding smoke tests;
4. compare prompt/cache/accepted-task metrics with prior pins;
5. inspect plugin/package changes;
6. promote only on pass;
7. otherwise keep previous pins and record an integration blocker.

Never upgrade production first and qualify second.

## Self-uplift mission

Give Hermes this mission from the constrained bootstrap/canary profile:

> Implement the agentic uplift defined by this repository using the durable execution contract and sliced uplift skill. Treat each phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable state transition. During trusted bootstrap, use direct coding/shell capability only within the explicitly allowed canary/overlay/worktree scope; after the Pi/enforcement path passes its canary, revoke those capabilities from the production orchestrator and use typed Pi delegation for coding. Preserve upstream upgradeability, keep old `state.db` as read-only evidence rather than migrated memory, collect deterministic evidence for every gate, and mark a phase `BLOCKED` or `ROLLBACK` rather than weakening a security/privacy boundary. Verify assumptions against the installed Hermes/Pi versions before implementation.

## Canonical index

Start with:

- `docs/agentic-uplift/implementation-playbook.md`
- `docs/agentic-uplift/agent-execution-contract.md`
- `docs/agentic-uplift/bootstrap-authority.md`
- `skills/hermes-stack-uplift/SKILL.md`
- `docs/agentic-uplift/artifact-usability-review.md`
- `docs/agentic-uplift/adversarial-review.md`
- `docs/agentic-uplift/research/legacy-state-curation.md`
- `docs/agentic-uplift/research/router-training-control.md`
- `docs/agentic-uplift/research/mission-context-architecture.md`
- `docs/agentic-uplift/research/security-zero-trust-pii.md`
- `docs/agentic-uplift/research/hermes-pi-lsp.md`

Keep this root document compact. Put detailed changing research in canonical topic documents and load it only when needed.
