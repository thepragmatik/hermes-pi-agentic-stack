# Hermes + Pi Agentic Stack

A local-first, production-oriented control repository for uplifting **NousResearch/hermes-agent** into a slim orchestrator and **earendil-works/pi** into its constrained coding-worker path.

Target workstation: Apple Silicon / MacBook Pro M3 Max 128 GB, while preserving headroom for normal browser/build/LSP/container work.

> **Maturity:** the architecture/configuration is researched/designed and several repository/site/router fixtures are smoke-tested. It is coherent enough to begin the controlled uplift from Phase 00. It is **not** evidence that the external security boundary, Pi path, router, LCM+Mnemosyne runtime or full stack are already target-Mac validated or production-approved.

## Architecture at a glance

```text
User / mission
   |
   v
Hermes control plane
   |
   +--> local LCM context recovery + Mnemosyne durable memory
   |
   v
Tier 0 deterministic local privacy/security/policy
   |-- LOCAL_ONLY --> local path / BLOCKED
   v
local mission router
rules/state -> embeddings -> ModernBERT only if earned
   |
   +--> research | coding | hybrid | review | auxiliary | abstain
   v
model-role binding
   v
OpenRouter                         <-- default external inference gateway
   v
policy-compatible physical provider
   |
   +--> research/synthesis model role
   |
   `--> coding role -> typed Hermes->Pi -> disposable worktree/sandbox/LSP
                                           |
                                           v
                                   tests/scanners/review/merge gate
```

**Responsibility split:** local deterministic policy decides whether data may leave the machine; the local mission router decides lane/model role/model; OpenRouter is downstream and may choose the physical inference provider subject to our constraints. OpenRouter Auto is a bounded bootstrap/shadow/fallback experiment, never the privacy boundary or final mission classifier.

Direct Z.ai/DeepSeek APIs are benchmarked alternatives, not the default architecture. The preferred initial inference credential footprint is only `OPENROUTER_API_KEY`.

---

# Fresh Install: Manual Bootstrap Steps

The human performs this foundation once. Then Hermes takes over **one observable phase at a time**.

For full explanations and rollback/isolation choices, read [`docs/agentic-uplift/fresh-install-bootstrap.md`](docs/agentic-uplift/fresh-install-bootstrap.md).

## 0. Bootstrap isolation

A Hermes profile is **not a sandbox**. Preferred: create a dedicated **Standard (non-admin)** macOS account in **System Settings -> Users & Groups**, do not expose production/customer repos or unrelated credentials to it, and run the bootstrap there.

Running Hermes under your normal developer account is a trusted-bootstrap fallback, not structural isolation. Record that explicitly if you choose it.

## 1. Install current Hermes

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc
hermes --version
```

## 2. Clone this repository

Use your already-configured GitHub authentication; never paste GitHub credentials into Hermes/chat/docs.

```bash
mkdir -p ~/src
cd ~/src
git clone https://github.com/thepragmatik/hermes-pi-agentic-stack.git
cd hermes-pi-agentic-stack
STACK_REPO="$(pwd -P)"
git status --short
git rev-parse HEAD
```

## 3. Create a minimal isolated Hermes profile

```bash
hermes profile create uplift --no-skills \
  --description "Controlled Hermes + Pi staged self-uplift orchestrator."
hermes profile show uplift
```

Do **not** clone an old profile/home/session DB.

## 4. Use current Hermes Blank Slate setup

```bash
uplift setup
```

Choose **Blank Slate**. Keep the bootstrap narrow; do not enable the broad skill/plugin/MCP catalogue.

## 5. Configure OpenRouter + one bootstrap model

```bash
uplift model
```

In the current Hermes model wizard:

1. choose **OpenRouter**;
2. enter the API key in the Hermes prompt (not shell history or this repo);
3. choose the current **GLM-5.3-Flash-class** bootstrap model;
4. record the exact resolved model ID.

Research snapshot 2026-08-30: `z-ai/glm-5.3-flash`. **Use the live picker at implementation time rather than treating this slug as permanent.**

Verify without exposing the key:

```bash
uplift config get model --json
uplift status
```

Do not add direct Z.ai/DeepSeek credentials yet.

## 6. Point the profile at the repo and expose only the uplift skill

