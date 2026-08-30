# Hermes + Pi Agentic Stack — Control Playbook

Snapshot: 2026-08-30

This is the repository-level control document for implementing and continuously validating a local-first, high-throughput agentic software-development stack built around **NousResearch/hermes-agent** as the orchestration/control plane and **earendil-works/pi** as the isolated coding-worker harness.

The detailed research and implementation material is intentionally split into canonical topic documents under `docs/agentic-uplift/`. This root playbook defines the mission, architecture, rollout order, acceptance gates, and upgrade discipline so Hermes can execute the uplift without duplicating tens of thousands of tokens of detail into every session.

## Mission

Build a production-grade workflow on Apple Silicon that:

- keeps Hermes as the single mission entry point and control-plane orchestrator;
- routes research/synthesis to the configured DeepSeek-class cloud model and coding/tool work to the configured GLM-class model;
- uses a very small local router rather than a permanently resident large generative model;
- delegates coding through a typed Hermes → Pi boundary rather than allowing the orchestrator to silently code directly;
- enforces filesystem, shell, network, credential, PII, secret, and merge policy outside model prompts;
- uses language servers to improve code navigation, diagnostics, rename/refactor and bounded context retrieval;
- minimizes repeated prompt/spec/tool-schema prefill while preserving quality and auditability;
- supports mission-sensitive Spec Kit profiles rather than running the full artifact pipeline for every change;
- remains upgrade-safe as Hermes and Pi change frequently;
- measures accepted-task quality, latency, retries, cache behavior, human intervention, and spend before promotion.

## Architecture decision

Use four routing/control layers:

1. **Tier 0 — deterministic policy gate.** Resolve explicit coding/research signals, privacy class, local-only requirements, repository state, and non-negotiable security rules.
2. **Tier 1 — tiny local semantic classifier.** Start with Qwen3-Embedding-0.6B prototypes or an equivalent compact encoder. Fine-tune ModernBERT only after a representative, redacted, outcome-labelled corpus exists.
3. **Tier 2 — uncertainty/difficulty escalation.** Use abstention/margin thresholds and optionally a RouteLLM-style difficulty router calibrated on actual DeepSeek-vs-GLM outcomes.
4. **Tier 3 — execution.** Pin the chosen cloud model/provider for the session to preserve cache affinity and behavioral stability.

Do **not** make a 20B–100B+ local generative model the always-on router on a 128 GB unified-memory workstation. Keep large local models on-demand for offline review/fallback experiments.

See: [`docs/agentic-uplift/research/local-routing-models.md`](docs/agentic-uplift/research/local-routing-models.md).

## Zero-trust invariant

`SOUL.md`, `USER.md`, task prompts, project docs, LSP output, tool output, and child-agent prose are **not authorization mechanisms**.

The Hermes orchestrator profile must have no arbitrary shell, source-write, merge, or unrestricted credential capability. Coding is performed by a constrained Pi worker launched from a trusted bridge with:

- a validated task envelope;
- a fixed role-to-capability mapping;
- a dedicated git worktree;
- environment scrubbing and temporary HOME;
- filesystem scope;
- shell/command policy;
- network allowlist/default deny;
- task-scoped credentials only when required;
- PII + secret egress scanning;
- deterministic test/LSP/security evidence requirements;
- an independent review/merge gate.

See:

- [`protocols/pi-task-envelope.schema.json`](protocols/pi-task-envelope.schema.json)
- [`protocols/uplift-state.schema.json`](protocols/uplift-state.schema.json)
- [`configs/policy.example.yaml`](configs/policy.example.yaml)
- [`docs/agentic-uplift/research/security-zero-trust-pii.md`](docs/agentic-uplift/research/security-zero-trust-pii.md)
- [`docs/agentic-uplift/research/hermes-pi-lsp.md`](docs/agentic-uplift/research/hermes-pi-lsp.md)

## Context and token strategy

Optimize four separate quantities: logical input tokens, fresh billable input, cached billable input, and prefill/TTFT compute.

Preserve current Hermes context-engine strengths before replacing them. The primary optimization sequence is:

1. measure prompt contributions and current compaction/cache behavior;
2. remove duplicated policy/procedural prose;
3. separate orchestrator and coder tool schemas;
4. keep stable system/policy/project invariants before volatile mission/tool content;
5. replace large project-context files with indexes + retrieval;
6. use task-scoped spec/code slices for Pi instead of replaying the full Hermes session;
7. tune lean compaction and model-specific thresholds using accepted-task quality;
8. pin provider/model per session and measure provider-side cached-input counters;
9. use MLX-LM/vLLM KV/prompt caches only for models actually served locally.

