# Artifact Usability & Fit-for-Purpose Review

## Verdict

**Fresh-install operating manual / controlled autonomous uplift: fit to begin Phase 00. Unattended production authority: not yet fit.**

The routing redesign improves the operating manual without changing that maturity conclusion: the stack now has a thin replaceable routing contract and a broader capability/workflow ontology, but advanced routers remain research/shadow candidates until representative outcome evidence exists.

## Readiness taxonomy

| Artifact | What it is | What it is not | Status |
|---|---|---|---|
| `README.md` + `fresh-install-bootstrap.md` | human bootstrap/runbook | OS sandbox implementation | designed/execution-ready |
| `UPLIFT_MISSION.md` | one-command staged mission seed | durable state/security policy | designed |
| `policy.example.yaml` | declarative policy intent | sandbox/egress enforcement | designed; enforcement P0 |
| routing mission/decision schemas v1.0 | stable framework-neutral mission/profile + decision interface | production inference engine | designed/schema-ready |
| Pi task schema v2.2 | typed delegation + routing-stage provenance | transport/auth/containment | schema-ready; integration P0 |
| uplift-state v1.1 | phase/report/restart/adoption contract | persistence daemon | schema-ready; persistence P0 |
| router benchmark | common multi-label/workflow/economic harness | representative production corpus | prototype + rules smoke-tested; representative evidence P0 |
| deterministic rules/state router | bootstrap/Phase-30 baseline and safety smoke | final learned router | smoke-tested fixture only |
| Aurelio adapter path | lightweight semantic challenger | complete policy/workflow/economic router | researched/designed |
| vLLM Semantic Router adoption path | leading medium-term richer routing candidate behind our contract | mandatory runtime or security boundary | researched/designed; bake-off P0 |
| LLMRouter / RouteLLM paths | research-plane algorithms / Tier-3 scorer | required hot-path runtime | researched/designed |
| custom ModernBERT | later multi-label/multi-head candidate | justified training project today | researched/deferred |
| OpenRouter Auto | bounded shadow/teacher/bootstrap/fallback comparator | privacy/security authority | researched/designed shadow use |
| sliced uplift skill | progressive-disclosure 00–70 procedure | security boundary | prototype-ready |
| OpenRouter routing design/config | gateway/model/provider ownership | proven provider/privacy behaviour | designed; canary P0 |
| LCM + Mnemosyne baseline | selected local context/memory path | installed target-Mac subsystem | config-ready; runtime P0 |
| Pages site | public human/agent operating manual | secret-bearing runtime store | deployed/validated surface |

## P0 gates before unattended production authority

1. **Bootstrap containment:** verify the actual bootstrap isolation mode; a Hermes profile is not a sandbox.
2. **External capability enforcement:** production Hermes direct source-write/arbitrary-shell bypass must fail structurally after cutover.
3. **Cloud egress/privacy:** prove `LOCAL_ONLY`, secrets/PII, network and ZDR/provider requirements cannot be weakened by any learned router, OpenRouter Auto, fallback or direct adapter.
4. **Routing contract implementation:** derive authoritative eligibility/capability facts from runtime state and validate `routing-mission` / `routing-decision` before execution.
5. **Representative router evidence:** redacted/deduplicated real mission corpus with task-family/workflow labels, temporal holdout and actual accepted outcomes; compare rules, embeddings, Aurelio, vLLM Semantic Router and relevant research-plane scorers.
6. **Outcome economics:** join route/model/provider/workflow choice to accepted/rejected, tests/review, retries, cached/fresh tokens, TTFT/wall time, cost, switches and human override without retaining sensitive raw prompts by default.
7. **OpenRouter effective-policy evidence:** test provider requirements, model/provider fallback, data/ZDR behavior and any required session affinity through the actual installed Hermes/gateway path; unsupported raw OpenRouter fields must not be assumed enforced.
8. **Typed Pi integration:** implement bridge, v2.2 routing provenance, current RPC completion semantics, idempotency, containment and evidence collection.
9. **Durable state persistence:** atomically persist/recover uplift-state v1.1 across planned fresh sessions and crashes.
10. **LCM + Mnemosyne target-Mac qualification:** exact recovery, recall quality, local-only operation, backup/restore, resource and poisoning tests.
11. **Pi/LSP supply-chain/compatibility:** pinned/audited extensions and language fixtures under external containment.
12. **Target-Mac whole-system evidence:** realistic workstation pressure, failure injection and end-to-end rollback.

