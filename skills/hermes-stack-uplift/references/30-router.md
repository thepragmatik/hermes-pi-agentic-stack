# Phase 30 — Local Mission Router + OpenRouter Roles

Start this phase in the **fresh optimized Hermes session required by Checkpoint A**.

Implement routing in this order:

1. Tier 0 deterministic local privacy/security policy;
2. deterministic agent-state gates;
3. compact semantic routing;
4. confidence calibration, hysteresis and abstention;
5. optional second-stage difficulty/preference escalation.

Separate responsibilities:

```text
local policy -> local mission lane -> model role/model -> OpenRouter -> physical provider
```

`LOCAL_ONLY` never reaches OpenRouter. The local router decides research/coding/hybrid/review/auxiliary/abstain and role/model; OpenRouter provider routing is downstream. OpenRouter Auto is a shadow/fallback experiment only, never privacy or final mission classification.

Follow `research/router-training-control.md` and `research/openrouter-routing.md`. Compare deterministic state rules, embedding prototypes and frozen `nomic-ai/modernbert-embed-base` 256d/768d with the same calibrated lightweight head. Fine-tune ModernBERT only after representative redacted real missions/outcomes, deduplication, stable ontology, mission/repository/session/time holdout, ambiguous/hybrid examples and frozen-head plateau show it is justified.

Route **phases rather than micro-turns**. Use hysteresis; measure route-switch rate and OpenRouter model/physical-provider cache continuity.

Keep volatile model IDs in `configs/models.example.yaml`/runtime locks. Research snapshot intent is GLM-5.3-Flash-class for bootstrap/coding and DeepSeek-V4-Flash-class for research, both through OpenRouter; re-verify exact current IDs via Hermes/OpenRouter before binding.

Use only provider-routing fields actually supported by the installed Hermes release. Do not assume an OpenRouter preset overrides Hermes request-level provider policy without an explicit effective-policy test.

Run a representative redacted shadow corpus. Promotion evidence includes accepted-task utility/regret, high-severity lane errors, zero observed `LOCAL_ONLY -> cloud`, calibration/abstention, route-switch rate, cache continuity, local latency/RSS, tool correctness and retries.

## Restart/Canary Checkpoint B

A passing Phase 30 enters **shadow mode only**. Reload/restart the router integration if required and prefer a fresh shadow session so the tested router/config is demonstrably active. Do not grant routing authority yet.

Persist state/evidence, send the required phase-boundary report, and stop before Phase 40.
