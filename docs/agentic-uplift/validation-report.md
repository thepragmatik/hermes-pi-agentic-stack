# Refinement Validation Report

Snapshot: 2026-08-31.

## Maturity vocabulary

Use the repository's canonical maturity labels without collapsing them:

`researched -> designed -> prototype -> smoke-tested -> target-Mac-validated -> shadow -> canary -> production-approved`

A schema/config/research note is not a runtime implementation; a CI smoke is not representative target-Mac evidence; shadow recommendations have no production authority.

## Final pre-launch remediation

A release-readiness audit after the routing refactor found several concrete drift/implementation defects. They were corrected before launch rather than accepted as documentation debt:

- removed legacy `routing.hybrid_enabled` policy intent and retained capability/workflow-first routing;
- replaced stale T1 `research|coding|hybrid|local_only` lane projection with workflow/stage/task-family/model-role routing state;
- corrected LCM + Mnemosyne qualification failures to block/rollback **Phase 20**, not Phase 30;
- aligned routing-decision, Pi task and uplift-state maturity vocabulary with `target-Mac-validated`;
- made uplift-state structurally enforce exactly one ordered `00 -> 70` phase sequence;
- added first-class `dogfood-A0` checkpoint state and example evidence;
- initialized the optional embedding router's `embedding_floor` correctly;
- changed router-benchmark external adapters to fail closed **before prompt handoff** whenever deterministic Tier-0 state says `cloud_allowed=false`, not only when the privacy label is `LOCAL_ONLY`;
- made human approval explicitly **additive after mandatory P0 evidence passes** across the mission, execution contract and Phase 40/50/60 transitions; approval cannot waive failed/missing P0 evidence;
- added adversarial hypothesis 85 for attempted human waiver of a failed P0 gate;
- converted those findings into persistent validator regression assertions, including a dynamic external-adapter canary.

## Executed repository / Pages gate

On pre-launch implementation head `59e480a294369c845e3906970f7bf6e83bde32dc`, GitHub Pages workflow run **33385391824** completed successfully on 2026-08-31. Both the build and Pages deployment jobs succeeded.

The build gate executed:

- Python 3.12 compilation of router/site tooling;
- generation of **26 human pages plus the progressive-disclosure agent surface**;
- internal-link and Markdown/`llms.txt` alternate validation;
- accessible architecture SVG checks;
- SHA-256 + byte-size validation of every raw source in agent manifest v5;
- exact agent/raw equality for execution-critical mission/contracts/examples/configs;
- five-tier architecture graph v3 assertions;
- routing mission/decision schema v1.0 + examples;
- Pi task envelope **v2.2** + routing-stage provenance checks;
- uplift-state v1.1 + structurally exact ordered `00 -> 70` lifecycle checks;
- `dogfood-A0` checkpoint schema/example checks;
- canonical maturity-vocabulary equality across routing/Pi/uplift-state contracts;
- required human/agent routing entry surfaces;
- regression assertions against legacy `hybrid_enabled`, stale T1 lane projection and wrong Phase-30 memory blocking;
- evidence-first human-approval/mandatory-P0 invariants across mission/playbook/phase slices;
- embedding-router `embedding_floor` initialization assertion;
- a dynamic canary proving an `INTERNAL` mission with deterministic `cloud_allowed=false` does **not** invoke a configured external router adapter and resolves to the local-only path;
- the zero-dependency rules router against the checked-in 32-mission fixture with hard-violation failure enabled;
- Pages artifact upload and deployment.

The validator reported:

```text
OK: validated 26 HTML pages, pre-launch regression invariants, routing contracts,
progressive-disclosure agent surface, hashed raw manifest, five-tier OpenRouter architecture,
Pi routing traceability, exact 00-70 lifecycle, dogfood-A0, evidence-first authority gates,
cloud-ineligible adapter guard, rules smoke task-micro-F1=0.923, workflow=0.875, hard=0
```

The uploaded Pages artifact digest was independently matched to GitHub's recorded SHA-256, and the deployed artifact contained 110 files / 26 HTML pages with the corrected raw policy, mission-context, memory research/setup, mission, schemas and agent entry surfaces.

These routing numbers are intentionally **smoke evidence only**. The broader fixture makes the simple rules baseline imperfect rather than preserving the old artificially clean research/coding five-class result. No hard eligibility violation was observed in the fixture, but this is not DLP/security proof or production router evidence.

