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

During refinement these checks/reviews found real defects rather than merely confirming the design: invalid YAML frontmatter caused by an unquoted colon; incomplete SVG accessibility metadata; insufficient warning that policy examples are not enforcement; an overbroad privacy regex that treated the vocabulary word “PII” as sensitive payload; a secret-pattern punctuation edge case; inconsistent bootstrap/security/Pi ordering; and insufficiently explicit context/memory ownership.

Those findings were corrected in canonical source.

## Latest GitHub Pages gate

On the latest context/memory publication candidate, GitHub Actions completed successfully:

- Python 3.12 compilation of `tools/router-bench/router_bench.py`, `tools/site/build_site.py` and `tools/site/validate_site.py`;
- generation of the complete human/agent site;
- validation of **21 HTML pages and agent endpoints**;
- internal site links and alternate representations;
- accessible architecture SVG title/description checks;
- upload of the Pages artifact;
- successful GitHub Pages deployment.

The public generated surface now includes the local context/memory research page plus non-secret Hermes/Mnemosyne canary configuration examples in both raw and agent-facing surfaces.

## Router regression evidence

The last executed deterministic router smoke corpus produced **1.000 accuracy, 1.000 macro-F1 and 1.000 repeat determinism**, with zero observed high-severity lane errors over the small regression fixture. Warm routing latency was sub-millisecond in the available Linux/x86-64 validation runtime.

These numbers are regression evidence only. They are **not** claims about semantic-router accuracy, provider quality, M3 Max latency or production workload performance.

## LCM + Mnemosyne evidence status

Current status: **researched + repository/config validated; not yet canary runtime qualified on the target Mac.**

The repository now contains:

- `docs/agentic-uplift/research/local-context-memory-stack.md` — ownership, alternatives, setup, four-profile benchmark, promotion and rollback design;
- `configs/hermes-local-context-memory.example.yaml` — Hermes canary fragment selecting LCM and Mnemosyne plus Tool Search;
- `configs/mnemosyne-local.example.yaml` — conservative local-only memory behavior without secrets/remote endpoints;
- Phase 30 execution gates in `implementation-playbook.md`;
- the matching sliced context/memory skill reference;
- adversarial tests for duplicate memory authority, poisoning, unexpected network fallback, SQLite recovery, tool-schema overhead and release/default drift.

The research currently targets stable LCM `v0.20.0`, Mnemosyne core `v3.15.1` and Hermes integration `v0.5.0`, but **Phase 00/30 must re-verify current stable releases, effective config and security notes before installation**. A later stable version is not automatically rejected; an RC is not automatically promoted.

### Runtime evidence still required

On the target Mac, compare the same long-horizon missions across:

1. built-in compressor + built-in memory/session_search;
2. LCM + built-in memory;
3. built-in compressor + Mnemosyne conservative local mode;
4. LCM + Mnemosyne conservative local mode.

Collect at minimum:

- accepted-task success/quality;
- exact-detail recovery after multiple compactions;
- restart/session recovery;
- cross-session durable-recall precision/recall and stale/irrelevant recall;
- injected-memory and plugin/tool-schema tokens;
- total/fresh/cached input and TTFT/wall time;
- compaction/recovery calls;
- SQLite/store growth, RSS, memory pressure and swap;
- memory poisoning/contradiction behavior;
- backup/restore integrity;
- independent context-engine and memory-provider rollback;
- successful context/memory operation with outbound network denied after provisioning.

No context/memory profile receives production authority until those gates pass. If the LCM+Mnemosyne pair loses to a simpler profile, promote the simpler qualified profile.

## Target-machine / production evidence gaps

The available CI runtime is Linux/x86-64, not the target M3 Max. Production promotion still requires:

- representative redacted mission corpus and temporal router holdout;
- real provider/tool outcomes;
- target-Mac context/memory/router/resource measurements under normal browser/build/container pressure;
- external capability/sandbox enforcement tests;
- egress PII/secret canaries;
- current Pi RPC compatibility and isolation evidence;
- LSP compatibility suite;
- failure injection for outage, retry, corrupted state, malicious context/memory/tool output and rollback.

## Maturity conclusion

The repository is **coherent and sufficiently detailed to start the controlled autonomous uplift mission from Phase 00 in a clean canary/bootstrap profile**. It is not evidence that the production uplift has already succeeded.

Hermes may autonomously execute read-only and canary phases according to the execution contract, but must mark `BLOCKED`/`ROLLBACK` instead of promoting any component whose mandatory runtime/security/local-only gate is unresolved.
