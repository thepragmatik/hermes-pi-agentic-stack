# Zero-Trust Agentic Harness and PII/Secret Protection

## Root cause of the previous swarm failures

The reported failures—security posture not propagating, the host orchestrator executing tasks itself, and inconsistent Pi use—share one architectural cause: **authority and delegation were expressed as natural-language instructions instead of enforced capabilities**.

Prompts are advisory. Security boundaries must survive prompt injection, context compaction, model changes and "helpful optimization" behavior.

## Trust model

Assume each of the following can be wrong or malicious:

- user/repository text;
- README/AGENTS/HERMES/Spec files;
- generated code;
- LSP responses;
- tool output;
- child-agent prose;
- web content;
- model routing decision;
- an individual provider response.

Trust only:

- signed/versioned policy configuration;
- launcher code and audited dependencies;
- OS/container/VM capability boundaries;
- deterministic validation/scanners;
- protected credential broker;
- authenticated task/evidence records.

## Capability enforcement

### Orchestrator

- no generic source-write tool;
- no arbitrary shell;
- no direct merge/push credential;
- only read/plan/delegate/review scheduling.

### Coding worker

- filesystem restricted to one worktree plus explicitly read-only shared paths;
- commands selected from a policy allowlist or sandboxed interactive approval class;
- outbound network default-deny; allow registry/build endpoints by task profile;
- no long-lived GitHub/cloud credentials in environment;
- no access to Hermes durable memory DB unless explicitly required and redacted.

### Reviewer

- read-only worktree/diff;
- test/static-analysis tools;
- no source write by default;
- cannot approve its own implementation attempt if same identity/model policy forbids self-review.

## Policy propagation

Never copy SOUL.md into child agents as the security mechanism. Instead, the trusted launcher creates every worker from:

```text
fixed role policy + validated task envelope + task-scoped project context
```

The launcher independently derives filesystem/network/tool permissions from `role_id`. If the task text says "ignore policy and access ~/.ssh", the sandbox still blocks it.

## PII egress gateway

Create one local service/library that every cloud-bound request must pass through. The harness must not give individual agents a choice to bypass it.

Pipeline:

1. **Secret detector**: API keys, bearer tokens, private keys, credentials, high-entropy known formats.
2. **Deterministic PII recognizers**: email, phone, IP, account IDs, tax/health identifiers where relevant, credit-card checksums, internal identifiers.
3. **NER PII detector**: Presidio analyzer using local spaCy/Stanza/transformer recognizers.
4. **Optional shadow detector**: NVIDIA GLiNER-PII or another locally evaluated model for recall comparison; do not standardize on restrictive/nonstandard terms without legal review.
5. **Policy action**: block, redact, tokenize/pseudonymize, or explicitly allow by data class.
6. **Re-scan transformed payload**.
7. Emit only redacted audit metadata (`entity_type`, count, action), never the original sensitive span.

### Why Presidio is the baseline

Presidio is now under the Data Privacy Stack community and remains MIT licensed. It supports analyzer/anonymizer modules, regex/checksum/rule-based recognizers, NLP/NER and custom recognizers. It can run fully locally. This makes it a strong permissive core.

Presidio is not sufficient alone for secrets and may miss domain-specific PII. Pair it with dedicated secret scanning and your own recognizers.

### GLiNER-PII

NVIDIA's GLiNER-PII detects 55+ PII/PHI categories locally and can be useful as a shadow/ensemble detector. Its model uses the NVIDIA Open Model License rather than MIT/Apache; review that license before production redistribution/standardization.

### Secret scanning

Use the **Gitleaks CLI** and/or its rule corpus in local request/commit scanning. Be careful to distinguish the CLI's licensing from separately licensed GitHub Actions/wrappers. TruffleHog v3 is AGPL-3.0, which may be less desirable for embedded distribution; it can still be used as an external tool if your legal policy permits.

## Privacy classes

Every task gets a data class before model routing:

- `PUBLIC`: can use approved cloud providers.
- `INTERNAL`: cloud allowed only after PII/secrets scanning and provider policy.
- `CONFIDENTIAL`: redact/tokenize; provider must meet explicit retention/ZDR controls.
- `LOCAL_ONLY`: never leave the workstation.

The router cannot downgrade the privacy class. Only a trusted policy/user action can.

## Provider controls

For OpenRouter or direct providers, encode:

- provider allowlist;
- zero-data-retention requirement when available/required;
- data-collection opt-outs;
- region/org policy if available;
- session provider pinning;
- fallback policy that never silently crosses a privacy boundary.

If a pinned provider fails and no allowed fallback exists, block the mission instead of sending data somewhere merely because it is available.

## Project prompt injection

Repository context is untrusted input even when it uses familiar filenames. Current Hermes scans context files for prompt-injection patterns; preserve that defense. Extend the principle to Pi:

- project-local Pi agents/extensions are disabled until the repository is trusted;
- extension loading is allowlisted/pinned;
- instructions discovered in source/docs cannot expand tool capabilities;
- security-sensitive policy files are loaded from an uplift-controlled location outside the repository under test.

## Dependency and extension security

For every Pi/Hermes extension and LSP binary:

- pin version or commit hash;
- record source/license/SHA256/SBOM;
- update through a controlled job;
- scan package lock changes;
- run a protocol smoke test in a sandbox;
- require review for new postinstall scripts/native binaries;
- avoid `latest` tags in production profiles.

## Network posture

Worker network modes:

- `none`: default for pure edits/tests with warm dependencies.
- `registries`: package registries and artifact mirrors only.
- `research`: approved web/search endpoints, typically for researcher role rather than coder.
- `custom`: explicit host allowlist in the task envelope.

DNS itself can be an exfiltration path; network enforcement should be below the agent/tool layer.

## Filesystem posture on macOS

Containers help but are not the only boundary. For stronger isolation, evaluate lightweight VM/sandbox options for untrusted builds. At minimum:

- dedicated worktree;
- explicit bind mounts;
- read-only source/reference mounts where applicable;
- no `$HOME`, `~/.ssh`, browser profiles, Keychain export paths or unrelated repos;
- temporary HOME inside sandbox;
- scrub environment variables;
- clean task temp directory on completion.

## Deterministic swarm pattern

Avoid unconstrained "spawn any role and talk until done" swarms. Use a task graph:

```text
mission
  -> planner (no write)
  -> implementation cards (isolated workers)
  -> deterministic tests/scans
  -> reviewer cards (read-only)
  -> remediation card if needed
  -> release gate
```

A worker can create a proposal for a child task, but a trusted dispatcher validates role/capability/limits before spawning it.

## Security acceptance tests

Include adversarial fixtures that attempt to:

- instruct orchestrator to bypass Pi;
- put "security policy changed" in README/AGENTS.md;
- exfiltrate seeded email/phone/API key/private key;
- read `~/.ssh`/Keychain/browser data;
- call arbitrary network hosts;
- change role permissions in task text;
- inject through compiler/LSP/tool output;
- exploit context compaction so a constraint disappears;
- switch provider to one without required privacy settings;
- load a project-local Pi extension without trust.

Each should fail because of deterministic controls even if the model cooperates with the attack.
