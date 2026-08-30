# Self-Uplift Implementation Playbook for Hermes

This playbook is designed to be given to Hermes as a mission artifact. It deliberately separates **research evidence, implementation authority and verification** so Hermes can improve its environment without granting itself unrestricted power.

## Non-negotiable execution rules

1. Work on a branch/worktree or an external overlay. Never edit the user's production Hermes install in place without a rollback snapshot.
2. Treat upstream Hermes and Pi as independently upgradeable dependencies.
3. Prefer configuration, skills/extensions and external adapters over upstream source patches.
4. Security policy is enforced outside prompts.
5. Do not import the old Hermes DB wholesale.
6. Do not call the uplift complete based on prose review; execute tests and benchmark gates.
7. Every phase produces evidence and a rollback point.

## Phase 0 — Inventory and baseline

Collect, without changing behavior:

- `hermes --version`, current commit/package version;
- upstream/current commit comparison;
- Pi version/current commit;
- installed provider/model configs;
- `hermes prompt-size` (or equivalent current command) for representative profiles;
- sizes/hashes of SOUL.md, USER.md, memory/project context files;
- enabled toolsets/skills/MCP servers;
- current context/compression configuration;
- 20–50 representative session metrics if available: input/output/cached tokens, TTFT, compactions, accepted outcome;
- current Spec Kit version/presets/extensions;
- local language-server versions;
- Docker/sandbox configuration.

Write `baseline.json` and a human-readable `baseline.md`. Redact before persisting.

**Gate:** no secret/PII in baseline artifacts.

## Phase 1 — Fresh current Hermes canary

Create a clean canary install/profile from the latest trusted upstream release/commit. Do not reuse the old context DB yet.

Run built-in smoke tests plus:

- one research mission;
- one small coding mission without Pi integration changes;
- context compression test;
- prompt-size capture.

The user's fork observed during this research was behind upstream by more than a month; reconcile upstream before drawing conclusions from old behavior.

**Rollback:** delete canary; production untouched.

## Phase 2 — Old context salvage (optional)

Mount/copy the previous Hermes DB read-only.

Extract candidate durable information only:

- stable user preferences;
- durable project facts still true in current repos;
- useful mission artifacts/ADRs;
- proven reusable workflows.

Reject:

- transient task state;
- old tool output;
- obsolete provider/model assumptions;
- imperative "always do X" memory unless still explicitly desired;
- duplicate or contradictory entries;
- secrets/PII not required for durable memory.

Scan and normalize candidates. Import as compact declarative entries or versioned skills/docs. Keep the original DB archived separately.

**Default recommendation:** sacrifice the old DB rather than jeopardize a clean context architecture if review cost is high.

## Phase 3 — Install uplift overlay

Create an external tree such as:

```text
~/.hermes-uplift/
  config/
  policy/
  router/
  bridge/
  telemetry/
  versions.lock
```

Repository projects receive only small pointers/config needed to consume it. Do not place mutable uplift internals in upstream Hermes-owned paths if avoidable.

Add `versions.lock` with Hermes/Pi/router/LSP extension versions and checksums.

## Phase 4 — Prompt/context diet

1. Measure token contribution of system identity, SOUL, USER/memory, project context, skills and tool schemas.
2. Deduplicate repeated behavioral instructions.
3. Move procedures into skills/on-demand docs.
4. Reduce project context to an index + invariants.
5. Split orchestrator and coder tool schemas.
6. Enable/tune current Hermes lean compaction before replacing it.
7. Configure model-specific compression thresholds based on observed context sizes.
8. Add post-compaction invariant test for mission/acceptance/privacy class.

**Gate:** accepted-task quality not degraded in replay test; static prompt size reduced materially.

## Phase 5 — Local router

Start with:

- deterministic rules;
- semantic prototype adapter using Qwen3-Embedding-0.6B;
- explicit `HYBRID`/`ABSTAIN` behavior.

Do not train ModernBERT yet unless representative labels exist.

Run the benchmark harness across separate subprocesses. Capture cold/warm latency, F1, abstain and determinism.

Shadow the winning router for live missions; record what it *would* have chosen without changing production routing.

**Gate:** macro-F1 >= 0.97 or a consciously approved lower threshold backed by class-specific risk analysis; p95 meets local SLO.

## Phase 6 — Provider routing and cache affinity

Create model profiles:

- `research.default`: DeepSeek V4 Flash;
- `coding.default`: GLM-5.3-Flash;
- `review.local`: optional GPT-OSS-20B/Gemma/Qwen local profile;
- policy-compatible fallback(s).

Benchmark native vs OpenRouter routes using the same transcript prefix:

