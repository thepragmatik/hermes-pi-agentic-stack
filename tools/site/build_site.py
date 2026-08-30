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
    "architecture.html": ("Architecture", "docs/agentic-uplift/architecture.md"),
    "fresh-install.html": ("Fresh Install & Manual Bootstrap", "docs/agentic-uplift/fresh-install-bootstrap.md"),
    "start-uplift.html": ("Start the Uplift", "UPLIFT_MISSION.md"),
    "playbook.html": ("Phase-by-Phase Playbook", "docs/agentic-uplift/implementation-playbook.md"),
    "execution-contract.html": ("Agent Execution Contract", "docs/agentic-uplift/agent-execution-contract.md"),
    "bootstrap.html": ("Trusted Bootstrap Authority", "docs/agentic-uplift/bootstrap-authority.md"),
    "context-memory-setup.html": ("LCM + Mnemosyne Baseline Setup", "docs/agentic-uplift/local-context-memory-setup.md"),
    "skills.html": ("Context, Skill Slimming & Slicing", "docs/agentic-uplift/research/skill-slimming-slicing.md"),
    "routing-openrouter.html": ("Routing, OpenRouter & Model Roles", "docs/agentic-uplift/research/openrouter-routing.md"),
    "pi-lsp.html": ("Hermes -> Pi & LSP", "docs/agentic-uplift/research/hermes-pi-lsp.md"),
    "security.html": ("Security, Privacy & Zero Trust", "docs/agentic-uplift/research/security-zero-trust-pii.md"),
    "adversarial-review.html": ("Adversarial Review", "docs/agentic-uplift/adversarial-review.md"),
    "artifact-review.html": ("Validation & Readiness", "docs/agentic-uplift/artifact-usability-review.md"),
    "validation.html": ("Executed Validation Evidence", "docs/agentic-uplift/validation-report.md"),
    "upgrade-rollback.html": ("Upgrade & Rollback Operations", "skills/hermes-stack-uplift/references/70-upgrades-and-rollback.md"),
    "publishing.html": ("Human + Agent Publishing", "docs/agentic-uplift/site-publishing.md"),
    "sources.html": ("Research Sources", "docs/agentic-uplift/SOURCES.md"),
    "research/routing.html": ("Local Routing Research", "docs/agentic-uplift/research/local-routing-models.md"),
    "research/router-training.html": ("Router Training & ModernBERT", "docs/agentic-uplift/research/router-training-control.md"),
    "research/context.html": ("Context & Token Optimization", "docs/agentic-uplift/research/context-token-optimization.md"),
    "research/mission-context.html": ("Mission Context Architecture", "docs/agentic-uplift/research/mission-context-architecture.md"),
    "research/legacy-state.html": ("Legacy Hermes State Curation", "docs/agentic-uplift/research/legacy-state-curation.md"),
    "research/local-context-memory.html": ("Local Context & Memory Research", "docs/agentic-uplift/research/local-context-memory-stack.md"),
    "research/spec-kit.html": ("Spec Kit Profiles", "docs/agentic-uplift/spec-kit-profiles.md"),
    "research/savings.html": ("Savings Model", "docs/agentic-uplift/savings-model.md"),
}

