# Phase 00 — Preflight

Confirm the human foundation from `docs/agentic-uplift/fresh-install-bootstrap.md` before changing behaviour.

Verify target machine, free disk/memory pressure, Git status, exact repository commit, current Hermes profile/home/version, bootstrap isolation mode, policy SHA-256, rollback/evidence directory and current Pi version if installed.

Verify effective OpenRouter provider + exact single bootstrap model ID with current Hermes config/status tools **without printing the API key**. The research snapshot GLM-5.3-Flash ID is not a substitute for live verification. Confirm no direct-provider credential is required yet and no legacy Hermes/LCM/Mnemosyne DB is attached to the clean profile.

Capture prompt/context/tool/skill inventory and create schema-valid uplift state at `00-preflight` if no state exists.

**Gate:** clean profile runs, repo/policy/model/version evidence is known, bootstrap boundary is explicit, and no sensitive-data/credential boundary is unresolved.

**Adoption:** no optimization is assumed yet. Normally no restart.

Persist evidence/state, send the required phase-boundary report, then stop before Phase 10.
