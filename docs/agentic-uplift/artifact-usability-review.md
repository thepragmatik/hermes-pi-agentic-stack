# Artifact Usability & Fit-for-Purpose Review

## Verdict

**Architecture review / controlled prototype: fit. Unattended production self-uplift: not yet fit.**

This is deliberately stricter than the architecture adversarial review. A sound design can still fail because an artifact is ambiguous, non-executable, stale, or falsely appears to enforce policy.

## Readiness taxonomy

| Artifact | What it is | What it is not | Current status |
|---|---|---|---|
| `policy.example.yaml` | declarative policy intent | sandbox/egress enforcement | design-ready; enforcement P0 |
| Pi task schema | typed delegation contract | transport/auth/sandbox | schema-ready; integration P0 |
| uplift state schema | resumability contract | durable state store | schema-ready; persistence P0 |
| router benchmark | comparative test harness | production router | smoke-tested; live corpus P0 |
| sliced uplift skill | progressive-disclosure procedure | security boundary | prototype-ready |
| playbook | ordered implementation guidance | proof implementation succeeded | review-ready |
| Pages site | human/agent publication view | canonical secret-bearing store | publication-ready after CI deploy |

## P0 gates before unattended authority

1. Implement an external capability broker that makes orchestrator source-write/arbitrary-shell impossible, rather than merely instructing Hermes not to use them.
2. Implement egress scanning and network policy with seeded PII/secret canaries; prove `LOCAL_ONLY` cannot reach cloud adapters.
3. Implement the Hermes-to-Pi bridge with schema validation, idempotency, bounded retries, worktree isolation and evidence collection.
4. Persist uplift state atomically outside chat history; resume from that state after process/session restart.
5. Build a representative, redacted routing corpus from real mission distributions and temporal holdouts. The included corpus is a regression smoke set only.
6. Pin/audit Pi extensions and LSP servers; add upgrade compatibility tests.
7. Run target-machine measurements on the M3 Max under realistic browser/build/container pressure.
8. Add failure-injection tests for provider outage, partial worker completion, invalid LSP output, malicious repository instructions, and duplicate destructive retries.

## Concrete defects found during refinement

- The original Tier-0 privacy regex treated the word **“PII” itself** as sensitive payload, so a harmless request to *research PII detection tools* could be forced to `LOCAL_ONLY`. The rule is being narrowed to explicit local-only instructions and credential/identifier-shaped payload signals.
- The original policy YAML could be mistaken for enforcement. It now carries an explicit warning and versioned enforcement requirements.
- The original Pi schema lacked phase/attempt/risk/policy-digest/rollback bindings, making retries and resumability ambiguous. Version 2 binds those fields.
- Conversational phase memory was underspecified. A separate uplift-state schema now defines `PENDING → EXECUTING → COMPLETE | BLOCKED | ROLLBACK`.
- SVG diagrams were visually useful but not deterministic for text-only agents. Architecture now has Markdown and graph-JSON canonical representations.
- The initial benchmark corpus is far too small to substantiate production routing claims; all such scores are explicitly labelled smoke/regression evidence.

## Real-world operator UX review

A human operator needs one clear start page, explicit maturity labels, commands that are safe to copy, rollback instructions adjacent to mutating steps, and visible distinction between “recommended” and “implemented.” The Pages generator makes those labels part of the human site and exposes the same canonical source to agents.

An autonomous agent needs smaller requirements: a stable start URI/file, machine contracts, phase/state identifiers, deterministic evidence paths, and a rule to fetch only relevant slices. `llms.txt`, `agent/START.md`, JSON Schemas and the sliced skill provide that entry surface.

## Kill criteria

Stop or roll back the uplift if any of these occur: security policy can be bypassed by prompt/tool output; destructive retries are not idempotent; high-severity routing error exceeds the chosen threshold; accepted-task quality regresses materially; steady-state swap harms normal workstation use; upstream upgrade requires repeated invasive patches; or state recovery cannot prove which operations already executed.
