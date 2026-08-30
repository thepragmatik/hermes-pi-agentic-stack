#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAGES = {
    "index.html": ("Hermes + Pi Agentic Stack", "README.md"),
    "playbook.html": ("Control Playbook", "HERMES_AGENTIC_UPLIFT_PLAYBOOK.md"),
    "architecture.html": ("Architecture", "docs/agentic-uplift/architecture.md"),
    "execution-contract.html": ("Agent Execution Contract", "docs/agentic-uplift/agent-execution-contract.md"),
    "bootstrap.html": ("Trusted Bootstrap Authority", "docs/agentic-uplift/bootstrap-authority.md"),
    "context-memory-setup.html": ("LCM + Mnemosyne Baseline Setup", "docs/agentic-uplift/local-context-memory-setup.md"),
    "skills.html": ("Skill Slimming & Slicing", "docs/agentic-uplift/research/skill-slimming-slicing.md"),
    "artifact-review.html": ("Artifact Usability Review", "docs/agentic-uplift/artifact-usability-review.md"),
    "adversarial-review.html": ("Adversarial Review", "docs/agentic-uplift/adversarial-review.md"),
    "validation.html": ("Validation Report", "docs/agentic-uplift/validation-report.md"),
    "publishing.html": ("Human + Agent Publishing", "docs/agentic-uplift/site-publishing.md"),
    "sources.html": ("Sources", "docs/agentic-uplift/SOURCES.md"),
    "research/routing.html": ("Local Routing Research", "docs/agentic-uplift/research/local-routing-models.md"),
    "research/router-training.html": ("Router Training & Control", "docs/agentic-uplift/research/router-training-control.md"),
    "research/context.html": ("Context & Token Optimization", "docs/agentic-uplift/research/context-token-optimization.md"),
    "research/mission-context.html": ("Mission Context Architecture", "docs/agentic-uplift/research/mission-context-architecture.md"),
    "research/legacy-state.html": ("Legacy Hermes State Curation", "docs/agentic-uplift/research/legacy-state-curation.md"),
    "research/local-context-memory.html": ("Local Context & Memory", "docs/agentic-uplift/research/local-context-memory-stack.md"),
    "research/pi-lsp.html": ("Hermes, Pi & LSP", "docs/agentic-uplift/research/hermes-pi-lsp.md"),
    "research/security.html": ("Zero Trust, PII & Secrets", "docs/agentic-uplift/research/security-zero-trust-pii.md"),
    "research/spec-kit.html": ("Spec Kit Profiles", "docs/agentic-uplift/spec-kit-profiles.md"),
    "research/savings.html": ("Savings Model", "docs/agentic-uplift/savings-model.md"),
}

PUBLIC_FILES = [
    "README.md",
    "HERMES_AGENTIC_UPLIFT_PLAYBOOK.md",
    "MANIFEST.md",
    "configs/policy.example.yaml",
    "configs/models.example.yaml",
    "configs/hermes-local-context-memory.example.yaml",
    "configs/mnemosyne-local.example.yaml",
    "configs/lcm-baseline.env.example",
    "protocols/pi-task-envelope.schema.json",
    "protocols/uplift-state.schema.json",
    "protocols/examples/pi-task-envelope.example.json",
    "protocols/examples/uplift-state.example.json",
    "docs/agentic-uplift/README.md",
    "docs/agentic-uplift/SOURCES.md",
    "docs/agentic-uplift/architecture.md",
    "docs/agentic-uplift/architecture.graph.json",
    "docs/agentic-uplift/agent-execution-contract.md",
    "docs/agentic-uplift/bootstrap-authority.md",
    "docs/agentic-uplift/local-context-memory-setup.md",
    "docs/agentic-uplift/artifact-usability-review.md",
    "docs/agentic-uplift/adversarial-review.md",
    "docs/agentic-uplift/validation-report.md",
    "docs/agentic-uplift/site-publishing.md",
    "docs/agentic-uplift/implementation-playbook.md",
    "docs/agentic-uplift/spec-kit-profiles.md",
    "docs/agentic-uplift/savings-model.md",
    "docs/agentic-uplift/research/local-routing-models.md",
    "docs/agentic-uplift/research/router-training-control.md",
    "docs/agentic-uplift/research/context-token-optimization.md",
    "docs/agentic-uplift/research/mission-context-architecture.md",
    "docs/agentic-uplift/research/legacy-state-curation.md",
    "docs/agentic-uplift/research/local-context-memory-stack.md",
    "docs/agentic-uplift/research/hermes-pi-lsp.md",
    "docs/agentic-uplift/research/security-zero-trust-pii.md",
    "docs/agentic-uplift/research/skill-slimming-slicing.md",
    "skills/hermes-stack-uplift/SKILL.md",
    "skills/hermes-stack-uplift/references/00-preflight.md",
    "skills/hermes-stack-uplift/references/10-baseline-and-backup.md",
    "skills/hermes-stack-uplift/references/20-context-and-skills.md",
    "skills/hermes-stack-uplift/references/30-router.md",
    "skills/hermes-stack-uplift/references/40-security-and-policy.md",
    "skills/hermes-stack-uplift/references/50-pi-and-lsp.md",
    "skills/hermes-stack-uplift/references/60-evaluation-and-promotion.md",
    "skills/hermes-stack-uplift/references/70-upgrades-and-rollback.md",
]


