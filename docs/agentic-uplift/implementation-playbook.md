# Self-Uplift Implementation Playbook for Hermes

Snapshot: 2026-08-31.

This is the **single canonical execution lifecycle** for Hermes to uplift its stack. The only phase sequence is:

```text
00 -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70
```

Detailed research is supporting evidence, not another phase system. The conversation is not execution state.

Use with:

- `UPLIFT_MISSION.md` — staged launcher and boundary rules;
- `fresh-install-bootstrap.md` — human foundation;
- `agent-execution-contract.md` — state/evidence/authority contract;
- `bootstrap-authority.md` — temporary root-of-trust transition;
- `skills/hermes-stack-uplift/` — progressive-disclosure phase slices;
- `protocols/uplift-state.schema.json` — durable mission state;
- `protocols/routing-mission.schema.json` and `routing-decision.schema.json` — framework-neutral routing seam;
- `research/local-routing-models.md` — routing architecture/framework assessment;
- `research/openrouter-routing.md` — gateway/provider boundary;
- `local-context-memory-setup.md` — fixed LCM + Mnemosyne baseline.

---

# Operating model

Every phase follows:

```text
small reversible change
 -> deterministic + representative tests
 -> adversarial challenge
 -> compare with baseline
 -> persist evidence/state
 -> report boundary
 -> fresh session/reload/recreate if required
 -> only then next phase
```

Hermes returns control at every phase boundary. A phase may contain a smaller mid-phase dogfood gate when that gives a cleaner causal measurement.

## Non-negotiable rules

1. Work in a clean profile/canary/worktree/overlay; never mutate the only working installation first.
2. A Hermes profile or `terminal.cwd` is not a filesystem sandbox.
3. Security/privacy/capability eligibility is enforced outside prompts, skills, context engines, memory and learned routing.
4. `LOCAL_ONLY` never reaches OpenRouter/direct cloud/Auto/fallback.
5. Known tools, modality, context limits, network/sandbox permissions, ZDR/retention and policy-required approval/review are hard eligibility facts, not learned preferences.
6. Do not transplant old Hermes/LCM/Mnemosyne databases into the clean profile.
7. LCM + Mnemosyne is the selected context/memory baseline; failures block/rollback rather than trigger autonomous redesign.
8. Every mutating phase has an independently reversible checkpoint.
9. Temporary bootstrap write/shell authority is narrow and revoked after the typed Pi path is proven.
10. No phase completes from prose review alone; evidence proves gates.
11. Persist state/evidence before conversational reporting.
12. Routing frameworks are replaceable behind the routing mission/decision contracts.
13. Research and coding are important task families, not a closed-world routing ontology.
14. Optimize accepted-mission quality/cost/latency/retries/human effort, not token price or classifier F1 alone.
15. **Mandatory P0 gates pass before any policy-required human approval can authorize a stronger transition. Approval is additive authority, never a waiver or substitute for failed/missing evidence.**

## Routing ownership

```text
MISSION + durable state
  -> Tier 0 deterministic eligibility/security
  -> Tier 1 multi-label mission-profile inference
  -> Tier 2 bounded workflow/agent selection
  -> Tier 3 model-role/model economic optimization
  -> Tier 4 OpenRouter-first gateway/provider execution
```

OpenRouter Auto is a sanitized shadow/bootstrap/fallback/teacher signal only. It cannot restore cloud eligibility, grant tools, select Pi authority or replace our workflow semantics.

---

# Required phase-boundary report

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

Persist the machine-readable equivalent in uplift-state first.

---

# Phase 00 — Preflight

**Purpose:** prove the manual foundation before changing behaviour.

Collect without mutation:

- macOS/architecture, free disk and memory pressure;
- Hermes version/profile/home and repo commit;
- bootstrap isolation mode and allowed mutation paths;
- effective OpenRouter provider + exact bootstrap model ID, never the key;
- effective provider/account privacy posture;
- Pi version or `not-installed`;
- current context/compression/memory/tools/plugins/skills/MCP state;
- prompt/context baseline contribution sizes;
- legacy state locations without attaching them;
- policy digest and rollback/checkpoint directory;
- representative baseline missions.

**Gate:** clean profile independently runs; repo/policy/model are known; no legacy store is attached; no sensitive boundary is ambiguous.

**Approval:** if the operator deliberately uses a weaker-than-preferred but still bounded/documented bootstrap isolation mode, record it and require human approval. **Unresolved sensitive-data, credential or containment uncertainty is a blocker and cannot be approved around.**