```bash
cd "$STACK_REPO"
uplift config set terminal.cwd "$STACK_REPO"
PROFILE_CONFIG="$(uplift config path)"
PROFILE_HOME="$(dirname "$PROFILE_CONFIG")"
mkdir -p "$PROFILE_HOME/skills"
ln -sfn "$STACK_REPO/skills/hermes-stack-uplift" \
  "$PROFILE_HOME/skills/hermes-stack-uplift"
uplift skills list
```

The narrow profile should not inherit the full bundled skill catalogue.

## 7. Establish durable local uplift state/evidence

```bash
mkdir -p "$PROFILE_HOME/uplift/evidence" "$PROFILE_HOME/uplift/checkpoints"
printf '%s\n' "$STACK_REPO" > "$PROFILE_HOME/uplift/repository.path"
git -C "$STACK_REPO" rev-parse HEAD > "$PROFILE_HOME/uplift/repository.sha"
shasum -a 256 "$STACK_REPO/configs/policy.example.yaml" \
  > "$PROFILE_HOME/uplift/policy.sha256"
```

Runtime state belongs at `$PROFILE_HOME/uplift/uplift-state.json` and must validate against `protocols/uplift-state.schema.json`. Chat is not state.

## 8. Health check

```bash
uplift config check
uplift doctor
uplift dump
uplift config get model --json
git -C "$STACK_REPO" status --short
git -C "$STACK_REPO" rev-parse HEAD
```

Record Hermes version, Pi version if installed, repo SHA, bootstrap profile/isolation mode, OpenRouter provider + exact model ID, policy digest and rollback path. Never record the API key.

---

# START THE UPLIFT

After the manual steps above, there is one documented takeover action:

```bash
cd "$STACK_REPO"
uplift chat --query-file UPLIFT_MISSION.md
```

Current Hermes `--query-file` sends the file literally as the first normal turn and keeps an interactive terminal session open. [`UPLIFT_MISSION.md`](UPLIFT_MISSION.md) tells Hermes to:

- read the execution contract and durable state first;
- load `hermes-stack-uplift` and **only the current phase slice**;
- execute phases in order `00 -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70`;
- persist checkpoints/evidence/state;
- never treat prompt/YAML/memory as security enforcement;
- keep privacy decisions local before OpenRouter;
- stop and report after **every** phase instead of disappearing into one long session.

```text
manual user setup
  -> one query-file bootstrap action
  -> Hermes executes current phase
  -> persists evidence/state
  -> reports phase boundary
  -> fresh session/reload/recreate when checkpoint says so
  -> human continues to next phase
```

---

## The iterative uplift lifecycle

| Phase | Bounded objective | Adoption/restart boundary |
|---|---|---|
| **00 Preflight** | environment/version/repo/policy/provider/isolation truth | none |
| **10 Baseline + Backup** | before metrics, restore checkpoint, optional read-only legacy salvage | none normally |
| **20 Context + Skills** | prompt diet, progressive-disclosure skills, Spec Kit slicing, **LCM+Mnemosyne baseline** | **Checkpoint A: first improvements usable; fresh Hermes session required** |
| **30 Router** | local rules/state/embedding router; ModernBERT only later; OpenRouter role bindings | **Checkpoint B: shadow only; fresh/reloaded shadow session** |
| **40 Security + Policy** | real capability/egress/secret/PII/sandbox enforcement | **Checkpoint C: human security authority gate** |
| **50 Hermes->Pi + LSP** | typed RPC, containment, worktrees, language fixtures, coding cutover | **Checkpoint D: recreate disposable Pi workers** |
| **60 Evaluation + Promotion** | whole-stack adversarial/matched comparison + multi-role model/provider promotion | **Checkpoint E: ordinary dual/multi-role operation** |
| **70 Upgrades + Rollback** | recurring canary/update/restart/rollback discipline | **Checkpoint F: maintenance cycle** |

### When Hermes first benefits from the uplift

**After Phase 20 passes.** Hermes must explicitly report:

> **The first token/context improvements are ready to use.**

Then close the pre-optimization conversation and begin Phase 30 in a fresh session using the slimmed profile, sliced skill and qualified LCM+Mnemosyne configuration. Carrying the original giant bootstrap transcript forward would undermine the optimization we just proved.

## Required report after every phase

