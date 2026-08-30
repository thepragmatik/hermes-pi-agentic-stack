# Adversarial Architectural Review

Assume the proposed system is wrong until evidence proves otherwise. Each item is a failure hypothesis to test, not a claim that the control is already implemented.

## Routing, models and economics

### 1. Hybrid mission is forced into one lane
**Failure:** architecture + implementation work is routed wholly to research or coding. **Control:** explicit `hybrid`/abstain; research artifact then typed coding task; score margin and downstream regret. **Kill:** >1% high-severity wrong-lane errors on representative holdout.

### 2. Router overfits synthetic prompts
**Control:** redacted real missions, mission/repo/session/time holdout, near-duplicate removal, shadow before authority.

### 3. Router consumes workstation headroom
**Control:** small encoder/head; local control-plane memory SLO; generative models on demand only.

### 4. Provider churn destroys prefix cache
**Failure:** cheapest/fastest physical provider is reconsidered every request. **Control:** phase/session affinity, track physical-provider continuity + cache-read share, switch only on explicit failure/regret policy.

### 5. Cheap endpoint creates expensive retries
**Control:** optimize cost/minutes/retries/human intervention per **accepted task**, not nominal $/M.

### 6. Promotional pricing becomes architecture
**Control:** volatile prices live in measured config/evidence; steady-state decisions survive promotion expiry.

### 7. Cached tokens are misread as no savings
**Control:** separate logical/fresh/cached input, output/reasoning, cost and TTFT.

### 8. RouteLLM score is misnamed mission probability
**Control:** RouteLLM-style logic is optional difficulty/preference escalation only after pair-specific recalibration.

### 9. ModernBERT is fine-tuned prematurely
**Failure:** synthetic labels create a sophisticated wrong boundary. **Control:** rules -> frozen embeddings/head -> representative redacted outcomes -> fine-tune only after stable ontology/holdout/plateau.

### 10. Router telemetry becomes a privacy corpus
**Control:** outcome/features over raw prompts; local redaction; short retention; controlled sampled training records.

## OpenRouter gateway

### 11. OpenRouter Auto becomes the privacy router
**Failure:** Auto/fallback sends data that local policy should keep local. **Control:** deterministic privacy decision executes before any OpenRouter call; `LOCAL_ONLY` exits the cloud path. **Kill:** any seeded `LOCAL_ONLY` payload reaches OpenRouter.

### 12. OpenRouter Auto replaces the final mission classifier
**Failure:** local router is built but ignored because Auto is convenient. **Control:** Auto only bootstrap/shadow/bounded fallback; evidence records actual role/model; production lane comes from local router.

### 13. Model selection and provider selection are conflated
**Failure:** physical provider choice silently changes the model/mission semantics. **Control:** local router -> role/model binding -> OpenRouter model ID -> physical-provider routing; log both layers distinctly.

### 14. Hermes request policy overrides OpenRouter preset policy
**Failure:** a preset looks privacy-restricted, but request-level `provider_routing` changes provider constraints. **Control:** do not use preset as sole authority; one canonical Hermes request policy + account/workspace guardrails; effective-policy canary. **Kill:** observed provider violates intended privacy/parameter constraint.

### 15. OpenRouter account guardrail is mistaken for local DLP
**Control:** account ZDR/data restrictions are defense in depth. Local secret/PII/egress gate still decides whether the request exists at all.

### 16. Exacto/tool routing fights cache stickiness
**Failure:** tool-accuracy provider reordering constantly changes provider and destroys prefix cache. **Control:** benchmark accepted-task quality vs cache loss; use sticky/explicit routing policy where it wins.

### 17. Stale model slug breaks bootstrap
**Control:** `hermes model` live picker at install; record resolved ID; snapshot slugs are examples only; stop on unavailable/incompatible tool model.

### 18. One bootstrap model becomes permanent by inertia
**Control:** Phase 30/60 explicitly benchmark role separation; Bootstrap Mode ends only by evidence, not convenience.

### 19. Direct-provider fallback silently expands credential surface
**Control:** no direct key by default. Add direct Z.ai/DeepSeek only after matched benchmark justifies the additional secret/integration; fallback cannot activate merely because a key exists.

### 20. OpenRouter/provider rate limit is the real bottleneck
**Control:** concurrency/load/queue/fallback testing; include queue delay and reliability in accepted-task economics.

## Context, skills and memory

### 21. Compaction drops a security constraint
**Control:** security/data class lives in deterministic state/policy outside summarised conversation; validate after compaction.

### 22. SOUL/skill/memory is treated as authorization
**Control:** no capability depends on advisory text; external enforcement wins.

### 23. Skill catalogue grows until slicing loses
**Control:** narrow profile/`--no-skills`, class-level parent, measure catalogue + loaded-support tokens.

### 24. Micro-skill explosion creates trigger ambiguity
**Control:** class-level umbrella skill + phase references/scripts; measure wrong/missed selection.

### 25. Pruned reference is assumed still active
**Control:** pruned = unloaded; reload current slice before relying on it.

### 26. LCM + Mnemosyne both become durable semantic authorities
**Control:** LCM=current-session context/recovery; Mnemosyne=curated cross-session memory; LCM semantic/proactive/temporal cross-session families off in baseline. **Kill:** provenance/owner of a recalled fact cannot be determined.