---

# Phase 10 — Baseline + Backup + Optional Legacy Curation

**Purpose:** establish the before-state and recovery path.

Run representative missions with the single bootstrap model and capture:

- fresh/cached/total input and output;
- prompt/tool/skill/project-context contribution;
- TTFT/wall time;
- model/provider continuity where observable;
- retries/tool errors;
- accepted-task success/human intervention;
- RSS/memory pressure/swap;
- context compaction/recovery behavior.

Preserve previous/current profiles and relevant SQLite stores using safe backup/checkpoint procedures. Prove restore instructions/checksums.

Legacy `state.db` salvage defaults to `SKIPPED`. If needed, use `research/legacy-state-curation.md`: immutable original, working copy, local discovery, selected export, local PII/secret scan, provenance/hashes, contradiction review, tiny admitted result. Never bulk-import old Hermes/LCM/Mnemosyne databases.

**Gate:** before metrics and verified restore path exist; salvage is skipped or safely curated.

---

# Phase 20 — Context + Skills + LCM/Mnemosyne

**Purpose:** make the uplift begin paying for itself before routing complexity.

## 20A/B — Prompt diet + progressive-disclosure skills

Measure then remove/deduplicate repeated identity/project prose, irrelevant skills/tool schemas and whole documents that belong in T2 artifacts.

Preserve:

```text
T0 = byte-stable identity/invariants/small catalog
T1 = bounded current mission/phase capsule
T2 = logs/diffs/research/spec/evidence loaded only when required
```

Use:

```text
small eligible catalog -> parent SKILL.md -> one current phase slice -> support artifact on demand
```

Measure fixed/hot context, skill/tool-schema input, cached input, wrong/missed loads and accepted-task quality.

### Dogfood Gate A0

Before adding LCM/Mnemosyne or Spec Kit changes:

1. persist exact slimmed config and a reversible checkpoint;
2. resume **Phase 20** in a fresh session with the slimmed T0/T1/skill layout;
3. hold bootstrap model/OpenRouter policy constant;
4. rerun a small matched Phase-10 subset;
5. proceed only if accepted-task quality is non-inferior and context/token evidence improves.

Otherwise repair/rollback slimming first.

## 20C — LCM + Mnemosyne fixed baseline

Follow `local-context-memory-setup.md`:

```text
LCM          = current-session exact context / compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = large/raw artifacts
Git/ADR/spec = project truth
```

Prove pinned/effective config, repeated compaction drill-down, restart recovery, curated Mnemosyne lifecycle, low stale recall, no transcript duplication, Tool Search schema control, independent backup/restore and local-only operation with outbound network denied after provisioning.

## 20D — Spec Kit projection

Validate Micro/Patch, Lite, Standard and High-Assurance profiles. Durable specs stay T2; T1 receives only current requirements/acceptance/tasks. Policy may escalate assurance; models cannot downgrade it.

**Gate:** A0 passed; hot context materially smaller; initial skill-input target >=30% reduction on representative skill-heavy missions; T1 normally <=8K; LCM/Mnemosyne local/recovery/backup gates pass; accepted-task quality non-inferior.

### Checkpoint A

Report **“The first token/context improvements are ready to use.”** Start Phase 30 in a fresh optimized session.

---

# Phase 30 — Routing Contracts + Small Router + Shadow Bake-off

**Purpose:** introduce routing incrementally without making the uplift depend on an advanced router.

## 30A — Establish the contract seam

Validate examples against:

- `protocols/routing-mission.schema.json`;
- `protocols/routing-decision.schema.json`.

A mission profile separates:

- **primary inferred capability/workflow signals:** multi-label task families, domain, phase, complexity, uncertainty, reasoning/tool intensity;
- **secondary deterministic constraints:** privacy, cloud eligibility, tools/capabilities, modality, context, Pi requirement, network/sandbox, ZDR/retention, risk/review/approval;
- **tertiary optimization:** quality floor, latency/cost preference, reliability, cache affinity and switch budget.

A route decision returns bounded workflow stages + agents + model roles/models + gateway/provider requirements. Do not emit a single `hybrid` label for a mission such as `research -> design -> implementation -> test -> review`.

## 30B — First hot-path router: rules/state

Start with the smallest useful local router:

```text
Tier 0 deterministic eligibility
 + deterministic workflow/state gates
 + simple multi-label task-family rules
 + safe abstention
```

