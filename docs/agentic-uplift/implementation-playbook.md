# Self-Uplift Implementation Playbook for Hermes

Snapshot: 2026-08-30.

This is the **single canonical execution lifecycle** for Hermes to uplift its own stack. It deliberately uses the same `00 -> 70` phase IDs as `skills/hermes-stack-uplift/` and `protocols/uplift-state.schema.json`.

There is no second hidden `00 -> 140` lifecycle. Detailed research is supporting evidence, not another phase system.

Use together with:

- `UPLIFT_MISSION.md` — one-command staged mission launcher;
- `docs/agentic-uplift/fresh-install-bootstrap.md` — human foundation before Hermes begins;
- `docs/agentic-uplift/agent-execution-contract.md` — durable authority/state/evidence rules;
- `docs/agentic-uplift/bootstrap-authority.md` — temporary root-of-trust transition;
- `skills/hermes-stack-uplift/SKILL.md` — progressive-disclosure phase map;
- `protocols/uplift-state.schema.json` — machine-readable mission state;
- `docs/agentic-uplift/research/openrouter-routing.md` — gateway/model/provider ownership;
- `docs/agentic-uplift/local-context-memory-setup.md` — fixed LCM + Mnemosyne baseline.

The chat transcript is not execution state.

---

# Operating model

## Iterative self-improvement, not one giant session

Every phase follows the same loop:

```text
bounded change
  -> deterministic + representative tests
  -> adversarial challenge
  -> compare with baseline
  -> persist evidence/state
  -> checkpoint
  -> phase report to human
  -> fresh session/reload/recreate if beneficial
  -> only then next phase
```

A phase may be autonomous internally, but Hermes **returns control at every phase boundary**. Do not carry one enormous pre-optimization conversation through the entire uplift.

When a phase contains multiple meaningful subsystems, use a smaller **mid-phase dogfood gate** before layering the next subsystem whenever that gives a clean causal measurement. Such a gate keeps the same phase `EXECUTING`, persists evidence/checkpoint state, and may resume the same phase in a fresh session. A regression is repaired/rolled back before the next subsystem is introduced.

## Routing ownership

```text
mission
  -> Tier 0 deterministic local privacy/security/policy
  -> Tier 1 local mission router
  -> model-role binding
  -> OpenRouter model ID
  -> OpenRouter physical provider
```

Privacy/security decisions never move downstream into OpenRouter. OpenRouter Auto is a bounded bootstrap/shadow/fallback experiment, not the final mission router.

## Bootstrap Mode

Before Phase 30 has a qualified router, use one configured OpenRouter bootstrap model for ordinary non-`LOCAL_ONLY` uplift work. Research snapshot candidate: GLM-5.3-Flash-class. The exact current model ID is selected through the installed Hermes `model` picker and recorded in evidence rather than hard-coded as timeless truth.

Preferred initial external inference credential footprint is only `OPENROUTER_API_KEY`. Direct provider keys are added only after later matched-task evidence justifies their extra attack/operational surface.

## Non-negotiable rules

1. Work in a clean profile/canary/worktree/overlay; never mutate the only running production installation first.
2. A Hermes profile and `terminal.cwd` are state/workspace controls, **not a filesystem sandbox**.
3. Security, privacy and capability policy is enforced outside prompts, skills, context engines and memory providers.
4. `LOCAL_ONLY` never reaches OpenRouter or another cloud provider.
5. Do not transplant an old Hermes/LCM/Mnemosyne database into the clean profile.
6. LCM + Mnemosyne is the selected local context/memory baseline; if a mandatory baseline gate fails, Phase 20 is `BLOCKED`/`ROLLBACK`, not an invitation for the agent to redesign memory autonomously.
7. Durable state conforms to the uplift-state schema; every mutating phase has a rollback checkpoint.
8. Temporary bootstrap write/shell authority is narrow and revocable. After the Pi path is proven, production coding must cross the typed Pi boundary.
9. No phase completes from prose review alone. Evidence must prove its acceptance gate.
10. At each phase boundary persist state/evidence **before** reporting conversationally.
11. Do not batch independent improvements merely because they share a phase number; dogfood a reversible improvement before adding a subsystem that could hide its effect.

---

# Phase-boundary report contract

After **every phase**, stop and report:

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

