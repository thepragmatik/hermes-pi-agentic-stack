# Adversarial Architectural Review

Assume the proposed system is wrong until evidence proves otherwise. Each item is a failure hypothesis to test, not a claim that the control is already implemented.

## Routing ontology, eligibility and workflow

### 1. Multi-stage mission is collapsed into `hybrid`
**Failure:** `research -> design -> implementation -> tests -> review` loses stage ownership/tool/model/review semantics. **Control:** multi-label task families + ordered workflow stages in routing contracts. **Kill:** representative multi-stage mission cannot be reconstructed from routing-decision evidence.

### 2. Task-family vocabulary becomes a new rigid taxonomy
**Control:** task families are routing features, not product ontology; add/change only when real outcomes show material routing consequence. Unknown/OOD may abstain.

### 3. Learned router overrides deterministic eligibility
**Failure:** semantic confidence makes `LOCAL_ONLY`, network, ZDR or unavailable capability eligible. **Control:** Tier 0 executes first and wins conflicts; derivation provenance recorded. **Kill:** any learned/framework output changes a hard constraint.

### 4. Stale capability metadata authorizes impossible route
**Failure:** model/tool context/modality/structured-output capability changed upstream. **Control:** runtime capability catalog/version evidence; fail closed and refresh before selection. **Kill:** task reaches a model/agent lacking a required capability.

### 5. Context-window arithmetic is wrong
**Control:** measured request/context/reserve accounting, not model-name assumptions. Include tools/system/output budget. **Kill:** selected model truncates a mandatory input or cannot reserve required output/tool loop.

### 6. Workflow planner creates an unbounded swarm
**Control:** bounded stage graph, explicit agents/capabilities/budget/review; Hermes retains workflow authority. **Kill:** router framework can dynamically create unrestricted agents/tools.

### 7. Router overfits synthetic prompt wording
**Control:** locally redacted real missions/outcomes, mission/repo/session/time holdouts, duplicate removal, temporal canary, shadow before authority.

### 8. Short follow-up text causes stage thrashing
**Control:** durable workflow/session state, hysteresis and switch budget; route stages rather than isolated turns. Measure workflow/model/provider switches.

### 9. Multi-label thresholds explode task count
**Failure:** low thresholds predict every related capability, causing complex workflow/model choice. **Control:** calibrated per-head thresholds, max/compatibility logic, abstention/OOD, stage evidence. **Kill:** task-set size/false-positive rate causes material workflow regret.

### 10. Correlated multi-head ModernBERT errors look like confidence
**Control:** head-wise calibration plus joint error analysis/OOD; deterministic constraints remain external; temporal holdout and shadow.

### 11. Router consumes workstation headroom
**Control:** startup/RSS/CPU/p95/p99 SLO under realistic workstation load; heavy research frameworks stay off hot path.

### 12. Semantic classifier is accurate but workflow is wrong
**Control:** evaluate task/profile inference and whole-workflow outcome separately. Primary decision uses accepted-mission regret/economics.

### 13. Rules look weak only because benchmark labels favor semantics
**Control:** adjudicate workflow/constraint consequences; include economics and abstention. A simpler router is allowed to win.

### 14. OOD mission is confidently forced into known tasks
**Control:** uncertainty/OOD/abstention evaluation; human/resolver path; do not reward forced coverage.

### 15. Deterministic rules accidentally infer privacy from keywords alone
**Failure:** discussing PII is mistaken for containing PII. **Control:** authoritative privacy input/state + typed secret/PII scanners; keyword rules only seed fixture cases, not final DLP.

## Framework adoption / fork risks

### 16. Aurelio Semantic Router becomes the whole architecture
**Control:** use as a Tier-1 component behind contracts; hard eligibility/workflow/economics remain external.

### 17. vLLM Semantic Router signal is mistaken for security authority
**Control:** its PII/jailbreak/auth/etc signals are defense-in-depth or routing features; our external Tier-0 boundary remains authoritative.

### 18. vLLM Semantic Router runtime is heavier than its savings
**Control:** compare full control-plane/Envoy/process/RSS/ops cost against rules/embedding/Aurelio on cost per accepted mission. **Kill:** no material outcome benefit after operational cost.

### 19. vLLM roadmap feature is treated as stable capability
**Control:** pin stable release/docs; distinguish released session-aware routing from evolving agent/workflow/context roadmap; no production dependency on backlog claims.

### 20. Router replay/body capture becomes a privacy store
**Control:** disable or tightly scope request/response capture; redacted hashes/features by default; explicit retention/permissions if replay is needed. **Kill:** sensitive raw missions accumulate unintentionally.

### 21. Semantic cache crosses privacy/tenant boundaries
**Control:** cache namespace/privacy review; exclude sensitive classes; verify no cross-session/tenant semantic retrieval.

### 22. LLMRouter research dependencies leak into hot path
**Failure:** Torch/Transformers/Gradio/PyG/etc become always-resident dependencies. **Control:** research-plane isolation; export only winning small artifact/adapter.

