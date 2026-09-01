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

The Phase-50 protocol, containment, privacy and bypass gates must pass before any production coding-authority cutover. If policy requires human approval, that approval is **additional after the mandatory gates pass**; it cannot waive or substitute for a failed/unproven gate.

Persist state/evidence, send the required phase-boundary report, and stop before Phase 60.

## Proven behavior (uplift mission evidence, 2026-09-01)

The plan text above was implemented and qualified during the hermes-pi-agentic-stack
uplift mission (Phases 50–60, branch `uplift/bootstrap`, commits 3509ebb→8f2cbd1).
What is actually proven, with evidence in the uplift profile state:

- **Bridge mechanics (B2/B3):** typed v2-envelope validation with policy-digest binding,
  local pipe/stdin/stdout RPC only, disposable git worktrees, env allowlist
  (LANG/PATH/SHELL/TERM/TMPDIR), credential vars blocked, `agent_settled` completion,
  idempotent replay on duplicate `task_id`+`idempotency_key`, timeout cancellation.
  Proven offline with fixture workers (26-test suite in `tests/test_pi_bridge.py`).
- **Containment (B4):** macOS Seatbelt (sbpl) profile with default-allow plus explicit
  structural denials; fs-escape, network and credential reads fail structurally under the
  SAME profile used for real missions. Canonical `/private` tmp paths are the trap —
  deny both spellings. Probe matrix and lessons: `references/execution-lessons.md`.
- **Cloud canary (B5):** worker keeps `deny network*`; the ONLY route to the cloud model
  is parent-proxied model egress over an inherited fd-pipe (`--model-proxy`). The deny was
  NOT weakened. Worker-direct cloud egress was NOT proven and is not claimed.
- **Direct-edit rejection (B6):** `reject_direct_edit()` rejects "skip Pi"/"edit directly"/
  bypass directives with a typed `BridgeError` BEFORE worker launch; proven live (rc=3,
  no worktree created). At bridge level the typed boundary is the only coding path.
  OS/operator-level removal of Hermes' generic tools remains EXTERNAL/operator-owned —
  this Hermes version exposes no permissions/hooks config keys. Zero-trust is NOT claimed.
- **LSP:** pyright 1.1.413, typescript-language-server 5.3.0, jdtls 1.60.0,
  kotlin-language-server 1.3.13 pinned with diagnostics severity/file bounding.
  HTML/CSS: provisionable via `npx -y -p vscode-langservers-extracted@4.10.0`
  (binaries launch; full LSP-handshake smoke pending — see Phase 70 evidence).
- **Session Capability Modes (Phase 70):** `--capability-mode restricted|pi-coding` on the
  bridge run command; default `restricted` denies `--model-proxy` structurally.
  See `references/session-capability-modes.md`.