It must work without Torch/Transformers/Envoy/cloud dependencies and establish latency/RSS/security/economic controls.

## 30C — Shadow semantic/framework challengers

Run through adapters that consume/emit our contracts:

A. deterministic rules/state;
B. minimal local embedding prototype;
C. Aurelio Semantic Router with a local encoder;
D. vLLM Semantic Router in shadow;
E. ModernBERT only when its later data gate is satisfied;
F. relevant LLMRouter algorithms in the research plane;
G. RouteLLM-style Tier-3 preference scorer;
H. OpenRouter Auto on policy-approved sanitized work in shadow.

Current hypothesis: **vLLM Semantic Router is the strongest medium-term adoption candidate**, because its maintained signal/projection/decision system and v0.3 session-aware model-switch work align well with Tier 1/3. But it remains a challenger until it earns its heavier operational footprint. Prefer config/adapters/upstream contributions; do not fork now.

Aurelio is the lighter semantic challenger. LLMRouter remains a lab. RouteLLM scores strong-vs-economical choices after eligibility/workflow, not mission type.

## 30D — Model-role and gateway binding

Roles are reusable capability/economic pools, not task labels. Start with a small set such as `general.default`, `reasoning.default`, `research.default`, `coding.default`, `review.default`, `multimodal.default`, `local.default` and optional `auxiliary.cheap`, with exact IDs bound only after matched benchmarks.

OpenRouter remains Tier 4. Current Hermes supports only a subset of raw OpenRouter provider controls; abstract route requirements such as ZDR/session affinity must be demonstrably enforced by Hermes, account policy or a thin audited adapter, otherwise fail closed.

Do not rely on provider stickiness unless stable session-key propagation is proven. Measure actual model/provider continuity and cached tokens.

## 30E — Shadow telemetry/evaluation

Keep the explicit bootstrap/fixed path authoritative while candidates recommend routes.

Default telemetry stores no raw sensitive prompt. Record redacted feature/hash + route engine/version, mission profile, workflow/model/provider decision, tokens/cached tokens, router latency/RSS, TTFT/wall time, tool calls, retries/fallbacks/switches, tests/review result, human override, accepted/rejected, failure reason and cost where available.

Measure:

- hard-eligibility violations — mandatory zero;
- multi-label task-family metrics and uncertainty/abstention;
- workflow/stage accuracy where labels are meaningful;
- accepted-task/mission regret versus matched eligible paths;
- cost per accepted mission;
- tool/capability failures;
- retries/human overrides;
- workflow/model/provider switch rate;
- cache continuity;
- TTFT/wall time;
- local p50/p95/p99 and RSS;
- dependency/operational complexity.

### Checkpoint B

A passing Phase 30 is **shadow only**. Reload/restart the routing integration if needed and start a fresh shadow session. No learned/framework router receives authority.

---

# Phase 40 — Security + Policy Enforcement + Authority Gate

**Purpose:** turn policy/eligibility prose into structural enforcement before multi-model/delegated cloud authority.

Implement external controls for:

- role/capability validation;
- workspace/path/symlink scope;
- process/command policy;
- environment allowlist/scrubbing;
- task-scoped credentials;
- network default-deny/allowlist and egress;
- secret detection;
- typed/context-aware PII transform/block plus re-scan;
- policy digest/idempotency/evidence journal;
- sandbox launcher/containment;
- independent review/merge authority.

Routing-specific enforcement must prove:

- deterministic routing-mission constraints are authoritative;
- `LOCAL_ONLY` cannot reach OpenRouter/Auto/fallback/direct cloud;
- stale/learned capability metadata cannot authorize unavailable tools/modalities/context/network;
- required ZDR/retention/provider rules fail closed if the client/gateway cannot enforce them;
- model/provider fallback cannot cross a hard eligibility boundary;
- direct-provider fallback cannot activate merely because a credential exists.

Use adversarial PII/secret/technical-text fixtures. `security-guidance` WARN is defense in depth only.

### Checkpoint C

All mandatory P0 enforcement/egress/containment/privacy gates for the requested authority increase must pass first. Failed, missing or unproven mandatory evidence means `BLOCKED`/`ROLLBACK` and no authority increase. **Only after those gates pass**, explicit human approval is additionally required before stronger routing/delegation/cloud authority. Human approval cannot waive a mandatory gate.

---

# Phase 50 — Hermes -> Pi + LSP + Disposable Worker Activation