Persist the same fields (or machine-readable equivalents) in the uplift-state/evidence record. A human may approve continuation even when the next phase does not strictly require approval; the important invariant is that phase transitions remain observable.

---

# Phase 00 — Preflight

**Purpose:** prove that the manual foundation is correct before changing behaviour.

Human setup should already have followed `fresh-install-bootstrap.md` and launched `UPLIFT_MISSION.md`.

Collect without mutation:

- macOS version/architecture; free disk; memory pressure;
- Hermes version, profile/home and exact repo commit;
- bootstrap isolation mode and allowed mutation paths;
- effective OpenRouter provider + exact bootstrap model ID, never the key;
- provider-routing config/account privacy posture available at this point;
- Pi version if installed, otherwise `not-installed`;
- current context/compression/memory settings;
- current LCM/Mnemosyne presence without attaching old stores;
- enabled tools/plugins/skills/MCPs and prompt-size/context measurements;
- old Hermes state locations for later read-only preservation;
- policy digest;
- rollback/checkpoint directory;
- representative baseline workload candidates.

Run current Hermes health/config checks from the bootstrap manual. Capture redacted `baseline-preflight` evidence.

**Gate:** clean profile is independently runnable; repo commit and policy digest are known; bootstrap provider works; no legacy DB is silently attached; no production credential/data boundary is ambiguous.

**Adoption state:** nothing optimized yet.

**Restart:** none normally.

**Human approval:** required if bootstrap isolation is weaker than the documented preferred boundary or any sensitive-data uncertainty exists.

---

# Phase 10 — Baseline + Backup + Optional Legacy Curation

**Purpose:** make the before-state measurable and recoverable.

## Baseline

Run representative missions with the single bootstrap model and record:

- total/fresh/cached input and output;
- system/tool/skill/project-context contributions;
- TTFT/wall time;
- provider identity/continuity where observable;
- retries/tool errors;
- accepted-task success and human intervention;
- workstation RSS/memory pressure/swap;
- current context compactions/recovery behaviour.

Do not optimize yet; a baseline changed mid-measurement is not a baseline.

## Backup/checkpoint

Preserve the previous installation/profile/home and current bootstrap profile before mutations. Use profile export and/or filesystem/SQLite-safe backup appropriate to each store. Record hashes and restore instructions.

## Legacy `state.db`

Old state is historical evidence, not memory to transplant. Default salvage status is `SKIPPED`.

If useful history is genuinely missing from authoritative repositories/ADRs, follow `research/legacy-state-curation.md`:

- freeze/checksum original;
- operate only on a copy;
- discover locally before export;
- prefer selected prompts-only export;
- keep raw exports `LOCAL_ONLY`;
- independently scan secrets + typed PII;
- retain raw-source and sanitized hashes separately;
- extract provenance-bearing candidates;
- adversarially compare with current truth;
- admit only durable accepted knowledge to its proper authoritative surface.

Never bulk-import the old DB, LCM DB or Mnemosyne DB.

**Gate:** before-state metrics exist; restore path/checksums verify; salvage is `SKIPPED` or independently safe/proven.

**Adoption state:** baseline only.

**Restart:** no unless backup tooling required quiescing/restarting a service.

**Human approval:** yes for any legacy material whose privacy/provenance remains ambiguous.

---

# Phase 20 — Context + Skill Slimming/Slicing + Local Context/Memory Baseline

**Purpose:** this is the first phase designed to make the uplift **pay for itself** in token/context quality.

## 20A — Narrow profile and prompt diet

Measure first, then remove/deduplicate:

- repeated identity/behaviour prose;
- project information duplicated across SOUL/user/project/chat/memory;
- irrelevant bundled skills;
- always-hot procedures that belong in sliced skills/references/scripts;
- toolsets/schema not required by the orchestrator role;
- whole research/spec documents that can remain external and be retrieved by slice.

Preserve the three-temperature context model:

```text
T0 = byte-stable identity/invariants/catalogue
T1 = bounded current mission/phase capsule
T2 = raw logs/diffs/research/spec/evidence retrieved only when required
```

Keep stable prompt order and role/model/provider affinity where it improves cache continuity. Instrument prompt/context size rather than assuming changes saved tokens.

## 20B — Skill progressive disclosure

Use the `hermes-stack-uplift` class-level skill:

```text
small eligible catalogue
 -> short parent SKILL.md
 -> one current phase reference
 -> script/template/research only if required
```

Do not create one micro-skill per task. Measure catalogue tokens, parent tokens, loaded-support tokens, unnecessary loads, post-compaction reloads, missed/wrong selection, accepted-task quality and cached input.

A skill/reference pruned from working context is considered **unloaded**; reload it before relying on its instructions.

## Dogfood Gate A0 — context/skill changes before memory layering

Before installing/activating LCM + Mnemosyne or adding Spec Kit changes:

1. persist Phase 20 as `EXECUTING` and record the exact context/skill configuration;
2. create a reversible pre-dogfood checkpoint;
3. close the pre-slimming conversation and resume **Phase 20** in a fresh Hermes session using the slimmer T0/T1 + sliced-skill layout;
4. keep the same bootstrap model, OpenRouter policy and other variables stable;
5. run a small matched subset of the Phase 10 representative workload;
6. compare fixed/hot input, skill/tool-schema input, cached input, TTFT, accepted-task quality, wrong/missed skill loads and human intervention;
7. persist `phase20-dogfood-A0` evidence.

Continue only when accepted-task quality is non-inferior and context/token evidence measurably improves. If it regresses materially, repair or roll back the slimming increment **before** introducing the context-engine/memory baseline.

This is deliberately a mid-phase gate: it does not mark Phase 20 complete or permit Phase 30. It exists to obtain an early self-benefit and preserve causal attribution.

## 20C — LCM + Mnemosyne fixed baseline

Follow `local-context-memory-setup.md` exactly:

```text
LCM          = current-session exact context / compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = large/raw evidence
Git/ADR/spec = project truth
```

Initial baseline keeps overlapping autonomous semantic/temporal/proactive LCM memory features off while Mnemosyne owns durable cross-session memory; Mnemosyne uses local embeddings, strict curated writes and the checked-in narrow tool surface.

Prove:

- profile-local pinned installs/effective config;
- exact LCM drill-down after repeated compaction;
- restart/session recovery;
- curated Mnemosyne global/canonical write/recall/update/invalidate lifecycle;
- low stale/irrelevant recall;
- no raw transcript/evidence duplication;
- Tool Search controls non-core schema footprint;
- independent backups/restores;
- after dependencies/model files are provisioned, context/memory continues to work with outbound network denied.

Diagnostic built-in/LCM-only/Mnemosyne-only profiles may isolate faults but do not compete to replace the chosen architecture.

## 20D — Spec Kit/context projection

Implement/validate Micro/Patch, Lite, Standard and High-Assurance Spec Kit profiles. Generated artifacts stay durable in T2; T1 receives only current requirements/acceptance/task slices. Policy may escalate assurance; the model may not downgrade a required profile.

## Phase 20 gate

Require:

- Dogfood Gate A0 proved the context/skill change independently before later Phase-20 layers;
- fixed/hot context materially reduced versus Phase 10 without accepted-task regression;
- initial target >=30% lower skill-related input on skill-heavy representative missions;
- T1 normally bounded <=8K tokens and smaller for simple phases;
- LCM exact-recovery and Mnemosyne curated-recall/offline/backup gates pass;
- no duplicate context/memory authority;
- no hidden cloud dependency for context/memory;
- prompt/cache instrumentation proves what changed.

### Restart Checkpoint A — mandatory fresh session

When the gate passes, report exactly:

> **The first token/context improvements are ready to use.**

Persist Phase 20 complete, close the Phase-20 qualification chat, and start Phase 30 in a **fresh Hermes session using the uplifted profile/configuration**. This prevents Phase-20 qualification context from contaminating later router measurements.

**What is now usable:** optimized context/skill layout and qualified LCM+Mnemosyne baseline.

**Human approval:** no for the fresh-session adoption when all Phase 20 gates passed; yes if any context/memory P0 is unresolved.

---

# Phase 30 — Local Mission Router + OpenRouter Model Roles (Shadow Only)

**Purpose:** build mission routing without requiring it for bootstrap.

## 30A — Routing layers

Implement in order:

1. Tier 0 deterministic privacy/security policy — `LOCAL_ONLY` local/block;
2. deterministic state gates;
3. compact semantic classifier;
4. calibration + hysteresis + abstention;
5. optional second-stage difficulty/preference component.

