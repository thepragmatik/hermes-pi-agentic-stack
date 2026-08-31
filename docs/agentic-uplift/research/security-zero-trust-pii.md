# Zero-Trust Agentic Harness and PII/Secret Protection

## Root cause of previous swarm failures

The reported failures—security posture not propagating, the host orchestrator executing tasks itself, and inconsistent Pi use—share one architectural cause: **authority and delegation were expressed as natural-language instructions instead of enforced capabilities**.

Prompts, routing scores and model/provider responses are advisory. Security boundaries must survive prompt injection, context compaction, model changes, router replacement and "helpful optimization" behavior.

## Trust model

Assume user/repository text, context files, generated code, LSP/tool output, child-agent prose, web content, learned/framework routing output and provider responses can be wrong or malicious.

Trust only versioned policy, audited launcher/enforcement code, OS/container/VM capability boundaries, deterministic validators/scanners, protected credential brokerage and authenticated task/evidence/state records.

## Tier-0 routing eligibility is part of the security boundary

Before semantic/task/workflow/model routing, derive authoritative facts into `routing-mission`:

- privacy class and `LOCAL_ONLY`;
- cloud eligibility;
- secret/PII action;
- actual tool/capability availability;
- required modality/structured output/context window;
- network and sandbox requirements;
- ZDR/data-collection requirements;
- destructive/high-risk/human-review requirements.

A learned classifier, Aurelio/vLLM signal, RouteLLM score, OpenRouter Auto result, model fallback or memory recall **cannot downgrade or override these facts**. If a downstream component proposes an ineligible route, reject the route rather than weakening Tier 0.

Security-oriented signals from a router framework may be defense-in-depth or observability, but they are not DLP/authorization unless they are independently enforced outside the model/router process.

## Capability enforcement

### Orchestrator
- no generic production source-write tool after cutover;
- no arbitrary shell;
- no direct merge/push credential;
- read/plan/delegate/review scheduling only.

### Coding worker
- filesystem restricted to one worktree plus explicit read-only shared paths;
- command/process policy below the model;
- outbound network default-deny with task-scoped exceptions;
- no long-lived GitHub/cloud credentials in environment;
- no Hermes/memory DB access unless explicitly justified and redacted.

### Reviewer
- read-only worktree/diff;
- deterministic test/static-analysis tools;
- source write disabled by default;
- independent-review requirement is enforced when risk policy demands it.

## Policy propagation

Never copy SOUL/skill text into child agents as the security mechanism. A trusted launcher builds each worker from:

```text
validated routing decision
+ fixed role policy
+ validated Pi task envelope / policy digest
+ task-scoped project context
```

Pi envelope v2.2 includes routing provenance so the worker cannot silently become detached from the mission/stage decision that authorized it.

## PII / secret egress gateway

Every cloud-bound request must pass one local fail-closed boundary:

1. dedicated secret detector;
2. deterministic/domain PII recognizers;
3. local NER/Presidio-style PII detector;
4. optional locally evaluated shadow detector;
5. policy action: block/redact/tokenize/explicit allow by class;
6. re-scan transformed payload;
7. emit only redacted audit metadata.

Typed technical fields/code/config must not be blindly rewritten by generic prose regexes. On uncertain transformation, block/escalate instead of silently corrupting the payload.

Presidio is a permissive local baseline for PII analysis/anonymization but is not sufficient for secrets or organization-specific identifiers. Pair it with dedicated secret scanning and custom deterministic recognizers.

## Privacy classes

- `PUBLIC`: approved cloud route allowed subject to capability/provider policy.
- `INTERNAL`: cloud allowed only after secret/PII scanning and provider policy.
- `CONFIDENTIAL`: transform/block as configured; provider must satisfy explicit retention/ZDR requirements.
- `LOCAL_ONLY`: never leave the workstation.

The router cannot downgrade the class. Only trusted policy/user authority can change it.

