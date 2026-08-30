# Phase 40 — Security, Policy and Bootstrap Enforcement

Follow `docs/agentic-uplift/bootstrap-authority.md` for the temporary root-of-trust transition.

During bootstrap, use the existing Hermes write/shell capability only inside the explicitly constrained canary/overlay/worktree scope while building the replacement enforcement path. Do **not** remove that bootstrap capability until the Pi path is proven; doing so would create a circular dependency.

Build policy intent into real external controls before granting a cloud worker production authority:

- role/capability validation;
- filesystem/workspace scope;
- process/command policy;
- environment allowlist/scrubbing;
- task-scoped credential brokerage;
- network/egress policy;
- deterministic secret detection plus typed PII detection/redaction/tokenization;
- evidence and policy-digest binding;
- sandbox launcher/containment interface;
- merge/review authority separation.

Enable Hermes `security-guidance` in WARN mode when available as cheap defense in depth for Hermes-owned write/patch content. It is not DLP, a sandbox, or a review of Pi worktree changes.

Seed canaries and prove local-only/secret payloads fail closed. Do not promote while policy exists only as YAML/prompts, and do not treat a passing sanitizer unit test as proof of containment.

The phase may complete the enforcement substrate while bootstrap authority still exists in canary scope. Final revocation of direct Hermes coding/shell authority happens only after Phase 50 proves the replacement Pi path and a privacy-controlled worker canary.
