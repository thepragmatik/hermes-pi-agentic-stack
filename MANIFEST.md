# Repository Manifest

This is the standalone, upgrade-safe control repository for the Hermes + Pi stack. It remains separate from upstream Hermes, Pi, LCM and Mnemosyne source repositories.

## Canonical operating spine

```text
README.md                              # human start + manual bootstrap summary
UPLIFT_MISSION.md                      # exact first-turn staged mission
HERMES_AGENTIC_UPLIFT_PLAYBOOK.md      # compact architecture/control summary
docs/agentic-uplift/
  fresh-install-bootstrap.md
  agent-execution-contract.md
  implementation-playbook.md           # single 00-70 lifecycle
  architecture.md
  architecture.graph.json
  architecture.html                    # checked-in presentation view only
  bootstrap-authority.md
  local-context-memory-setup.md
  artifact-usability-review.md
  adversarial-review.md
  validation-report.md
  savings-model.md
  site-publishing.md
  SOURCES.md
  research/
    local-routing-models.md             # broad routing/framework assessment
    router-training-control.md          # outcome learning / ModernBERT gates
    openrouter-routing.md               # gateway/provider ownership
    context-token-optimization.md
    mission-context-architecture.md
    local-context-memory-stack.md
    legacy-state-curation.md
    hermes-pi-lsp.md
    security-zero-trust-pii.md
    skill-slimming-slicing.md
skills/hermes-stack-uplift/
  SKILL.md
  references/00-preflight.md ... 70-upgrades-and-rollback.md
protocols/
  routing-mission.schema.json           # v1.0 framework-neutral mission/profile contract
  routing-decision.schema.json          # v1.0 workflow/model/provider decision contract
  uplift-state.schema.json              # v1.1 phase/report/restart/adoption state
  pi-task-envelope.schema.json          # v2.2 typed worker + routing provenance
  examples/
    routing-mission.example.json
    routing-decision.example.json
    pi-task-envelope.example.json
    uplift-state.example.json
configs/
  models.example.yaml                   # model roles + gateway/provider requirements
  policy.example.yaml
  hermes-local-context-memory.example.yaml
  lcm-baseline.env.example
  mnemosyne-local.example.yaml
tools/router-bench/
  router_bench.py                       # common multi-label/workflow/outcome harness
  sample_missions.jsonl                 # 32-mission smoke fixture
  README.md
tools/site/
.github/workflows/pages.yml
```

## One authoritative lifecycle

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

## Routing ownership

```text
mission + durable state
 -> Tier 0 deterministic eligibility/security
 -> Tier 1 multi-label mission profile
 -> Tier 2 bounded workflow/agent selection
 -> Tier 3 model-role/model optimization
 -> Tier 4 OpenRouter-first gateway/provider execution
```

Research/coding are important task families, not the complete ontology. Multi-stage missions remain ordered stages rather than a single `hybrid` class.

Hard eligibility facts (`LOCAL_ONLY`, cloud eligibility, tools/capabilities, modality, context, network/sandbox, ZDR) cannot be overridden by learned/framework output. `routing-mission` and `routing-decision` keep Hermes/Pi independent of the selected router framework.

OpenRouter is the default external gateway; direct providers/local adapters are replaceable challengers. OpenRouter Auto is bounded bootstrap/shadow/teacher/fallback research only after Tier-0 eligibility.

## Router maturity / candidates

```text
initial Phase-30 baseline = deterministic rules + explicit state + abstention
semantic challenger       = minimal embedding / Aurelio Semantic Router
medium-term candidate     = vLLM Semantic Router behind our contract
research plane            = LLMRouter + RouteLLM experiments/training
future learned candidate  = multi-label/multi-head ModernBERT if evidence earns it
```

Advanced candidates are not bootstrap dependencies and receive no authority in Phase 30. Phase 60 promotes only measured winners.

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

## Human Pages surface

`tools/site/build_site.py` generates 26 human pages from canonical source. Key routing surfaces include `architecture.html`, `routing-openrouter.html`, `research/routing.html` and `research/router-training.html`, plus readiness/adversarial/validation pages.

## Agent surface

```text
llms.txt
agents.txt
agent/START.md
agent/UPLIFT_MISSION.md
agent/manifest.json
agent/architecture.graph.json
agent/protocols/routing-mission.schema.json
agent/protocols/routing-decision.schema.json
agent/protocols/pi-task-envelope.schema.json
agent/protocols/uplift-state.schema.json
agent/protocols/examples/*.json
agent/configs/*.yaml|*.example
agent/skills/hermes-stack-uplift/**
raw/**                                   # canonical hashed copies
```

Agents start at `llms.txt` / `agent/START.md`, then load mission + durable state + parent skill + one current phase slice. Routing contracts are loaded when routing/worker execution requires them; the site deliberately does not publish `llms-full.txt`.

## Fresh implementation start

```bash
uplift chat --query-file UPLIFT_MISSION.md
```

Phase 20 contains Dogfood Gate A0 and Checkpoint A. Phase 30 starts fresh with the simple routing baseline in shadow; it does not wait for vLLM Semantic Router or ModernBERT.

## Validation workflow

```bash
python3 -m py_compile tools/router-bench/router_bench.py tools/site/build_site.py tools/site/validate_site.py
python3 tools/site/build_site.py --output _site
python3 tools/site/validate_site.py --site _site
```

`validate_site.py` also executes the zero-dependency rules router against the checked-in 32-mission fixture with `--fail-on-hard-violations`, validates routing/Pi/state schemas/examples, agent/raw hashes, five-tier architecture and progressive-disclosure entry surfaces.

For explicit router output:

```bash
python3 tools/router-bench/router_bench.py \
  --dataset tools/router-bench/sample_missions.jsonl \
  --routers rules \
  --repeat 3 \
  --fail-on-hard-violations \
  --pretty
```

A CI pass is smoke/config evidence, not target-Mac or production routing evidence. Do not commit API keys, raw PII corpora, model conversations, Hermes/LCM/Mnemosyne databases or unredacted telemetry.