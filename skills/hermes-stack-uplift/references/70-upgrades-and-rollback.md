# Phase 70 — Upgrades and Rollback

Treat Hermes and Pi as independently pinned upstream dependencies. Rehearse upgrades in a disposable profile/worktree, reapply the overlay, run contract/security/router/context smoke tests, compare metrics, then promote pins. Roll back on integration-point drift or regression. Track any unavoidable upstream patch for removal/upstreaming.

Keep the last validated pins/checkpoint immediately recoverable.
