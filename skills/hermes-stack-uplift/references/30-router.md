# Phase 30 — Router

Implement routing in this order:

1. Tier 0 deterministic security/privacy rules;
2. deterministic agent-state gates;
3. compact semantic routing;
4. confidence calibration, hysteresis and abstention;
5. optional learned/difficulty escalation.

Separate mission-type routing from strong-vs-weak difficulty routing. Validate explicit `hybrid`, `local_only` and `abstain`. Provider/model selection is a downstream role binding and should remain session-sticky.

Before fine-tuning any encoder, run the curriculum in `docs/agentic-uplift/research/router-training-control.md`: compare always-research, always-coding, deterministic state rules, Qwen3-Embedding-0.6B prototypes, and frozen `nomic-ai/modernbert-embed-base` (256d and 768d) with the same calibrated linear/logistic head plus explicit state features. Fine-tune ModernBERT-base only if the frozen-head baseline plateaus on representative pair-specific data.

Route **phases rather than micro-turns**. Keep the current lane inside a calibrated middle confidence band; switch only at meaningful phase boundaries or when the new-lane confidence/margin clears the entry threshold. Measure route-switch rate and provider cache continuity.

Run the regression corpus plus a representative redacted holdout split by mission/repository/session/time rather than random turns. A mention of security/PII technology is not itself sensitive payload.

Promotion evidence must include downstream accepted-task utility/regret, high-severity wrong-lane errors, retries/human overrides, route-switch rate, cache-hit continuity, local latency/memory and classification/calibration metrics. Security-class violations remain fail-closed and outside the learned router.