## Routing correction now embodied in the repo

The previous architecture implicitly treated routing as a classifier over `research | coding | hybrid | review | auxiliary | abstain`, and the old benchmark even used model/lane names (`deepseek`, `glm`, `hybrid`) as ground truth. That was too narrow and mixed four separate decisions.

The canonical routing ownership is now:

```text
Tier 0 deterministic eligibility / policy
 -> Tier 1 multi-label mission/capability profile
 -> Tier 2 bounded workflow + agent selection
 -> Tier 3 model-role/model economic optimization
 -> Tier 4 OpenRouter-first provider execution
```

Research and coding remain important task families. Multi-stage work is represented explicitly, e.g. `research -> architecture_design -> coding_implementation -> testing -> security_review`, instead of collapsing to `hybrid`.

Hard facts such as privacy class, cloud eligibility, available tools, required modality, actual context requirement, network/sandbox permissions and ZDR requirements are derived/enforced deterministically. Learned/framework outputs cannot override them.

## Build/adopt/fork posture

- **Initial production candidate:** rules + explicit state + abstention; add a tiny semantic component only if it earns measurable benefit.
- **Aurelio Semantic Router:** good local Tier-1 semantic primitive/challenger, but insufficient as the complete architecture.
- **vLLM Semantic Router:** strongest current medium-term adoption candidate because its released/configurable signal/session/model-routing work overlaps many of our needs. Prefer upstream/config/adapters; its heavier control-plane/runtime must beat simpler alternatives on accepted-mission economics.
- **LLMRouter:** useful router laboratory for broad algorithm comparison; keep research dependencies out of the hot path.
- **RouteLLM:** optional Tier-3 strong-vs-economical scorer after workflow/eligibility, recalibrated to our model outcomes.
- **OpenRouter Auto:** shadow/teacher signal only on already eligible/sanitized missions.
- **ModernBERT:** defer training until the ontology and outcome dataset are stable and simpler/frozen baselines plateau.

A fork is justified only by a materially valuable unmet requirement that cannot reasonably be upstreamed/adapted, with a small isolated patch set, conformance/security tests, rebase capacity and measured benefit larger than maintenance cost.

## Real-world operator UX

A new operator should be able to answer: what the stack is; how to bootstrap it; what Phase 20 dogfoods first; that Phase 30 starts with a simple router in shadow; which routing facts are deterministic; which frameworks are only challengers; when a fresh session/worker is required; and what evidence is required for promotion.

## Agent UX

`UPLIFT_MISSION.md`, the execution contract, uplift-state, routing mission/decision schemas and the current phase slice form the execution spine. Agents should not ingest the framework research corpus by default. `llms.txt` / `agent/START.md` expose the routing contracts and current-phase sources through progressive disclosure.

## Kill criteria

Stop/rollback on any structural privacy/capability bypass; learned override of Tier-0 facts; `LOCAL_ONLY -> cloud`; unavailable required tool/modality/context; unbounded workflow expansion; unsupported provider requirement treated as enforced; fallback crossing ZDR/data/capability constraints; routing telemetry becoming an uncontrolled sensitive corpus; unexplained Pi task routing provenance; destructive retry ambiguity; material accepted-mission regression; unexpected LCM/Mnemosyne network dependency; uncontained Pi; or any promotion that requires weakening a mandatory gate.