See: [`docs/agentic-uplift/research/context-token-optimization.md`](docs/agentic-uplift/research/context-token-optimization.md).

## Skill slimming and slicing

Treat skills as a progressive-disclosure context system, not as markdown files that are all permanently “active”. The optimized hierarchy is:

1. a narrow Hermes profile decides which skill catalog is eligible;
2. each catalog description is only a routing hint;
3. `SKILL.md` contains invariants, a phase map, and instructions for what to load next;
4. phase/topic details live in `references/` and are loaded only when needed;
5. deterministic mechanics live in `scripts/` rather than being re-generated from prose;
6. a pruned skill is treated as **not loaded** until explicitly reloaded;
7. the curator archives or consolidates stale/overlapping skills, but rare recovery/security procedures are protected by tests.

The repository includes a concrete sliced skill at [`skills/hermes-stack-uplift/`](skills/hermes-stack-uplift/) and the research rationale at [`docs/agentic-uplift/research/skill-slimming-slicing.md`](docs/agentic-uplift/research/skill-slimming-slicing.md).

The goal is not “more micro-skills”. Excessive slicing creates catalog growth, retrieval thrash and instruction inconsistency. Slice by **phase or concern with a clear load boundary** and measure skill-related input tokens per accepted task.


## Spec Kit strategy

Use deterministic risk/complexity selection for four profiles:

- **Micro/Patch** — localized low-risk change; compact change contract only.
- **Lite** — bounded feature; compact spec + plan, tasks only when useful.
- **Standard** — cross-component feature/refactor; normal SDD flow.
- **High Assurance** — auth/security/PII/destructive migrations/large architectural blast radius; full flow plus threat model, rollback, evidence matrix and adversarial review.

Use Spec Kit presets/extensions rather than maintaining a private fork of core templates. Generated Markdown is durable source material, not mandatory hot-context material: index it and retrieve only sections required by the current task.

See: [`docs/agentic-uplift/spec-kit-profiles.md`](docs/agentic-uplift/spec-kit-profiles.md).

## Router evaluation

Use the repository benchmark rig before granting routing authority:

```bash
python3 -m py_compile tools/router-bench/router_bench.py
python3 tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --output /tmp/router-smoke.json
```

Then benchmark the same held-out mission corpus with rules, embedding prototypes, Semantic Router, a fine-tuned ModernBERT checkpoint, and a RouteLLM-style difficulty adapter in isolated processes.

Production promotion requires representative held-out data, a temporal canary, explicit abstention behavior, zero observed `LOCAL_ONLY -> cloud` errors, and task-class-specific error analysis. Initial engineering target: macro-F1 >= 0.97, warm p95 <= 50 ms on the target Mac, subject to validation against real missions.

See: [`tools/router-bench/README.md`](tools/router-bench/README.md).

## Implementation order

Execute the canonical staged playbook rather than enabling every component at once:

1. capture baseline telemetry;
2. establish a fresh current Hermes canary and current Pi compatibility baseline;
3. optionally salvage only reviewed durable knowledge from the old Hermes context DB;
4. install the versioned external uplift overlay;
5. diet prompt/context/tool schemas and validate quality;
6. deploy the local router in shadow mode, then canary mode;
7. benchmark and pin cloud providers/models;
8. implement the Hermes → Pi typed bridge and remove direct coding capability from orchestrator mode;
9. add pinned/audited LSP integration;
10. add PII/secrets egress enforcement;
11. install Spec Kit mission profiles;
12. replace unconstrained swarms with capability-validated task graphs;
13. execute the adversarial suite;
14. canary, compare accepted-task economics, and promote gradually.

Canonical implementation detail: [`docs/agentic-uplift/implementation-playbook.md`](docs/agentic-uplift/implementation-playbook.md).

## Adversarial gate

The uplift is not complete until it survives the failure catalogue in [`docs/agentic-uplift/adversarial-review.md`](docs/agentic-uplift/adversarial-review.md), including:

- hybrid route misclassification;
- synthetic benchmark overfit;
- provider/cache churn;
- prompt-compaction loss of security state;
- SOUL-policy non-propagation;
- orchestrator bypass of Pi;
- Pi protocol breakage after upgrades;
- malicious project/LSP/tool output;
- PII/secret false negatives and false positives;
- extension supply-chain changes;
- task retry of destructive operations;
- reviewer/implementer correlated blind spots;
- memory pressure/swap under realistic workstation load;
- rate-limit/concurrency bottlenecks at high token volume.

Security failures fail closed. Do not weaken a boundary to make an upgrade or benchmark pass.

