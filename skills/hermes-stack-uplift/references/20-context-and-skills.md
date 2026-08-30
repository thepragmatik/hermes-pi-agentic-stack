# Phase 20 — Context and Skills

Measure fixed prompt/context with Hermes prompt-size/context tooling where available. Preserve Hermes' existing prompt-assembly/compression strengths; do not replace the context engine merely to implement this uplift.

Apply the mission-context architecture in `docs/agentic-uplift/research/mission-context-architecture.md`:

- **T0 stable prefix** — identity, minimal invariants, stable profile/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded current objective/phase/constraints/acceptance/routing/evidence pointers, regenerated only at meaningful phase boundaries;
- **T2 artifact memory** — logs, diffs, Pi RPC streams, benchmarks, research captures and large Spec Kit/source artifacts kept outside hot context and retrieved by slice.

Stabilize prefix ordering, move procedures out of always-hot SOUL/USER/project files, prune tool schemas, retrieve long artifacts by slice, and install the sliced uplift skill. Do not mirror the same mission state or raw evidence into chat, memory, project context and artifacts simultaneously.

Benchmark unsliced vs sliced skill usage and T0/T1/T2 behavior on identical missions. Track T0/T1 tokens, T1 update count, T2 bytes produced vs loaded, fresh/cached input, compactions and accepted-task quality.

Do not hide security invariants solely in optional slices. Initial skill target: >=30% lower skill-related input tokens with non-inferior accepted-task quality; initial T1 target is normally <=8K tokens and smaller for simple phases. These are engineering targets, not guarantees.
