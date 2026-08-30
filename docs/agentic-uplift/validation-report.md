# Refinement Validation Report

Snapshot: 2026-08-30.

## Evidence levels

This repository distinguishes four levels deliberately:

1. **researched** — supported by current primary/upstream sources;
2. **config/design validated** — repository artifacts are coherent and CI/site checks pass;
3. **canary runtime qualified** — exact pinned software has been installed and tested on a disposable target-machine profile;
4. **production promoted** — representative workload, adversarial, rollback and security gates passed and the change was deliberately promoted.

Do not report a lower level as a higher one.

## Executed repository / CI checks

The refinement package executes or is designed to execute: Python compilation for router/site tools; JSON parsing and JSON-Schema validation of task/state examples; YAML/frontmatter checks; site generation; internal-link validation; Markdown/`llms.txt` alternate checks; accessible SVG title/description checks; agent-manifest generation; and router smoke/regression tests.

During refinement these checks/reviews found real defects rather than merely confirming the design: invalid YAML frontmatter; incomplete SVG accessibility metadata; insufficient warning that policy examples are not enforcement; an overbroad privacy regex; a secret-pattern punctuation edge case; inconsistent bootstrap/security/Pi ordering; insufficient state/context ownership; duplicate-memory risk; canary write-approval semantics incompatible with autonomy; and ambiguity over whether LCM + Mnemosyne was a selected baseline or merely a challenger.

Those findings were corrected in canonical source.

## Latest GitHub Pages gate

On the fixed LCM + Mnemosyne baseline publication candidate, GitHub Actions completed successfully:

- Python 3.12 compilation of `tools/router-bench/router_bench.py`, `tools/site/build_site.py` and `tools/site/validate_site.py`;
- generation of **22 human pages plus the agent surface**;
- validation of **22 HTML pages and agent endpoints**;
- internal site links and Markdown/`llms.txt` alternate representations;
- accessible architecture SVG title/description checks;
- publication of `context-memory-setup.html`;
- raw + agent publication of the complete Hermes baseline config, LCM environment contract and Mnemosyne local config;
- Pages artifact upload and deployment pipeline accepted.

The generated agent manifest declares LCM + Mnemosyne as the context/memory baseline and `llms.txt` exposes the setup/runbook without requiring full-site ingestion.

## Router regression evidence

The last executed deterministic router smoke corpus produced **1.000 accuracy, 1.000 macro-F1 and 1.000 repeat determinism**, with zero observed high-severity lane errors over the small regression fixture. Warm routing latency was sub-millisecond in the available Linux/x86-64 validation runtime.

These numbers are regression evidence only. They are **not** claims about semantic-router accuracy, provider quality, M3 Max latency or production workload performance.

## LCM + Mnemosyne evidence status

Architecture status: **selected baseline**.

Evidence status: **researched + repository/config/site validated; not yet canary runtime qualified on the target Mac.**

The repository now contains one coherent baseline path:

- `docs/agentic-uplift/local-context-memory-setup.md` — install, pin, effective config, admission, health, compaction, offline, backup, rollback and upgrade procedure;
- `docs/agentic-uplift/research/local-context-memory-stack.md` — ownership/rationale/risks and evidence requirements;
- `configs/hermes-local-context-memory.example.yaml` — complete Hermes composition;
- `configs/lcm-baseline.env.example` — LCM scalar baseline;
- `configs/mnemosyne-local.example.yaml` — Mnemosyne local-only subconfiguration;
- Phase 30 execution gates in `implementation-playbook.md`;
- matching sliced context/memory skill guidance;
- adversarial tests for duplicate authority, poisoning, relevance, unexpected network fallback, SQLite recovery, tool-schema overhead and release/default drift.

Initial stable research pins are LCM `v0.20.0`, Mnemosyne core `3.15.1` and Hermes wrapper `0.5.0`. **Phase 00/30 must re-verify current stable releases, effective config and security notes before installation.** Unreleased `main`, release candidates and betas are not automatic upgrades.

### Baseline effective-config intent

The selected baseline requires:

```text
context.engine = lcm
compression.enabled = true
memory.provider = mnemosyne
memory.memory_enabled = false
memory.user_profile_enabled = false
memory.write_approval = false
Tool Search = on
LCM semantic/proactive/temporal cross-session memory = off
Mnemosyne transcript autosave + LLM/auto-sleep/persona/richer recall = off
Mnemosyne embeddings = local FastEmbed/ONNX
```

This removes duplicate built-in durable-memory authority while keeping Mnemosyne autonomous under a strict admission policy and narrow tool allowlist.

### Runtime evidence still required

On the target Mac, execute the required LCM + Mnemosyne baseline on representative long-horizon missions and collect at minimum:

- successful profile-local LCM install + resolved stable tag/commit;
- successful Mnemosyne side-venv/wrapper install + exact package pins;
- effective Hermes/provider config evidence matching the checked-in baseline;
- LCM exact-detail recovery after multiple compactions;
- restart/session recovery;
- Mnemosyne global/canonical memory lifecycle;
- durable-recall precision and stale/irrelevant-memory injection;
- autonomous curated memory writes under the strict classifier/admission policy;
- absence of transcript/raw-evidence duplication into Mnemosyne;
- injected-memory and plugin/tool-schema tokens;
- total/fresh/cached input and TTFT/wall time;
- SQLite/store growth, RSS, macOS memory pressure and swap;
- memory poisoning/contradiction behavior;
- independent backup/restore integrity for LCM and Mnemosyne;
- successful context/memory operation with outbound network denied after dependency/model provisioning;
- independent rollback to the previous known-good profile without deleting diagnostic stores.

Built-in-only, LCM-only and Mnemosyne-only profiles may be used to isolate a regression, but they no longer compete for production selection. If the required pair fails a mandatory gate, Phase 30 is `BLOCKED`/`ROLLBACK`; Hermes does not autonomously choose another memory architecture.

The stable Mnemosyne 3.15.x research pin predates later relevance/prefetch work, so **irrelevant-memory injection is explicitly blocking**. Do not pin unreleased `main` merely to bypass that test; qualify the next stable release normally.

## Target-machine / production evidence gaps

The available CI runtime is Linux/x86-64, not the target M3 Max. Production promotion still requires:

- the LCM + Mnemosyne runtime evidence above;
- representative redacted mission corpus and temporal router holdout;
- real provider/tool outcomes;
- target-Mac router/resource measurements under normal browser/build/container pressure;
- external capability/sandbox enforcement tests;
- egress PII/secret canaries;
- current Pi RPC compatibility and isolation evidence;
- LSP compatibility suite;
- failure injection for outage, retry, corrupted state, malicious context/memory/tool output and rollback.

## Maturity conclusion

The repository is **coherent and sufficiently detailed to start the controlled autonomous uplift mission from Phase 00 in a clean canary/bootstrap profile**. The LCM + Mnemosyne architecture decision is fixed and its setup/configuration is execution-ready, but this is not evidence that the target-Mac runtime baseline or the production uplift has already succeeded.

Hermes may autonomously execute read-only and canary phases according to the execution contract. It must mark `BLOCKED`/`ROLLBACK` instead of substituting another memory architecture or promoting any component whose mandatory runtime/security/local-only gate is unresolved.
