# Architecture — Canonical Text Representation

This Markdown plus `architecture.graph.json` is canonical for deterministic agent/reviewer interpretation. SVG/HTML diagrams are presentation views.

## Components and trust boundaries

1. **Terminal/User** performs the minimal manual bootstrap and submits the staged mission to Hermes.
2. **Hermes control plane** plans, routes, delegates and reviews. Temporary direct bootstrap authority is canary-scoped; steady-state orchestrator authority cannot bypass Pi for coding.
3. **LCM + Mnemosyne** provide local current-session context recovery and curated cross-session durable memory. Neither is execution/security authority.
4. **Tier-0 policy/privacy gate** deterministically decides local/cloud eligibility and egress requirements before learned/model/provider routing.
5. **Local mission router** uses rules/state, then a compact embedding classifier and later ModernBERT only if evidence earns it. It emits `research`, `coding`, `hybrid`, `review`, `auxiliary`, `local_only` or `abstain` plus confidence/reason.
6. **Model-role binder** maps the lane to a versioned model role. Volatile concrete model IDs live in config/locks/evidence.
7. **OpenRouter gateway** is the default external inference gateway. It receives only policy-approved cloud work and may select a physical inference provider subject to our provider-routing/privacy/parameter constraints. OpenRouter Auto is not the privacy gate or final mission router.
8. **Research/review executor** runs the selected cloud model role through OpenRouter (or a deliberately qualified direct-provider exception).
9. **Pi bridge** validates a typed task envelope + policy digest, creates an isolated worktree/containment boundary and launches a bounded Pi worker.
10. **Pi worker** performs coding/tool loops using the coding role and LSP servers; it cannot merge/self-approve.
11. **Evidence/review gate** runs tests, LSP fixtures, secret/PII/egress scans and independent review.
12. **Merge/Human gate** promotes only accepted evidence according to maturity/approval policy.
13. **Durable uplift state** records phase/checkpoint/report/restart/adoption state independently of model context.

## Core data flow

```text
mission
 -> local Tier-0 privacy/security policy
 -> local mission router
 -> model-role binding
 -> OpenRouter model ID
 -> policy-compatible physical provider
 -> {research/review | typed Pi task | auxiliary}
 -> evidence
 -> review/merge gate
```

`LOCAL_ONLY` exits the cloud path before OpenRouter.

## Bootstrap data flow

```text
clean narrow Hermes
 -> OpenRouter
 -> one verified GLM-Flash-class bootstrap model
 -> 00 preflight
 -> 10 baseline
 -> 20 context/skills + LCM/Mnemosyne
 -> fresh session (Checkpoint A)
 -> 30 router shadow
 -> 40 security authority gate
 -> 50 Pi/LSP workers
 -> 60 multi-role promotion
 -> 70 recurring upgrades/rollback
```

## Context and state ownership

```text
T0 stable prefix = identity/invariants/small skill+tool catalogue
T1 mission capsule = current bounded phase/objective/constraints/evidence pointers
T2 artifacts = full logs/diffs/research/specs/benchmarks/RPC, fetched on demand
LCM = current-session exact context/compaction recovery
Mnemosyne = curated cross-session durable memory
state.db = raw Hermes session history/forensic search
uplift-state = deterministic mission authority
Git/ADR/spec = project truth
Kanban = optional operational projection
```

Stable prefix and role/model/provider should remain sticky within a phase/session when that improves cache continuity and behavioural consistency.

## Non-negotiable invariants

- Security/privacy/capability decisions are enforced outside prompts, memory and OpenRouter.
- `LOCAL_ONLY` never enters OpenRouter or a direct cloud provider.
- The local router chooses lane/model role/model; OpenRouter only routes the downstream physical provider within policy.
- OpenRouter Auto cannot override local policy or replace the final mission classifier.
- Coding crosses the Hermes -> Pi typed boundary after authority cutover.
- Worker write/process/network/credential scopes are explicit and default-deny.
- Implementer cannot self-approve merge.
- Durable state, not conversation, determines phase/task execution and restart/adoption decisions.
- A phase ends with persisted evidence/report and returns control before the next phase.
- Upstream Hermes/Pi/LCM/Mnemosyne and model/provider bindings remain independently upgradeable/pinned.
