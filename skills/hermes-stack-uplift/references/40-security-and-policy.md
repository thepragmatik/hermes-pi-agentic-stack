# Phase 40 — Security, Policy and Authority Gate

Follow `docs/agentic-uplift/bootstrap-authority.md` and `research/security-zero-trust-pii.md`.

During bootstrap, direct Hermes write/shell capability exists only inside the explicitly constrained canary scope needed to build the replacement path. Do not call this zero-trust.

Build policy intent into external controls:

- role/capability validation;
- filesystem/workspace/path/symlink scope;
- process/command policy;
- environment allowlist/scrubbing;
- task-scoped credential brokerage;
- network default-deny/allowlist and egress policy;
- deterministic secret detection + typed/context-aware PII handling + re-scan;
- policy digest/evidence/idempotency binding;
- sandbox/containment interface;
- independent merge/review authority.

## OpenRouter enforcement

Privacy is decided locally **before** OpenRouter. Prove `LOCAL_ONLY` cannot reach OpenRouter through Auto, fallback, retry or provider failover. Verify only approved role/model bindings can make cloud requests; effective Hermes request-level provider routing and OpenRouter account guardrails do not conflict; direct-provider fallback cannot activate just because a key exists.

Do not rely on OpenRouter presets as the only provider-policy boundary until their interaction with Hermes request-level `provider_routing` is explicitly tested.

Enable Hermes `security-guidance` WARN mode where available as defense in depth only; it is not sandbox/DLP/Pi review.

Seed secrets, PII and technical false-positive fixtures. A policy YAML, prompt or sanitizer unit test is not containment evidence.

## Adoption Checkpoint C — evidence first, approval second

This is the security-critical boundary.

1. **First**, every mandatory P0 enforcement/egress/containment/privacy gate for the requested authority increase must pass with durable evidence.
2. Any failed, missing or unproven mandatory P0 gate means `BLOCKED`/`ROLLBACK`; remain at the existing authority level and repair/requalify.
3. **Only after those gates pass**, explicit human approval is additionally required before granting stronger cloud routing/delegation authority.
4. Human approval is not a waiver, exception or substitute for mandatory P0 evidence.

Restart/reload enforcement/router processes when needed to prove the tested policy digest is actually active.

Persist state/evidence, send the required phase-boundary report, and stop before Phase 50.
