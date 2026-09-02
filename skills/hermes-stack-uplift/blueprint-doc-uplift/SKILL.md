---
name: blueprint-doc-uplift
description: "Use for repo doc uplift with SVG diagrams and push handoffs."
---

# Blueprint Documentation Uplift

Proven workflow from the mission-end blueprint refresh of hermes-pi-agentic-stack (2026-09-01): adversarial doc review + four production SVG diagrams + README restructure, committed in reviewable layers.

## SVG diagram conventions (validated on GitHub)

- Standalone SVGs in a `diagrams/` dir, referenced from markdown via image syntax (`![alt](path.svg)`). GitHub renders markdown image refs to SVG but does NOT render inline `<svg>` blocks in markdown — inline SVG belongs only in `.html` presentation views.
- Canonical-representation rule: keep machine-readable sources (e.g. `architecture.graph.json` + markdown) canonical for agents; label SVGs as presentation views and never let a diagram contradict canonical text — add a precedence note where both appear.
- Design system: one shared semantic palette (e.g. rose=security, blue=deterministic control, amber=delegation, emerald=evidence, violet=memory), tinted dashed panels for trust zones (dashed = external/operator-owned), legends for non-obvious symbols, `<title>`+`<desc>` a11y, viewBox-only sizing.
- Dark-mode: embed `@media (prefers-color-scheme: dark)` swaps in an SVG `<style>` block; validate against `#0d1117` (GitHub dark), not just white. Avoid `fill:#fff` text on transparent backgrounds — invisible in dark mode.
- Verify VISUALLY, not just XML-parse: `qlmanage -t -s 1400 -o /tmp <file>.svg` renders a PNG; inspect with the vision tool. Screenshot review catches text overflow and box overlaps that XML validation misses — check sublabels touching box edges and captions grazing zone boundaries (these survived a subagent's own screenshot pass).
- Perfect the design on ONE diagram, then replicate the system across the set.

## README as hero artifact (user preference)

The user explicitly wants the README uplifted with diagrams — it is the first thing users see on GitHub. Structure that worked: hero diagram right after the intro → "What was proven" callout with headline metrics → audience-split quick start ("For humans" / "For agents") → deep detail below the fold. Keep the dense imperative tone; no marketing fluff. Keep maturity/status claims in sync with actual mission state — stale "designed but not proven" banners after a mission succeeded are a major reader-facing defect.

## PII scan of large diffs (BSD/macOS)

macOS grep has no `-P`, and `-E` chokes on lookarounds; scan with Python `re` over `git diff <base>..<head>` added lines instead — per-commit AND aggregate, plus commit messages. Known false positives to whitelist: `sk-` inside words like `task-envelope`; synthetic security-gate fixtures (`sk-or-...nopq`, `ghp_AB...3456`, `/Users/someuser`, the canonical AWS doc example key) are intentional test vectors — verify fixtures are truncated/fake, then clear. High-entropy heuristics also hit SHA digests and long test method names; inspect before flagging.

## git push 403 with a fine-grained PAT

Symptom: `remote: Permission to <owner>/<repo>.git denied to <owner>` / 403 on push, while clone/fetch and `gh api` work.

Diagnosis chain that resolved it: `gh auth status` (token type — `github_pat_` prefix = fine-grained) → `ssh -T git@github.com` (SSH auth works) → fine-grained PATs need **Contents: Read and write** repo permission for git push; metadata-only grants pass REST reads but fail push. Two fixes: `git remote set-url origin git@github.com:<owner>/<repo>.git` (SSH, instant), or regenerate the PAT with Contents read/write. Never log or persist the token value.

## Site-generator pages: fix the renderer, not the content (DRY)

When the artefact set renders through a custom static-site generator (e.g. a stdlib `build_site.py`), audit the RENDERER first: the 2026-09-02 "ugly tables" complaint traced to the generator emitting pipe-tables as escaped `<pre>` text dumps. One TDD'd `render_table()` function (test scaffold asserting `<th>`/`<td>` output, red→green) fixed every affected page at once. Unit tests for a generator: import the module and call `render_md(md_string, page)` directly with small markdown fixtures.

- f-string CSS trap: layout templates are often one big f-string; inserted CSS must DOUBLE its braces (`{{color:#fff}}`) or Python evaluates them as expressions. Symptom: Pyright flags `overflow`/`padding` as undefined variables on the template line.
- Inlined-SVG grep trap: once a builder INLINES an SVG into HTML, the file's filename string no longer appears in the output — verify injection by grepping the `<title id>` value, never the filename.
- Heading-marker injection: mapping `page -> (heading_text, svg_fn)` and replacing `<h1>{marker}</h1>` works, but confirm the rendered heading level first and add a built-output assertion test, or a marker drift silently skips injection.
- Mermaid vs hand SVG for offline/zero-dependency sites: vendored `mermaid.min.js` (~1.2 MB) breaks a stdlib-only builder and CDN scripts fail offline — hand-authored SVG in the house palette is the default; treat live-Mermaid as a user-request follow-up only.
- Build outputs are often gitignored (GitHub Pages builds at deploy): check `git ls-files _site | head -1` BEFORE planning a commit of generated pages.
- Harden the site validator alongside: SVG XML parse over `diagrams/*.svg` + "no raw table dump" page checks become permanent regression gates (TDD these too).

## Commit layering for reviewable handoffs

Split doc uplift into logical commits — (1) surgical doc fixes, (2) diagrams, (3) README uplift — so the human can review each layer before merging. Orchestrator never merges/tags/pushes; hand exact commands to the user at the boundary.
