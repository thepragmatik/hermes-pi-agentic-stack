# Adversarial Architectural Review

This document assumes the proposed system is wrong until evidence proves otherwise.

## 1. Router confidently misclassifies hybrid work

**Failure:** an architecture request includes "implement a prototype" and is routed wholly to DeepSeek research or wholly to Pi coding.

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

**Failure:** GLM-5.3-Flash promotional rate doubles after the launch period and destroys a budget forecast.

**Control:** model economics use list price for steady-state design; promotional price shown separately. Pricing pulled into a periodically refreshed config, not hardcoded into policy.

## 7. Prompt cache makes token dashboard look unchanged

**Failure:** team expects cached tokens to vanish from usage counts and concludes caching failed.

**Control:** separate logical input, fresh input, cached input, cost and TTFT metrics.

## 8. Context compaction drops a security constraint

**Failure:** free-form summary forgets "do not send customer records to cloud" after many turns.

**Control:** security/data class stored in deterministic task state outside conversation; re-injected/validated separately; post-compaction invariants.

## 9. SOUL.md treated as authorization

**Failure:** child ignores or never receives security prose.

**Control:** no security capability depends on SOUL. Sandbox/toolset/egress enforcement is external.

## 10. Orchestrator bypasses Pi

**Failure:** parent decides direct edits are more efficient.

**Control:** orchestrator profile has no write/shell capabilities. Only explicit maintenance profile can alter this.

## 11. Pi RPC protocol changes on update

**Failure:** daily Pi update breaks bridge event handling.

**Control:** pin known-good version; protocol conformance test; independent Hermes/Pi version locks; automatic rollback to previous Pi package.

## 12. LSP extension becomes supply-chain path

**Failure:** third-party extension update runs unexpected code or accesses broader filesystem.

**Control:** pin/review/version; sandbox extension/LSP process; lockfile/SBOM; no auto-install from project content.

## 13. Kotlin LSP Alpha instability

**Failure:** Gradle/Android project import or refactor breaks.

**Control:** official JetBrains LSP with project-level compatibility tests; graceful fallback to compiler/test navigation for normal edits; require explicit LSP pass for semantic refactor tasks.

## 14. LSP diagnostics flood context

**Failure:** thousands of workspace errors get appended to model calls.

**Control:** changed-file/high-severity cap; counts + on-demand detail.

## 15. PII scanner false negatives

**Failure:** custom account/customer identifiers are not recognized.

**Control:** deterministic organization-specific recognizers, seeded canaries, ensemble shadow testing, local-only class for sensitive projects.

## 16. PII scanner false positives corrupt code

**Failure:** identifiers/examples are redacted and code generation becomes invalid.

**Control:** field-aware scanning; only redact cloud-bound natural-language/content fields according to policy; code transformations require explicit entity types and tests. Block instead of silently mutating when uncertainty is high.

## 17. Secret scanner confused with PII scanner

**Failure:** Presidio catches names/emails but an API token leaves the machine.

**Control:** dedicated secret layer before PII NER; high-confidence credential formats always block.

## 18. Old Hermes DB reintroduces context bloat/injection

**Failure:** bulk-import restores stale mission instructions and huge memories.

**Control:** read-only migration; export candidate facts/artifacts; scan/dedupe/human or reviewer approval; import only durable normalized entries.

## 19. Spec Kit Lite becomes "skip thinking"

**Failure:** token optimization strips requirements and increases rework.

**Control:** minimum acceptance/non-goals/risk fields in every profile; profile escalates automatically on ambiguity/security/blast radius; compare accepted-task quality.

## 20. Spec Kit full flow remains in every task because agents choose safety

**Failure:** model conservatively chooses High Assurance for everything.

**Control:** deterministic minimum/maximum profile policy with measurable selection criteria; human can escalate.

## 21. RouteLLM historical weights are assumed universal

**Failure:** GPT-4/Mixtral preference model sends DeepSeek/GLM incorrectly.

**Control:** RouteLLM is experimental until recalibrated/retrained on paired target-model outcomes. Do not call its pretrained score "coding probability".

## 22. Dataset licenses contaminate a distributable router

**Failure:** gated/custom/noncommercial data becomes embedded in a model intended for unrestricted redistribution.

**Control:** dataset bill of materials; separate internal-use and distributable training recipes; prefer Apache/MIT/compatible data for the distributable model; legal review for ODC/custom terms.

## 23. Raw telemetry becomes a new privacy database

**Failure:** optimization logs preserve prompts/source snippets.

**Control:** local redaction before logging; feature/outcome telemetry over raw text; short retention for sampled training records; encryption/access controls.

## 24. Task retry repeats destructive operation

**Failure:** worker is restarted and reruns migration/delete/publish.

**Control:** task idempotency keys, command classes, durable operation journal, explicit non-repeatable operation acknowledgement.

## 25. Reviewer shares implementer blind spot

**Failure:** same model/provider reviews its own work and rubber-stamps it.

**Control:** deterministic tests first; independent reviewer process; diversify model for high-risk tasks; protected human gate where required.

## 26. Docker is mistaken for complete macOS isolation

**Failure:** mounted HOME/socket/credential paths expose host secrets or Docker daemon gives broad host authority.

**Control:** minimal mounts, no daemon socket, scrub env, dedicated HOME, network policy, consider stronger VM/sandbox for untrusted builds.

## 27. Offloading/paging works in a benchmark but ruins sustained UX

**Failure:** a huge local model runs once but creates memory pressure/swap during actual multitasking.

**Control:** benchmark under realistic browser/build load; monitor memory pressure and swap; reject steady-state swap dependency.

## 28. Daily upstream updates silently invalidate uplift assumptions

**Failure:** Hermes context/prompt interfaces change while overlay still "works" superficially.

**Control:** daily update on canary clone; smoke + protocol + security tests; compare prompt-size/cache metrics; promote pinned version only on pass.

## 29. Cost savings are dominated by reasoning/output tokens

**Failure:** input cache optimization looks great but high reasoning effort expands billed output.

**Control:** log hidden/visible reasoning accounting where provider exposes it; cap reasoning by mission class; evaluate quality vs output cost.

## 30. Throughput limit, not price, becomes bottleneck at 4B tokens/month

**Failure:** cheapest endpoint cannot sustain concurrency/rate limits and queues tasks.

**Control:** load-test target concurrency, provider quotas and failover; include queue delay in cost/quality score; maintain at least one policy-compatible fallback.

# Promotion decision

Production promotion requires evidence that the system improves **accepted-task cost and latency without degrading accepted-task quality or weakening privacy/security**. A token-saving system that increases retries, human intervention or escaped defects has failed even when the billing dashboard looks better.
