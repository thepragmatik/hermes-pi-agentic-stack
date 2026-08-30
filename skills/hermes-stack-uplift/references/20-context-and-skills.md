# Phase 20 — Context, Skills and Local Memory

**Architecture decision:** LCM + Mnemosyne is the required clean-profile baseline. Diagnostic controls are retained only to isolate regressions; Hermes must not autonomously substitute a different production memory provider/context engine if the required pair fails a mandatory gate.

Apply `docs/agentic-uplift/research/mission-context-architecture.md`:

- **T0 stable prefix** — identity, minimal invariants, stable profile/tool schemas and compact skill catalog;
- **T1 mission capsule** — bounded current objective/phase/constraints/acceptance/routing/evidence pointers, regenerated only at meaningful phase boundaries;
- **T2 artifact/evidence memory** — logs, diffs, Pi RPC streams, benchmarks, research and large Spec Kit/source artifacts remain outside hot context and are retrieved by slice.

Then follow `docs/agentic-uplift/local-context-memory-setup.md` and `docs/agentic-uplift/research/local-context-memory-stack.md`.

## Baseline ownership

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw host session history / forensic search
uplift-state = deterministic mission authority
T2 evidence  = raw logs/diffs/results
Git/ADR/spec = project truth
```

Memory never overrides policy, uplift-state, Git/ADR/spec or immutable evidence.

## LCM baseline

Pin the current qualified **stable** LCM release profile-locally; initial research pin is `v0.20.0`. Record full commit/tag and apply `configs/lcm-baseline.env.example` through the canary launcher.

Required initial posture:

- `context.engine: lcm`;
- Hermes compression lifecycle remains enabled;
- threshold 0.35, fresh tail 32, depth 3, leaf floor 20K;
- dynamic chunking/full-sweep disabled initially;
- LCM embeddings OFF;
- LCM proactive recall OFF;
- LCM temporal rollups OFF;
- optional slash command OFF;
- profile-scoped default DB path;
- prove exact-detail drill-down, multiple compactions, restart, doctor/integrity and backup.

Do not promote an LCM RC merely because upstream `main` is newer.

## Mnemosyne baseline

Use a profile-owned side venv and wrapper integration; initial stable research pins are core `3.15.1` and Hermes wrapper `0.5.0`. Use `mnemosyne-memory[embeddings]`, not `[all]`, and provision the local `BAAI/bge-small-en-v1.5` FastEmbed model before offline qualification.

Apply the complete composition in `configs/hermes-local-context-memory.example.yaml` and the Mnemosyne detail in `configs/mnemosyne-local.example.yaml`.

Required effective state:

```text
memory.provider = mnemosyne
memory.memory_enabled = false
memory.user_profile_enabled = false
memory.write_approval = false
sync_roles = []
local embeddings only
write_classifier = strict
default durable scope = global
session cross-recall = false
```

Explicitly keep host/remote LLM, LLM conflict detection, auto-sleep, persona, enhanced/fact/polyphonic recall, proactive linking, query-intent and remote sync OFF. Bound provider prefetch initially to 800 content characters.

Only expose the narrow curation/inspection Mnemosyne tool set defined in the baseline config. Hard-delete, remote sync/shared, graph, persona, scratchpad, import/export and sleep tools stay outside the ordinary orchestrator profile.

Built-in MEMORY/USER are disabled deliberately: Mnemosyne is the sole durable-memory provider; `state.db/session_search` remains the raw session-history path.

## Memory admission

Use canonical Mnemosyne memory only for stable one-current-value profile/operator facts. Use ordinary global memory for compact durable lessons/decisions that do not belong in Git/ADR/spec.

Never store mission state, raw logs/diffs/Pi streams, source corpora, secrets/PII, temporary blockers/tasks, whole session summaries or unsanitized legacy material in Mnemosyne.

## Tool/schema containment

Hermes Tool Search is mandatory in this baseline so LCM/Mnemosyne non-core tools are progressively disclosed. Use the versioned config (`5%`, default search 5, max 20, listing auto, listing budget 4000) and measure actual schema tokens/cold-tool round trips.

## Qualification

Retain these only as diagnostic component-isolation controls:

1. built-in compressor + no external provider;
2. LCM + no external provider;
3. built-in compressor + Mnemosyne;
4. **LCM + Mnemosyne required baseline**.

The first three do not compete for production selection.

Seed exact details before multiple compactions; verify restart recovery, global/canonical memory behavior, stale/contradictory rejection, irrelevant-memory injection, no PII/secret durable memory and T2 retrieval by pointer.

The stable Mnemosyne 3.15.x research pin predates later relevance/prefetch work, so irrelevant-memory injection is a blocking test. Do not jump to unreleased `main`; canary-upgrade a future stable normally.

After package/model provisioning, deny outbound network and prove LCM compaction/retrieval plus Mnemosyne global/canonical write/recall/restart/backup still work. Any remote fallback fails the phase.

Promotion requires non-inferior accepted-task quality, reliable exact-detail recovery, low-noise durable recall, no unexpected egress, bounded tool/schema cost, verified backup/restore and acceptable target-Mac RSS/memory pressure.

If a mandatory LCM/Mnemosyne gate fails, mark the phase `BLOCKED` or `ROLLBACK`. Do **not** promote Holographic/OpenViking or another memory architecture autonomously.

Do not hide security invariants solely in optional slices or memory. Initial skill target remains >=30% lower skill-related input tokens with non-inferior accepted-task quality; T1 is normally <=8K tokens and smaller for simple phases. These are engineering targets, not guarantees.
