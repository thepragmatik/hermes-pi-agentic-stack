# Repository Manifest

This repository is the standalone, upgrade-safe control repository for the Hermes + Pi agentic development stack. It intentionally remains separate from upstream Hermes and Pi source repositories.

## Repository layout

```text
README.md
HERMES_AGENTIC_UPLIFT_PLAYBOOK.md
MANIFEST.md
configs/
  policy.example.yaml
protocols/
  pi-task-envelope.schema.json
docs/agentic-uplift/
  README.md
  SOURCES.md
  architecture.html
  implementation-playbook.md
  adversarial-review.md
  savings-model.md
  spec-kit-profiles.md
  research/
    local-routing-models.md
    context-token-optimization.md
    hermes-pi-lsp.md
    security-zero-trust-pii.md
tools/router-bench/
  README.md
  router_bench.py
  sample_missions.jsonl
  requirements-optional.txt
```

Generated Python bytecode, local benchmark outputs, logs, databases, credentials, secrets and environment files are excluded by `.gitignore`.

## Suggested implementation workflow

```bash
git switch main
git pull --ff-only
git switch -c uplift/<mission-name>

python3 -m py_compile tools/router-bench/router_bench.py
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

## Upstream relationship

Hermes and Pi should normally be installed/pinned independently and updated from their upstream projects. This repository should integrate with them through documented configuration, skills/extensions, RPC/headless interfaces, launchers, policies, and narrow adapters. Any unavoidable upstream patch should be feature-flagged, covered by an integration test, and tracked for upstreaming or removal.