## Routing architecture now validated as repository design

Canonical responsibility chain:

```text
MISSION + durable state
 -> Tier 0 deterministic eligibility/security
 -> Tier 1 multi-label mission/capability profile
 -> Tier 2 bounded workflow/agent selection
 -> Tier 3 model-role/model economic optimization
 -> Tier 4 OpenRouter-first gateway/provider execution
 -> outcomes -> offline research/training plane
```

Research and coding remain first-class task families; they are not the complete ontology. Multi-stage missions remain ordered stages rather than a `hybrid` label.

### Hard vs learned fields

Tier-0/runtime facts include privacy class, `LOCAL_ONLY`, cloud eligibility, secret/PII policy, actual tools/capabilities, required modality/structured output/context, network/sandbox constraints and ZDR requirements. Learned/framework output cannot override them.

Tier-1 learned/semantic signals may estimate task families, domain, phase, complexity, uncertainty, tool/reasoning intensity and expected context needs. Tier 2 selects a bounded workflow; Tier 3 selects among eligible model roles/models. OpenRouter normally performs only downstream provider execution within requirements.

### Thin routing contracts

- `protocols/routing-mission.schema.json` v1.0 — framework-neutral mission facts/profile/requirements.
- `protocols/routing-decision.schema.json` v1.0 — eligible workflow/stages, model selection and provider requirements.
- `protocols/pi-task-envelope.schema.json` v2.2 — Phase-50+ worker request with `mission_id`, `stage_id`, workflow and routing-decision digest.
- `protocols/uplift-state.schema.json` v1.1 — exact ordered phase/state/report/checkpoint contract including Dogfood A0.

This keeps Hermes/Pi semantics replaceable across rules, Aurelio, vLLM Semantic Router, ModernBERT or future adapters.

## Router candidate evidence status

| Candidate | Intended role | Current evidence |
|---|---|---|
| deterministic eligibility + rules/state + abstention | initial Phase-30 baseline | **prototype / smoke-tested on 32-mission fixture** |
| minimal embedding prototype | small semantic challenger | designed/prototype path; target-Mac bake-off pending |
| Aurelio Semantic Router | lightweight local Tier-1 semantic component | researched/designed adapter; bake-off pending |
| vLLM Semantic Router | richer signal/session/model-routing candidate | **researched/designed; strongest medium-term adoption candidate; no authority yet** |
| LLMRouter algorithms | research/training/evaluation laboratory | researched/designed research-plane integration |
| RouteLLM-style scorer | Tier-3 strong-vs-economical/difficulty score | researched/designed; requires our outcome recalibration |
| OpenRouter Auto | bootstrap/shadow/teacher/fallback comparator | researched/designed shadow use only after Tier-0 approval |
| custom ModernBERT | future multi-label/multi-head mission profiler | researched/deferred; not trained |

No advanced router is required to start the uplift. Phase 30 first uses the simple rules/state contract in **shadow** while candidates are compared. Only Phase 60 may promote routing authority.

## ModernBERT training gate

Do not train merely to improve the checked-in smoke F1. Training becomes justified only when:

- task/workflow vocabulary is stable because it has material routing consequences;
- representative Hermes/Pi missions are locally redacted and deduplicated;
- train/test split prevents mission/repo/session/time leakage and includes a later temporal canary;
- outcomes include accepted/rejected, tests/review, retries, human overrides and real model/provider economics;
- ambiguous/OOD/multi-stage work is represented;
- frozen embedding/Aurelio/vLLM-configured/simple baselines plateau for reasons attributable to representation rather than bad labels/workflow design;
- a multi-label/multi-head model improves held-out accepted-mission regret/calibration, not only classification F1.

Known Tier-0 facts are never ModernBERT targets for authority.

## Fork gate

No router fork is currently justified. Maintain an upstream fork only if all are true:

1. a materially valuable requirement remains unmet;
2. upstream/config/adapter contribution is unavailable or fails the requirement;
3. the patch set stays small/isolated behind our routing contract;
4. conformance/security tests cover the divergence;
5. ongoing upstream rebase/security-review capacity exists;
6. measured quality/cost/latency/security/resilience benefit exceeds fork maintenance cost.

