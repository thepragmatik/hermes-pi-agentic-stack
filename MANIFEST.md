# Repository Manifest

This repository is the standalone, upgrade-safe control repository for the Hermes + Pi agentic development stack. It intentionally remains separate from upstream Hermes and Pi source repositories.

## Canonical source layout

```text
README.md
HERMES_AGENTIC_UPLIFT_PLAYBOOK.md
MANIFEST.md
configs/
  policy.example.yaml
  models.example.yaml
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
  validation-report.md
  site-publishing.md
  implementation-playbook.md
  artifact-usability-review.md
  adversarial-review.md
  savings-model.md
  spec-kit-profiles.md
  research/
    local-routing-models.md
    context-token-optimization.md
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

## Generated GitHub Pages surface

`tools/site/build_site.py` generates the site in `docs/` while keeping research source under `docs/agentic-uplift/`.

Key generated endpoints:

```text
docs/index.html
docs/architecture.html
docs/playbook.html
docs/execution-contract.html
docs/skills.html
docs/artifact-review.html
docs/adversarial-review.html
docs/research/*.html
docs/llms.txt
docs/agents.txt
docs/agent/START.md
docs/agent/manifest.json
docs/agent/architecture.graph.json
docs/agent/protocols/pi-task-envelope.schema.json
docs/agent/configs/policy.example.yaml
docs/agent/skills/hermes-stack-uplift/**
```

The site deliberately does **not** publish a monolithic `llms-full.txt`. Agents should start at `llms.txt`, fetch `agent/START.md`, and load only the relevant canonical slice.

## Suggested implementation workflow

```bash
git switch main
git pull --ff-only
git switch -c uplift/<mission-name>

python3 -m py_compile tools/router-bench/router_bench.py tools/site/build_site.py tools/site/validate_site.py
python3 tools/site/build_site.py
python3 tools/site/validate_site.py

python3 tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --output /tmp/router-smoke.json

# Implement one gated uplift phase at a time.
# Run the relevant validation and adversarial checks.
git add -A
git commit
git push -u origin HEAD
```

Use pull requests for implementation changes and preserve `main` as the last validated stack state.

## Important maturity rule

A documented policy, JSON Schema, diagram or playbook is **not equivalent to implemented enforcement**. Read `docs/agentic-uplift/artifact-usability-review.md` and satisfy its P0 gates before enabling unattended self-uplift.

Generated Python bytecode, local benchmark outputs, logs, databases, credentials, secrets and environment files are excluded by `.gitignore`.

## Upstream relationship

Hermes and Pi should normally be installed/pinned independently and updated from their upstream projects. This repository should integrate with them through documented configuration, skills/extensions, RPC/headless interfaces, launchers, policies, and narrow adapters. Any unavoidable upstream patch should be feature-flagged, covered by an integration test, and tracked for upstreaming or removal.