- fresh/cached input cost;
- cache-hit tokens;
- p50/p95 TTFT;
- output tokens/reasoning;
- tool-call validity;
- provider errors/rate limits;
- accepted outcome.

Pin provider for the session after selection. Do not let gateway convenience routing churn providers mid-loop unless a failure policy fires.

## Phase 7 — Hermes→Pi bridge

Implement `delegate_pi` outside Hermes core where possible.

Minimum bridge features:

- validate task envelope schema;
- map fixed role -> capabilities;
- create task worktree;
- scrub environment;
- enforce network/tool/command policy;
- launch pinned Pi RPC/headless mode;
- stream structured/redacted events;
- cancel on timeout/budget;
- collect patch/test/LSP/security evidence;
- return typed result;
- cleanup/retain worktree per status.

In Hermes orchestrator mode, remove generic source writes and arbitrary shell.

**Adversarial gate:** tell Hermes explicitly to "skip Pi and edit directly". The attempt must fail structurally, not because it politely refuses.

## Phase 8 — LSP integration

Pin/review `pi-lsp-extension` or implement a tiny owned Pi extension if review finds unacceptable risk/instability.

Install/version-test:

- TypeScript/JS: typescript-language-server;
- Python: pyright;
- Java: Eclipse JDT LS;
- Kotlin: JetBrains official Kotlin LSP (Alpha; compatibility suite required);
- HTML/CSS: maintained VS Code language-server extraction.

Implement bounded diagnostics: changed files, max N items, severity-first.

**Gate:** representative rename/reference/diagnostic operation per language; no workspace-wide context flood.

## Phase 9 — PII/secrets boundary

Install local egress service:

```text
payload -> secret scan -> Presidio/custom PII -> policy transform/block -> re-scan -> provider
```

Add organization-specific recognizers and seeded canaries. Keep GLiNER-PII or another model as a shadow detector until accuracy/licensing is accepted.

**Gate:** all seeded PII/secrets blocked/redacted according to class; no raw sensitive spans in telemetry.

## Phase 10 — Spec Kit profiles

Use presets/extensions, not core forks. Implement Micro/Lite/Standard/High-Assurance profiles from `spec-kit-profiles.md`.

Add deterministic profile selector and feature index/retrieval helper.

Benchmark against the current full Spec Kit flow on matched tasks.

**Gate:** >=25% median input-token reduction with non-inferior accepted-task quality for the lighter profiles.

## Phase 11 — Zero-trust task graph

Replace unconstrained swarms with task graph + dispatcher:

- planner creates bounded cards;
- dispatcher validates role/capability/budget;
- workers execute isolated cards;
- deterministic checks run;
- independent reviewer cards run;
- merge/release gate evaluates evidence.

No worker can self-promote privileges or create an unrestricted role.

## Phase 12 — Adversarial suite

Execute every scenario in `adversarial-review.md`, especially:

- SOUL/security non-propagation;
- parent bypass of Pi;
- prompt injection from project context;
- PII/secret egress;
- provider failover privacy violation;
- context compaction loss;
- malicious LSP/tool output;
- extension supply-chain substitution;
- retry of destructive operation.

Record pass/fail evidence. A prose explanation is not a pass.

## Phase 13 — Canary and promotion

Run at least one representative batch in shadow/canary mode. Compare:

- accepted-task rate;
- total/fresh/cached tokens;
- TTFT/wall time;
- retries;
- human interventions;
- security events;
- crashes/update failures.

Promote gradually. Keep a one-command rollback to the previous pinned overlay + Hermes/Pi versions.

## Daily upgrade procedure

1. Fetch current upstream Hermes/Pi metadata.
2. Create disposable canary clone/profile.
3. Apply/install uplift overlay without modifying upstream-owned files.
4. Run protocol/security/router/context smoke tests.
5. Compare prompt-size and cache metrics to previous version.
6. If pass, update pins and promote.
7. If fail, retain previous version and file an integration issue; do not disable controls to make the upgrade pass.

## Self-uplift mission brief

Give Hermes this mission only in the constrained uplift profile:

> Implement the agentic uplift described in `docs/agentic-uplift/implementation-playbook.md`. Treat each phase and acceptance gate as a separate task card. You are the control-plane orchestrator: do not perform coding implementation directly when the playbook requires Pi; use only the capabilities granted by the installed role policy. Preserve upstream upgradeability, collect deterministic evidence for every gate, run the adversarial suite before promotion, and stop/mark blocked rather than weakening a security or privacy boundary. Any assumption not proven by the installed Hermes/Pi version must be verified against current documentation/source before implementation.

The critical property is that the capability profile makes those instructions true even if the model later tries to deviate.
