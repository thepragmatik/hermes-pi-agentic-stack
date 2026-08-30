# Router benchmark rig

This rig compares local routing strategies in **fresh processes by default** so model startup cost, resident memory, and warmed classification latency are visible separately. It deliberately records a SHA-256 of each prompt rather than raw prompt text unless `--include-text` is explicitly enabled.

## 1. Start with the zero-dependency baseline

```bash
cd tools/router-bench
python3 router_bench.py \
  --dataset sample_missions.jsonl \
  --routers rules \
  --repeat 20 \
  --pretty \
  --output rules.json
```

## 2. Embedding prototype router

For the target M3 Max, start with Qwen3-Embedding-0.6B and compare it against a very small embedding model to quantify the latency/accuracy tradeoff.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install 'sentence-transformers>=3'

python router_bench.py \
  --dataset sample_missions.jsonl \
  --routers rules,prototype \
  --embedding-model Qwen/Qwen3-Embedding-0.6B \
  --repeat 20 \
  --output embedding.json
```

The supplied prototype utterances are only smoke-test seeds. Replace them with redacted, adjudicated production examples before making a decision.

## 3. Aurelio Semantic Router

Pin **0.1.16 or later** rather than old releases. Version 0.1.15 contained an important security fix and 0.1.16 is the contemporary baseline used by this playbook.

```bash
pip install 'semantic-router[local]>=0.1.16'
python router_bench.py \
  --dataset missions-held-out.jsonl \
  --routers semantic-router \
  --semantic-model sentence-transformers/all-MiniLM-L6-v2 \
  --repeat 20 \
  --output semantic-router.json
```

Then repeat with a stronger local encoder. The framework should be treated as an adapter, not as an architectural dependency.

## 4. Fine-tuned ModernBERT

After collecting production-like labels and fine-tuning a sequence classifier whose `id2label` values are `deepseek`, `glm`, `hybrid`, and optionally `abstain`:

```bash
python router_bench.py \
  --dataset missions-held-out.jsonl \
  --routers modernbert \
  --modernbert-model ./models/modernbert-mission-router \
  --repeat 20 \
  --output modernbert.json
```

Do **not** train this from scratch. Start from ModernBERT-base and use public seed data plus redacted Hermes mission logs and active-learning/adjudication data as described in the research note.

## 5. RouteLLM

RouteLLM's public pretrained routers estimate *strong-model preference/difficulty*; they were not trained to classify `research` versus `coding`. This adapter exists so you can measure whether difficulty is useful as a **second-stage** gate. Its historical MF router can require an OpenAI-compatible embedding/API configuration and should not be treated as the near-zero-cost Tier-1 router.

```bash
pip install routellm
export OPENAI_API_KEY=...  # if required by the selected RouteLLM config
python router_bench.py \
  --dataset missions-held-out.jsonl \
  --routers routellm \
  --routellm-strong-label deepseek \
  --routellm-weak-label glm \
  --routellm-threshold 0.55 \
  --output routellm.json
```

For production, retrain/calibrate RouteLLM on **paired DeepSeek-vs-GLM outcomes from your own missions** if you want it to select between those models.

## 6. Any academic/custom router

Expose it as a command that reads one prompt from stdin and emits:

```json
{"label":"glm","confidence":0.91}
```

Then:

```bash
python router_bench.py \
  --dataset missions-held-out.jsonl \
  --routers my-router \
  --external 'my-router=./my_router_cli --json' \
  --output custom.json
```

## Multi-session terminal evaluation

Run separate tabs if you want to observe memory pressure interactively:

```bash
# tab 1
python router_bench.py --dataset missions-held-out.jsonl --routers rules --repeat 100 --output /tmp/rules.json

# tab 2
python router_bench.py --dataset missions-held-out.jsonl --routers prototype --repeat 100 --output /tmp/prototype.json

# tab 3
python router_bench.py --dataset missions-held-out.jsonl --routers semantic-router --repeat 100 --output /tmp/semantic.json

# tab 4 — only after a checkpoint exists
python router_bench.py --dataset missions-held-out.jsonl --routers modernbert --modernbert-model ./models/router --repeat 100 --output /tmp/modernbert.json
```

The rig itself isolates routers by subprocess unless `--in-process` is requested, so a single command is enough for repeatable machine-readable comparison too.

## Production evaluation protocol

Use at least three datasets:

1. **Clean held-out:** normal historical missions never used to tune the router.
2. **Boundary/adversarial:** mixed research+code prompts, short prompts, indirect phrasing, prompt injection, and deliberate PII/local-only cases.
3. **Temporal canary:** newest 5–10% of redacted missions, never retrospectively used for tuning.

Track macro-F1 *and* the asymmetric errors. `local_only -> cloud` is a security incident, not just a classification miss. `glm -> deepseek` and `deepseek -> glm` should also be tracked separately because the operational cost differs.

Recommended initial gate: macro-F1 >= 0.97, zero observed `local_only -> cloud` in the security test set, p50 <= 20 ms and p95 <= 50 ms after warmup on the target Mac. Calibrate abstention rather than forcing low-confidence guesses.