### 27. Memory poisoning gains authority
**Control:** recalled/recovered text remains untrusted; policy/uplift-state/Git/immutable evidence outrank memory; strict Mnemosyne admission and seeded injection tests. **Kill:** memory changes security/acceptance without authoritative evidence.

### 28. “Local-only memory” silently calls cloud
**Control:** remote sync/embedding/host-LLM/auto-synthesis off; after provisioning, deny outbound network and prove compaction/write/recall/restart.

### 29. SQLite upgrade/crash loses the only store
**Control:** quiescent/plugin-supported backups, WAL consistency, canary schema upgrades, restore/rollback tests, never upgrade only surviving DB first.

### 30. Memory/plugin schemas erase context savings
**Control:** Hermes Tool Search, narrow Mnemosyne allowlist, measure eager/deferred schema tokens + cold-tool cost.

### 31. Release defaults silently widen memory behaviour
**Control:** stable pins + captured effective config; explicit critical values; RC/beta not auto-promoted.

### 32. Mnemosyne recall is irrelevant/noisy
**Control:** bounded prefetch, strict admission, relevance/staleness corpus; stable 3.15.x baseline must pass irrelevant-injection tests before authority.

### 33. Old `state.db` reimports stale/injected context
**Control:** immutable evidence only; local discovery/minimal export/sanitization/provenance/current-truth review; never attach old DB.

## Bootstrap and restart lifecycle

### 34. Hermes profile is mistaken for sandbox
**Control:** dedicated standard macOS account or independently qualified containment. `terminal.cwd`, profile and SOUL are not filesystem security.

### 35. Docker bootstrap mount exposes too much host state
**Control:** qualify exact Hermes Docker backend/version/mount provenance; minimal mounts/no daemon socket; do not assume `docker_mount_cwd_to_workspace` is safe just because it is named “sandbox”.

### 36. Phase 20 improvement remains trapped in old chat context
**Failure:** slim config passes but the same giant bootstrap transcript continues. **Control:** mandatory Checkpoint A fresh Hermes session. **Kill:** Phase 30 benchmark runs in pre-optimization session.

### 37. Router config is changed but stale process/session is tested
**Control:** Checkpoint B reload/fresh shadow session and evidence of effective config/hash.

### 38. Security policy changes without process restart
**Control:** Checkpoint C records active policy digest and restarts/reloads enforcement processes when required.

### 39. Pi workers survive the cutover with old env/policy/model
**Control:** Checkpoint D recreates disposable workers; do not reuse stale long-running worker state.

### 40. “Promoted” session still uses old bootstrap model/router
**Control:** Checkpoint E fresh ordinary session + captured model/provider/router/context pins.

### 41. Phase report exists only in conversation
**Failure:** crash/new session loses warnings/restart decision. **Control:** uplift-state v1.1 requires boundary report for COMPLETE/BLOCKED/ROLLBACK.

### 42. Agent auto-starts next phase before human sees boundary
**Control:** mission/skill contract says one phase per observable run; persist/report/stop.

## Pi, security and operations

### 43. Orchestrator bypasses Pi after cutover
**Control:** production orchestrator has no generic source-write/arbitrary-shell capability; direct-edit bypass test must fail structurally.

### 44. Pi RPC drift creates premature completion
**Control:** current protocol conformance; `agent_settled` completion; pinned independent versions; retry/reconciliation tests.

### 45. Pi containment is assumed from RPC/worktree
**Control:** external filesystem/process/network/credential boundary; deny actions structurally under malicious instructions.

### 46. Task retry repeats destructive operation
**Control:** idempotency keys, durable operation journal, reconciliation before replay, explicit non-repeatable operation handling.

### 47. PII false positives corrupt technical text
**Control:** typed/field-aware scanning; distinguish code/config from prose; block on uncertainty rather than silently mutate.

### 48. PII false negatives leak organization identifiers
**Control:** custom deterministic recognizers + seeded canaries + local-only class; secret scanner remains separate and first.

### 49. Same model/provider rubber-stamps its own work
**Control:** deterministic evidence first, independent reviewer; high-risk review should use independent model family or protected human gate.

### 50. LSP/package update is a supply-chain path
**Control:** pin/audit/SBOM/compatibility fixtures; no install from untrusted project instructions; containment.

### 51. Spec Kit “Lite” removes necessary thinking
**Control:** minimum acceptance/non-goals/risk fields and deterministic assurance escalation; compare accepted quality.

### 52. High Assurance is chosen for everything
**Control:** deterministic profile selection bounds; measure context/rework; human may escalate.

### 53. Huge local model/offload ruins workstation UX
**Control:** realistic browser/build/container load; memory pressure/swap SLO; reject steady-state swap dependency.

### 54. Continuous update invalidates overlay assumptions
**Control:** Phase 70 one-component canary, new session/workers where required, protocol/security/context/memory/router/provider/LSP tests and rollback.

## Promotion decision

Production promotion requires evidence that the whole system improves **accepted-task quality/economics and long-horizon recovery without weakening privacy/security**. A cheaper, more cached, more “memory-rich” or more autonomous system has failed if it increases escaped defects, stale influence, retries, hidden egress, human recovery work or rollback uncertainty.