### 23. RouteLLM score is misnamed mission probability
**Control:** RouteLLM-style logic is Tier-3 strong-vs-economical scoring only after eligibility/workflow; recalibrate on our actual model outcomes.

### 24. OpenRouter Auto teacher becomes ground truth
**Control:** Auto disagreement is one weak signal; compare to actual accepted outcomes/human review. Its objective/model pool may drift.

### 25. OpenRouter Auto is queried with unsanitized mission
**Control:** only Tier-0-approved sanitized work may enter Auto shadow. **Kill:** any ineligible/raw-sensitive mission reaches Auto.

### 26. A fork is created for convenience
**Control:** fork gate requires materially valuable unmet requirement, failed/unavailable upstream path, small isolated patch, conformance tests, rebase capacity and benefit > maintenance cost.

### 27. Fork misses upstream security/stability fixes
**Control:** automated upstream delta/security review + canary/conformance suite. **Kill:** fork cannot rebase promptly on a critical upstream fix.

## Model selection and outcome learning

### 28. ModernBERT is trained prematurely
**Control:** rules/embedding/Aurelio/vLLM-config baselines first; representative redacted outcomes, stable ontology, learning curves and holdouts required.

### 29. ModernBERT learns deterministic policy fields
**Control:** do not train heads for known privacy/tool/network/modality/context facts. Learned conflicts cannot override Tier 0.

### 30. Temporal leakage inflates router metrics
**Control:** split by mission/repository/session/time cohort; no adjacent turns/near duplicates across train/test.

### 31. Model quality is confounded with physical provider quality
**Control:** record model and provider separately where observable; compare gateway/provider effects independently.

### 32. Cost per token replaces cost per accepted mission
**Control:** include retries, failures, latency, human intervention, cache and acceptance. Promotional pricing is not architecture.

### 33. Outcome labels encode reviewer/model bias
**Control:** deterministic tests first; independent/blinded review for sampled ambiguous outcomes; record human override and reviewer identity/family class where appropriate.

### 34. Telemetry becomes a sensitive training corpus
**Control:** redacted feature summary/hash by default; raw prompts only explicit sampled local dataset with privacy review/retention.

### 35. Telemetry misses rejected/failed missions
**Control:** log failure reason/retry/abstention/override, not only successful paths; otherwise learning optimizes survivorship bias.

### 36. Provider/model switch cost is omitted
**Control:** model/provider/workflow switch counts, cache-read share, context-transfer cost and behavior regression are part of tertiary objective.

## OpenRouter / Tier-4 gateway

### 37. OpenRouter becomes privacy router
**Control:** Tier 0 decides before request exists. Account ZDR/data policies are defense in depth.

### 38. Model and provider selection are conflated
**Control:** routing-decision separates model role/model from provider policy; telemetry records both.

### 39. Hermes request policy and OpenRouter account/preset policy conflict
**Control:** one tested effective-policy path; do not assume precedence; canary actual provider behavior.

### 40. Unsupported Hermes field is silently assumed enforced
**Failure:** raw OpenRouter supports ZDR/session/performance option but installed Hermes does not forward it. **Control:** prove Hermes, account policy or audited gateway adapter enforces; otherwise block.

### 41. Missing OpenRouter `session_id` invalidates cache economics
**Control:** integration test stable session-key propagation; measure provider/model continuity and cached tokens. Do not claim stickiness from docs alone.

### 42. Sticky provider preserves a degraded endpoint too long
**Control:** session affinity is preference/budgeted state, not absolute; explicit reliability/failure escape and recorded switch reason.

### 43. Cheapest provider causes retries/tool failure
**Control:** eligible-provider filter then accepted-mission economics; benchmark price/latency/throughput sorts against tool quality/retries.

### 44. Physical-provider fallback crosses data policy
**Control:** ZDR/data collection/allowlist constraints are hard provider requirements. **Kill:** fallback lands on provider outside them.

### 45. Model fallback crosses capability/quality floor
**Control:** a different-model fallback must re-run Tier-3 eligibility; gateway cannot silently choose a model missing tools/context/modality/review independence.

### 46. Provider identity is unobservable and attribution is guessed
**Control:** distinguish `unknown` from inferred; do not blame/credit model/router with unsupported provider attribution.

### 47. Auto/fallback becomes permanent by inertia
**Control:** explicit maturity/boundary; Phase 60 promotion from measured evidence only.

### 48. Direct-provider credentials silently expand attack surface
**Control:** no direct keys by default; matched evidence and explicit exception required.

### 49. OpenRouter/provider rate limits dominate latency
**Control:** load/queue/reliability/rate-limit tests; include in accepted-mission economics.

## Context, skills and memory

### 50. Compaction drops a security constraint
**Control:** security/data class lives in deterministic state/policy outside summary conversation.

### 51. SOUL/skill/memory is treated as authorization
**Control:** advisory context never grants structural capability.

### 52. Skill catalogue regrows until slicing loses
**Control:** narrow profile/parent skill/phase references; measure catalog + loaded-support tokens.

### 53. Micro-skill explosion creates trigger ambiguity
**Control:** class-level umbrella + phase refs/scripts; measure wrong/missed selection.

