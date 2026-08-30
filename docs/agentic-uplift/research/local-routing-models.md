# Local Routing Models and Router Frameworks — 2026 Assessment

## Mission routing is not the same as model difficulty routing

The first control decision in this workflow is categorical: should the mission be handled as research/synthesis, coding/tool action, hybrid, or local-only? That is different from the classic "strong model vs weak model" problem.

A robust pipeline can use both:

- **Intent/model-choice router**: predicts the best execution lane from task semantics and state.
- **Difficulty router**: predicts whether the default lane/model is likely to fail and should escalate.

Trying to make one legacy preference router solve both makes calibration opaque.

## Recommended router candidates

### 1. Deterministic rules — mandatory Tier 0

Use rules for high-precision signals and security constraints: explicit requests to edit/run/test, source-file paths, stack traces, `git diff`, compiler errors, explicit research verbs, web-source requirements, local-only/privacy tags and workflow state.

Rules are not a complete classifier. Their purpose is to cheaply resolve obvious cases and guarantee safety invariants. Ambiguous requests fall through to a learned semantic router.

### 2. Qwen3-Embedding-0.6B — best initial semantic baseline

Why:

- ~0.6B parameter embedding model;
- Apache-2.0 model card;
- supports semantic similarity/classification workflows;
- small enough to remain warm without materially competing with browsers/builds;
- can be used with prototype utterances first, then a lightweight linear classifier.

Recommended use: encode the latest user mission plus a compact state summary, compare against calibrated route prototypes, and abstain below a threshold/margin.

### 3. ModernBERT-base — preferred learned classifier after telemetry exists

ModernBERT-base is an encoder-class model (roughly 149M parameters) designed for retrieval/classification with long context relative to classic BERT. It is a better architectural match for a route classifier than a generative LLM.

Do not fine-tune it immediately. First gather route/outcome labels. Fine-tuning too early bakes guesses about the workload into the router and creates false confidence.

Suggested graduation criteria:

- >= 10k deduplicated, redacted, outcome-labeled missions;
- stable label ontology for at least 2–4 weeks;
- paired outcome data for ambiguous research/code missions;
- held-out corpus that includes short prompts, long specs, logs, mixed-language prompts and adversarial examples.

### 4. EmbeddingGemma — ultra-small embedding alternative

Google's EmbeddingGemma is ~300M parameters and designed for on-device embedding/classification, including quantized configurations with very small RAM footprints. It is attractive for an ultra-light router. Check the Gemma model terms against your deployment/licensing policy before standardizing it; it is not an Apache-2.0 equivalent by default.

### 5. Semantic Router (Aurelio AI)

Semantic Router remains a strong benchmark candidate: MIT licensed, actively maintained in 2026, and supports local encoders/indexes. It is especially good for prototype/utterance routing and fast iteration.

Production recommendation: use it behind your own `Router` interface rather than coupling Hermes directly to its classes. That makes it easy to replace after the bake-off.

### 6. RouteLLM (LMSYS)

RouteLLM is Apache-2.0 and provides MF, weighted-ranking, BERT, causal-LLM and random routers. Its published framing is strong-vs-weak model routing; the project reports up to 85% cost savings while retaining 95% GPT-4 benchmark performance for its historical setup.

Important limitations for this use case:

- pretrained routers were trained around historical GPT-4/Mixtral preference data, not DeepSeek-V4-Flash vs GLM-5.3-Flash mission outcomes;
- current documentation notes that MF/SW-ranking live inference can require an OpenAI embedding key, undermining a strict zero-cloud routing goal unless adapted;
- a high "strong model win rate" is a difficulty signal, not automatically a coding signal.

Use RouteLLM in the rig as a secondary/difficulty experiment, then retrain/recalibrate on paired DeepSeek/GLM outcomes before production.

## Large generative models considered for local routing