The local router chooses **lane/model role/model**. OpenRouter is the downstream gateway and may choose the physical provider subject to policy.

## 30B — Training progression

```text
rules/state
 -> embedding prototype
 -> collect representative redacted outcomes
 -> fine-tuned ModernBERT only if justified
```

Compare deterministic rules/state, Qwen3 embedding prototype and frozen `nomic-ai/modernbert-embed-base` 256d/768d with the same calibrated lightweight head. Do not fine-tune ModernBERT until:

- route ontology is stable;
- real redacted missions/outcomes exist;
- near duplicates are removed;
- mission/repository/session/time holdouts are clean;
- ambiguous/hybrid examples exist;
- paired specialist outcomes show the frozen representation is the bottleneck.

RouteLLM-style models, if retained, are optional **difficulty/escalation** layers, not the primary research-vs-code classifier.

## 30C — OpenRouter role bindings

Keep volatile IDs in config/evidence. Research-snapshot intent:

```text
bootstrap.default -> GLM-5.3-Flash-class via OpenRouter
coding.default    -> GLM-5.3-Flash-class via OpenRouter
research.default  -> DeepSeek-V4-Flash-class via OpenRouter
review.default    -> independent family after benchmark
auxiliary.cheap   -> optional, benchmark first
```

Use `configs/models.example.yaml` and `research/openrouter-routing.md`. Verify exact model IDs with current Hermes/OpenRouter at execution time.

Current Hermes provider-routing controls may constrain sort/only/ignore/order/parameter support/data collection. Do not invent unsupported Hermes keys. OpenRouter account/workspace privacy guardrails are additional defense.

Avoid provider churn. Measure effective physical provider continuity and cache-read tokens; optimize accepted-task economics, not nominal price/M alone.

OpenRouter Auto can be a shadow comparator/fallback experiment only. It never handles privacy classification.

## 30D — Shadow evaluation

The router emits recommendations while the bootstrap model/current explicit lane remains authoritative. Log feature/outcome summaries without storing raw sensitive prompts.

Measure:

- downstream accepted-task regret;
- high-severity wrong lane;
- zero observed `LOCAL_ONLY -> cloud`;
- calibration/abstention;
- route-switch rate;
- cache continuity;
- local p50/p95 latency/RSS;
- provider/tool correctness and retries.

### Restart/Canary Checkpoint B

After Phase 30 gates pass, reload/restart the router integration if required and begin a **fresh shadow-mode session**. Do not grant routing authority yet.

**What is now usable:** router observability/shadow recommendations, explicit role bindings, OpenRouter provider-routing policy.

**Human approval:** not required for shadow-only operation; required before any shortcut that would give a not-yet-secured router/delegator stronger authority.

---

# Phase 40 — Security + Policy Enforcement + Authority Gate

**Purpose:** turn policy prose into external enforcement before multi-model/delegated cloud authority.

Follow `bootstrap-authority.md` and `research/security-zero-trust-pii.md`.

Implement external controls for:

- role/capability validation;
- workspace/path/symlink scope;
- process/command policy;
- environment allowlist/scrubbing;
- task-scoped credential brokerage;
- network default-deny/allowlist and egress decision;
- dedicated secret detection;
- typed/context-aware PII detection/transformation;
- post-transform re-scan;
- policy digest binding;
- evidence journal and idempotency state;
- sandbox launcher/containment interface;
- independent review/merge authority.

## OpenRouter-specific enforcement

The privacy decision occurs **before** an OpenRouter call. Provider/model routing cannot override it.

Enforce/verify:

- only approved OpenRouter model roles can receive cloud-bound tasks;
- `LOCAL_ONLY` cannot reach OpenRouter even through Auto/fallback/error recovery;
- request-level Hermes provider-routing policy does not accidentally weaken account guardrails;
- effective provider/data-collection behaviour is recorded where observable;
- no provider preset is assumed to override request-level routing without a test;
- direct-provider fallback cannot activate merely because an API key exists.

Seed secrets/PII and adversarial technical-text false-positive fixtures. Block rather than silently corrupt code/config when classification is uncertain.

Enable Hermes `security-guidance` WARN mode where available as defense in depth only; it is not DLP or containment.

### Adoption Checkpoint C — human authority gate

