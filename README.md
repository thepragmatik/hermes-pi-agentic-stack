# Hermes + Pi Agentic Stack

A production-oriented, local-first agentic software development stack built around **NousResearch/hermes-agent** as the orchestration/control plane and **earendil-works/pi** as the isolated coding worker harness.

The blueprint targets a **MacBook Pro M3 Max with 128 GB unified memory** while preserving headroom for browsers, language servers, builds, containers, and normal developer workloads. It is designed for high-throughput workloads where routing quality, prompt-prefix stability, token efficiency, deterministic delegation, privacy, local context/memory, and upgrade safety matter more than running the largest possible local model.

## Architecture at a glance

```text
Terminal / user
      |
      v
Hermes control plane
      |
      +--> REQUIRED local context + memory baseline
      |      LCM (current-session context/recovery)
      |      Mnemosyne (curated cross-session memory)
      |      state.db/session_search (raw session history)
      |
      +--> deterministic policy + privacy gate
      |
      v
local mission router
rules -> semantic classifier -> uncertainty/difficulty gate
      |                                      |
      | research / synthesis                 | code / tool execution
      v                                      v
qualified research role                typed Hermes -> Pi RPC
                                             |
                                             v
                                      isolated Pi worker
                                      + git worktree
                                      + sandbox / egress policy
                                      + qualified coding role
                                      + LSP servers
                                             |
                                             v
                                      tests + scanners + diff
                                             |
                                             v
                                      review / merge gate
```

Security-critical controls are enforced outside prompts, context engines and memory providers. `SOUL.md`, remembered text and agent instructions are behavioral/advisory context, not authorization boundaries.

## Human and agent documentation

The repository intentionally publishes the same knowledge through several representations:

- **Live human website:** https://thepragmatik.github.io/hermes-pi-agentic-stack/
- **Raw/canonical Markdown:** human pages declare Markdown alternates; research remains version-controlled Markdown.
- **Agent discovery:** `llms.txt` and `agent/START.md` on the Pages site provide a small entry point instead of encouraging full-corpus ingestion.
- **Machine contracts:** JSON Schema, policy/config YAML, an architecture graph JSON file, and a hashed agent manifest.
- **Diagrams:** accessible SVGs remain useful to humans and multimodal agents, while text/JSON representations are canonical for deterministic agent consumption.

## Start here

- [`HERMES_AGENTIC_UPLIFT_PLAYBOOK.md`](HERMES_AGENTIC_UPLIFT_PLAYBOOK.md) — compact control architecture, rollout order and promotion gates.
- [`docs/agentic-uplift/implementation-playbook.md`](docs/agentic-uplift/implementation-playbook.md) — canonical staged autonomous uplift execution plan.
- [`docs/agentic-uplift/local-context-memory-setup.md`](docs/agentic-uplift/local-context-memory-setup.md) — clinical LCM + Mnemosyne installation, effective config, health, offline, backup and rollback procedure.
- [`docs/agentic-uplift/research/local-context-memory-stack.md`](docs/agentic-uplift/research/local-context-memory-stack.md) — ownership, design rationale, risks and qualification evidence for the local baseline.
- [`docs/agentic-uplift/research/legacy-state-curation.md`](docs/agentic-uplift/research/legacy-state-curation.md) — safe curation of prior Hermes `state.db` rather than DB transplantation.
- [`docs/agentic-uplift/artifact-usability-review.md`](docs/agentic-uplift/artifact-usability-review.md) — real-world fit-for-purpose review and production readiness gaps.
- [`docs/agentic-uplift/adversarial-review.md`](docs/agentic-uplift/adversarial-review.md) — explicit architecture/context/memory/security failure modes and kill criteria.
- [`docs/agentic-uplift/research/skill-slimming-slicing.md`](docs/agentic-uplift/research/skill-slimming-slicing.md) — progressive-disclosure skill design and evaluation plan.
- [`docs/agentic-uplift/agent-execution-contract.md`](docs/agentic-uplift/agent-execution-contract.md) — resumable, evidence-bound execution state machine.
- [`docs/agentic-uplift/validation-report.md`](docs/agentic-uplift/validation-report.md) — executed checks, evidence levels and explicit remaining runtime gaps.
- [`tools/router-bench/`](tools/router-bench/) — isolated-process router evaluation harness and sample missions.
- [`protocols/pi-task-envelope.schema.json`](protocols/pi-task-envelope.schema.json) — typed Hermes-to-Pi delegation contract.
- [`configs/hermes-local-context-memory.example.yaml`](configs/hermes-local-context-memory.example.yaml) — complete non-secret Hermes baseline composition for LCM + Mnemosyne + Tool Search.
- [`configs/lcm-baseline.env.example`](configs/lcm-baseline.env.example) — pinned LCM scalar baseline, applied profile-locally.
- [`configs/mnemosyne-local.example.yaml`](configs/mnemosyne-local.example.yaml) — conservative local-only Mnemosyne subconfiguration.
- [`configs/policy.example.yaml`](configs/policy.example.yaml) — policy intent example (not enforcement by itself).
- [`skills/hermes-stack-uplift/`](skills/hermes-stack-uplift/) — sliced Hermes skill for executing the uplift with progressive disclosure.