| Model | 2026 shape | Fit on 128 GB? | Router verdict | Better role |
|---|---|---:|---|---|
| Qwen3.8-Flash-Next | 125B language params, ~6B active, plus very large n-gram embedding/MTP components | quantized variants may technically fit only with substantial footprint/headroom tradeoff | **No as resident router** | on-demand local multimodal/agent fallback after ecosystem matures |
| Gemma 4 E2B/E4B | edge-oriented small variants | yes | possible but still generative overkill | local light agent/reviewer |
| Gemma 4 12B | personal-computer class | yes | no need for binary routing | local reviewer/coding fallback |
| Gemma 4 26B A4B / 31B | stronger local reasoning | yes in quantized form | too much resident RAM for routing | heavyweight reviewer |
| Llama 4 Scout | 17B active / 109B total, very long context | possible only with aggressive quantization and large footprint | **No** | special long-context local experiments |
| GPT-OSS-20B | 21B total / 3.6B active; official 16 GB-class deployment | comfortably | unnecessary for routing | excellent local structured reviewer/fallback |
| GPT-OSS-120B | official ~80 GB-class deployment | technically but conflicts with workstation headroom | **No** | occasional offline heavyweight review only |

### SSD/page offloading warning

Do not make SSD paging a baseline architecture requirement on this Mac. vLLM's broader KV/offload ecosystem has historically been strongest on CUDA/ROCm/XPU. vLLM-Metal exists for Apple Silicon and uses an MLX-oriented backend, but the exact feature parity of CPU/SSD offload connectors must be verified against the version you deploy. Unified memory also changes the economics: "CPU offload" is not the same optimization as discrete-GPU VRAM offload.

For local models, prefer MLX-LM prompt caching, quantized KV where supported, bounded KV size and on-demand model loading before relying on sustained swap/page pressure.

## Training data: do not start ModernBERT from scratch

You do not need to create all data from zero. Build a **mixture with careful licensing and local relabeling**:

1. **SWE-bench / SWE-bench Multilingual** — software-engineering issue prompts; MIT repository/license. Strong coding-positive seed set.
2. **CodeSearchNet query/doc pairs** — useful coding/search language; repository code/docs MIT but individual source-code licenses are carried per sample, so respect those metadata if using raw code.
3. **BFCL** — Apache-2.0 agent/tool-use evaluation data; valuable for tool-action/coding-adjacent intent.
4. **RouteLLM `gpt4_judge_battles`** — Apache-2.0, ~109k preference examples; valuable for difficulty/preference experiments, not direct intent labels.
5. **WildChat-1M** — broad real-world prompts under ODC-BY; useful for non-code/background negatives after privacy and license review. The dataset reports Presidio/rule de-identification but should still be scanned locally before use.
6. **LMSYS-Chat-1M** — useful real-world prompt distribution and explicitly mentions routing research, but it is gated under a custom dataset agreement with non-transfer obligations. Treat it as optional, not your dependency of record.
7. **Your own redacted Hermes mission telemetry** — ultimately the highest-value data because it captures your mission vocabulary, repositories, Spec Kit usage and routing outcomes.

### Labeling strategy

Use outcome labels, not just LLM opinions:

```text
mission -> candidate lane/model -> result
result = accepted? tests? reviewer score? latency? cost? retries? human override?
```

For a subset, run both DeepSeek and GLM against the same frozen task/environment. Create preference labels from deterministic acceptance criteria plus blinded review. That dataset can train both the mission classifier and a RouteLLM-style escalation model.

### Active-learning loop

1. Start with rules + semantic prototypes.
2. Log only redacted features, decision, confidence, chosen model and outcome.
3. Sample low-margin decisions, human overrides and failures for labeling.
4. Fine-tune ModernBERT/linear head.
5. Shadow it for a week; no routing authority.
6. Promote only if the held-out and live override metrics beat the prototype router.
7. Retrain on drift, not on a fixed calendar.

## Benchmark design

The supplied test harness measures:

- accuracy and macro-F1;
- per-class precision/recall/F1;
- confusion matrix;
- abstain rate;
- p50/p95/p99 decision latency;
- cold vs warm process behavior;
- deterministic-repeat agreement;
- optional model memory/RSS telemetry where available.

Run each router in a fresh subprocess to prevent one model/framework's caches from contaminating another's cold-start result.

## Recommended final routing policy

```text
if privacy/local-only/security rule => local-only / deny cloud
elif high-confidence deterministic coding => GLM lane
elif high-confidence deterministic research => DeepSeek lane
else:
    semantic = intent_router(mission + compact_state)
    if semantic.confidence >= T and margin >= M:
        route semantic target
    else:
        difficulty/preference gate or HYBRID
        HYBRID = DeepSeek planning artifact -> Pi/GLM implementation
```

For high-impact changes, the route itself should not decide merge authority.
