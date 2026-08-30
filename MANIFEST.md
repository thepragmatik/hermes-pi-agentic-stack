# Repository Manifest

This is the standalone, upgrade-safe control repository for the Hermes + Pi stack. It remains separate from upstream Hermes, Pi, LCM and Mnemosyne source repositories.

## Canonical operating spine

```text
README.md                              # human start + manual bootstrap summary
UPLIFT_MISSION.md                      # exact first-turn staged mission
HERMES_AGENTIC_UPLIFT_PLAYBOOK.md      # compact architecture/control summary
docs/agentic-uplift/
  fresh-install-bootstrap.md           # human-only foundation
  agent-execution-contract.md          # durable authority/recovery/report contract
  implementation-playbook.md           # single 00-70 lifecycle
  architecture.md
  architecture.graph.json
  bootstrap-authority.md
  local-context-memory-setup.md
  artifact-usability-review.md
  adversarial-review.md
  validation-report.md
  site-publishing.md
  SOURCES.md
  research/
    openrouter-routing.md
    local-routing-models.md
    router-training-control.md
    context-token-optimization.md
    mission-context-architecture.md
    local-context-memory-stack.md
    legacy-state-curation.md
    hermes-pi-lsp.md
    security-zero-trust-pii.md
    skill-slimming-slicing.md
skills/hermes-stack-uplift/
  SKILL.md
  references/
    00-preflight.md
    10-baseline-and-backup.md
    20-context-and-skills.md
    30-router.md
    40-security-and-policy.md
    50-pi-and-lsp.md
    60-evaluation-and-promotion.md
    70-upgrades-and-rollback.md
protocols/
  uplift-state.schema.json              # v1.1 phase/report/restart/adoption state
  pi-task-envelope.schema.json
  examples/
configs/
  models.example.yaml                   # OpenRouter gateway + role bindings
  policy.example.yaml
  hermes-local-context-memory.example.yaml
  lcm-baseline.env.example
  mnemosyne-local.example.yaml
tools/router-bench/
tools/site/
.github/workflows/pages.yml
```

## One authoritative lifecycle

The repository uses exactly:

```text
00 preflight
10 baseline + backup
20 context + skills
30 router
40 security + policy
50 Hermes->Pi + LSP
60 evaluation + promotion
70 upgrades + rollback
```

Research documents do not define extra phases. Every phase persists a v1.1 boundary report and stops before the next phase.

## Gateway / routing ownership

```text
local deterministic privacy/security policy
 -> local mission router
 -> model-role/model binding
 -> OpenRouter model ID
 -> OpenRouter physical-provider routing
```

OpenRouter is the default external gateway. OpenRouter Auto is bounded bootstrap/shadow/fallback research only and cannot make privacy/security or final mission-lane decisions. Direct provider credentials are benchmark-driven exceptions.

## State ownership

```text
LCM          -> current-session exact context / compaction recovery
Mnemosyne    -> curated cross-session durable memory
state.db     -> raw Hermes session history / forensic search
uplift-state -> deterministic mission/report/restart/adoption authority
T2 artifacts -> raw evidence/logs/diffs/results
Git/ADR/spec -> project truth
Kanban       -> optional operational projection
```

**LCM + Mnemosyne is the selected baseline architecture.** One-component profiles exist only for diagnosis/rollback. Failure of a mandatory pair gate produces `BLOCKED`/`ROLLBACK`, not an autonomous architecture substitution.

## Human Pages surface

`tools/site/build_site.py` generates the primary public manual from canonical source. Key routes include:

```text
index.html
architecture.html
fresh-install.html
start-uplift.html
playbook.html
execution-contract.html
bootstrap.html
context-memory-setup.html
skills.html
routing-openrouter.html
pi-lsp.html
security.html
adversarial-review.html
artifact-review.html
validation.html
upgrade-rollback.html
sources.html
research/*.html
```

## Agent surface

```text
llms.txt
agents.txt
agent/START.md
agent/UPLIFT_MISSION.md
agent/manifest.json
agent/architecture.graph.json
agent/protocols/pi-task-envelope.schema.json
agent/protocols/uplift-state.schema.json
agent/protocols/examples/*.json
agent/configs/models.example.yaml
agent/configs/hermes-local-context-memory.example.yaml
agent/configs/lcm-baseline.env.example
agent/configs/mnemosyne-local.example.yaml
agent/skills/hermes-stack-uplift/**
```

Agents start at `llms.txt` / `agent/START.md`, then load mission + durable state + parent skill + **one current phase slice**. The site deliberately does not publish `llms-full.txt`.

## Fresh implementation start

The operator follows `docs/agentic-uplift/fresh-install-bootstrap.md`, then from the repo root launches:

```bash
uplift chat --query-file UPLIFT_MISSION.md
```

Phase 20 is Checkpoint A: once context/skill + LCM/Mnemosyne gates pass, the pre-optimization session is closed and Phase 30 starts fresh on the uplifted profile.

## Validation workflow

```bash
python3 -m py_compile tools/router-bench/router_bench.py tools/site/build_site.py tools/site/validate_site.py
python3 tools/site/build_site.py --output _site
python3 tools/site/validate_site.py --site _site

python3 tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --output /tmp/router-smoke.json
```

Use the exact maturity labels in the playbook. A config/schema/diagram is not implemented enforcement; a CI pass is not target-Mac validation. Satisfy the artifact-readiness P0 gates before unattended production authority.

Do not commit API keys, environment secrets, raw PII corpora, Hermes/LCM/Mnemosyne databases or unredacted transcripts.
