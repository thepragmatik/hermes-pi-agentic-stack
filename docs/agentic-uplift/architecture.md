# Architecture — Canonical Text Representation

This Markdown is canonical for agents and reviewers. SVG/HTML diagrams are presentation views.

## Components and trust boundaries

1. **Terminal/User** submits a mission to Hermes.
2. **Hermes control plane** may read, plan, route, delegate and review but has no direct arbitrary shell/source-write/merge authority in orchestrator mode.
3. **Policy & privacy gate** deterministically classifies trust/privacy and enforces egress preconditions before learned routing.
4. **Local router** runs rules, then a tiny semantic classifier, then an uncertainty/difficulty gate. It emits `research`, `coding`, `hybrid`, `local_only` or `abstain` plus confidence/reason.
5. **Research executor** is a session-pinned cloud model/provider role.
6. **Pi bridge** validates a typed task envelope, creates an isolated worktree/sandbox and launches a bounded Pi worker.
7. **Pi worker** performs coding/tool loops using a coding-model role and LSP servers; it cannot merge its own change.
8. **Evidence/review gate** runs tests, LSP diagnostics, PII/secret scans and independent review.
9. **Merge/Human gate** promotes only accepted evidence.
10. **Durable state store** records phase/checkpoint/evidence state independently of model context.

## Core data flow

`mission -> policy/privacy -> router -> {research | Pi task graph | local-only} -> evidence -> review -> merge`

Stable context precedes volatile context in prompts: security/invariants and stable tool schemas first; project summary/retrieved slices next; current task and latest tool output last. Provider/model remains sticky inside a session when possible so prefix-cache affinity is preserved.

## Non-negotiable invariants

- Security is enforced outside prompts.
- `LOCAL_ONLY` never enters a cloud model/router.
- Coding crosses the Hermes→Pi typed boundary.
- Worker write/network/credential scopes are explicit and default-deny.
- Implementer cannot self-approve merge.
- Durable state, not conversation, determines whether a phase/task already executed.
- Large local generative models are on-demand reviewers/fallbacks, not always-on routers.
- Upstream Hermes/Pi remain independently upgradeable dependencies.
