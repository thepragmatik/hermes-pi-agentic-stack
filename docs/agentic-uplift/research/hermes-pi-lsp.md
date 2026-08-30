# Hermes → Pi Integration and LSP Design

## Integration goal

Hermes remains the single mission entry point and control-plane planner. Pi is the only standard path for coding execution. The integration must be deterministic enough that the orchestrator cannot silently start coding itself or inconsistently bypass Pi.

## Use Pi RPC/headless mode, not terminal prompt choreography

Pi supports non-interactive/headless/RPC-style operation. This gives the bridge a structured stdin/stdout event surface and is much more robust than spawning an interactive terminal and relying on prompt text.

Recommended process model:

```text
Hermes
  |
  | delegate_pi(task envelope)
  v
Trusted bridge/launcher (Python)
  |- validate schema + signature/policy
  |- create git worktree
  |- build sandbox profile
  |- launch Pi RPC subprocess
  |- pin model/provider/toolset
  |- stream typed events
  |- enforce timeout/budgets
  |- collect evidence bundle
  v
Pi worker (Node/TS)
  |- file tools (workspace only)
  |- LSP tools
  |- test/build allowlist
  '- no merge credential
```

## Why a narrow bridge beats a merged harness

Do not deeply embed Pi's internal TypeScript classes into Hermes core unless necessary. A process boundary gives:

- version independence (Hermes and Pi can update daily);
- resource accounting per task;
- OS-level termination;
- capability isolation;
- simpler protocol testing;
- easier replacement of Pi later;
- clearer audit log.

The bridge should depend on Pi's documented RPC/event contract, not implementation-private modules.

## `delegate_pi` contract

Input is a signed/validated task envelope (see `protocols/pi-task-envelope.schema.json`) containing:

- task ID and idempotency key;
- role from a fixed catalog;
- objective and acceptance criteria;
- relevant spec/artifact paths;
- allowed filesystem roots;
- allowed command families;
- network policy/allowlist;
- model/provider profile;
- max wall time / token / cost budget;
- PII/privacy classification;
- required evidence.

Output is never just prose. It must contain a result object:

```json
{
  "status": "completed|blocked|failed",
  "task_id": "...",
  "base_sha": "...",
  "head_sha": "...",
  "changed_files": ["..."],
  "tests": [{"command":"...","exit_code":0,"summary":"..."}],
  "lsp": {"errors":0,"warnings":2},
  "security": {"pii_scan":"pass","secret_scan":"pass"},
  "assumptions": [],
  "unresolved": [],
  "artifacts": ["..."],
  "ready_for_review": true
}
```

Hermes reads this handoff and decides what review task to dispatch. It does not reinterpret "looks good" as merge permission.

## Worker lifecycle

1. Resolve current repository SHA.
2. Create a dedicated worktree under an uplift-controlled root.
3. Materialize only task-scoped secrets/credentials, preferably none.
4. Start LSP servers lazily.
5. Start Pi RPC with a stable policy prefix and explicit tool allowlist.
6. Stream events to the bridge. Store redacted structured telemetry.
7. On destructive/network operation, the policy layer decides—not the model prompt.
8. Run acceptance commands.
9. Run PII/secrets/diff scanners.
10. Generate evidence bundle.
11. Terminate Pi/LSP processes and clean temporary credentials.
12. Keep worktree for review or delete on rollback.

## Role catalog

Dynamic roles are allowed only as *labels mapped to predefined capabilities*.

Example:

| Role | Read | Write | Shell | Network | Merge |
|---|---:|---:|---:|---:|---:|
| `researcher` | artifact/docs | no source | safe read tools | allowlisted web/API | no |
| `coder` | workspace | workspace | build/test allowlist | dependency registries only | no |
| `reviewer` | workspace/diff | comments/evidence only | test/static analysis | usually off | no |
| `release` | signed artifacts | release metadata | release allowlist | release endpoints | gated |

An LLM may request `role=coder`; it cannot invent `role=root-coder` or add shell/network capabilities.

## LSP strategy

A current third-party `pi-lsp-extension` provides diagnostics, hover, definition, references, symbols, rename preview, completion and code-oriented operations, with lazy/shared language-server processes. It includes mappings for TypeScript/JavaScript, Python and Java. Treat it as a useful accelerator, not a trust anchor: pin a reviewed commit/version and vendor a lockfile/SBOM if productionized.

### Language server matrix

| Language | Server | Status/recommendation |
|---|---|---|
| TypeScript / JavaScript | `typescript-language-server --stdio` | mature; Apache-2.0 package |
| Python | `pyright-langserver --stdio` | mature; MIT |
| Java | Eclipse JDT LS (`jdtls`) | mature; EPL-2.0; Java 21+ runtime in current docs |
| Kotlin | JetBrains official `kotlin-lsp --stdio` | **use official server**; Alpha in 2026, IntelliJ-backed; test Gradle/Maven/Android cases |
| HTML | VS Code HTML language server extraction | use maintained/pinned package; MIT wrapper/VS Code licensing |
| CSS | VS Code CSS language server extraction | same |
| JSON (useful) | VS Code JSON language server | optional |

### Kotlin note

The situation improved materially in 2026: JetBrains now documents an official Kotlin Language Server based on IntelliJ/Kotlin infrastructure. It is still Alpha, so the playbook should keep a compatibility test suite and make Kotlin LSP failure non-fatal to coding, while still failing the *refactor-quality gate* when a task explicitly requires semantic refactoring.

## Bounded diagnostic injection

LSP can itself become a token firehose. Never append full workspace diagnostics to every model turn.

Rules:

- after an edit, return diagnostics for changed files only;
- cap to N highest-severity diagnostics (e.g. 10) plus counts;
- provide a tool for explicit deeper diagnostics;
- use symbol/definition/reference calls to fetch precise context instead of opening entire files;
- cache immutable symbol data for a task where safe;
- redact file content before any cloud-bound diagnostic context if privacy policy requires it.

## Hermes orchestrator toolset

The strongest fix for the previous "orchestrator starts coding itself" failure is structural. In orchestrator profile, expose only:

- session/artifact search;
- read-only repo metadata;
- task board / Kanban functions;
- `delegate_pi`;
- `delegate_research` / provider model call abstraction;
- reviewer dispatch;
- policy/telemetry status.

Do **not** expose generic shell, arbitrary file write, source edit, package install or git merge. If an emergency maintenance mode needs them, make that a separate explicit profile requiring human activation.

## Idempotency and retries

Agent tasks must tolerate process failure. Every envelope has an idempotency key. The launcher records task state transitions in a local durable DB. A retry either resumes an intact worktree or creates a new attempt from the same base SHA. It never blindly repeats a destructive command.

## Review topology

A good default is **implementer ≠ reviewer**:

- Pi/GLM implements.
- A separate reviewer profile receives the diff, acceptance criteria and selected source context, preferably read-only.
- High-risk tasks can use a different model/provider for diversity.
- Deterministic tests/scanners gate both.
- Human approval remains configurable for protected branches/release actions.

## Upgrade compatibility

The bridge should run protocol conformance tests against the installed Pi version during every update:

- start/stop RPC;
- tool event schema;
- cancellation;
- malformed event handling;
- model/profile selection;
- no-tools/allowlist behavior;
- context compaction event handling if consumed;
- one representative LSP edit.

If conformance breaks, retain the previous pinned Pi version while Hermes can still upgrade independently.
