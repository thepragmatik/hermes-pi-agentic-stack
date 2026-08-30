# Adversarial Architectural Review

This document assumes the proposed system is wrong until evidence proves otherwise.

## 1. Router confidently misclassifies hybrid work

**Failure:** an architecture request includes "implement a prototype" and is routed wholly to research or wholly to Pi coding.

**Consequence:** poor implementation context, unnecessary tokens, or research quality loss.

**Control:** explicit `HYBRID`/abstain class; route to research plan artifact first, then coding task envelope. Train on hybrid examples and score margin, not just top probability.

**Kill criterion:** >1% high-severity model-choice errors on held-out production-like hybrid tasks.

## 2. Router benchmark overfits synthetic prompts

**Failure:** prototype utterances or generated labels look perfect but real missions use project-specific language and long Spec Kit text.

**Control:** reserve chronological live holdout; include actual redacted mission briefs; deduplicate near matches; shadow-test before authority.

## 3. Large local router consumes workstation headroom

**Failure:** a "smart" generative router holds tens of GB and causes browser/build/container memory pressure.

**Control:** router memory SLO; control plane <5 GB target; generative models on demand only.

## 4. Provider switch destroys prefix cache

**Failure:** gateway chases the cheapest/fastest provider each request. Cache hit rate collapses; TTFT and fresh-input bill rise.

**Control:** session-affine provider pinning; cache-adjusted provider score; switch only on explicit failure policy.

## 5. Cheap provider has poor tool correctness

**Failure:** $/token optimization produces more invalid tool calls/retries than a slightly more expensive provider.

**Control:** optimize **cost per accepted task**, not token price. Track retries, tool-schema validity, test pass and wall time.

## 6. Launch pricing disappears

**Failure:** promotional rate ends and destroys a budget forecast.

**Control:** model economics use list price for steady-state design; promotional price shown separately. Pricing belongs in periodically refreshed config, not hardcoded policy.

## 7. Prompt cache makes token dashboard look unchanged

**Failure:** cached tokens remain in logical usage counts and the team concludes caching failed.

**Control:** separate logical input, fresh input, cached input, cost and TTFT metrics.

## 8. Context compaction drops a security constraint

**Failure:** free-form summary forgets "do not send customer records to cloud" after many turns.

**Control:** security/data class is deterministic task state outside conversation/memory; re-injected and validated separately; post-compaction invariants.

## 9. SOUL.md treated as authorization

**Failure:** child ignores or never receives security prose.

**Control:** no security capability depends on SOUL. Sandbox/toolset/egress enforcement is external.

## 10. Orchestrator bypasses Pi

**Failure:** parent decides direct edits are more efficient.

**Control:** production orchestrator profile has no write/shell capabilities after cutover. Only an explicitly separate bootstrap/emergency profile can retain temporary authority.

## 11. Pi RPC protocol changes on update

**Failure:** Pi update breaks bridge event handling or completion semantics.

**Control:** pin known-good version; protocol conformance test; treat `agent_settled` as completion; independent Hermes/Pi version locks; automatic rollback.

## 12. LSP extension becomes supply-chain path

**Failure:** third-party extension update runs unexpected code or accesses broader filesystem.

**Control:** pin/review/version; sandbox extension/LSP process; lockfile/SBOM; no auto-install from project content.

## 13. Kotlin LSP instability

**Failure:** Gradle/Android project import or refactor breaks.

**Control:** official LSP with project compatibility tests; graceful fallback to compiler/test navigation; explicit semantic-refactor gate.

## 14. LSP diagnostics flood context

**Failure:** thousands of workspace errors get appended to model calls.

**Control:** changed-file/high-severity cap; counts + on-demand detail.

## 15. PII scanner false negatives

**Failure:** custom account/customer identifiers are not recognized.

**Control:** deterministic organization-specific recognizers, seeded canaries, ensemble shadow testing, local-only class for sensitive projects.

## 16. PII scanner false positives corrupt code

**Failure:** identifiers/examples are redacted and code generation becomes invalid.

**Control:** field-aware scanning; only transform policy-approved natural-language/content fields; block rather than silently mutate when uncertainty is high.

## 17. Secret scanner confused with PII scanner

**Failure:** PII detector catches names/emails but an API token leaves the machine.

**Control:** dedicated secret layer before PII NER; high-confidence credential formats always block.

## 18. Old Hermes DB reintroduces context bloat/injection

**Failure:** bulk import restores stale mission instructions and huge memories.

**Control:** immutable/read-only legacy archive; curated local export; independent PII/secret sanitization; provenance/current-truth review; never attach the old DB as production memory.

## 19. Spec Kit Lite becomes "skip thinking"

**Failure:** token optimization strips requirements and increases rework.

**Control:** minimum acceptance/non-goals/risk fields in every profile; profile escalates automatically on ambiguity/security/blast radius; compare accepted-task quality.

## 20. Spec Kit full flow remains in every task because agents choose safety

**Failure:** model conservatively chooses High Assurance for everything.

**Control:** deterministic minimum/maximum profile policy with measurable selection criteria; human can escalate.

## 21. RouteLLM historical weights are assumed universal

**Failure:** historical preference model sends current target models incorrectly.

**Control:** RouteLLM is experimental until recalibrated/retrained on paired target-model outcomes. Do not call its pretrained score "coding probability".

## 22. Dataset licenses contaminate a distributable router

**Failure:** gated/custom/noncommercial data becomes embedded in a model intended for unrestricted redistribution.

**Control:** dataset bill of materials; separate internal-use and distributable recipes; prefer compatible data; legal review where needed.

## 23. Raw telemetry becomes a new privacy database

