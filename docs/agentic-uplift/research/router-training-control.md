# Router Training and Control Refinement

## Decision

Do not jump directly from rule/prototype routing to full encoder fine-tuning. Use a staged curriculum that makes mistakes observable and cheap to reverse:

```text
security/privacy hard gate
  -> deterministic agent-state gate
  -> frozen semantic encoder + calibrated head
  -> confidence / hysteresis / abstention
  -> optional fine-tuned ModernBERT
  -> optional pairwise difficulty/escalation model
```

The router should optimize **downstream accepted-task utility and route stability**, not classification accuracy in isolation.

## Frozen ModernBERT baseline

Benchmark `nomic-ai/modernbert-embed-base` as an immediate challenger to Qwen3-Embedding-0.6B.

Why it belongs in the bake-off:

- derived from ModernBERT-base;
- Apache-2.0;
- approximately 0.1B parameters;
- 8,192-token ModernBERT context family;
- 768-dimensional embeddings with a supported 256-dimensional Matryoshka representation;
- trained specifically for embedding/retrieval/classification-like use rather than generation.

The Nomic model card requires query/document prefixes. Treat prefix choice as part of the pinned router configuration rather than an incidental prompt detail.

Benchmark both 256d and 768d. The smaller representation may be enough for a small route ontology and reduces downstream classifier/index memory, but only measurements on the held-out mission corpus should decide.

## Do not fine-tune the encoder first

Stage A should freeze the encoder and train only one of:

- multinomial logistic regression;
- calibrated linear head;
- very small MLP when linear separation is demonstrably insufficient.

This gives a fast retraining loop and makes it easier to distinguish a bad label ontology from a representation problem.

Fine-tune `answerdotai/ModernBERT-base` only after the frozen-head baseline plateaus on representative data. ModernBERT-base is a 149M-parameter Apache-2.0 encoder trained on English and code with native long-context support up to 8,192 tokens, making it a sensible classification architecture when a learned boundary is actually needed.

## Input is semantic text plus explicit state

Do not force the encoder to infer operational state that Hermes already knows deterministically.

Recommended feature vector:

```text
semantic_embedding(mission capsule / latest task)
phase
current_lane
file_write_requested
test_failure_present
tool_action_pending
external_research_required
repo_dirty
worker_active
security_class
spec_kit_profile
recent_route_switches
last_route_confidence
```

Categorical/boolean state can be concatenated to the frozen embedding before the small head or handled by a separate deterministic gate.

Security/privacy class is not a learnable preference. It remains an external hard gate.

## Route phases, not micro-turns

A good router should not reconsider the cloud specialist after every trivial follow-up.

Examples:

- a Pi coding worker is active and the next message is steering/follow-up -> remain coding;
- a failing test is being repaired -> remain coding unless a deliberate research escalation is requested;
- a research synthesis phase is collecting sources -> remain research;
- a research plan has been accepted and execution begins -> phase boundary permits research -> coding transition.

This reduces model/provider churn, preserves cache affinity and prevents semantic noise in short follow-ups from flipping the lane.

## Hysteresis

Use separate enter/leave thresholds rather than one decision threshold.

Conceptually:

```text
if hard_gate:
    obey hard gate
elif confidence >= ENTER_NEW_LANE and margin >= ENTER_MARGIN:
    switch lane
elif confidence <= ABSTAIN_THRESHOLD:
    abstain / request resolver
else:
    stay on current lane
```

Tune the middle band from observed regret. A slightly slower correct phase transition is usually cheaper than repeated DeepSeek/GLM oscillation and cache loss.

## Training curriculum

### Stage 0 — deterministic baselines

Measure:

1. always research;
2. always coding;
3. current deterministic rules;
4. rules + structured state.

### Stage 1 — frozen embeddings

Compare at minimum:

- Nomic ModernBERT Embed 256d;
- Nomic ModernBERT Embed 768d;
- Qwen3-Embedding-0.6B;
- any smaller licensing-compatible encoder that materially improves latency/memory.

Fit the same calibrated head and state features to each so the comparison is fair.

### Stage 2 — active learning

Prioritize labeling:

- low-margin decisions;
- route switches;
- human overrides;
- hybrid missions;
- failures/retries;
- tasks where DeepSeek and GLM outcomes disagree;
- long Spec Kit missions;
- prompts containing security vocabulary but no sensitive payload.

### Stage 3 — paired outcome data

For a controlled subset, run both candidate specialists against the same frozen task/environment. Label using deterministic acceptance evidence plus blinded review.

This pair-specific dataset matters more than generic public intent labels for the final DeepSeek-vs-GLM boundary.

### Stage 4 — encoder fine-tuning only if justified

Fine-tune ModernBERT when all are true:

- frozen encoder + head has plateaued;
- route ontology has been stable for multiple weeks;
- representative pair-specific data exists;
- mission/repository-level holdout regret improves, not merely row-level F1;
- calibration remains acceptable after fine-tuning.

## Evaluation split

Do not randomly split near-duplicate turns from the same mission across train/test.

Split by **mission / repository / session / time cohort** so the holdout represents genuinely unseen work. Keep a later temporal canary for drift.

## Primary metrics

Classification metrics remain useful, but the promotion hierarchy should be:

1. accepted-task utility / regret;
2. security-class violations (must be zero for `LOCAL_ONLY -> cloud`);
3. wrong-lane high-severity errors;
4. retries and human overrides;
5. route-switch rate per mission;
6. provider/model cache-hit continuity;
7. mission duration and TTFT;
8. total/fresh/cached tokens and cost;
9. macro-F1, per-class precision/recall and calibration;
10. local router latency and resident memory.

A router with slightly lower F1 can still be superior if it abstains safely, avoids costly oscillation and produces better accepted-task outcomes.

## Promotion rule

The learned router receives authority only after it beats deterministic/state baselines on a held-out mission corpus and survives a shadow period.

Initial engineering targets remain useful but are not sufficient by themselves:

- macro-F1 >= 0.97 on representative held-out missions;
- zero observed `LOCAL_ONLY -> cloud` errors;
- warm p95 local decision latency <= 50 ms on the target Mac;
- route-switch rate materially below a no-hysteresis challenger;
- accepted-task quality non-inferior to the best fixed-lane baseline.

## Relationship to RouteLLM

RouteLLM remains an optional **difficulty / escalation** component. Do not confuse its strong-vs-weak preference framing with the primary research-vs-coding lane decision. Any RouteLLM-style model must be recalibrated on actual specialist outcomes before authority.
