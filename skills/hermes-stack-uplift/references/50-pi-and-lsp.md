# Phase 50 — Pi, LSP and Authority Cutover

Implement the Hermes -> Pi RPC/headless bridge against the current Pi protocol and the bootstrap rules in `docs/agentic-uplift/bootstrap-authority.md`.

Validate every task against the v2 envelope, bind the current policy digest, enforce idempotency/attempt semantics and workspace/network scopes, use ephemeral git worktrees, and collect structured evidence. Use local pipe/stdin/stdout RPC only; never expose Pi RPC as an unauthenticated network service.

Treat Pi `agent_settled` as task-run completion. `agent_end` is only the end of a low-level run and may still be followed by retry, compaction retry or queued continuation.

Before cloud-enabled canary work, prove with fake/local fixtures:

- RPC framing and malformed-message handling;
- worktree isolation and symlink/path escape denial;
- minimal environment/credential exposure;
- denied-network behavior;
- timeout/cancellation;
- duplicate destructive retry/idempotency handling;
- malicious repository instruction containment;
- evidence integrity and cleanup/recovery.

Pi has no built-in filesystem/process/network/credential permission boundary. Qualify a pinned external sandbox/container/micro-VM/capability-broker layer and prove denied actions fail structurally.

Pin/audit LSP integration and language servers for Java/Kotlin/Python/TypeScript/JavaScript/HTML/CSS. Bound diagnostics/context injection to relevant symbols/files.

After a non-sensitive privacy-controlled Pi canary passes, complete the authority cutover:

1. switch production Hermes to the constrained orchestrator profile;
2. remove generic source-write and arbitrary-shell capability from that profile;
3. make typed Pi delegation the only coding execution path;
4. verify an explicit instruction to skip Pi and edit directly fails structurally;
5. record the new policy digest and cutover evidence.

Worker cannot merge or self-approve. Bootstrap authority may remain only in a disposable emergency/canary profile and is never silently re-enabled for normal operation.