This phase is security-critical. While any P0 enforcement boundary remains unproven, **human approval is required** before granting stronger routing/delegation/cloud authority.

A YAML config, schema or passing sanitizer unit test is not evidence of structural containment.

**What is now usable:** enforcement substrate and adversarial evidence; not necessarily production authority.

**Restart:** restart/recreate enforcement/router processes when required to ensure the tested policy/config digest is the one actually active.

---

# Phase 50 — Hermes -> Pi Bridge + LSP + Disposable Worker Activation

**Purpose:** move coding/tool loops behind the typed worker boundary.

Build `delegate_pi` outside Hermes core where possible, against the current Pi RPC/headless contract.

Each task must:

- validate the v2 task envelope and current policy digest;
- use attempt/idempotency/reconciliation semantics;
- create an ephemeral git worktree;
- receive minimal environment/credentials;
- use external filesystem/process/network/credential containment;
- use local stdin/stdout/pipe RPC, never an unauthenticated network listener;
- treat Pi `agent_settled` as fully-settled completion, not merely `agent_end`;
- store raw event streams as bounded local evidence, not mirrored hot Hermes context;
- produce compact typed result/evidence;
- prevent worker self-merge/self-approval.

Before cloud credentials, prove fake/local RPC framing, path/symlink denial, environment leak denial, network denial, timeout/cancel, destructive retry/idempotency, malicious-repo instructions, cleanup/recovery and evidence integrity.

Pin/audit LSP integration for Java, Kotlin, Python, TypeScript/JavaScript and HTML/CSS. Inject only relevant changed-file/symbol/severity diagnostics, not workspace floods.

Activate cloud coding only after Phase 40 egress/containment canaries pass. Route the coding role through the configured OpenRouter model binding; physical provider remains downstream policy.

## Bounded task graph / Kanban

Use typed bounded tasks rather than unconstrained swarms. Kanban may project blocked/review/retry state for operations, but `uplift-state` remains mission authority and immutable evidence remains proof.

## Authority cutover

Once a privacy-controlled Pi canary passes:

1. switch ordinary Hermes to the constrained orchestrator profile;
2. remove generic production source-write/arbitrary-shell capability;
3. make typed Pi delegation the production coding path;
4. instruct Hermes to skip Pi and edit directly — the attempt must fail structurally;
5. persist the new capability/policy digest evidence.

### Worker Checkpoint D

Recreate Pi workers under the validated bridge/LSP/sandbox/model configuration. Workers are disposable; do not reuse stale workers created before the policy/model/LSP cutover.

**What is now usable:** typed disposable coding workers and bounded LSP flow, assuming all Phase 40/50 gates passed.

**Human approval:** required for production authority cutover until the artifact-readiness P0 gates have concrete evidence.

---

# Phase 60 — Full Evaluation + Multi-Role Promotion

**Purpose:** decide whether the uplift as a system is better and safe enough for ordinary use.

Run the complete matched/adversarial corpus across:

- context/skills + LCM/Mnemosyne;
- router shadow vs explicit/fixed controls;
- OpenRouter bootstrap/research/coding/review role candidates;
- direct Z.ai/DeepSeek endpoint challengers **only if** credential/integration cost is justified for the benchmark;
- provider-routing modes/continuity/cache;
- external security/PII/secret/egress controls;
- Pi RPC/containment/retry/recovery;
- LSP language fixtures;
- Spec Kit profiles;
- bounded task/review graph;
- failure injection and rollback.

Primary decision metric is **accepted-task quality + cost/minutes/retries/human intervention**, not token price or classifier F1 alone.

Require:

- accepted-task quality non-inferior within the chosen confidence interval;
- zero observed mandatory privacy/capability violations;
- context/token improvements survive representative long missions;
- LCM/Mnemosyne recall remains low-noise and local-only;
- router improves utility/regret and remains calibrated;
- OpenRouter provider routing meets privacy/parameter/reliability requirements;
- cache continuity is acceptable;
- direct APIs do not provide enough material advantage to justify defaulting away from OpenRouter, or the exception is explicitly documented;
- Pi/LSP workers pass isolation and language fixtures;
- workstation memory pressure/swap is acceptable under realistic load;
- rollback is rehearsed.

### Promotion Checkpoint E

Only now enable ordinary multi-role operation:

