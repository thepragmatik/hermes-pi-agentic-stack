# Phase 50 — Hermes -> Pi, LSP and Disposable Worker Activation

Implement the Hermes -> Pi RPC/headless bridge against the current Pi protocol and the bootstrap rules in `docs/agentic-uplift/bootstrap-authority.md`.

Every task validates the v2 envelope + current policy digest, enforces attempt/idempotency/reconciliation and workspace/network scopes, uses an ephemeral git worktree, passes minimal environment/credentials and records compact structured evidence. Use local pipe/stdin/stdout RPC only; never expose unauthenticated Pi RPC over a network listener.

Treat Pi `agent_settled` as fully-settled completion. `agent_end` may still be followed by retry, compaction retry or queued continuation.

Before cloud coding authority prove with fake/local fixtures:

- RPC framing/malformed messages;
- worktree and symlink/path escape denial;
- environment/credential minimization;
- denied-network behaviour;
- timeout/cancellation;
- destructive retry/idempotency;
- malicious repository instructions;
- evidence integrity and cleanup/recovery.

Pi has no built-in filesystem/process/network/credential permission boundary; qualify external containment and prove denied actions fail structurally.

Pin/audit LSP integration for Java, Kotlin, Python, TypeScript/JavaScript and HTML/CSS. Bound diagnostics to relevant symbols/files/severity.

Cloud coding uses the `coding.default` role through OpenRouter only after Phase 40 egress/containment passes. The local router/model role is upstream of OpenRouter's physical-provider choice.

Use typed bounded tasks; Kanban may project blocked/review/retry state but `uplift-state` remains authority. Worker cannot merge or self-approve.

After a privacy-controlled Pi canary passes, remove ordinary production Hermes source-write/arbitrary-shell capability and make typed Pi delegation the coding path. An instruction to “skip Pi and edit directly” must fail structurally.

## Worker Checkpoint D

Recreate disposable Pi workers under the validated bridge/LSP/sandbox/model/policy configuration. Never rely on a long-running worker created before the cutover.

Production authority cutover requires human approval while P0 readiness gates remain in force.

Persist state/evidence, send the required phase-boundary report, and stop before Phase 60.