**Purpose:** move implementation/tool loops behind a typed worker boundary.

Build `delegate_pi` outside Hermes core where possible. Each production task must:

- validate current task-envelope schema + policy digest;
- bind to the routing mission/stage/decision that selected the Pi stage;
- use attempt/idempotency/reconciliation semantics;
- create an ephemeral git worktree;
- receive minimal environment/credentials;
- use external filesystem/process/network/credential containment;
- use local stdin/stdout/pipe RPC, never unauthenticated network RPC;
- treat Pi `agent_settled` as fully-settled completion;
- store raw events as bounded local evidence, not hot Hermes context;
- return compact typed result/evidence;
- prevent self-merge/self-approval.

Before cloud credentials, prove fake/local RPC framing, path/symlink/environment/network denial, timeout/cancel, destructive retry/idempotency, malicious-repo instruction resistance, cleanup/recovery and evidence integrity.

Pin/audit LSP for Java, Kotlin, Python, TypeScript/JavaScript and HTML/CSS. Inject only relevant changed-file/symbol/severity diagnostics.

Only after Phase 40 canaries pass may a cloud-eligible `pi_worker` stage use `coding.default` or another eligible coding role.

### Checkpoint D

Recreate disposable Pi workers under the tested bridge/LSP/sandbox/routing/model config. After authority cutover, direct production editing by Hermes must fail structurally.

The Phase-50 protocol, containment, privacy and bypass gates must pass before coding-authority cutover. Any policy-required human approval is additional **after** those mandatory gates pass and cannot waive them.

---

# Phase 60 — Full Outcome/Economic Evaluation + Promotion

**Purpose:** decide whether the whole uplift and any router candidate are better/safe enough for ordinary use.

Run matched/adversarial missions across:

- context/skills + LCM/Mnemosyne;
- deterministic router baseline and all technically feasible Phase-30 shadow candidates;
- workflow transitions including research/design/implementation/test/review rather than only single-family prompts;
- OpenRouter model-role candidates and gateway/provider policies;
- direct/local gateway challengers only when integration/credential cost is justified;
- security/PII/secret/egress controls;
- Pi containment/RPC/retry/recovery;
- LSP fixtures;
- Spec Kit profiles;
- failure injection/rollback.

## Router bake-off

Use the same versioned mission corpus and mission/repo/session/time cohort splits for:

```text
A rules/state
B minimal embeddings
C Aurelio Semantic Router
D vLLM Semantic Router
E ModernBERT only if data gate passed
F relevant LLMRouter algorithms
G RouteLLM-style Tier-3 scoring
H OpenRouter Auto sanitized shadow
```

Do not pretend every research candidate is directly comparable on every metric. Evaluate task/profile inference, deterministic eligibility, workflow/model economics and runtime operations separately, then compare end-to-end accepted-mission outcomes where feasible.

Primary promotion metrics:

1. zero mandatory privacy/capability/ZDR/network/sandbox violations;
2. accepted-mission quality/regret versus best eligible matched path;
3. **cost per accepted mission** including retries/failures;
4. tool/workflow capability failures;
5. human override/retry/fallback rate;
6. unnecessary workflow/model/provider switches;
7. cache continuity/cached-token share;
8. TTFT/wall time/throughput;
9. calibrated task/profile/uncertainty metrics;
10. router latency/RSS and operational complexity.

A simpler router wins if it captures most economic benefit with materially lower operational burden.

## ModernBERT gate

Do not train merely because Phase 60 exists. Fine-tuning requires stable multi-label ontology, representative locally redacted/deduplicated real Hermes missions, multi-stage coverage, matched workflow/model/provider outcomes, clean mission/repo/session/time holdouts, stable learning curves/calibration and evidence that simpler rules/embedding/Aurelio/vLLM-config approaches plateau due to representation—not label/policy/workflow flaws.

A future ModernBERT should use calibrated multi-label/multi-head outputs such as task families, domains, phase, complexity, reasoning/tool intensity, context-need band and uncertainty. Never train heads for deterministic eligibility facts.

## vLLM adoption/fork gate

Prefer vLLM Semantic Router configuration/adapters/upstream contribution. Maintain a fork only if a mandatory materially valuable requirement cannot be expressed through stable extension/config interfaces, upstream cannot accommodate it in bounded time, the patch stays small/isolated/tested/rebaseable, and measured quality/cost/latency/security/resilience benefit exceeds ongoing fork maintenance.

### Checkpoint E

