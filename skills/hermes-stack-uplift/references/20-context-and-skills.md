# Phase 20 — Context, Skills and Local Memory

Measure fixed prompt/context with Hermes prompt-size/context tooling. Preserve a built-in compressor + compact MEMORY/USER + `session_search` control profile; do not destroy the baseline while qualifying alternatives.

Apply `docs/agentic-uplift/research/mission-context-architecture.md`:

- **T0 stable prefix** — identity, minimal invariants, stable profile/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded current objective/phase/constraints/acceptance/routing/evidence pointers, regenerated only at meaningful phase boundaries;
- **T2 artifact/evidence memory** — logs, diffs, Pi RPC streams, benchmarks, research and large Spec Kit/source artifacts remain outside hot context and are retrieved by slice.

Then follow `docs/agentic-uplift/research/local-context-memory-stack.md` and qualify four profiles on identical long-horizon missions:

1. built-in compressor + built-in memory/session_search;
2. LCM + built-in memory;
3. built-in compressor + Mnemosyne conservative local mode;
4. LCM + Mnemosyne conservative local mode.

Ownership for the preferred pair is strict:

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw host session history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = raw logs/diffs/results
```

Initial LCM: pin a qualified stable release, keep optional temporal/proactive/cross-session semantic-memory features off while Mnemosyne owns durable memory, and prove exact-detail drill-down, restart, backup and DB integrity.

Initial Mnemosyne: local embeddings only; `sync_roles: []`; explicit curated writes; strict write classifier; no remote sync/embedding/LLM endpoints; no host LLM; no tool-call autosave; no persona/enhanced/fact/polyphonic/proactive recall or automatic LLM-backed sleep until separately qualified. Use write approval for the memory-quality canary, then deliberately remove it only after the precision/hygiene gate if autonomous writes are promoted.

Enable Hermes Tool Search so LCM/Mnemosyne non-core tool schemas are progressively disclosed rather than all kept hot. Keep provider/plugin membership stable within a phase to preserve prompt-cache affinity.

After provisioning dependencies/models, deny outbound network and prove context compaction/recovery plus memory write/recall still work. A local-primary path with an unnoticed cloud fallback fails this phase.

Benchmark unsliced vs sliced skill usage and context/memory profiles. Track T0/T1 tokens, T1 update count, T2 bytes produced vs loaded, injected-memory tokens, tool-schema tokens, fresh/cached input, exact-detail recovery, recall precision/staleness, compactions, TTFT, RSS/store growth and accepted-task quality.

Promotion requires non-inferior accepted-task quality, better long-horizon recovery, useful low-noise durable recall, no unexpected network egress, no raw evidence/transcript duplication into memory, and rehearsed independent rollback to `context.engine: compressor` + `hermes memory off`.

Do not hide security invariants solely in optional slices or memory. Initial skill target remains >=30% lower skill-related input tokens with non-inferior accepted-task quality; T1 is normally <=8K tokens and smaller for simple phases. These are engineering targets, not guarantees.