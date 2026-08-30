# Hermes Agentic Uplift Blueprint — 2026-08-30

## Scope

This repository-ready overlay is a production-oriented blueprint for a MacBook Pro M3 Max with 128 GB unified memory running Hermes Agent as the control-plane orchestrator and Pi as the dedicated coding worker. The measured workload baseline supplied for planning is **3,888,531,773 tokens/month**.

The design assumes the workstation also runs browsers, language servers, builds, Docker/VM workloads and ordinary developer applications. It therefore optimizes for **low resident memory, stable cloud prefix caching, deterministic delegation, privacy at the cloud boundary, and upgrade-safe extensions rather than invasive Hermes forks**.

## Executive architecture decision

Use a **small local control plane**, not a large resident generative router:

1. **Tier 0 deterministic gate** — explicit intent, security/privacy class, repository state, file types, tool/command cues and mission policy.
2. **Tier 1 local semantic classifier** — start with Qwen3-Embedding-0.6B prototypes or ModernBERT; train ModernBERT only after collecting a representative labeled mission set.
3. **Tier 2 uncertainty/difficulty gate** — optional RouteLLM-style preference routing for ambiguous cases after it is calibrated to your *actual* DeepSeek-vs-GLM outcomes.
4. **Tier 3 execution** — DeepSeek V4 Flash for research/synthesis and GLM-5.3-Flash for code/tool loops, with provider pinned for each session.
5. **Policy plane outside the LLM** — capabilities, PII/secrets egress filtering, network access, workspace boundaries and merge gates are enforced by code/configuration, not SOUL.md.

### Why this is the right shape

A binary or small multiclass router does not need 20B–125B generative weights permanently occupying unified memory. Models such as Qwen3.8-Flash-Next, Gemma 4, Llama 4 Scout and GPT-OSS are useful *on-demand local fallback/reviewer* options, but are economically and operationally excessive for intent classification. The always-on control plane should generally remain below a few GB, leaving memory headroom for developer workloads.

## Corrected interpretation of the Hermes prefill problem

Current Hermes already has a more contemporary context engine than many older installations: session-start frozen memory/context snapshots to preserve stable prefixes, lean compaction, old tool-output pruning, in-place compaction, model-specific thresholds and a pluggable context engine. Therefore the highest-leverage 2026 optimization for cloud models is not "add a local KV cache to Hermes". It is:

- keep the **system/tool/context prefix byte-for-byte stable** across sequential calls;
- put stable policy/context before volatile content;
- avoid changing provider/model mid-session;
- trim project context files, tool schemas and Spec Kit artifacts from the hot prefix;
- retrieve only the relevant slices of long artifacts;
- exploit provider-side cached input accounting and measure actual cache-hit tokens;
- use MLX/vLLM KV/prompt caches only when the model itself is served locally.

## Target topology

```text
User / Terminal
      |
      v
Hermes control session
(read / plan / delegate only)
      |
      +--> local policy gate --> PII + secret + trust classification
      |
      v
Local router daemon
rules -> semantic -> uncertainty
      |                         \
      | research                 \ coding/hybrid
      v                           v
DeepSeek V4 Flash        Hermes delegate_pi RPC tool
session pinned                |
                               v
                         isolated Pi worker
                       + git worktree/sandbox
                       + pinned GLM-5.3-Flash
                       + LSP-aware operations
                               |
                               v
                       evidence/review gateway
                       tests + diff + scanners
                               |
                               v
                           merge/human gate
```

`architecture.html` contains inline SVG diagrams for this topology, the prompt/cache layout and the zero-trust worker flow.

## Recommended baseline stack

