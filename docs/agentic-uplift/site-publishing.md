# GitHub Pages: Human + Agent Publication

## Goal

Publish one evidence set through representations optimized for different readers without creating divergent truth. Canonical sources remain Markdown/JSON/YAML in the repository. The site is generated from them.

## Human surface

The site has a short landing page and dedicated pages for architecture, playbook, execution contract, skill slicing, artifact review, adversarial review, routing, context, Pi/LSP, security, Spec Kit, savings, validation and sources. Each HTML page links to its canonical Markdown alternate.

## Agent surface

`/llms.txt` is deliberately small. It points to `/agent/START.md`, the machine manifest, architecture graph, schemas, configs and sliced skill. Agents should fetch only the slice needed for the active phase. We intentionally do not publish a monolithic `llms-full.txt`, because that recreates the context-bloat problem this stack is solving.

SVGs are retained for humans and multimodal systems, but they are not the sole representation. Architecture is also published as Markdown and graph JSON. Important SVGs require `<title>` and `<desc>` plus nearby textual explanation.

## Public-boundary rule

Treat Pages output as PUBLIC even if the source repository is private. Never publish context databases, production transcripts, secrets, credentials, raw PII datasets, private evidence bundles or unredacted customer/project material. The build includes an allowlist of public source paths rather than copying the repository wholesale.

## Deployment

`.github/workflows/pages.yml` builds the site into `_site`, validates it, uploads a Pages artifact and deploys it. The workflow requests Pages enablement through the official configure-pages action. Availability for a private repository still depends on the GitHub account/plan and repository Pages settings.

Expected project URL after successful deployment: `https://thepragmatik.github.io/hermes-pi-agentic-stack/`.