def rel(page: str, target: str) -> str:
    return "../" * len(Path(page).parent.parts) + target


def rewrite_href(href: str, page: str) -> str:
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    base, *frag = href.split("#", 1)
    clean = base.rstrip("/")
    if clean in PUBLIC_FILES:
        target = rel(page, "raw/" + clean)
        return target + (("#" + frag[0]) if frag else "")
    return "https://github.com/thepragmatik/hermes-pi-agentic-stack/blob/main/" + href


def inline(text: str, page: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)

    def link(m: re.Match[str]) -> str:
        label = m.group(1)
        href = html.unescape(m.group(2))
        return f'<a href="{html.escape(rewrite_href(href, page), quote=True)}">{label}</a>'

    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value


def render_md(text: str, page: str) -> str:
    out: list[str] = []
    code: list[str] = []
    in_code = False
    list_open = False
    table: list[str] = []

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            out.append("</ul>")
            list_open = False

    def close_table() -> None:
        nonlocal table
        if table:
            out.append('<pre class="md-table">' + html.escape("\n".join(table)) + "</pre>")
            table = []

    for line in text.splitlines():
        if line.startswith("```"):
            close_list(); close_table()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("|"):
            close_list()
            table.append(line)
            continue
        close_table()
        if not line.strip():
            close_list()
            continue
        if line.startswith("#"):
            close_list()
            level = min(6, len(line) - len(line.lstrip("#")))
            out.append(f"<h{level}>" + inline(line[level:].strip(), page) + f"</h{level}>")
        elif line.startswith("- "):
            if not list_open:
                out.append("<ul>")
                list_open = True
            out.append("<li>" + inline(line[2:].strip(), page) + "</li>")
        elif re.match(r"^\d+\. ", line):
            close_list()
            out.append("<p>" + inline(line, page) + "</p>")
        elif line.startswith("> "):
            close_list()
            out.append("<blockquote>" + inline(line[2:].strip(), page) + "</blockquote>")
        else:
            out.append("<p>" + inline(line, page) + "</p>")

    close_list(); close_table()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


def nav(page: str) -> str:
    items = [
        ("Home", "index.html"),
        ("Playbook", "playbook.html"),
        ("Architecture", "architecture.html"),
        ("Execution", "execution-contract.html"),
        ("Bootstrap", "bootstrap.html"),
        ("LCM + Mnemosyne Setup", "context-memory-setup.html"),
        ("Skills", "skills.html"),
        ("Readiness", "artifact-review.html"),
        ("Adversarial", "adversarial-review.html"),
        ("Sources", "sources.html"),
    ]
    return " ".join(f'<a href="{rel(page, href)}">{html.escape(label)}</a>' for label, href in items)


