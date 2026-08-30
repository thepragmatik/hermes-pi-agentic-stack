# Fresh Install: Manual Bootstrap Steps

Snapshot: 2026-08-30. Re-verify current stable software/model choices when executing.

This is the **human-only foundation** before Hermes starts the staged self-uplift. The objective is a clean, narrow Hermes profile with one OpenRouter credential/model, the repository available locally, the uplift skill discoverable, a rollback path, and no inherited legacy state.

## 0. Establish a real bootstrap boundary

A Hermes profile isolates configuration/state but **does not sandbox filesystem access**. `terminal.cwd`, SOUL text and skill instructions are not security boundaries.

Preferred bootstrap on macOS:

1. In **System Settings -> Users & Groups**, create a dedicated **Standard (non-admin)** macOS account for the uplift.
2. Do not grant that account access to production/customer repositories, production credential stores, SSH keys or unrelated sensitive directories.
3. Log into that account and perform the remaining steps there.

This gives the initial self-uplift an OS-account boundary before the stack has built its final Pi/capability broker. If you deliberately run Hermes under your normal developer account instead, record that decision as **trusted bootstrap authority**: it is not structurally restricted and must not be described as zero-trust.

Hermes also provides a Docker terminal backend, but Docker/workspace behaviour is version-sensitive and has had current integration defects. Treat Docker as a component to qualify against the installed Hermes release rather than blindly assuming it is the bootstrap boundary. Phase 40/50 must still prove the final containment path.

## 1. Install current Hermes

On the dedicated bootstrap account:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc
hermes --version
```

If the installer tells you to use a different shell-init file, follow its printed instruction. Do not reuse/copy the old Hermes home into this account/profile.

## 2. Clone this control repository

The repository is currently public, so a read-only HTTPS clone does not require a GitHub credential. If repository visibility or access policy changes later, use your normal authenticated GitHub method. Never paste a GitHub credential into this document or the Hermes chat.

```bash
mkdir -p ~/src
cd ~/src
git clone https://github.com/thepragmatik/hermes-pi-agentic-stack.git
cd hermes-pi-agentic-stack
STACK_REPO="$(pwd -P)"
git status --short
git rev-parse HEAD
```

The working tree should be clean. Record the commit SHA in baseline evidence.

## 3. Create a narrow profile with no bundled skill catalogue

Current Hermes supports named profiles and `--no-skills`:

```bash
hermes profile create uplift --no-skills \
  --description "Controlled Hermes + Pi staged self-uplift orchestrator."
```

The profile command creates the `uplift` wrapper/alias. Confirm it exists:

```bash
hermes profile show uplift
uplift config path
```

Do **not** use `--clone` or `--clone-all`: the point is to avoid inheriting old sessions, context, memory or skills.

## 4. Run Blank Slate setup

```bash
uplift setup
```

Choose **Blank Slate**. Current Hermes documents this mode as the provider/model plus only File Operations and Terminal, with web/browser/code execution/vision/memory/delegation/cron/skills/plugins/MCP and several automatic behaviours off until explicitly enabled.

Do not enable the broad default skill/tool/plugin catalogue during bootstrap.

## 5. Configure OpenRouter and one bootstrap model securely

Run the current canonical provider/model wizard:

```bash
uplift model
```

In the wizard:

1. choose **OpenRouter**;
2. enter the OpenRouter API key when Hermes prompts for it;
3. select the current **GLM-5.3 Flash-class** OpenRouter model intended for bootstrap;
4. record the exact model ID Hermes resolves.

Research snapshot on 2026-08-30: `z-ai/glm-5.3-flash`. Do **not** blindly paste that ID months later; use the live picker and verify it still exists and supports the required tool parameters.

Hermes stores provider secrets in the profile's secret environment rather than in this repository. Preferred initial external inference credential footprint is only:

```text
OPENROUTER_API_KEY
```

Do not add direct Z.ai/DeepSeek keys yet.

Verify the effective selection without printing the secret:

```bash
uplift config get model --json
uplift status
```

## 6. Point the profile at this repository

The CLI itself uses the launch directory; also set an explicit profile working directory for gateway/other launches:

```bash
cd "$STACK_REPO"
uplift config set terminal.cwd "$STACK_REPO"
```

Current Hermes has a documented `skills.external_dirs` feature, but current releases have had list-value config edge cases. For the bootstrap, avoid ambiguous list serialization and expose exactly one repository skill with a profile-local symlink:

```bash
PROFILE_CONFIG="$(uplift config path)"
PROFILE_HOME="$(dirname "$PROFILE_CONFIG")"
mkdir -p "$PROFILE_HOME/skills"
ln -sfn "$STACK_REPO/skills/hermes-stack-uplift" \
  "$PROFILE_HOME/skills/hermes-stack-uplift"
