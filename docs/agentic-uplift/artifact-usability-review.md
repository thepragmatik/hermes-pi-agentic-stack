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
| LCM + Mnemosyne baseline configs | selected local context/memory configuration contract | installed/benchmarked production subsystem | config-ready; target-Mac qualification P0 |
| local context/memory setup runbook | deterministic install/verify/offline/backup/rollback procedure | evidence those steps have run on the target Mac | execution-ready; runtime evidence P0 |
| playbook | ordered implementation guidance | proof implementation succeeded | review-ready |
| Pages site | human/agent publication view | canonical secret-bearing store | deployed; public/sanitized surface only |

## P0 gates before unattended authority

1. Implement an external capability broker that makes orchestrator source-write/arbitrary-shell impossible, rather than merely instructing Hermes not to use them.
2. Implement egress scanning and network policy with seeded PII/secret canaries; prove `LOCAL_ONLY` cannot reach cloud adapters.
3. Implement the Hermes-to-Pi bridge with schema validation, idempotency, bounded retries, worktree isolation and evidence collection.
4. Persist uplift state atomically outside chat history; resume from that state after process/session restart.
5. Build a representative, redacted routing corpus from real mission distributions and temporal holdouts. The included corpus is a regression smoke set only.
6. Pin/audit Pi extensions and LSP servers; add upgrade compatibility tests.
7. Run target-machine measurements on the M3 Max under realistic browser/build/container pressure.
8. Add failure-injection tests for provider outage, partial worker completion, invalid LSP output, malicious repository instructions, and duplicate destructive retries.
9. Qualify the required **LCM + Mnemosyne baseline** on the target Mac: exact LCM recovery, Mnemosyne recall precision/staleness, tool/context token overhead, restart/backup/restore, memory poisoning, storage/RSS growth, autonomous curated writes, and successful context/memory operation with outbound network denied. Rehearse independent rollback without silently promoting another architecture.

## Concrete defects found during refinement

- The original Tier-0 privacy regex treated the word **“PII” itself** as sensitive payload, so a harmless request to *research PII detection tools* could be forced to `LOCAL_ONLY`. The rule was narrowed to explicit local-only instructions and credential/identifier-shaped payload signals.
- The original policy YAML could be mistaken for enforcement. It now carries an explicit warning and versioned enforcement requirements.
- The original Pi schema lacked phase/attempt/risk/policy-digest/rollback bindings, making retries and resumability ambiguous. Version 2 binds those fields.
- Conversational phase memory was underspecified. A separate uplift-state schema defines `PENDING → EXECUTING → COMPLETE | BLOCKED | ROLLBACK`.
- SVG diagrams were visually useful but not deterministic for text-only agents. Architecture now has Markdown and graph-JSON canonical representations.
- The initial benchmark corpus is far too small to substantiate production routing claims; all such scores are explicitly labelled smoke/regression evidence.
- The initial memory recommendation treated built-in memory as the long-term default and underweighted the previously successful LCM + Mnemosyne pattern. The architecture now fixes **LCM=current-session context/recovery** and **Mnemosyne=curated durable memory**, with `state.db`, uplift-state and project truth remaining separate authorities.
- The first LCM/Mnemosyne refinement still framed the pair as a canary winner in a four-profile production bake-off. That no longer matches the selected architecture. Component-isolation controls remain for diagnosis only; baseline failure now produces `BLOCKED`/`ROLLBACK` rather than autonomous substitution.
- Keeping built-in MEMORY/USER alongside Mnemosyne would create duplicate durable-memory guidance/authority and unnecessary prompt/tool surface. The baseline now explicitly disables both built-in stores while leaving the external provider active.
- Requiring write approval for every Mnemosyne durable write would make the supposed autonomous baseline dependent on human staging approval. The baseline instead uses autonomous writes with a strict classifier, explicit admission policy, narrow tool allowlist and adversarial tests.
- LCM v0.20 includes optional semantic/cross-session recall and Mnemosyne can automatically persist/inject/consolidate memory. Enabling all features in both would duplicate state and context. Overlapping LCM semantic/proactive/temporal memory and Mnemosyne transcript/LLM/persona/sleep features are explicitly disabled.
- Mnemosyne's effective configuration defaults have changed over time. The playbook therefore pins stable releases, explicitly sets baseline behavior, checks effective runtime config and treats upstream default drift as a qualification failure until reviewed.
- Stable Mnemosyne 3.15.x predates later upstream work on relevance/prefetch behavior. The baseline does not chase unreleased `main`; irrelevant-memory injection is a blocking target-Mac test and future stable releases are canary-qualified normally.

## Real-world operator UX review

A human operator needs one clear start page, explicit maturity labels, commands that are safe to copy, rollback instructions adjacent to mutating steps, and visible distinction between “selected architecture” and “runtime-qualified implementation.” `docs/agentic-uplift/local-context-memory-setup.md` now provides one deterministic context/memory setup path, while the Pages generator exposes the same canonical source to agents.

An autonomous agent needs a stable start URI/file, machine contracts, phase/state identifiers, deterministic evidence paths, explicit state ownership, and a rule to fetch only relevant slices. `llms.txt`, `agent/START.md`, JSON Schemas and the sliced skill provide that entry surface.

For context/memory specifically, the operator must be able to answer **where a fact came from and which store is authoritative**. Remembered content is advisory. Current policy/uplift state/repository truth/evidence outrank both LCM-recovered text and Mnemosyne recall.

## Kill criteria

Stop or roll back the uplift if any of these occur: security policy can be bypassed by prompt/tool/memory output; destructive retries are not idempotent; high-severity routing error exceeds the chosen threshold; accepted-task quality regresses materially; steady-state swap harms normal workstation use; context/memory unexpectedly requires network access; built-in and external memory become competing authorities; memory poisoning or stale/irrelevant recall influences an acceptance/security decision; autonomous memory writes cannot satisfy the admission policy; SQLite backup/recovery cannot be proven; upstream upgrade requires repeated invasive patches; or state recovery cannot prove which operations already executed.