```text
local policy
 -> local mission router with authority
 -> research/coding/review role binding
 -> OpenRouter
 -> policy-compatible physical provider
```

Keep OpenRouter Auto bounded to explicitly approved fallback/auxiliary cases.

A production promotion checkpoint records exact Hermes/Pi/LCM/Mnemosyne/router/model/provider-policy pins.

**Human approval:** required for production promotion while the repository's P0 readiness policy says so.

---

# Phase 70 — Upgrade + Rollback Discipline

**Purpose:** make the uplift maintainable rather than a one-time installation event.

Treat Hermes, Pi, LCM, Mnemosyne, router models/classifiers, LSPs and model/provider bindings as independently pinned dependencies.

For each update:

1. inspect current trusted release/security/model metadata;
2. create a disposable canary/new workers/session;
3. quiesce/backup SQLite stores before schema-affecting changes;
4. update one bounded layer;
5. reapply only versioned overlay/config;
6. run relevant protocol/security/context/memory/router/LSP/model/provider smoke + adversarial tests;
7. compare prompt/cache/recall/accepted-task metrics with prior pins;
8. start a fresh session/recreate workers where stale prompt/plugin/runtime state would hide the change;
9. promote only on pass;
10. otherwise roll back to the previous known-good pin and record the blocker.

Do not automatically chase model `latest` aliases, release candidates or transient OpenRouter provider prices in production. Re-verify current role bindings periodically, but keep phases/sessions sticky once selected.

### Upgrade Checkpoint F

Persist the recurring canary/restart/rollback policy and prove one end-to-end rollback exercise.

**What is now usable:** repeatable maintenance cycle.

---

# Restart/adoption matrix

| Boundary | Change state | Required action |
|---|---|---|
| after 00 | observed only | continue after report |
| after 10 | baseline/backups durable | restart only if backup tooling required it |
| **A0 inside 20** | context/skill slimming staged | **fresh Phase-20 continuation session; matched dogfood subset; repair/rollback before adding LCM/Mnemosyne on regression** |
| **A after 20** | context/skills + LCM/Mnemosyne adopted | **fresh Hermes session required before Phase 30** |
| **B after 30** | router qualified for shadow | reload/restart integration if needed; fresh shadow session recommended |
| **C after 40** | security substrate staged/proven | human authority gate; restart enforcement processes when config digest changes |
| **D after 50** | Pi/LSP path validated | **recreate disposable Pi workers**; production coding cutover only with approval |
| **E after 60** | multi-role system promoted | fresh ordinary session on final role/router/provider config |
| **F at 70** | recurring upgrade policy | canary new sessions/workers per changed component |

---

# Maturity vocabulary

Use these labels consistently:

- `researched` — current evidence/source supports the idea;
- `designed` — coherent contract/config exists;
- `prototype` — implementation exists but lacks broad evidence;
- `smoke-tested` — narrow deterministic fixture passed;
- `target-Mac validated` — representative M3 Max evidence exists;
- `shadow` — observes/recommends without authority;
- `canary` — bounded real authority/workload;
- `production-approved` — all mandatory promotion gates and required human approval passed.

Do not describe a documented config as an implemented security control.

---

# Autonomous stop conditions

Hermes must persist `BLOCKED`/`ROLLBACK`, report, and stop when:

- backup/checkpoint cannot be verified;
- a raw legacy artifact would need cloud exposure;
- current stable dependency/model/provider semantics cannot be verified;
- Phase 20 Dogfood Gate A0 regresses accepted-task quality or fails to show measurable context/token benefit;
- Phase 20 LCM/Mnemosyne mandatory gates fail;
- supposedly local context/memory unexpectedly uses network;
- Phase 20 fresh-session checkpoint cannot be established cleanly;
- router attempts `LOCAL_ONLY -> cloud`;
- OpenRouter/Auto/provider fallback would weaken privacy policy;
- sanitizer/secret/PII/egress enforcement fails;
- external Pi containment is unproven;
- provider credential exposure exceeds the allowed worker boundary;
- Pi completion/retry state cannot be reconciled;
- direct Hermes coding bypass remains possible after intended cutover;
- stale worker/session state means the tested config is not demonstrably active;
- accepted-task quality materially regresses;
- production promotion would require disabling a mandatory control.

Stopping at a phase boundary is correct behaviour, not mission failure.