| Layer | Baseline | Rationale |
|---|---|---|
| Mission router | rules + Qwen3-Embedding-0.6B prototypes | Apache-2.0, small enough to keep warm, no generation latency |
| Learned router | ModernBERT-base fine-tuned on production labels | 149M-class encoder; classification-native |
| Router framework | thin internal interface + Semantic Router adapter | avoids framework lock-in; Semantic Router is MIT and actively maintained |
| Difficulty router | RouteLLM MF/BERT only after recalibration | good strong-vs-weak formulation, but not a native research-vs-code classifier |
| Research cloud | DeepSeek V4 Flash | long context, automatic provider caching, strong research/agent behavior |
| Coding cloud | GLM-5.3-Flash | strong terminal/agent results and aggressive 2026 pricing |
| Cloud gateway | benchmark native APIs against OpenRouter | price alone is insufficient; compare cache hit, p95 TTFT, tool correctness, outages |
| Local inference | MLX-LM first; vLLM-Metal where needed | Apple-Silicon-native; avoid Linux/CUDA assumptions |
| Coding delegation | Pi RPC/headless subprocess | stable typed boundary instead of terminal prompt choreography |
| Code intelligence | reviewed/pinned Pi LSP extension + official language servers | diagnostics/refactors without injecting entire files into LLM context |
| PII | Presidio + deterministic recognizers | MIT, local, extensible |
| Secret leakage | Gitleaks CLI/rules plus request-time patterns | secret detection is separate from PII detection |
| Isolation | per-task worktree + sandbox profile + egress allowlist | deterministic zero-trust boundary |
| Spec Kit | Lite / Standard / High-Assurance presets | spend context only where ambiguity/risk justifies it |
| Telemetry | structured local JSONL/SQLite, redacted before persistence | supports reproducible evaluation without storing raw PII |

## Memory posture for 128 GB unified memory

A model "fitting" in 128 GB is not sufficient. The workstation must remain useful under browser/build/container pressure. Use these initial operating constraints and tune from macOS memory-pressure telemetry:

- reserve **35–45 GB** for macOS + ordinary developer applications + transient spikes;
- keep the normal routing/security/control-plane footprint **well below 5 GB**;
- keep large local reviewer/fallback models **unloaded until needed**;
- prefer a practical resident-model budget of **40–70 GB** rather than designing against the 128 GB theoretical ceiling;
- treat sustained swap/SSD paging as a failed steady-state configuration, not an optimization target.

## Rollout order

1. Capture baseline telemetry from representative research, coding, hybrid, bug-fix and architecture missions.
2. Bring a **fresh latest Hermes** to parity with upstream before applying the overlay. Keep the previous install read-only.
3. Export only durable, reviewed knowledge from the old context DB; do not bulk-import stale instructions/history.
4. Install capability policy and the privacy/secrets egress gate.
5. Install the local router and run `tools/router-bench/router_bench.py` in isolated subprocess sessions.
6. Add the Hermes→Pi RPC bridge and typed task envelope.
7. Add LSP servers and bounded diagnostic injection.
8. Add Spec Kit mission profiles.
9. Tune context ordering, compression thresholds and provider stickiness using measured cache-hit data.
10. Run the adversarial suite, canary the uplift, then promote.

## Production acceptance gates

- Intent/model-choice router macro-F1 **>= 0.97** on a representative held-out corpus.
- Explicit `abstain`/hybrid behavior is measured; uncertain requests are not silently forced into a class.
- Local routing p50 **<= 20 ms** and p95 **<= 50 ms** after warm-up on the target Mac for the chosen configuration.
- Orchestrator mode has **no direct source-write or arbitrary-shell capability**.
- Every coding task is delegated through a typed Pi task envelope into an isolated workspace.
- Every outbound cloud payload passes PII and secret scanning; seeded canaries are blocked in tests.
- Tool/schema/context prefix stability is measured and provider cached-input ratio materially improves.
- Spec Kit profile selection lowers median input tokens per accepted task by **>= 25%** compared with the current all-phases flow.
- Daily Hermes upstream-update rehearsal passes without overwriting uplift-owned files.
- Quality gate: accepted-task success rate is non-inferior to baseline within the chosen confidence interval.

## Files in this bundle

- `research/local-routing-models.md`
- `research/context-token-optimization.md`
- `research/hermes-pi-lsp.md`
- `research/security-zero-trust-pii.md`
- `spec-kit-profiles.md`
- `implementation-playbook.md`
- `adversarial-review.md`
- `savings-model.md`
- `architecture.html`
- `../../tools/router-bench/router_bench.py`
- `../../protocols/pi-task-envelope.schema.json`
- `../../configs/policy.example.yaml`
- `SOURCES.md`

## Upgrade-safe rule

**This uplift is an overlay, not an ongoing fork patch set.** Prefer Hermes extensions/skills/config, external daemons and narrow adapters. Any unavoidable upstream patch must be feature-flagged, covered by an integration test, and tracked for upstreaming/removal. Daily upgrade automation should fail closed if an uplift integration point changes.