Current posture for vLLM Semantic Router is **adopt/configure/extend upstream first**, not fork.

## OpenRouter evidence boundary

OpenRouter remains the default external gateway because it can remove provider-health/routing/failover infrastructure from our hot path. The routing contract can express provider allow/deny, parameter/data/ZDR requirements, price/latency/throughput preference, fallback and session/cache affinity.

However, the raw OpenRouter API supports more controls than the currently documented Hermes `provider_routing` surface. A hard requirement is credited only when the installed Hermes request path, OpenRouter account/workspace policy or a small audited gateway adapter proves it is enforced. Do not assume ZDR/session-affinity behavior merely because OpenRouter exposes the capability.

OpenRouter Auto cannot decide privacy/cloud eligibility and is not final workflow authority.

## Outcome-learning contract

Future router learning should use privacy-minimized joins such as:

```text
mission/profile digest
 -> workflow/stage/router recommendation
 -> model role/model/provider where observable
 -> fresh/cached/output tokens + TTFT/wall time
 -> tool calls/failures + retries + workflow/model/provider switches
 -> tests/review/human override
 -> accepted/rejected + failure reason + actual/estimated cost
```

The target is: **which eligible workflow/model maximizes probability of accepted completion under this mission's constraints and budget?** Raw sensitive prompts are not routine telemetry.

## Fresh-install / phase evidence

The manual-to-autonomous handoff remains:

```text
clean Hermes bootstrap + one verified OpenRouter model
 -> uplift chat --query-file UPLIFT_MISSION.md
 -> one observable 00-70 phase at a time
```

Phase 20 contains Dogfood Gate A0 for prompt/skill slimming before LCM/Mnemosyne/Spec Kit layering. Checkpoint A starts Phase 30 in a fresh optimized session. Phase 30's advanced candidates remain shadow-only. At Checkpoint C all mandatory P0 security gates pass **before** required human approval may authorize stronger authority. Pi workers begin behind typed containment in Phase 50; routing/model/provider promotion is Phase 60 and follows the same evidence-first approval ordering.

## LCM + Mnemosyne evidence status

Architecture status: **selected baseline**.

Evidence status: **researched + config/repository/site validated; not yet target-Mac validated.** Phase 20 must still prove exact LCM recovery, Mnemosyne relevance/admission, offline operation after provisioning, independent backup/restore, resource use and poisoning/contradiction behavior on the target Mac.

## Remaining target-machine / production P0 evidence

Unattended production authority still requires:

- actual fresh-install/manual-bootstrap rehearsal on the target Mac;
- Phase-20 Dogfood Gate A0 + full LCM/Mnemosyne target-Mac qualification;
- representative redacted/deduplicated routing corpus with temporal holdout and real outcome joins;
- target-Mac bake-off of rules, minimal embeddings, Aurelio, vLLM Semantic Router and technically feasible research candidates;
- Phase-30 shadow evidence including abstention/OOD, capability/workflow failures, router RSS/latency, switching/cache behavior and accepted-mission regret;
- real OpenRouter model/provider results including effective ZDR/data/provider/fallback/session semantics through the actual integration path;
- external capability/sandbox/network/credential enforcement;
- deterministic egress PII/secret canaries proving prohibited content cannot reach OpenRouter/Auto/direct cloud;
- current Pi RPC `agent_settled` behavior, v2.2 routing provenance and containment evidence;
- LSP compatibility/supply-chain fixtures;
- failure injection for router/framework outage, stale capability catalogs, provider/model fallback, corrupted state/memory, malicious repository/tool output and rollback;
- all mandatory P0 evidence before any policy-required human approval at Checkpoint C or later authority/promotional gates.

## Maturity conclusion

The operating manual is **coherent, source-integrated, smoke-validated and compatible with the early-dogfood `00 -> 70` uplift**. The final pre-launch remediation specifically converted the discovered drift classes into persistent regression checks rather than relying on this review remaining perfect forever.

The repository is suitable to start **controlled Phase 00** once this evidence-only report commit itself passes the same build/validation/Pages deployment gate. This conclusion does **not** pre-approve unattended production authority. The initial router used when Phase 30 arrives remains deterministic eligibility + rules/explicit state + abstention in shadow; routing becomes progressively smarter only when observed Hermes/Pi outcomes justify promotion without weakening hard constraints or operational resilience.
