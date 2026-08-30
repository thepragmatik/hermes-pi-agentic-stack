# Hermes + Pi Agentic Stack

A production-oriented, local-first agentic software development stack built around **NousResearch/hermes-agent** as the orchestration/control plane and **earendil-works/pi** as the isolated coding worker harness.

The blueprint targets a **MacBook Pro M3 Max with 128 GB unified memory** while preserving headroom for browsers, language servers, builds, containers, and normal developer workloads. It is designed for high-throughput workloads where routing quality, prompt-prefix stability, token efficiency, deterministic delegation, privacy, and upgrade safety matter more than running the largest possible local model.

## Architecture at a glance

```text
Terminal / user
      |
      v
Hermes control plane
      |
      +--> deterministic policy + privacy gate
      |
      v
local mission router
rules -> semantic classifier -> uncertainty/difficulty gate
      |                                      |
      | research / synthesis                 | code / tool execution
      v                                      v
DeepSeek-class cloud model             typed Hermes -> Pi RPC
                                             |
                                             v
                                      isolated Pi worker
                                      + git worktree
                                      + sandbox / egress policy
                                      + GLM-class coding model
                                      + LSP servers
                                             |
                                             v
                                      tests + scanners + diff
                                             |
                                             v
                                      review / merge gate
```

Security-critical controls are enforced outside prompts. `SOUL.md` and other agent instructions are behavioral guidance, not authorization boundaries.

## Human and agent documentation

The repository intentionally publishes the same knowledge through several representations:

- **Human website:** GitHub Pages content is generated under `docs/`; once Pages is enabled from `main` → `/docs`, the expected project URL is `https://thepragmatik.github.io/hermes-pi-agentic-stack/`.
- **Raw/canonical Markdown:** human pages declare Markdown alternates; research remains version-controlled Markdown.
- **Agent discovery:** `docs/llms.txt` and `docs/agent/START.md` provide a small entry point instead of encouraging full-corpus ingestion.
- **Machine contracts:** JSON Schema, policy/config YAML, an architecture graph JSON file, and a hashed agent manifest.
- **Diagrams:** accessible SVGs remain useful to humans and multimodal agents, but text/JSON representations are canonical for deterministic agent consumption.

## Start here

- [`HERMES_AGENTIC_UPLIFT_PLAYBOOK.md`](HERMES_AGENTIC_UPLIFT_PLAYBOOK.md) — consolidated research, architecture, implementation plan, adversarial review, and rollout gates.
- [`docs/agentic-uplift/README.md`](docs/agentic-uplift/README.md) — executive architecture summary.
- [`docs/agentic-uplift/implementation-playbook.md`](docs/agentic-uplift/implementation-playbook.md) — staged clean-slate/self-uplift execution plan.
- [`docs/agentic-uplift/architecture.html`](docs/agentic-uplift/architecture.html) — standalone HTML architecture document with inline SVG diagrams.
- [`docs/agentic-uplift/artifact-usability-review.md`](docs/agentic-uplift/artifact-usability-review.md) — real-world fit-for-purpose review and production readiness gaps.
- [`docs/agentic-uplift/adversarial-review.md`](docs/agentic-uplift/adversarial-review.md) — explicit architecture failure modes, edge cases, and trade-offs.
- [`docs/agentic-uplift/research/skill-slimming-slicing.md`](docs/agentic-uplift/research/skill-slimming-slicing.md) — progressive-disclosure skill design and evaluation plan.
- [`docs/agentic-uplift/agent-execution-contract.md`](docs/agentic-uplift/agent-execution-contract.md) — resumable, evidence-bound execution state machine.
- [`docs/agentic-uplift/validation-report.md`](docs/agentic-uplift/validation-report.md) — checks actually executed during refinement and explicit remaining gaps.
- [`docs/agentic-uplift/site-publishing.md`](docs/agentic-uplift/site-publishing.md) — human/agent representation rules and GitHub Pages setup.
- [`tools/router-bench/`](tools/router-bench/) — isolated-process router evaluation harness and sample missions.
- [`protocols/pi-task-envelope.schema.json`](protocols/pi-task-envelope.schema.json) — typed Hermes-to-Pi delegation contract.
- [`configs/policy.example.yaml`](configs/policy.example.yaml) — policy intent example (not enforcement by itself).
- [`skills/hermes-stack-uplift/`](skills/hermes-stack-uplift/) — a concrete sliced Hermes skill for executing the uplift.

## Design principles

1. **Small always-on control plane.** Use rules plus a small embedding/classification model for routing instead of keeping a large generative model resident.
2. **Cloud model pinning per session.** Preserve provider-side prefix-cache affinity and behavioral consistency.
3. **Typed delegation.** Hermes plans, routes, delegates, and evaluates; Pi owns coding/tool loops in constrained workers.
4. **Security outside the LLM.** Filesystem, process, network, credential, PII, secret, and merge permissions are enforced by code/configuration.
5. **Retrieval over replay.** Long specifications, history, and tool outputs are retrieved/summarized rather than injected repeatedly.
6. **Mission-sensitive Spec Kit.** Micro/Lite/Standard/High-Assurance profiles spend specification tokens in proportion to ambiguity and risk.
7. **Upgrade-safe overlay.** Prefer external daemons, extensions, skills, presets, and narrow adapters over invasive Hermes/Pi forks.
8. **Measure accepted-task economics.** Optimize latency, retries, cached input, tool correctness, and human intervention—not just $/M tokens.

## Repository posture

This repository is intended to remain separate from upstream Hermes and Pi source trees. It should contain the **versioned overlay, adapters, policies, evaluation tooling, and operational playbook**. Daily/regular upstream upgrades can therefore be rehearsed and rolled back without overwriting stack-specific improvements.

Do not commit API keys, raw PII evaluation corpora, Hermes context databases, credentials, or unredacted production transcripts.

## Current stage

The repository is an evidence-backed architecture and controlled-prototyping package, **not yet an unattended production self-uplift system**. The artifact usability review identifies P0 implementation gates before unattended authority is allowed. Production implementation should proceed through those gates rather than enabling all components at once.