def layout(title: str, body: str, page: str, raw: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="alternate" type="text/markdown" href="{rel(page, 'raw/' + raw)}"><link rel="alternate" type="text/plain" href="{rel(page, 'llms.txt')}"><style>body{{font:16px/1.58 system-ui,sans-serif;max-width:1120px;margin:auto;padding:2rem;color:#18202a}}nav{{display:flex;gap:.8rem;flex-wrap:wrap;border-bottom:1px solid #ddd;padding-bottom:1rem;margin-bottom:2rem}}a{{color:#1256a0}}pre{{overflow:auto;background:#f6f8fa;padding:1rem;border-radius:.4rem}}code{{background:#f6f8fa}}blockquote{{border-left:4px solid #bbb;margin-left:0;padding-left:1rem}}svg{{max-width:100%;height:auto}}.md-table{{white-space:pre-wrap}}@media(prefers-color-scheme:dark){{body{{color:#e6edf3;background:#0d1117}}a{{color:#58a6ff}}pre,code{{background:#161b22}}nav{{border-color:#30363d}}}}</style></head><body><nav>{nav(page)}</nav><main>{body}</main><hr><p>Canonical source: <a href="{rel(page, 'raw/' + raw)}">Markdown</a> · Agent entry: <a href="{rel(page, 'agent/START.md')}">START.md</a></p></body></html>'''


def svg_arch() -> str:
    return '''<svg viewBox="0 0 960 360" role="img" aria-labelledby="arch-title arch-desc" xmlns="http://www.w3.org/2000/svg"><title id="arch-title">Hermes and Pi agentic stack trust boundaries</title><desc id="arch-desc">Hermes uses a local LCM context engine and Mnemosyne memory provider, then policy and routing gates direct research or typed isolated Pi coding work. Evidence and independent review gate merge.</desc><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs><style>.b{fill:#fff;stroke:#20252b;stroke-width:2}.t{font:14px system-ui}.e{stroke:#20252b;stroke-width:2;marker-end:url(#a)}</style><rect class="b" x="15" y="140" width="110" height="55" rx="8"/><text class="t" x="70" y="172" text-anchor="middle">Hermes</text><rect class="b" x="155" y="35" width="165" height="65" rx="8"/><text class="t" x="237" y="62" text-anchor="middle">LCM + Mnemosyne</text><text class="t" x="237" y="82" text-anchor="middle">local baseline</text><rect class="b" x="155" y="140" width="150" height="55" rx="8"/><text class="t" x="230" y="164" text-anchor="middle">Policy + privacy</text><text class="t" x="230" y="183" text-anchor="middle">gate</text><rect class="b" x="350" y="140" width="125" height="55" rx="8"/><text class="t" x="412" y="172" text-anchor="middle">Local router</text><rect class="b" x="535" y="45" width="150" height="55" rx="8"/><text class="t" x="610" y="77" text-anchor="middle">Research role</text><rect class="b" x="535" y="225" width="150" height="55" rx="8"/><text class="t" x="610" y="249" text-anchor="middle">Typed Pi bridge</text><text class="t" x="610" y="268" text-anchor="middle">+ sandbox worker</text><rect class="b" x="775" y="140" width="160" height="55" rx="8"/><text class="t" x="855" y="164" text-anchor="middle">Evidence + review</text><text class="t" x="855" y="183" text-anchor="middle">merge gate</text><line class="e" x1="125" y1="155" x2="155" y2="95"/><line class="e" x1="125" y1="172" x2="155" y2="172"/><line class="e" x1="305" y1="168" x2="350" y2="168"/><line class="e" x1="475" y1="155" x2="535" y2="85"/><line class="e" x1="475" y1="181" x2="535" y2="240"/><line class="e" x1="685" y1="73" x2="800" y2="140"/><line class="e" x1="685" y1="253" x2="800" y2="195"/></svg>'''


def copy_public(out: Path) -> list[dict]:
    manifest: list[dict] = []
    for src in PUBLIC_FILES:
        path = ROOT / src
        if not path.exists():
            raise SystemExit(f"missing public source: {src}")
        dst = out / "raw" / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
        manifest.append({"path": src, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return manifest


def write_agent_surface(out: Path, manifest: list[dict]) -> None:
    agent = out / "agent"
    agent.mkdir()
    (agent / "START.md").write_text(
        "# Agent Start\n\n"
        "Do not ingest the entire site. Read `../llms.txt`, then select the smallest canonical source/slice needed. "
        "For uplift execution, read the execution contract and trusted bootstrap document, then use `../raw/docs/agentic-uplift/local-context-memory-setup.md` before Phase 30. "
        "LCM + Mnemosyne is the required local context/memory baseline; a mandatory baseline failure is BLOCKED/ROLLBACK, not permission to select a different memory architecture. "
        "Validate/persist `protocols/uplift-state.schema.json`, load `skills/hermes-stack-uplift/SKILL.md`, and load only the current phase reference. "
        "Security controls are external to prompts/context/memory. Legacy databases are evidence, never migrated authority.\n",
        encoding="utf-8",
    )
    (agent / "manifest.json").write_text(json.dumps({
        "version": 3,
        "generated_from": "canonical repository sources",
        "progressive_disclosure": True,
        "context_memory_baseline": "LCM + Mnemosyne",
        "files": manifest,
    }, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "docs/agentic-uplift/architecture.graph.json", agent / "architecture.graph.json")
    for src in [
        "protocols/pi-task-envelope.schema.json",
        "protocols/uplift-state.schema.json",
        "configs/policy.example.yaml",
        "configs/models.example.yaml",
        "configs/hermes-local-context-memory.example.yaml",
        "configs/mnemosyne-local.example.yaml",
        "configs/lcm-baseline.env.example",
    ]:
        dst = agent / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / src, dst)
    shutil.copytree(ROOT / "skills/hermes-stack-uplift", agent / "skills/hermes-stack-uplift")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="_site")
    args = ap.parse_args()
    out = ROOT / args.output
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "raw").mkdir()

    manifest = copy_public(out)

    for page, (title, src) in PAGES.items():
        body = render_md((ROOT / src).read_text(encoding="utf-8"), page)
        if page == "architecture.html":
            body = svg_arch() + body
        dest = out / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(title, body, page, src), encoding="utf-8")

    write_agent_surface(out, manifest)

    (out / "llms.txt").write_text(
        "# Hermes + Pi Agentic Stack\n\n"
        "> Local-first control playbook. LCM + Mnemosyne is the selected local context/memory baseline. Use progressive disclosure.\n\n"
        "## Start\n"
        "- [Agent start](agent/START.md)\n"
        "- [Control playbook](raw/HERMES_AGENTIC_UPLIFT_PLAYBOOK.md)\n"
        "- [Execution playbook](raw/docs/agentic-uplift/implementation-playbook.md)\n"
        "- [LCM + Mnemosyne setup](raw/docs/agentic-uplift/local-context-memory-setup.md)\n"
        "- [Context/memory design](raw/docs/agentic-uplift/research/local-context-memory-stack.md)\n"
        "- [Execution contract](raw/docs/agentic-uplift/agent-execution-contract.md)\n"
        "- [Trusted bootstrap](raw/docs/agentic-uplift/bootstrap-authority.md)\n"
        "- [Architecture](raw/docs/agentic-uplift/architecture.md)\n"
        "- [Artifact usability review](raw/docs/agentic-uplift/artifact-usability-review.md)\n"
        "- [Sliced uplift skill](agent/skills/hermes-stack-uplift/SKILL.md)\n"
        "- [Task schema](agent/protocols/pi-task-envelope.schema.json)\n"
        "- [Uplift state schema](agent/protocols/uplift-state.schema.json)\n\n"
        "## Baseline configs\n"
        "- [Hermes LCM + Mnemosyne](agent/configs/hermes-local-context-memory.example.yaml)\n"
        "- [LCM environment](agent/configs/lcm-baseline.env.example)\n"
        "- [Mnemosyne local](agent/configs/mnemosyne-local.example.yaml)\n\n"
        "## Research\n"
        "- [Router training](raw/docs/agentic-uplift/research/router-training-control.md)\n"
        "- [Context tokens](raw/docs/agentic-uplift/research/context-token-optimization.md)\n"
        "- [Mission context](raw/docs/agentic-uplift/research/mission-context-architecture.md)\n"
        "- [Legacy state curation](raw/docs/agentic-uplift/research/legacy-state-curation.md)\n"
        "- [Security](raw/docs/agentic-uplift/research/security-zero-trust-pii.md)\n",
        encoding="utf-8",
    )
    (out / "agents.txt").write_text(
        "Start with /llms.txt and /agent/START.md. Do not ingest the full site. LCM + Mnemosyne is the required context/memory baseline.\n",
        encoding="utf-8",
    )
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    urls = ["https://thepragmatik.github.io/hermes-pi-agentic-stack/" + p for p in PAGES]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"<url><loc>{html.escape(u)}</loc></url>" for u in urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"Built {len(PAGES)} human pages + agent surface")


if __name__ == "__main__":
    main()