Only successful Phase-60 evidence can promote ordinary routing authority/multi-role operation:

```text
Tier 0 deterministic eligibility
 -> promoted Tier 1/2/3 router implementation
 -> selected workflow/model role/model
 -> OpenRouter-first Tier 4
 -> eligible physical provider
```

Record exact Hermes/Pi/LCM/Mnemosyne/router/contracts/models/gateway policy pins. If readiness policy requires human production approval, request it **only after all mandatory promotion gates pass**; approval cannot waive failed or missing evidence. Then start the fresh ordinary session on the exact evidence-qualified, approved configuration.

---

# Phase 70 — Upgrade + Rollback Discipline

**Purpose:** make the uplift maintainable.

Treat Hermes, Pi, LCM, Mnemosyne, router frameworks/models/contracts, LSPs and gateway/model/provider bindings as independently pinned components.

For each update:

1. inspect trusted release/security/model metadata;
2. create disposable canary/new workers/session;
3. backup SQLite stores before schema changes;
4. update one bounded layer;
5. reapply only versioned config/adapter/overlay;
6. run relevant protocol/security/context/memory/router/LSP/model/provider smoke + adversarial tests;
7. compare prompt/cache/recall/accepted-mission metrics;
8. start fresh session/recreate workers when stale runtime state would hide the change;
9. promote only on pass;
10. otherwise rollback and record blocker.

A router framework upgrade must still pass the framework-neutral contract suite. A fork, if one ever exists, must prove it has not drifted from upstream security/stable fixes.

Do not chase `latest`, RCs or transient provider prices automatically.

### Checkpoint F

Persist the recurring canary/restart/rollback policy and prove one end-to-end rollback exercise.

---

# Restart/adoption matrix

| Boundary | State | Required action |
|---|---|---|
| after 00 | observed | continue after report |
| after 10 | baseline/backups | restart only if needed |
| **A0 inside 20** | context/skill slimming staged | fresh Phase-20 continuation + matched dogfood; repair/rollback on regression |
| **A after 20** | context/skills + LCM/Mnemosyne active | fresh Hermes session before Phase 30 |
| **B after 30** | routing candidates shadowed | reload/restart as needed; no routing authority |
| **C after 40** | mandatory enforcement gates proven | then human authority approval; otherwise remain blocked |
| **D after 50** | Pi/LSP path validated | recreate disposable workers; evidence-qualified approved coding cutover only |
| **E after 60** | selected router/workflow/model system qualified | then required production approval + fresh ordinary session on exact promoted config |
| **F at 70** | recurring upgrade policy | canary sessions/workers per changed component |

---

# Maturity vocabulary

Use consistently:

- `researched` — current evidence supports idea/candidate;
- `designed` — coherent contract/config/evaluation plan exists;
- `prototype` — runnable implementation exists;
- `smoke-tested` — narrow deterministic fixture passed;
- `target-Mac validated` — representative target-workstation evidence exists;
- `shadow` — observes/recommends without authority;
- `canary` — bounded real authority/workload;
- `production-approved` — mandatory outcome/security/rollback gates passed and any required human approval was granted afterward.

Do not describe a documented router framework or config as implemented production routing.

---

# Autonomous stop conditions

Persist `BLOCKED`/`ROLLBACK`, report and stop when:

- backup/checkpoint cannot be verified;
- raw legacy material would need cloud exposure;
- stable dependency/model/gateway semantics cannot be verified;
- Phase-20 dogfood/context-memory gates fail;
- supposedly local context/memory unexpectedly uses network;
- a learned/router/gateway layer overrides or bypasses deterministic eligibility;
- router attempts `LOCAL_ONLY -> cloud`;
- required tools/modality/context/ZDR/network/sandbox constraints cannot be guaranteed;
- model/provider fallback crosses a hard eligibility/quality boundary;
- routing contract/engine output cannot be validated/reconciled;
- router research tooling would require storing sensitive raw prompts without approved need;
- security/secret/PII/egress enforcement fails;
- external Pi containment is unproven;
- Pi task cannot be attributed to an approved routing stage/policy digest;
- direct Hermes coding bypass remains possible after intended cutover;
- stale worker/session/router state means the tested configuration is not demonstrably active;
- accepted-task quality materially regresses;
- production promotion requires disabling a mandatory control;
- a human is willing to proceed but a mandatory P0 gate is failed, missing or unproven.

Stopping correctly is success of the control system, not mission failure.