## Acceptance gates

Before production promotion:

- routing quality is non-inferior on held-out and temporal canary data;
- no `LOCAL_ONLY` payload crosses the cloud egress boundary in seeded tests;
- orchestrator mode structurally cannot edit source or execute arbitrary shell commands;
- all coding tasks enter Pi through the typed task envelope;
- required tests, LSP diagnostics, PII scan and secret scan are represented in the evidence object;
- stable-prefix/provider cache metrics materially improve without quality regression;
- mission-sensitive Spec Kit profiles reduce median input tokens per accepted task materially (initial target >=25% versus the all-phases baseline);
- daily Hermes/Pi upgrade rehearsal passes protocol, security, router and context smoke tests;
- rollback to the previous pinned overlay + dependency versions is one documented operation;
- accepted-task success rate remains non-inferior within the chosen confidence interval.

## Economics

The supplied baseline is **3,888,531,773 logical tokens/month**. Treat savings as an experimentally measured range, not a promise. A sensible initial target is roughly **25–50% logical-token reduction** from context/spec/tool optimization plus materially higher cached-input share on long sequential sessions. Provider pricing is volatile enough that the stable KPI should be **cost and minutes per accepted task**, with retries and human intervention included.

See: [`docs/agentic-uplift/savings-model.md`](docs/agentic-uplift/savings-model.md).

## Upgrade discipline

This repository is an overlay/control repository, not a permanent fork of Hermes or Pi.

For each upstream update:

1. install/update in a disposable canary profile;
2. apply the pinned uplift overlay;
3. run protocol, router, context, security and representative coding smoke tests;
4. compare prompt-size/cache/accepted-task metrics with the prior pinned version;
5. promote the new pins only on pass;
6. otherwise retain the previous pins and file an integration issue.

Any unavoidable patch to upstream source must be feature-flagged, integration-tested, documented, and tracked for removal/upstreaming.

## Self-uplift mission for Hermes

Run Hermes under the constrained uplift/orchestrator profile and give it this mission:

> Implement the agentic uplift defined by this repository. Treat each phase and acceptance gate in `docs/agentic-uplift/implementation-playbook.md` as a separately auditable task. You are the control-plane orchestrator: do not perform coding directly when the playbook requires Pi; use only capabilities granted by the installed policy. Preserve upstream upgradeability, collect deterministic evidence for every gate, run the adversarial suite before promotion, and mark a phase blocked rather than weakening a security/privacy boundary. Verify assumptions against the installed Hermes/Pi versions before implementation.

## Canonical evidence and research index

- [`docs/agentic-uplift/README.md`](docs/agentic-uplift/README.md)
- [`docs/agentic-uplift/SOURCES.md`](docs/agentic-uplift/SOURCES.md)
- [`docs/agentic-uplift/architecture.html`](docs/agentic-uplift/architecture.html)
- [`docs/agentic-uplift/research/local-routing-models.md`](docs/agentic-uplift/research/local-routing-models.md)
- [`docs/agentic-uplift/research/context-token-optimization.md`](docs/agentic-uplift/research/context-token-optimization.md)
- [`docs/agentic-uplift/research/hermes-pi-lsp.md`](docs/agentic-uplift/research/hermes-pi-lsp.md)
- [`docs/agentic-uplift/research/security-zero-trust-pii.md`](docs/agentic-uplift/research/security-zero-trust-pii.md)

Keep this root document compact. Update canonical detailed documents rather than copying their full contents here; this is itself an application of the stack's context-diet principle.


## Readiness and publication

This repository distinguishes **design maturity** from **implemented enforcement**. Read [`docs/agentic-uplift/artifact-usability-review.md`](docs/agentic-uplift/artifact-usability-review.md) before granting unattended authority. The current bundle is suitable for architecture review and controlled prototyping; production self-uplift remains gated on the P0 controls in that review.

For resumable agent execution, use [`docs/agentic-uplift/agent-execution-contract.md`](docs/agentic-uplift/agent-execution-contract.md) rather than conversational memory as execution state.

Executed refinement evidence is recorded in [`docs/agentic-uplift/validation-report.md`](docs/agentic-uplift/validation-report.md). The GitHub Pages site is generated under `docs/`. Human pages link to raw Markdown alternates; agent discovery starts at `docs/llms.txt` and `docs/agent/START.md`. SVG diagrams are presentation views, while [`docs/agentic-uplift/architecture.md`](docs/agentic-uplift/architecture.md) and [`docs/agentic-uplift/architecture.graph.json`](docs/agentic-uplift/architecture.graph.json) are the canonical text/machine representations.
