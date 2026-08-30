# Phase 00 — Preflight

Confirm target machine, free disk, memory pressure, Docker/runtime availability, Git identity, network/provider access and current Hermes/Pi versions. Verify repository is clean. Read policy and compute its SHA-256. Create uplift state with status `PENDING`. Do not mutate installed Hermes/Pi yet.

Evidence: inventory JSON, version pins, policy digest, repository status. Block on unknown production credentials or unresolved sensitive-data boundary.