```

Verify:

```bash
uplift skills list
```

The intended result is the essential Hermes operating skill(s) plus `hermes-stack-uplift`, not the full bundled catalogue.

## 7. Create bootstrap evidence/checkpoint directories

Keep mutable runtime state out of canonical source while making it durable across chat resets:

```bash
mkdir -p "$PROFILE_HOME/uplift/evidence" "$PROFILE_HOME/uplift/checkpoints"
printf '%s\n' "$STACK_REPO" > "$PROFILE_HOME/uplift/repository.path"
git -C "$STACK_REPO" rev-parse HEAD > "$PROFILE_HOME/uplift/repository.sha"
shasum -a 256 "$STACK_REPO/configs/policy.example.yaml" \
  > "$PROFILE_HOME/uplift/policy.sha256"
```

The authoritative mutable execution state should live at:

```text
$PROFILE_HOME/uplift/uplift-state.json
```

and conform to `protocols/uplift-state.schema.json`. Evidence paths/hashes are referenced from that state; they are not replaced by chat memory.

## 8. Health/config validation

Run before handing control to Hermes:

```bash
uplift config check
uplift doctor
uplift dump
uplift config get model --json
git -C "$STACK_REPO" status --short
git -C "$STACK_REPO" rev-parse HEAD
```

Record at minimum:

- Hermes version;
- current profile/home;
- repo commit SHA;
- OpenRouter provider + exact bootstrap model ID (never the API key);
- Pi version if Pi is already installed, otherwise `not-installed`;
- policy digest;
- bootstrap isolation mode;
- rollback/checkpoint path.

Any missing/invalid provider config, dirty unexpected repo state, unknown legacy-state attachment, or inadequate bootstrap boundary is a Phase 00 blocker.

## 9. Start the uplift — one command

From the repository root:

```bash
cd "$STACK_REPO"
uplift chat --query-file UPLIFT_MISSION.md
```

Current Hermes documents `--query-file` as a normal first-turn query: file contents are passed literally and, on a real terminal, the normal interactive session remains open. That makes it more robust than trying to encode a long mission in shell quoting or relying on a slash command as the launcher.

`UPLIFT_MISSION.md` tells Hermes to read durable state, load the `hermes-stack-uplift` parent skill and only the current phase slice, execute one phase, persist evidence/state, report the phase boundary, and stop before starting the next phase.

## Manual setup -> Hermes takeover

```text
human creates isolated bootstrap account/profile
  -> installs/configures clean Hermes
  -> OpenRouter + one GLM-Flash-class bootstrap model
  -> clones repo + exposes one uplift skill
  -> records health/version/checkpoint evidence
  -> `uplift chat --query-file UPLIFT_MISSION.md`
  -> Hermes executes Phase 00 and reports
  -> human continues phase-by-phase
```

## Bootstrap Mode ends gradually

The single bootstrap model remains the default through the early context/skill work. Phase 30 builds and validates the local mission router in **shadow mode**. Multiple model roles are introduced only after routing and security gates justify them.

A fresh profile is not proof of enforcement. The P0 security/capability/Pi boundaries still have to be implemented and adversarially proven before unattended production authority.