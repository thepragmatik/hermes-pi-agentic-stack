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

The current repository gate executes Python compilation for router/site tooling, site generation, internal-link validation, Markdown/`llms.txt` alternate checks, accessible SVG checks, progressive-disclosure agent-surface checks, SHA-256 verification of every raw file listed by the agent manifest, JSON parsing and lifecycle assertions for task/state contracts, OpenRouter architecture assertions, agent/raw copy equality for execution-critical contracts/configs, and Pages build/deploy.

During refinement these checks/reviews found real defects rather than merely confirming the design, including: invalid YAML/frontmatter and SVG metadata in earlier revisions; policy examples that could be mistaken for enforcement; overbroad privacy/secret patterns; bootstrap/security/Pi ordering drift; duplicate memory authority; canary memory semantics incompatible with autonomy; two competing phase models (`00-70` vs an accumulated longer sequence); a Pi example incorrectly assigned to Phase 30 before Pi authority exists; an outdated standalone architecture diagram; stale direct-provider assumptions; a validator that did not require the new fresh-install/OpenRouter/start-mission surfaces; stale install wording that called the now-public control repository private; and a Phase-20 sequence that could have layered LCM/Mnemosyne and Spec Kit before independently dogfooding the first prompt/skill slimming increment.

Those defects are corrected in canonical source.

## Latest GitHub Pages / operating-manual gate

On implementation head `065be61364a02723d090cd60d99f968acb319909`, GitHub Actions completed successfully:

- Python 3.12 compilation of `tools/router-bench/router_bench.py`, `tools/site/build_site.py` and `tools/site/validate_site.py`;
- generation of **26 human pages plus the progressive-disclosure agent surface**;
- validation of all **26 HTML pages**, internal links and Markdown/`llms.txt` alternates;
- accessible architecture SVG title/description checks plus explicit OpenRouter/model-role/policy representation;
- required human routes for Architecture, Fresh Install, Start Uplift, phase playbook, Context + Skills, OpenRouter + Routing, Pi + LSP, Security, Adversarial Review, Readiness, Validation, Upgrades and Sources;
- required agent routes for `agent/START.md`, `agent/UPLIFT_MISSION.md`, manifest, architecture graph, schemas/examples, configs and sliced skill;
- SHA-256 and byte-size verification of every canonical raw source in the agent manifest;
- confirmation that the agent manifest declares OpenRouter as default gateway, LCM + Mnemosyne as the context/memory baseline and the `00,10,...,70` lifecycle;
- confirmation that the architecture graph contains deterministic policy, local router, model-role binding, OpenRouter, physical-provider, Pi-boundary and durable-state nodes;
- confirmation that Pi task schema **v2.1** binds exact lifecycle phase IDs plus `model_role`, LOCAL_ONLY fail-closed conditions and required approval evidence when policy requires approval;
- confirmation that the Pi worked example is Phase 50 (`50-pi-and-lsp`) using `coding.default`, not a pre-Pi router task;
- confirmation that uplift-state schema/example **v1.1** use exactly the eight `00-70` phases, persist restart/adoption/report decisions and declare OpenRouter runtime gateway;
- exact byte equality between raw and agent copies of mission, task/state contracts/examples and baseline model/context-memory configs;
- successful Pages artifact upload and deployment.

The stricter validator previously caught an identifier mismatch between its expected `model_role` graph node and the canonical graph's `role_binding` / `model_role_binding`; the validator was corrected to the canonical identifier rather than weakening the architecture.

The final readiness pass also verified current upstream Hermes documentation for the bootstrap-critical commands used by this manual: named profiles with `--no-skills`, `terminal.cwd`, interactive model/provider selection, OpenRouter provider-routing controls and `chat --query-file` remain current at the snapshot date.

## Fresh-install and execution-path evidence

The documentation has one explicit manual-to-autonomous handoff:

```text
human installs/configures clean Hermes bootstrap profile
-> one verified OpenRouter bootstrap model
-> repository available locally
-> uplift chat --query-file UPLIFT_MISSION.md
-> Hermes reads durable state + parent skill + one current phase slice
-> executes one bounded phase
-> persists evidence/state + reports boundary
-> stops before next phase
```

OpenRouter is the default external inference gateway. Deterministic privacy/security policy runs locally before every cloud request; the local mission router chooses lane/model role/model; OpenRouter selects only the downstream policy-compatible physical provider. OpenRouter Auto is not privacy authority or final mission-routing authority.

The lifecycle is singular and consistent across README, mission, playbooks, skill slices, schemas/examples, architecture and agent discovery:

```text
00 preflight
10 baseline + backup
20 context + skills + LCM/Mnemosyne
   -> Dogfood Gate A0: fresh Phase-20 continuation using prompt/skill slimming only
   -> Restart Checkpoint A: fresh optimized Hermes session before Phase 30
30 router
   -> Checkpoint B: shadow only
40 security + policy enforcement
   -> Checkpoint C: authority/human gate
50 Hermes->Pi + LSP
   -> Checkpoint D: recreate disposable workers
60 evaluation + promotion
   -> Checkpoint E: normal multi-role operation
70 upgrades + rollback
   -> Checkpoint F: recurring canary discipline
```

### Early dogfooding rule