PUBLIC_FILES = [
    "README.md",
    "UPLIFT_MISSION.md",
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
    "docs/agentic-uplift/fresh-install-bootstrap.md",
    "docs/agentic-uplift/local-context-memory-setup.md",
    "docs/agentic-uplift/artifact-usability-review.md",
    "docs/agentic-uplift/adversarial-review.md",
    "docs/agentic-uplift/validation-report.md",
    "docs/agentic-uplift/site-publishing.md",
    "docs/agentic-uplift/implementation-playbook.md",
    "docs/agentic-uplift/spec-kit-profiles.md",
    "docs/agentic-uplift/savings-model.md",
    "docs/agentic-uplift/research/openrouter-routing.md",
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
            close_list(); table.append(line); continue
        close_table()
        if not line.strip():
            close_list(); continue
        if line.startswith("#"):
            close_list()
            level = min(6, len(line) - len(line.lstrip("#")))
            out.append(f"<h{level}>" + inline(line[level:].strip(), page) + f"</h{level}>")
        elif line.startswith("- "):
            if not list_open:
                out.append("<ul>"); list_open = True
            out.append("<li>" + inline(line[2:].strip(), page) + "</li>")
        elif re.match(r"^\d+\. ", line):
            close_list(); out.append("<p>" + inline(line, page) + "</p>")
        elif line.startswith("> "):
            close_list(); out.append("<blockquote>" + inline(line[2:].strip(), page) + "</blockquote>")
        else:
            out.append("<p>" + inline(line, page) + "</p>")

    close_list(); close_table()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


def nav(page: str) -> str:
    items = [
        ("Home", "index.html"),
        ("Architecture", "architecture.html"),
        ("Fresh Install", "fresh-install.html"),
        ("Start Uplift", "start-uplift.html"),
        ("Phases", "playbook.html"),
        ("Context + Skills", "skills.html"),
        ("OpenRouter + Routing", "routing-openrouter.html"),
        ("Pi + LSP", "pi-lsp.html"),
        ("Security", "security.html"),
        ("Adversarial", "adversarial-review.html"),
        ("Readiness", "artifact-review.html"),
        ("Validation", "validation.html"),
        ("Upgrades", "upgrade-rollback.html"),
        ("Sources", "sources.html"),
    ]
    return " ".join(f'<a href="{rel(page, href)}">{html.escape(label)}</a>' for label, href in items)


def layout(title: str, body: str, page: str, raw: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="alternate" type="text/markdown" href="{rel(page, 'raw/' + raw)}"><link rel="alternate" type="text/plain" href="{rel(page, 'llms.txt')}"><style>body{{font:16px/1.58 system-ui,sans-serif;max-width:1180px;margin:auto;padding:2rem;color:#18202a}}nav{{display:flex;gap:.75rem;flex-wrap:wrap;border-bottom:1px solid #ddd;padding-bottom:1rem;margin-bottom:2rem}}a{{color:#1256a0}}pre{{overflow:auto;background:#f6f8fa;padding:1rem;border-radius:.4rem}}code{{background:#f6f8fa}}blockquote{{border-left:4px solid #bbb;margin-left:0;padding-left:1rem}}svg{{max-width:100%;height:auto}}.md-table{{white-space:pre-wrap}}@media(prefers-color-scheme:dark){{body{{color:#e6edf3;background:#0d1117}}a{{color:#58a6ff}}pre,code{{background:#161b22}}nav{{border-color:#30363d}}}}</style></head><body><nav>{nav(page)}</nav><main>{body}</main><hr><p>Canonical source: <a href="{rel(page, 'raw/' + raw)}">Markdown</a> · Agent entry: <a href="{rel(page, 'agent/START.md')}">START.md</a></p></body></html>'''


def svg_arch() -> str:
    return '''<svg viewBox="0 0 1100 370" role="img" aria-labelledby="arch-title arch-desc" xmlns="http://www.w3.org/2000/svg"><title id="arch-title">Hermes Pi OpenRouter agentic stack</title><desc id="arch-desc">Hermes uses local LCM and Mnemosyne, deterministic privacy policy, a local mission router and model-role binding before OpenRouter selects a policy-compatible physical provider. Coding then crosses a typed Pi boundary and evidence/review gates promotion.</desc><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs><style>.b{fill:#fff;stroke:#20252b;stroke-width:2}.t{font:13px system-ui}.e{stroke:#20252b;stroke-width:2;marker-end:url(#a)}</style><rect class="b" x="15" y="150" width="105" height="55" rx="8"/><text class="t" x="67" y="182" text-anchor="middle">Hermes</text><rect class="b" x="145" y="45" width="150" height="60" rx="8"/><text class="t" x="220" y="70" text-anchor="middle">LCM + Mnemosyne</text><text class="t" x="220" y="89" text-anchor="middle">local state/context</text><rect class="b" x="145" y="150" width="145" height="55" rx="8"/><text class="t" x="217" y="173" text-anchor="middle">Deterministic policy</text><text class="t" x="217" y="191" text-anchor="middle">privacy / egress</text><rect class="b" x="325" y="150" width="125" height="55" rx="8"/><text class="t" x="387" y="182" text-anchor="middle">Local router</text><rect class="b" x="485" y="150" width="130" height="55" rx="8"/><text class="t" x="550" y="173" text-anchor="middle">Model-role</text><text class="t" x="550" y="191" text-anchor="middle">binding</text><rect class="b" x="650" y="150" width="125" height="55" rx="8"/><text class="t" x="712" y="182" text-anchor="middle">OpenRouter</text><rect class="b" x="810" y="55" width="140" height="55" rx="8"/><text class="t" x="880" y="79" text-anchor="middle">Research/review</text><text class="t" x="880" y="97" text-anchor="middle">role</text><rect class="b" x="810" y="245" width="140" height="55" rx="8"/><text class="t" x="880" y="268" text-anchor="middle">Typed Pi worker</text><text class="t" x="880" y="286" text-anchor="middle">+ LSP/sandbox</text><rect class="b" x="975" y="150" width="115" height="55" rx="8"/><text class="t" x="1032" y="173" text-anchor="middle">Evidence /</text><text class="t" x="1032" y="191" text-anchor="middle">review gate</text><line class="e" x1="120" y1="165" x2="145" y2="100"/><line class="e" x1="120" y1="178" x2="145" y2="178"/><line class="e" x1="290" y1="178" x2="325" y2="178"/><line class="e" x1="450" y1="178" x2="485" y2="178"/><line class="e" x1="615" y1="178" x2="650" y2="178"/><line class="e" x1="775" y1="164" x2="810" y2="100"/><line class="e" x1="775" y1="192" x2="810" y2="255"/><line class="e" x1="950" y1="83" x2="995" y2="150"/><line class="e" x1="950" y1="273" x2="995" y2="205"/></svg>'''


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
        "Do not ingest the whole site. Execution order:\n\n"
        "1. Read `UPLIFT_MISSION.md`.\n"
        "2. Read the execution contract and schema-valid durable uplift state.\n"
        "3. Read `skills/hermes-stack-uplift/SKILL.md`.\n"
        "4. Load only the current `00-70` phase reference.\n"
        "5. Fetch only research/evidence required by that phase gate.\n\n"
        "Default external gateway is OpenRouter, but deterministic local privacy/security policy runs before every cloud request. "
        "The local router chooses lane/model role/model; OpenRouter may choose only the downstream physical provider within policy. "
        "OpenRouter Auto is never privacy or final mission authority. "
        "LCM + Mnemosyne is the required local context/memory baseline. "
        "At every phase boundary persist uplift-state/evidence, report to the human, and stop before the next phase.\n",
        encoding="utf-8",
    )
    shutil.copy2(ROOT / "UPLIFT_MISSION.md", agent / "UPLIFT_MISSION.md")
    (agent / "manifest.json").write_text(json.dumps({
        "version": 4,
        "generated_from": "canonical repository sources",
        "progressive_disclosure": True,
        "phase_lifecycle": ["00","10","20","30","40","50","60","70"],
        "default_gateway": "openrouter",
        "bootstrap_mode": "single verified OpenRouter model until Phase 30 shadow gate",
        "context_memory_baseline": "LCM + Mnemosyne",
        "files": manifest,
    }, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(ROOT / "docs/agentic-uplift/architecture.graph.json", agent / "architecture.graph.json")
    for src in [
        "protocols/pi-task-envelope.schema.json",
        "protocols/uplift-state.schema.json",
        "protocols/examples/pi-task-envelope.example.json",
        "protocols/examples/uplift-state.example.json",
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
        "> Staged local-first uplift. OpenRouter is the default external gateway; local deterministic privacy policy runs before cloud routing. Use progressive disclosure.\n\n"
        "## Execute / start\n"
        "- [Agent start](agent/START.md)\n"
        "- [Uplift mission](agent/UPLIFT_MISSION.md)\n"
        "- [Fresh install manual](raw/docs/agentic-uplift/fresh-install-bootstrap.md)\n"
        "- [Execution contract](raw/docs/agentic-uplift/agent-execution-contract.md)\n"
        "- [00-70 playbook](raw/docs/agentic-uplift/implementation-playbook.md)\n"
        "- [Sliced uplift skill](agent/skills/hermes-stack-uplift/SKILL.md)\n"
        "- [Uplift state schema](agent/protocols/uplift-state.schema.json)\n\n"
        "## Architecture / configuration\n"
        "- [Architecture](raw/docs/agentic-uplift/architecture.md)\n"
        "- [OpenRouter routing](raw/docs/agentic-uplift/research/openrouter-routing.md)\n"
        "- [Model roles](agent/configs/models.example.yaml)\n"
        "- [LCM + Mnemosyne setup](raw/docs/agentic-uplift/local-context-memory-setup.md)\n"
        "- [Hermes context/memory config](agent/configs/hermes-local-context-memory.example.yaml)\n"
        "- [LCM environment](agent/configs/lcm-baseline.env.example)\n"
        "- [Mnemosyne local config](agent/configs/mnemosyne-local.example.yaml)\n\n"
        "## Research / gates\n"
        "- [Router training / ModernBERT](raw/docs/agentic-uplift/research/router-training-control.md)\n"
        "- [Skill slicing](raw/docs/agentic-uplift/research/skill-slimming-slicing.md)\n"
        "- [Mission context](raw/docs/agentic-uplift/research/mission-context-architecture.md)\n"
        "- [Legacy state curation](raw/docs/agentic-uplift/research/legacy-state-curation.md)\n"
        "- [Security](raw/docs/agentic-uplift/research/security-zero-trust-pii.md)\n"
        "- [Adversarial review](raw/docs/agentic-uplift/adversarial-review.md)\n"
        "- [Readiness](raw/docs/agentic-uplift/artifact-usability-review.md)\n"
        "- [Validation](raw/docs/agentic-uplift/validation-report.md)\n",
        encoding="utf-8",
    )
    (out / "agents.txt").write_text(
        "Start at /llms.txt then /agent/START.md. Do not ingest the whole site. Execute one persisted 00-70 phase at a time. OpenRouter is downstream of local privacy and mission routing.\n",
        encoding="utf-8",
    )
    (out / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    urls = ["https://thepragmatik.github.io/hermes-pi-agentic-stack/" + p for p in PAGES]
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"<url><loc>{html.escape(u)}</loc></url>" for u in urls)
        + "\n</urlset>\n", encoding="utf-8")
    print(f"Built {len(PAGES)} human pages + agent surface")


if __name__ == "__main__":
    main()
