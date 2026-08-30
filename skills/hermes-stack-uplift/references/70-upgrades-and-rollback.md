# Phase 70 — Upgrades, Restarts and Rollback Discipline

Treat Hermes, Pi, LCM, Mnemosyne, router classifiers/models, LSPs and OpenRouter role/provider-policy bindings as independently pinned dependencies.

For every change:

1. inspect current trusted release/security/model/provider metadata;
2. create a disposable canary/session/workers;
3. quiesce/back up context/memory stores before schema-affecting changes;
4. change one bounded layer;
5. reapply only versioned overlay/config;
6. run the relevant protocol/security/context/memory/router/OpenRouter/LSP/coding smoke + adversarial tests;
7. compare prompt/cache/recall/accepted-task metrics with previous pins;
8. create fresh Hermes sessions and Pi workers whenever stale prompt/plugin/runtime state could hide the change;
9. promote only on pass;
10. otherwise roll back to the last known-good pin and record the blocker.

Do not chase release candidates, model `latest` aliases or transient cheapest OpenRouter physical providers in production. Re-verify bindings periodically, but preserve phase/session stickiness once selected.

Direct provider credentials remain absent unless a recurring matched benchmark continues to justify the exception.

## Upgrade Checkpoint F

Persist the recurring canary/restart/rollback policy and prove at least one end-to-end rollback exercise. Keep the last validated profile, provider/model role lock and context/memory/Pi checkpoints immediately recoverable.

Persist final state/evidence and send the required phase-boundary report. Future updates repeat this canary cycle rather than reopening the original uplift as one giant session.