**Failure:** optimization logs preserve prompts/source snippets.

**Control:** local redaction before logging; feature/outcome telemetry over raw text; short retention; encryption/access controls.

## 24. Task retry repeats destructive operation

**Failure:** worker is restarted and reruns migration/delete/publish.

**Control:** task idempotency keys, command classes, durable operation journal, explicit non-repeatable operation acknowledgement.

## 25. Reviewer shares implementer blind spot

**Failure:** same model/provider reviews its own work and rubber-stamps it.

**Control:** deterministic tests first; independent reviewer process; diversify model for high-risk tasks; protected human gate where required.

## 26. Docker is mistaken for complete macOS isolation

**Failure:** mounted HOME/socket/credential paths expose host secrets or Docker daemon gives broad host authority.

**Control:** minimal mounts, no daemon socket, scrub env, dedicated HOME, network policy, stronger VM/sandbox where necessary.

## 27. Offloading/paging works in a benchmark but ruins sustained UX

**Failure:** a huge local model runs once but creates memory pressure/swap during actual multitasking.

**Control:** benchmark under realistic browser/build load; monitor memory pressure and swap; reject steady-state swap dependency.

## 28. Daily upstream updates silently invalidate uplift assumptions

**Failure:** Hermes/Pi/plugin interfaces change while the overlay still "works" superficially.

**Control:** update on disposable canary; smoke/protocol/security/context/memory tests; compare prompt/cache/recall metrics; promote pinned versions only on pass.

## 29. Cost savings are dominated by reasoning/output tokens

**Failure:** input-cache optimization looks great but reasoning expands billed output.

**Control:** log reasoning accounting where available; cap reasoning by mission class; evaluate accepted quality vs total cost.

## 30. Throughput limit, not price, becomes bottleneck at high token volume

**Failure:** cheapest endpoint cannot sustain concurrency/rate limits and queues tasks.

**Control:** load-test concurrency/quotas/failover; include queue delay in score; maintain policy-compatible fallback.

## 31. LCM and Mnemosyne both become cross-session memory authorities

**Failure:** LCM semantic/proactive recall and Mnemosyne durable recall are enabled together. The same fact is independently summarized/stored/recalled, producing duplicate context, disagreement and unclear provenance.

**Control:** initial ownership is strict: LCM=current-session context/compaction recovery; Mnemosyne=curated durable cross-session memory. Keep LCM temporal/proactive/cross-session semantic features disabled while qualifying the pair. Measure duplicate recall and injected-token rate.

**Kill criterion:** the operator/agent cannot deterministically answer which store owns a remembered fact or duplicate recall materially affects decisions/tokens.

## 32. Memory poisoning gains authority after being remembered

**Failure:** malicious project/tool text is captured into Mnemosyne or recovered through LCM, then later appears trustworthy because it is "memory."

**Control:** all remembered/recovered text remains untrusted advisory context. Policy, uplift-state, current repository/spec/ADR truth and immutable evidence outrank memory. Curated Mnemosyne writes require provenance; canary uses write approval and strict classification. Add seeded prompt-injection memories and verify they cannot change capability/privacy policy.

**Kill criterion:** recalled content changes a security/acceptance decision without independent authoritative evidence.

## 33. "Local-only" context/memory silently falls back to network

**Failure:** embedding, consolidation, host-LLM, remote sync or auxiliary recall quietly uses a cloud endpoint when the local path fails.

**Control:** explicitly disable remote sync, embedding API, host/remote LLM paths and automatic LLM-backed consolidation in the initial Mnemosyne canary. Provision packages/models first, then run LCM compaction/recovery and Mnemosyne write/recall with outbound network denied.

**Kill criterion:** any required context/memory operation fails because a remote service is unavailable or makes unexpected outbound connections.

## 34. SQLite/store upgrade or crash loses context/memory

**Failure:** LCM/Mnemosyne schema upgrade, WAL handling, disk-full condition or abrupt process death corrupts the only useful store.

**Control:** never upgrade the only production DB first; use plugin-supported/quiescent backup; preserve DB/WAL/SHM consistency; test restart, integrity, backup restore and rollback on a copied canary; retain built-in/session-history fallback.

**Kill criterion:** restart/restore cannot prove recovery or rollback without deleting/rewriting the only surviving copy.

## 35. Plugin tool schemas erase context-slimming gains

**Failure:** LCM + Mnemosyne expose enough tools that their schemas become a large always-hot prompt prefix, offsetting skill slicing and compaction savings.

**Control:** enable Hermes Tool Search for non-core plugin/provider tools; measure eager vs deferred schema tokens, discovery accuracy and cold-tool round trips; keep tool membership stable within a phase to protect prompt-cache affinity.

**Kill criterion:** added schema/injected-memory tokens materially erase the net accepted-task token/cost benefit.

## 36. Release/default drift silently enables autonomous memory behavior

**Failure:** a new Mnemosyne/LCM release changes defaults (autosave, persona, auto-sleep, LLM path, recall features, schema) and production behavior expands without deliberate review.

**Control:** pin stable releases/commits; capture effective runtime config/status in evidence; set critical conservative values explicitly rather than trusting defaults; canary every release and inspect security notes/schema changes before promotion. Do not auto-promote RCs.

**Kill criterion:** production behavior depends on an unrecorded default or a release changes memory/network authority without an explicit policy/config diff.

# Promotion decision

Production promotion requires evidence that the system improves **accepted-task cost, latency and long-horizon recovery without degrading accepted-task quality or weakening privacy/security**. A token-saving or memory-rich system that increases retries, irrelevant recall, human intervention, stale-policy influence or escaped defects has failed even when its isolated benchmark scores look better.