Phase 20 now avoids batching its first useful optimization with later context/memory/spec layers. After prompt/context + skill slimming is staged, Hermes must:

1. keep Phase 20 `EXECUTING` and checkpoint the pre-dogfood configuration;
2. resume the same phase in a fresh session using the slimmer context/skill layout;
3. keep the bootstrap model/OpenRouter policy stable;
4. run a matched subset of the Phase-10 workload;
5. prove non-inferior accepted-task quality plus measurable context/token improvement;
6. persist `phase20-dogfood-A0` evidence;
7. repair/rollback before LCM/Mnemosyne if the first increment regresses.

Only then are LCM + Mnemosyne and Spec Kit layered onto the qualified slimmer baseline. After the complete Phase-20 gate, Hermes reports that the first token/context improvements are ready and starts Phase 30 in another fresh session so Phase-20 qualification context does not contaminate router measurements.

## Router regression evidence

The last executed deterministic router smoke corpus produced **1.000 accuracy, 1.000 macro-F1 and 1.000 repeat determinism**, with zero observed high-severity lane errors over the small regression fixture. Warm routing latency was sub-millisecond in the available Linux/x86-64 validation runtime.

These numbers are regression evidence only. They are **not** claims about ModernBERT/embedding-router accuracy, OpenRouter provider quality, M3 Max latency or production workload performance.

## LCM + Mnemosyne evidence status

Architecture status: **selected baseline**.

Evidence status: **researched + repository/config/site validated; not yet canary runtime qualified on the target Mac.**

The repository contains one coherent baseline path:

- `docs/agentic-uplift/local-context-memory-setup.md` — install, pin, effective config, admission, health, compaction, offline, backup, rollback and upgrade procedure;
- `docs/agentic-uplift/research/local-context-memory-stack.md` — ownership/rationale/risks and evidence requirements;
- `configs/hermes-local-context-memory.example.yaml` — complete Hermes composition;
- `configs/lcm-baseline.env.example` — LCM scalar baseline;
- `configs/mnemosyne-local.example.yaml` — Mnemosyne local-only subconfiguration;
- Phase 20 execution gates in `implementation-playbook.md` and the matching sliced skill reference;
- adversarial tests for duplicate authority, poisoning, relevance, unexpected network fallback, SQLite recovery, tool-schema overhead and release/default drift.

Initial stable research pins are LCM `v0.20.0`, Mnemosyne core `3.15.1` and Hermes wrapper `0.5.0`. **Phase 00/20 must re-verify current stable releases, effective config and security notes before installation.** Unreleased `main`, release candidates and betas are not automatic upgrades.

### Baseline effective-config intent

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

Built-in-only, LCM-only and Mnemosyne-only profiles may be used to isolate a regression, but they do not compete for production selection. If the required pair fails a mandatory gate, Phase 20 is `BLOCKED`/`ROLLBACK`; Hermes does not autonomously choose another memory architecture.

The stable Mnemosyne 3.15.x research pin predates later relevance/prefetch work, so **irrelevant-memory injection is explicitly blocking**. Do not pin unreleased `main` merely to bypass that test; qualify the next stable release normally.

## Remaining target-machine / production P0 evidence

The available repository CI runtime is Linux/x86-64, not the target M3 Max. Unattended production authority still requires:

- actual fresh-install/manual bootstrap rehearsal on the target Mac and captured effective Hermes/OpenRouter configuration;
- Dogfood Gate A0 evidence on the target Mac before later Phase-20 layering;
- target-Mac LCM + Mnemosyne runtime/offline/recovery/resource evidence above;
- representative redacted mission corpus and temporal router holdout;
- ModernBERT/embedding challenger measurements and router shadow evidence before routing authority;
- real OpenRouter model/provider outcomes including physical-provider/cache continuity, TTFT/throughput, tool correctness, retries, rate limits and accepted-task cost;
- implemented external capability/sandbox enforcement, not just policy YAML;
- deterministic egress PII/secret canaries proving LOCAL_ONLY cannot reach OpenRouter/cloud;
- current Pi RPC compatibility, `agent_settled` completion semantics and containment evidence;
- LSP compatibility suite;
- failure injection for provider outage/fallback, retry, corrupted state, malicious context/memory/repository/tool output, stale worker/session reuse and rollback;
- human approval at security-critical Checkpoint C and any other phase whose policy requires it.

## Maturity conclusion

The repository and Pages site are **coherent, internally cross-checked and sufficiently detailed to start the controlled staged uplift from Phase 00 in a clean bootstrap profile**. The documentation functions as one operating manual for humans and progressively disclosed agents rather than competing accumulated research paths.

The sequence intentionally targets early dogfooding: Phase 00 and 10 only establish safety/baseline; Phase 20A/B is the first reversible optimization; Dogfood Gate A0 exercises that increment immediately in a fresh same-phase session before LCM/Mnemosyne and Spec Kit are layered; the full Phase-20 adoption is then isolated again before router work begins.

This is still not evidence that production enforcement or target-Mac runtime qualification has succeeded. Hermes may execute the bounded phase workflow according to the execution contract, but it must stop at every phase boundary, persist/report state, and mark `BLOCKED`/`ROLLBACK` rather than bypassing an unresolved security, local-only, runtime, restart or human-approval gate.