### 54. Pruned reference is assumed active
**Control:** pruned = unloaded; reload before reliance.

### 55. LCM and Mnemosyne both become durable semantic authorities
**Control:** LCM=current-session exact recovery; Mnemosyne=curated cross-session memory; overlapping LCM semantic/proactive/temporal features off initially.

### 56. Memory poisoning gains authority
**Control:** policy/uplift-state/Git/evidence outrank recalled text; strict admission and seeded injection tests.

### 57. “Local-only memory” calls cloud
**Control:** remote sync/embedding/host LLM off; forced-offline proof after provisioning.

### 58. SQLite upgrade/crash loses only copy
**Control:** independent safe backup/restore and canary schema upgrade.

### 59. Memory/plugin schemas erase context savings
**Control:** Tool Search, narrow allowlist, eager/deferred schema token measurement.

### 60. Memory release defaults silently widen behavior
**Control:** stable pins + captured effective config; explicit critical settings.

### 61. Mnemosyne recall is irrelevant/noisy
**Control:** bounded prefetch/admission, relevance/staleness corpus; irrelevant injection is blocking.

### 62. Old `state.db` reimports stale/injected context
**Control:** immutable read-only curation pipeline, no attachment/transplant.

## Bootstrap / restart lifecycle

### 63. Hermes profile is mistaken for sandbox
**Control:** dedicated standard account or independently qualified containment.

### 64. Docker bootstrap mount exposes too much host state
**Control:** qualify exact backend/version/mounts; minimal mounts/no daemon socket.

### 65. Phase-20 slimming stays trapped in old conversation
**Control:** Dogfood A0 fresh same-phase continuation, then Checkpoint A fresh Phase-30 session.

### 66. Router config changes but stale runtime is tested
**Control:** Checkpoint B fresh/reloaded shadow session + exact contract/engine/config evidence.

### 67. Security policy changes without active-process proof
**Control:** Checkpoint C active policy digest/restart evidence.

### 68. Pi workers survive policy/routing/model cutover
**Control:** Checkpoint D recreates disposable workers.

### 69. Promoted session still uses bootstrap router/model
**Control:** Checkpoint E fresh session and captured routing/model/provider pins.

### 70. Phase report exists only in conversation
**Control:** uplift-state boundary report required.

### 71. Agent auto-starts next phase
**Control:** one phase per observable run; persist/report/stop.

## Pi, security and operations

### 72. Orchestrator bypasses Pi after cutover
**Control:** no generic production source-write/arbitrary-shell capability; direct-edit bypass test fails structurally.

### 73. Pi task cannot be traced to route decision
**Control:** task-envelope v2.2 binds mission ID, stage ID and decision hash. **Kill:** outcome cannot join to the decision that selected worker/model role.

### 74. Pi RPC drift creates premature completion
**Control:** current conformance + `agent_settled` completion + retry/reconciliation tests.

### 75. Pi containment is assumed from worktree/RPC
**Control:** external filesystem/process/network/credential boundary.

### 76. Task retry repeats destructive operation
**Control:** idempotency keys, operation journal, reconciliation before replay.

### 77. PII false positives corrupt technical text
**Control:** typed/field-aware scan; block on uncertainty rather than silently mutate code/config.

### 78. PII false negatives leak identifiers/secrets
**Control:** dedicated secret scanner + deterministic recognizers + seeded canaries.

### 79. Same model/provider rubber-stamps its own work
**Control:** deterministic evidence then independent review; high-risk review independence requirement.

### 80. LSP/package update becomes supply-chain path
**Control:** pin/audit/SBOM/compatibility fixtures; no install from untrusted project instructions.

### 81. Spec Kit Lite removes necessary thinking
**Control:** minimum acceptance/non-goals/risk fields and deterministic assurance escalation.

### 82. High Assurance is selected for everything
**Control:** bounded profile selection and measured context/rework.

### 83. Large local router/model ruins workstation UX
**Control:** realistic browser/build/container load, memory pressure/swap SLO.

### 84. Continuous update invalidates routing contracts
**Control:** contract conformance tests + Phase-70 one-component canary/rollback.

### 85. Human approval is treated as a waiver for failed P0 evidence
**Failure:** an operator says “proceed anyway” and Hermes promotes cloud/delegation/coding/production authority despite a failed, missing or unproven mandatory security/privacy/containment gate. **Control:** mandatory P0 evidence gates are evaluated first; policy-required human approval is a separate additive transition gate only after those gates pass. `BLOCKED`/`ROLLBACK` remains authoritative while any mandatory gate is unresolved. **Kill:** any stronger authority is granted because a human approved around a failed/missing P0 gate.

## Promotion decision

Production promotion requires evidence that the whole system improves **accepted-mission quality/economics and long-horizon recovery without weakening hard eligibility/security**. A router with better F1, a cheaper provider, a richer memory or a more sophisticated framework has failed if it increases capability bypass, escaped defects, stale influence, retries, hidden egress, switch/cache waste, human recovery work or rollback uncertainty.
