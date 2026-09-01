# Session Capability Modes — stack design principle

Human-approved addendum (2026-09-01). Generalizes to all future capability-UX
decisions in this stack.

> Capability changes are: session-scoped, user-flipped, structurally enforced,
> default-safe, and visible. Preferences control WHICH proven modes are
> available — they never substitute for a gate, and a gate's default posture is
> set by evidence, not by preference.

## Rules

1. **Consent is sticky but bounded** — one deliberate mode switch per session;
   no per-action approval fatigue.
2. **Default is the safe mode** — restrictive posture until the user flips it.
   Post-B6, "skip Pi, edit directly" must fail structurally.
3. **Preference = UX affordance; hook = enforcement** — the toggle flips a
   structural config/CLI hook, never prompt/skill text. Enforcement living in
   SOUL.md or a skill is advisory only and violates the Phase-40 line.
4. **Visible and reversible** — the active mode is always evident
   (recorded in every run's evidence JSON); switching back is symmetric.
5. **Post-B6 user choice remains** for: which tasks are delegated at all, and
   which capabilities (cloud canary, propagation) are enabled for the session.

## Implemented enforcement boundary (honest scoping)

This Hermes version (v0.20.6) exposes **no permissions/hooks config keys**
(Phase 60 evidence), so in-profile structural gating is impossible. The hook is
therefore implemented at the **bridge level** — the layer this mission controls:

- `tools/pi-bridge/pi_bridge.py run --capability-mode restricted|pi-coding`
  (default `restricted`).
- In `restricted` (default), `--model-proxy` (cloud model egress) raises a
  typed `BridgeError("capability_mode_denied: ...")` **before any worker
  launch or worktree creation** — no side effects.
- In `pi-coding` (explicit operator opt-in), the proxy path is enabled; the
  active mode is recorded in every run's evidence JSON
  (`capability_mode`, `model_proxy.capability_mode`).

**Enforcement boundary:** the bridge CLI and its evidence, NOT the orchestrator
process. An operator who bypasses the bridge is outside this gate — the same
EXTERNAL boundary recorded in Phase 60. Do not represent this as
orchestrator-level enforcement.

## Evidence both states fire

- Default state: `tests/test_pi_bridge.py::test_capability_mode_restricted_denies_model_proxy`
  — rc=3, typed error, no worktree created.
- Opted-in state: `tests/test_pi_bridge.py::test_capability_mode_pi_coding_opt_in_allows_proxy`
  — run proceeds offline; evidence records `capability_mode: pi-coding`.

## Mode applications

| Capability | Pre-B6 mode | Post-B6 mode |
|---|---|---|
| Coding path | opt into Pi-typed-delegation | Pi default; direct-edit structurally rejected |
| Cloud canary | per-run approval | session-scoped enable (`--capability-mode pi-coding`) |
| Router | shadow | authoritative only after Checkpoint-E evidence |
| Propagation | per-profile human approval | session-scoped per profile |
