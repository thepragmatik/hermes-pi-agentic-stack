# Artifact Usability & Fit-for-Purpose Review

## Verdict

**Fresh-install operating manual / controlled autonomous uplift: fit to begin Phase 00. Unattended production authority: not yet fit.**

The distinction matters: a coherent executable playbook can safely guide Hermes to build and test missing P0 controls without pretending those controls already exist.

## Readiness taxonomy

| Artifact | What it is | What it is not | Status |
|---|---|---|---|
| `README.md` + `fresh-install-bootstrap.md` | verified human bootstrap/runbook | OS sandbox implementation | designed/execution-ready |
| `UPLIFT_MISSION.md` | one-command staged mission seed | durable state/security policy | designed |
| `policy.example.yaml` | declarative policy intent | sandbox/egress enforcement | designed; enforcement P0 |
| Pi task schema | typed delegation contract | transport/auth/containment | schema-ready; integration P0 |
| uplift-state v1.1 | phase/report/restart/adoption contract | persistence daemon | schema-ready; persistence P0 |
| router benchmark | comparative fixture/harness | production router | smoke-tested; representative corpus P0 |
| sliced uplift skill | progressive-disclosure 00–70 procedure | security boundary | prototype-ready |
| OpenRouter routing design/config | gateway/model/provider ownership | proven provider/privacy behaviour | designed; canary P0 |
| LCM + Mnemosyne baseline configs/runbook | selected local context/memory path | installed target-Mac subsystem | config-ready; runtime P0 |
| canonical 00–70 playbook | ordered iterative implementation contract | evidence implementation succeeded | review/execution-ready |
| Pages site | public human/agent operating manual | secret-bearing runtime store | deployed/validated surface |

## P0 gates before unattended production authority

1. **Bootstrap containment:** verify the actual bootstrap isolation mode. A named Hermes profile is not a sandbox. Preferred dedicated non-admin macOS account or independently qualified containment must prevent silent production mutation.
2. **External capability enforcement:** make production Hermes direct source-write/arbitrary-shell bypass structurally impossible after cutover.
3. **Cloud egress/privacy:** implement and seed-test secret + typed PII + network policy; prove `LOCAL_ONLY` cannot reach OpenRouter, Auto, fallback or a direct provider.
4. **OpenRouter effective-policy evidence:** verify request-level Hermes provider routing + account/workspace guardrails + actual physical-provider behaviour; do not rely on untested preset precedence.
5. **Typed Pi integration:** implement bridge, current RPC completion semantics, idempotency, worktree/containment, bounded retries and evidence collection.
6. **Durable state persistence:** atomically write/validate uplift-state v1.1 outside chat and recover after planned Checkpoint-A fresh session plus crash/restart.
7. **Representative router evidence:** build redacted real mission/outcome corpus with stable ontology, deduplication and mission/repo/session/time holdout; the bundled dataset is regression smoke only.
8. **LCM + Mnemosyne target-Mac qualification:** exact recovery, recall relevance/staleness, local-only operation, backup/restore, storage/RSS, tool/context overhead and poisoning/admission tests.
9. **Pi/LSP supply-chain/compatibility:** pin/audit extensions and language servers; current protocol/language fixtures and external containment must pass.
10. **Target-Mac whole-system evidence:** realistic browser/build/container pressure, cache/TTFT/accepted-task economics, failure injection and end-to-end rollback.

## Major inconsistencies/gaps found and corrected

- **Two lifecycle systems:** canonical playbook had evolved to phases through 140 while the executable sliced skill/state remained 00–70. There is now one authoritative `00 -> 70` lifecycle everywhere.
- **No first-class human bootstrap:** repo previously assumed a sufficiently configured Hermes existed. README + `fresh-install-bootstrap.md` now document a clean `--no-skills` profile, Blank Slate, OpenRouter model wizard, repo/skill exposure, evidence directories, health checks and one start command.
- **Profile mistaken for isolation:** current Hermes profiles isolate state but not filesystem authority. The manual now requires an explicit bootstrap isolation decision and labels same-user local execution trusted root-of-trust rather than zero-trust.
- **Provider architecture ambiguous:** prior prose discussed cloud roles/providers without making the gateway boundary explicit. OpenRouter is now default gateway; local policy owns cloud eligibility, local router owns lane/model, OpenRouter owns downstream physical-provider routing.
- **Direct-provider bias:** direct Z.ai/DeepSeek credentials are no longer assumed. They remain measured exceptions only.
- **Bootstrap paradox:** optimized router is no longer required before it exists. Early phases use one verified GLM-Flash-class OpenRouter bootstrap model; multi-role routing starts only after Phase 30 shadow evidence.
- **Restart/context-decay gap:** Phase 20 improvements could previously remain trapped inside the old giant bootstrap conversation. Checkpoint A now requires a fresh optimized session; subsequent router/security/worker/promotion checkpoints record reload/restart/recreate decisions.
- **Progress existed only as prose:** uplift-state v1.1 now persists phase boundary report, adoption state, runtime gateway/router mode and Hermes/Pi restart actions.
- **OpenRouter Auto ambiguity:** Auto is now explicitly barred from privacy/security/final mission authority.
- **Provider-policy precedence risk:** current Hermes request-level `provider_routing` can interact with OpenRouter preset policy; the design requires effective-policy tests rather than assuming the stricter-looking layer wins.
- **ModernBERT timing:** full fine-tuning is explicitly delayed until representative redacted outcome data, stable ontology, deduplicated temporal holdout and frozen/prototype plateau exist.
- **Memory architecture drift:** LCM + Mnemosyne is fixed as baseline; built-in/one-component profiles are diagnostic only; failure blocks/rolls back instead of silently changing architecture.
- **Legacy state risk:** old `state.db` remains read-only evidence with local curation/provenance, never a DB transplant.

## Real-world operator UX

A new operator should now be able to answer, in order:

1. what the stack is and its maturity;
2. how to create the clean bootstrap;
3. which credential/model is required initially;
4. the exact takeover action;
5. what each phase does;
6. when improvements become usable;
7. when a fresh session/reload/recreated Pi worker is required;
8. what still requires human approval;
9. which evidence proves promotion.

The first value boundary is Phase 20. After its gate Hermes must say **“The first token/context improvements are ready to use.”** and start Phase 30 in a fresh session.

## Agent UX

An autonomous agent needs a small stable entry surface rather than the full corpus. `UPLIFT_MISSION.md`, `agent-execution-contract.md`, uplift-state schema and `hermes-stack-uplift` parent skill provide the execution spine; one current phase reference and only required research/evidence are loaded next. `llms.txt`/`agent/START.md` must mirror this ordering on Pages.

## Kill criteria

Stop/rollback on any structural privacy/capability bypass; `LOCAL_ONLY -> cloud`; unverified OpenRouter effective provider policy; destructive retry ambiguity; failure to recover uplift-state after planned fresh-session checkpoint; stale session/worker testing the wrong config; material accepted-task quality regression; unexpected LCM/Mnemosyne network dependency; stale/poisoned memory influencing security/acceptance; unproven SQLite restore; uncontained Pi; or a promotion that requires weakening a mandatory gate.