## Provider / gateway controls

The routing contract should express abstract hard provider requirements such as:

- allow/deny/approved-provider policy;
- ZDR/data-collection requirement;
- required parameter/tool/structured-output support;
- region/org restrictions where required;
- session/cache-affinity preference or requirement;
- fallback limits.

OpenRouter can implement useful downstream provider filtering/routing, but **do not assume every raw OpenRouter field is forwarded by the installed Hermes integration**. Prove the effective path through Hermes request policy, OpenRouter account/workspace guardrails or a small audited gateway adapter.

If ZDR, provider allowlist, capability or network requirements cannot be proven, block the cloud route. A provider/model fallback must be re-checked against the hard requirements; availability never authorizes a weaker boundary.

Session/provider stickiness is primarily an economic/continuity control, not authorization. If a pinned/sticky provider degrades, failover is allowed only to another route satisfying all hard requirements and must record the switch reason.

## Router telemetry and replay privacy

Routing research should store hashes/redacted features/outcomes by default, not raw mission prompts. If a framework provides replay, request-body capture, semantic cache or learning stores:

- disable them by default in the hot path;
- explicitly scope retention/permissions when needed;
- prevent cross-privacy-class/session/tenant semantic retrieval;
- keep sampled training records local, redacted and separately governed.

A sophisticated router must not create a new hidden corpus of sensitive work.

## Project prompt injection

Repository/context files remain untrusted. Instructions discovered in source/docs cannot expand capabilities, network policy, model/provider eligibility or human-review requirements. Project-local Pi extensions/agents remain disabled until trusted and pinned; security policy is loaded from uplift-controlled authority.

## Dependency and extension security

For Hermes/Pi/router/LSP extensions and binaries:

- pin version/commit;
- record source/license/hash/SBOM where practical;
- review lock/postinstall/native changes;
- run protocol/security smoke tests in containment;
- update through Phase-70 canary discipline;
- do not auto-promote `latest`, RC or roadmap-only features.

A vLLM Semantic Router fork, if ever created, requires explicit upstream-delta/security review and rebase capacity; upstream/config/adapters are preferred.

## Network posture

Worker modes:

- `none`: default for pure edits/tests with warm dependencies;
- `registries`: package/artifact endpoints only;
- `research`: approved web/search endpoints when policy permits;
- `custom`: explicit host allowlist in the task envelope.

DNS itself can exfiltrate data; enforcement belongs below the agent/tool layer.

## Filesystem posture on macOS

At minimum use dedicated worktree, explicit mounts, temporary HOME, scrubbed environment, no unrelated repo/browser/SSH/Keychain paths and deterministic cleanup. Evaluate stronger container/VM boundaries for untrusted builds.

## Bounded swarm pattern

Avoid unrestricted "spawn roles until done" behavior. A routing decision may propose a bounded workflow, but Hermes/trusted dispatcher validates every stage/agent/capability/budget/review requirement before launch:

```text
mission
 -> eligible bounded workflow stages
 -> isolated worker(s)
 -> deterministic tests/scans
 -> independent review where required
 -> remediation stage if bounded/approved
 -> release gate
```

## Security acceptance tests

Include fixtures that attempt to:

- override `LOCAL_ONLY` or privacy through semantic confidence;
- request unavailable tools/modality/context and force a weaker model;
- route through OpenRouter Auto before sanitization;
- fall back to a provider/model without required ZDR/data/tool constraints;
- exploit missing session/provider metadata as if it proved security;
- turn router replay/cache/telemetry into a sensitive-data store;
- instruct Hermes to bypass Pi;
- change policy in repository text;
- exfiltrate seeded PII/secrets or read unrelated local credentials;
- expand network/role permissions through task text;
- inject via compiler/LSP/tool output;
- exploit compaction so a constraint disappears;
- load untrusted project-local extensions.

Each should fail because of deterministic controls even if every model/router cooperates with the attack.