## State ownership

The design intentionally separates stores rather than calling all persistent information “memory”:

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission authority
T2 artifacts = raw logs/diffs/benchmarks/test evidence
Git/ADR/spec = project truth
Kanban       = optional operational projection/UI
```

**LCM + Mnemosyne is the selected baseline, not a production bake-off candidate.** Phase 30 uses built-in-only, LCM-only and Mnemosyne-only profiles only as diagnostic controls to isolate regressions. The required pair must pass long-horizon quality, exact-recovery, recall relevance, token/schema, local-only, resource, backup and rollback gates. Failure means `BLOCKED`/`ROLLBACK`; Hermes does not autonomously substitute another memory architecture.

Baseline defaults deliberately disable overlapping automation: LCM semantic/proactive/temporal cross-session memory is off; Mnemosyne transcript autosave, host/remote LLM paths, auto-sleep/persona and richer recall features are off; Hermes built-in MEMORY/USER are off; Mnemosyne autonomous curated writes remain on under a strict admission policy and narrow tool allowlist.

## Design principles

1. **Small always-on control plane.** Rules plus a small embedding/classification model route work instead of a resident generative router.
2. **Local context/memory with explicit ownership.** LCM and Mnemosyne have separate jobs; no hidden cloud memory dependency or duplicate durable authority.
3. **Cloud specialist pinning per phase/session.** Preserve provider-side prefix-cache affinity and behavioral consistency where cloud models are deliberately used.
4. **Typed delegation.** Hermes plans, routes, delegates and evaluates; Pi owns coding/tool loops in constrained workers after authority cutover.
5. **Security outside the LLM.** Filesystem, process, network, credential, PII, secret and merge permissions are enforced by code/configuration.
6. **Retrieval over replay.** Long specifications, history, evidence and tool outputs stay external and are retrieved by slice.
7. **Mission-sensitive Spec Kit.** Micro/Lite/Standard/High-Assurance profiles spend specification tokens in proportion to ambiguity and risk.
8. **Upgrade-safe overlay.** Prefer plugins, side venvs, external daemons, extensions, skills, presets and narrow adapters over invasive forks.
9. **Measure accepted-task economics.** Optimize quality, latency, retries, cached input, exact recovery, recall precision, tool correctness and human intervention—not just $/M tokens.

## Repository posture

This repository remains separate from upstream Hermes, Pi, LCM and Mnemosyne source trees. It contains the **versioned control design, config exemplars, policies/contracts, evaluation tooling and operational playbook**. Upstream upgrades are rehearsed in disposable canaries and rolled back independently.

Do not commit API keys, raw PII evaluation corpora, Hermes/LCM/Mnemosyne databases, credentials, environment secrets or unredacted production transcripts.

## Current stage

The repository is an evidence-backed architecture and controlled-prototyping package, **not yet an unattended production self-uplift system**. It is coherent enough to start Hermes at Phase 00 in a clean canary/bootstrap profile. The LCM + Mnemosyne architecture decision is fixed, but production promotion remains gated on target-Mac runtime/local-only/recovery evidence plus real external security/Pi enforcement and the remaining P0 gates.