```text
Phase completed:
What changed:
Evidence/gates passed:
Failures/warnings:
Token/context/cost impact observed:
Security impact:
What is now usable:
Does Hermes need a fresh session/restart?:
Does Pi need to be recreated/restarted?:
Remaining phases:
Next phase:
Human approval required before continuing?: yes/no
```

The same information is persisted in uplift-state v1.1; the conversational report is a human projection, not the only record.

---

## OpenRouter and model-role design

Default external inference flow:

```text
local deterministic policy
 -> local mission router
 -> model-role binding
 -> OpenRouter model ID
 -> OpenRouter physical provider
```

Research-snapshot role candidates:

```text
bootstrap.default -> GLM-5.3-Flash-class through OpenRouter
coding.default    -> GLM-5.3-Flash-class through OpenRouter
research.default  -> DeepSeek-V4-Flash-class through OpenRouter
review.default    -> independent family, benchmark before binding
auxiliary.cheap   -> optional, benchmark before binding
```

Exact IDs are volatile config/lock data. See [`configs/models.example.yaml`](configs/models.example.yaml) and [`docs/agentic-uplift/research/openrouter-routing.md`](docs/agentic-uplift/research/openrouter-routing.md).

Provider/model should remain sticky inside a long phase/session when that improves prompt caching or behaviour. Optimize **cost + minutes + retries + human intervention per accepted task**, not nominal $/M tokens.

OpenRouter Auto never decides privacy/security. Direct-provider APIs are periodic challengers/fallback optimization options only.

## ModernBERT progression

```text
rules + explicit state
 -> embedding/prototype classifier
 -> representative redacted production outcomes
 -> fine-tuned ModernBERT only if the frozen/prototype boundary plateaus
```

Promotion requires stable ontology, deduplication, privacy redaction, real outcome labels, mission/repo/session/time holdout and hybrid/ambiguous cases. RouteLLM-style routing is optional second-stage difficulty/preference logic, not the primary research-vs-code classifier.

## Context and memory ownership

```text
LCM          = current-session exact context + compaction recovery
Mnemosyne    = curated cross-session durable memory
state.db     = raw Hermes session history / forensic search
uplift-state = deterministic mission authority
T2 artifacts = raw logs/diffs/benchmarks/test evidence
Git/ADR/spec = project truth
Kanban       = optional operational projection
```

LCM + Mnemosyne is the **fixed baseline architecture**, though it still must be installed and target-Mac qualified. See [`docs/agentic-uplift/local-context-memory-setup.md`](docs/agentic-uplift/local-context-memory-setup.md).

## Security posture

Security-critical controls live outside prompts, context/memory and model routing. A model instruction, SOUL text, YAML example, OpenRouter guardrail or PII-library unit test is not by itself an enforcement boundary.

The system remains at human gates until P0 evidence proves external capability enforcement, cloud egress/privacy controls, current Pi containment/protocol behaviour, durable state/idempotency, target-Mac qualification and rollback.

## Start reading

1. [`docs/agentic-uplift/fresh-install-bootstrap.md`](docs/agentic-uplift/fresh-install-bootstrap.md) — manual setup.
2. [`UPLIFT_MISSION.md`](UPLIFT_MISSION.md) — exact staged mission sent to Hermes.
3. [`docs/agentic-uplift/implementation-playbook.md`](docs/agentic-uplift/implementation-playbook.md) — canonical 00–70 lifecycle.
4. [`docs/agentic-uplift/agent-execution-contract.md`](docs/agentic-uplift/agent-execution-contract.md) — state/evidence/recovery authority.
5. [`skills/hermes-stack-uplift/`](skills/hermes-stack-uplift/) — progressive-disclosure phase slices.
6. [`docs/agentic-uplift/research/openrouter-routing.md`](docs/agentic-uplift/research/openrouter-routing.md) — model/provider separation.
7. [`docs/agentic-uplift/artifact-usability-review.md`](docs/agentic-uplift/artifact-usability-review.md) — real readiness/P0 gaps.
8. [`docs/agentic-uplift/adversarial-review.md`](docs/agentic-uplift/adversarial-review.md) — failure catalogue.
9. [`docs/agentic-uplift/validation-report.md`](docs/agentic-uplift/validation-report.md) — evidence actually executed.

Human site: **https://thepragmatik.github.io/hermes-pi-agentic-stack/**

Agents should start at the site's `llms.txt` / `agent/START.md` and fetch only the current slice.
