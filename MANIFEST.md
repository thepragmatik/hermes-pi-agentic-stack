# Repository Manifest

This repository is the standalone, upgrade-safe control repository for the Hermes + Pi agentic development stack. It intentionally remains separate from upstream Hermes, Pi, LCM and Mnemosyne source repositories.

## Canonical source layout

```text
README.md
HERMES_AGENTIC_UPLIFT_PLAYBOOK.md
MANIFEST.md
configs/
  policy.example.yaml
  models.example.yaml
  hermes-local-context-memory.example.yaml
  mnemosyne-local.example.yaml
  lcm-baseline.env.example
protocols/
  pi-task-envelope.schema.json
  uplift-state.schema.json
  examples/
    pi-task-envelope.example.json
    uplift-state.example.json
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
docs/agentic-uplift/
  README.md
  SOURCES.md
  architecture.html
  architecture.md
  architecture.graph.json
  agent-execution-contract.md
  bootstrap-authority.md
  local-context-memory-setup.md
  validation-report.md
  site-publishing.md
  implementation-playbook.md
  artifact-usability-review.md
  adversarial-review.md
  savings-model.md
  spec-kit-profiles.md
  research/
    local-routing-models.md
    router-training-control.md
    context-token-optimization.md
    mission-context-architecture.md
    local-context-memory-stack.md
    legacy-state-curation.md
    hermes-pi-lsp.md
    security-zero-trust-pii.md
    skill-slimming-slicing.md
tools/router-bench/
  README.md
  router_bench.py
  sample_missions.jsonl
  requirements-optional.txt
tools/site/
  build_site.py
  validate_site.py
  requirements.txt
```

## State ownership map

The repository intentionally prevents “memory” from becoming a catch-all:

```text
LCM          -> current-session exact context / compaction recovery
Mnemosyne    -> curated cross-session durable memory
state.db     -> raw Hermes session history / forensic search
uplift-state -> deterministic mission authority
T2 artifacts -> raw evidence/logs/diffs/results
Git/ADR/spec -> project truth
Kanban       -> optional operational projection
```

**LCM + Mnemosyne is the selected baseline architecture.** Built-in-only, LCM-only and Mnemosyne-only profiles are diagnostic controls and rollback aids, not automatic production alternatives. Runtime promotion remains blocked until the required pair passes target-Mac exact-recovery, memory-relevance, local-only, resource, backup and rollback gates.

Canonical baseline setup/configuration:

- `docs/agentic-uplift/local-context-memory-setup.md`
- `configs/hermes-local-context-memory.example.yaml`
- `configs/lcm-baseline.env.example`
- `configs/mnemosyne-local.example.yaml`

## Generated GitHub Pages surface

`tools/site/build_site.py` generates the site while keeping canonical research source under `docs/agentic-uplift/`.

Key generated endpoints include:

```text
index.html
architecture.html
playbook.html
execution-contract.html
bootstrap.html
context-memory-setup.html
skills.html
artifact-review.html
adversarial-review.html
research/local-context-memory.html
research/*.html
llms.txt
agents.txt
agent/START.md
agent/manifest.json
agent/architecture.graph.json
agent/protocols/pi-task-envelope.schema.json
agent/protocols/uplift-state.schema.json
agent/configs/hermes-local-context-memory.example.yaml
agent/configs/lcm-baseline.env.example
agent/configs/mnemosyne-local.example.yaml
agent/skills/hermes-stack-uplift/**
```

The site deliberately does **not** publish a monolithic `llms-full.txt`. Agents should start at `llms.txt`, fetch `agent/START.md`, and load only the relevant canonical slice.

## Suggested implementation workflow

```bash
git switch main
git pull --ff-only
git switch -c uplift/<mission-name>

python3 -m py_compile tools/router-bench/router_bench.py tools/site/build_site.py tools/site/validate_site.py
python3 tools/site/build_site.py --output _site
python3 tools/site/validate_site.py --site _site

python3 tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --output /tmp/router-smoke.json

# Implement one gated uplift phase at a time.
# Phase 30 follows docs/agentic-uplift/local-context-memory-setup.md.
git add -A
git commit
git push -u origin HEAD
```

Use pull requests for implementation changes and preserve `main` as the last validated stack state.

## Important maturity rule

A documented policy, config example, JSON Schema, diagram or playbook is **not equivalent to implemented enforcement or qualified runtime behavior**. Read `docs/agentic-uplift/artifact-usability-review.md` and satisfy its P0 gates before enabling unattended production self-uplift.

Generated Python bytecode, local benchmark outputs, logs, databases, credentials, secrets and environment files are excluded by `.gitignore`.

## Upstream relationship

Hermes, Pi, LCM and Mnemosyne should normally be installed/pinned independently and updated from their upstream projects. This repository integrates with them through documented configuration, skills/extensions, RPC/headless interfaces, profile launchers, side venvs, policies and narrow adapters. Any unavoidable upstream patch should be feature-flagged, covered by an integration test, and tracked for upstreaming or removal.
