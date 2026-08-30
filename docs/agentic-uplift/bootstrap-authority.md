# Trusted Bootstrap Authority — Closing the Self-Uplift Loop

## Problem

The desired steady state is strict:

- Hermes is the control-plane orchestrator;
- Hermes cannot directly edit production source or run arbitrary shell commands;
- coding crosses a typed Hermes -> Pi boundary;
- Pi executes inside an external filesystem/process/network/credential boundary;
- cloud egress passes external PII/secret policy.

But those controls do not exist before the uplift builds them. Removing Hermes' coding/shell authority before the Pi bridge exists creates a circular dependency: no trusted mechanism remains to implement the bridge.

The solution is an explicit **trusted bootstrap authority** that is temporary, narrow, observable and revocable.

This is not the final security model. It is the root-of-trust transition into the final security model.

## Principle

**Capability reduction happens only after the replacement path has been implemented and proven.**

During bootstrap, current Hermes may use direct coding/shell capabilities only to construct the new external control plane in disposable/canary locations. It must never interpret temporary bootstrap authority as permanent production permission.

## Bootstrap write scope

Bootstrap mutations are limited to:

- this `hermes-pi-agentic-stack` repository on a dedicated branch/worktree;
- a new parallel canary `HERMES_HOME`;
- the versioned uplift overlay/control-plane directory;
- disposable test worktrees/sandboxes;
- explicit local evidence/report directories.

Bootstrap Hermes must not mutate:

- the currently running production Hermes checkout/home;
- the archived legacy Hermes home or original `state.db`;
- unrelated repositories;
- SSH/cloud credential stores;
- shell startup files or global dotfiles except explicitly reviewed/pinned integration links;
- production branches without a review/promotion gate.

When practical, enforce this scope outside the model with a dedicated OS/container/sandbox boundary. If the operator cannot establish an external boundary before bootstrap, treat the existing local user account as the temporary root of trust and compensate with parallel installs, git/worktree isolation, immutable archives, explicit path checks and frequent reversible checkpoints. Do not claim zero-trust until external enforcement exists.

## B0 — preflight and immutable checkpoints

Before the first mutation:

1. complete Phase 00 inventory;
2. archive/checksum the existing Hermes state;
3. create the clean parallel Hermes candidate location;
4. create a dedicated uplift branch/worktree;
5. persist uplift state and a bootstrap checkpoint;
6. record exact Hermes/Pi versions and the current policy digest;
7. enable Hermes `security-guidance` in WARN mode when available.

`security-guidance` is defense in depth only. It pattern-checks Hermes-owned write/patch content and does not sandbox Hermes or inspect independent Pi worktree changes.

## B1 — build policy/enforcement substrate before cloud worker authority

Implement the external control-plane primitives first:

- role/capability policy parser and validator;
- allowed workspace/path calculation;
- environment allowlist/scrubber;
- network/egress policy interface;
- secret + typed-PII scanner interface;
- evidence recorder;
- task/state schema validation;
- idempotency/attempt bookkeeping;
- sandbox launcher abstraction.

At this stage, fake/local fixtures are preferred. Do not require provider credentials merely to prove control flow.

## B2 — build the minimal Pi bridge with no production authority

Implement the Hermes -> Pi bridge against the current Pi RPC protocol.

Required protocol behavior includes:

- launch `pi --mode rpc` or an equivalently pinned embedding API;
- local pipe/stdin/stdout only; do not expose RPC on a network listener;
- validate the v2 task envelope and policy digest before launch;
- create an isolated disposable worktree;
- pass only the minimum environment/credentials required;
- enforce timeout, cancellation and attempt/idempotency semantics;
- treat Pi `agent_settled` as completion, not merely `agent_end`;
- collect compact typed evidence rather than mirroring raw RPC streams into Hermes context.

Current Pi explicitly documents `agent_end` as the end of a low-level run that may still be followed by retry/compaction/queued continuations; `agent_settled` is the fully-settled event.

## B3 — prove the worker path offline/local-first

Before cloud credentials are available to Pi, run:

1. fake RPC protocol test;
2. worktree isolation test;
3. path traversal/symlink escape tests;
4. environment-leak test;
5. denied-network test;
6. duplicate/idempotent retry test;
7. timeout/cancel test;
8. malicious repository instruction test;
9. evidence integrity test.

Use `PI_OFFLINE=1` where appropriate to suppress Pi startup network activity during offline fixtures. A passing fake-RPC test proves bridge mechanics only, not production security.

## B4 — prove external Pi containment

Pi does not provide a built-in permission system for filesystem/process/network/credential restriction. The final worker boundary must therefore be supplied externally.

Qualify one pinned containment implementation suitable for the target Mac/workflow. Candidates may include a reviewed Pi sandbox extension using OS-level sandboxing, a container/micro-VM pattern, or another operator-owned capability broker.

The containment test must prove denied filesystem/network/credential actions fail structurally even when the model explicitly requests them.

## B5 — enable privacy-controlled cloud canary

Only after the egress boundary passes seeded canaries may a Pi worker receive cloud-model access.

Run a non-sensitive canary mission and verify:

- provider/model pin;
- no unauthorized environment leakage;
- egress scanner evidence;
- worktree-only mutations;
- `agent_settled` completion handling;
- bounded retry behavior;
- deterministic tests/LSP evidence;
- worker cannot merge or self-approve.

Then run adversarial payloads containing seeded secrets/PII and prove fail-closed behavior.

## B6 — revoke bootstrap authority

This is the decisive transition.

Once the replacement path is proven:

1. switch production Hermes to the constrained orchestrator profile;
2. remove generic source-write and arbitrary-shell capability from that profile;
3. make `delegate_pi`/typed worker delegation the only coding execution path;
4. retain external policy/egress enforcement outside prompt/skill text;
5. verify an explicit instruction to "skip Pi and edit directly" fails structurally;
6. record the capability-reduction evidence and new policy digest.

After B6, direct bootstrap capabilities are not silently re-enabled for normal work. A future emergency bootstrap requires a new explicit checkpoint/approval and operates in a canary environment.

## Kanban projection

Hermes Kanban is useful as an optional operational mission ledger because it is durable across restarts and exposes blocked/review/retry states to humans and agents.

It is **not** the authoritative security/execution state. The versioned `uplift-state` object remains authoritative for phase, attempt, policy digest, checkpoints and evidence requirements.

Recommended relationship:

```text
uplift-state.json / schema   = execution authority
Kanban task/card             = operational projection / human supervision
immutable evidence files     = proof
```

Do not load the Kanban toolset into ordinary profiles merely for observability; current Hermes keeps its schema footprint at zero unless the profile/task explicitly enables the toolset.

## Autonomous execution rule

Hermes may execute B0-B6 autonomously only while each phase has deterministic acceptance evidence and the next phase does not require an unproven security boundary.

On ambiguity:

- missing capability/enforcement -> `BLOCKED`;
- security/privacy test failure -> `ROLLBACK` or `BLOCKED`;
- bootstrap implementation defect -> repair in canary and re-run evidence;
- desire to weaken a boundary to make progress -> **deny**;
- inability to prove the new worker path -> keep bootstrap authority confined to canary and do not promote.

The autonomous mission may progress without human intervention when gates pass; it must stop rather than improvise around a failed root-of-trust transition.
