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
    "routing-openrouter.html": ("OpenRouter Gateway & Provider Routing", "docs/agentic-uplift/research/openrouter-routing.md"),
    "pi-lsp.html": ("Hermes -> Pi & LSP", "docs/agentic-uplift/research/hermes-pi-lsp.md"),
    "security.html": ("Security, Privacy & Zero Trust", "docs/agentic-uplift/research/security-zero-trust-pii.md"),
    "adversarial-review.html": ("Adversarial Review", "docs/agentic-uplift/adversarial-review.md"),
    "artifact-review.html": ("Validation & Readiness", "docs/agentic-uplift/artifact-usability-review.md"),
    "validation.html": ("Executed Validation Evidence", "docs/agentic-uplift/validation-report.md"),
    "upgrade-rollback.html": ("Upgrade & Rollback Operations", "skills/hermes-stack-uplift/references/70-upgrades-and-rollback.md"),
    "publishing.html": ("Human + Agent Publishing", "docs/agentic-uplift/site-publishing.md"),
    "sources.html": ("Research Sources", "docs/agentic-uplift/SOURCES.md"),
    "research/routing.html": ("Mission Routing Architecture & Frameworks", "docs/agentic-uplift/research/local-routing-models.md"),
    "research/router-training.html": ("Router Training & ModernBERT", "docs/agentic-uplift/research/router-training-control.md"),
    "research/context.html": ("Context & Token Optimization", "docs/agentic-uplift/research/context-token-optimization.md"),
    "research/mission-context.html": ("Mission Context Architecture", "docs/agentic-uplift/research/mission-context-architecture.md"),
    "research/legacy-state.html": ("Legacy Hermes State Curation", "docs/agentic-uplift/research/legacy-state-curation.md"),
    "research/local-context-memory.html": ("Local Context & Memory Research", "docs/agentic-uplift/research/local-context-memory-stack.md"),
    "research/spec-kit.html": ("Spec Kit Profiles", "docs/agentic-uplift/spec-kit-profiles.md"),
    "research/savings.html": ("Savings Model", "docs/agentic-uplift/savings-model.md"),
}

PUBLIC_FILES = [
    "README.md", "UPLIFT_MISSION.md", "HERMES_AGENTIC_UPLIFT_PLAYBOOK.md", "MANIFEST.md",
    "configs/policy.example.yaml", "configs/models.example.yaml",
    "configs/hermes-local-context-memory.example.yaml", "configs/mnemosyne-local.example.yaml", "configs/lcm-baseline.env.example",
    "protocols/routing-mission.schema.json", "protocols/routing-decision.schema.json",
    "protocols/pi-task-envelope.schema.json", "protocols/uplift-state.schema.json",
    "protocols/examples/routing-mission.example.json", "protocols/examples/routing-decision.example.json",
    "protocols/examples/pi-task-envelope.example.json", "protocols/examples/uplift-state.example.json",
    "docs/agentic-uplift/README.md", "docs/agentic-uplift/SOURCES.md",
    "docs/agentic-uplift/architecture.md", "docs/agentic-uplift/architecture.graph.json",
    "docs/agentic-uplift/agent-execution-contract.md", "docs/agentic-uplift/bootstrap-authority.md",
    "docs/agentic-uplift/fresh-install-bootstrap.md", "docs/agentic-uplift/local-context-memory-setup.md",
    "docs/agentic-uplift/artifact-usability-review.md", "docs/agentic-uplift/adversarial-review.md",
    "docs/agentic-uplift/validation-report.md", "docs/agentic-uplift/site-publishing.md",
    "docs/agentic-uplift/implementation-playbook.md", "docs/agentic-uplift/spec-kit-profiles.md", "docs/agentic-uplift/savings-model.md",
    "docs/agentic-uplift/research/openrouter-routing.md", "docs/agentic-uplift/research/local-routing-models.md",
    "docs/agentic-uplift/research/router-training-control.md", "docs/agentic-uplift/research/context-token-optimization.md",
    "docs/agentic-uplift/research/mission-context-architecture.md", "docs/agentic-uplift/research/legacy-state-curation.md",
    "docs/agentic-uplift/research/local-context-memory-stack.md", "docs/agentic-uplift/research/hermes-pi-lsp.md",
    "docs/agentic-uplift/research/security-zero-trust-pii.md", "docs/agentic-uplift/research/skill-slimming-slicing.md",
    "tools/router-bench/README.md", "tools/router-bench/sample_missions.jsonl",
    "docs/agentic-uplift/diagrams/system-topology.svg", "docs/agentic-uplift/diagrams/mission-lifecycle.svg",
    "docs/agentic-uplift/diagrams/pi-bridge-flow.svg", "docs/agentic-uplift/diagrams/trust-boundaries.svg",
    "docs/agentic-uplift/diagrams/routing-tiers.svg",
    "docs/agentic-uplift/diagrams/phase-lifecycle.svg",
    "skills/hermes-stack-uplift/SKILL.md",
    "skills/hermes-stack-uplift/references/00-preflight.md", "skills/hermes-stack-uplift/references/10-baseline-and-backup.md",
    "skills/hermes-stack-uplift/references/20-context-and-skills.md", "skills/hermes-stack-uplift/references/30-router.md",
    "skills/hermes-stack-uplift/references/40-security-and-policy.md", "skills/hermes-stack-uplift/references/50-pi-and-lsp.md",
    "skills/hermes-stack-uplift/references/60-evaluation-and-promotion.md", "skills/hermes-stack-uplift/references/70-upgrades-and-rollback.md",
]

def rel(page: str, target: str) -> str:
    return "../" * len(Path(page).parent.parts) + target

def rewrite_href(href: str, page: str) -> str:
    if href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    base, *frag = href.split("#", 1); clean = base.rstrip("/")
    # Resolve repo-relative: md sources live in docs/agentic-uplift/ etc.
    src_dir = PAGES[page][1].rsplit("/", 1)[0] if "/" in PAGES[page][1] else ""
    candidates = ([f"{src_dir}/{clean}"] if src_dir else []) + [clean]
    resolved = next((c for c in candidates if c in PUBLIC_FILES), None)
    if resolved:
        target = rel(page, "raw/" + resolved)
        return target + (("#" + frag[0]) if frag else "")
    return "https://github.com/thepragmatik/hermes-pi-agentic-stack/blob/main/" + href

def inline(text: str, page: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    def link(m: re.Match[str]) -> str:
        label=m.group(1);href=html.unescape(m.group(2))
        return f'<a href="{html.escape(rewrite_href(href,page),quote=True)}">{label}</a>'
    value = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: f'<img src="{html.escape(rewrite_href(m.group(2),page),quote=True)}" alt="{html.escape(m.group(1))}">', value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value

def render_table(rows: list[str], page: str) -> str:
    """Render collected pipe-table lines as a real HTML table."""
    def cells(line: str) -> list[str]:
        s = line.strip().removeprefix("|").removesuffix("|")
        return [c.strip() for c in s.split("|")]
    header = cells(rows[0])
    body_rows = [r for r in rows[1:] if not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", r)]
    out = ['<div class="tblwrap"><table>']
    out.append("<thead><tr>" + "".join(f"<th>{inline(c,page)}</th>" for c in header) + "</tr></thead>")
    out.append("<tbody>")
    for r in body_rows:
        out.append("<tr>" + "".join(f"<td>{inline(c,page)}</td>" for c in cells(r)) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)

def render_md(text: str, page: str) -> str:
    out=[];code=[];in_code=False;list_open=False;table=[]
    def close_list():
        nonlocal list_open
        if list_open:out.append("</ul>");list_open=False
    def close_table():
        nonlocal table
        if table:out.append(render_table(table,page));table=[]
    for line in text.splitlines():
        if line.startswith("```"):
            close_list();close_table()
            if in_code:out.append("<pre><code>"+html.escape("\n".join(code))+"</code></pre>");code=[];in_code=False
            else:in_code=True
            continue
        if in_code:code.append(line);continue
        if line.startswith("|"):close_list();table.append(line);continue
        close_table()
        if not line.strip():close_list();continue
        if line.startswith("#"):
            close_list();level=min(6,len(line)-len(line.lstrip("#")));out.append(f"<h{level}>"+inline(line[level:].strip(),page)+f"</h{level}>")
        elif line.startswith("- "):
            if not list_open:out.append("<ul>");list_open=True
            out.append("<li>"+inline(line[2:].strip(),page)+"</li>")
        elif re.match(r"^\d+\. ",line):close_list();out.append("<p>"+inline(line,page)+"</p>")
        elif line.startswith("> "):close_list();out.append("<blockquote>"+inline(line[2:].strip(),page)+"</blockquote>")
        else:out.append("<p>"+inline(line,page)+"</p>")
    close_list();close_table()
    if in_code:out.append("<pre><code>"+html.escape("\n".join(code))+"</code></pre>")
    return "\n".join(out)

def nav(page: str) -> str:
    items=[("Home","index.html"),("Architecture","architecture.html"),("Fresh Install","fresh-install.html"),("Start Uplift","start-uplift.html"),("Phases","playbook.html"),("Context + Skills","skills.html"),("Routing","research/routing.html"),("OpenRouter","routing-openrouter.html"),("Pi + LSP","pi-lsp.html"),("Security","security.html"),("Adversarial","adversarial-review.html"),("Readiness","artifact-review.html"),("Validation","validation.html"),("Upgrades","upgrade-rollback.html"),("Sources","sources.html")]
    return " ".join(f'<a href="{rel(page,href)}">{html.escape(label)}</a>' for label,href in items)

def layout(title: str, body: str, page: str, raw: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="alternate" type="text/markdown" href="{rel(page,'raw/'+raw)}"><link rel="alternate" type="text/plain" href="{rel(page,'llms.txt')}"><style>body{{font:16px/1.6 ui-rounded,system-ui,-apple-system,sans-serif;max-width:1180px;margin:auto;padding:2rem;color:#2d2419;background:#fffaf3}}nav{{display:flex;gap:.75rem;flex-wrap:wrap;border-bottom:1px solid #e5d8c6;padding-bottom:1rem;margin-bottom:2rem}}a{{color:#9a5b2e}}pre{{overflow:auto;background:#f7efe2;padding:1rem;border-radius:.5rem}}code{{background:#f7efe2}}blockquote{{border-left:4px solid #d4a873;margin-left:0;padding-left:1rem}}svg{{max-width:100%;height:auto}}.tblwrap{{overflow:auto;margin:1rem 0}}table{{border-collapse:collapse;width:100%;font-size:.94em}}th{{background:#f7efe2;text-align:left;padding:.5rem .65rem;border-bottom:2px solid #d4a873}}td{{padding:.45rem .65rem;border-bottom:1px solid #e5d8c6;vertical-align:top}}tbody tr:nth-child(even){{background:#fbf5ec}}@media(prefers-color-scheme:dark){{body{{color:#e8dccf;background:#1c1917}}a{{color:#e0a370}}pre,code{{background:#29241e}}nav{{border-color:#443c33}}}}</style></head><body><nav>{nav(page)}</nav><main>{body}</main><hr><p>Canonical source: <a href="{rel(page,'raw/'+raw)}">Markdown</a> · Agent entry: <a href="{rel(page,'agent/START.md')}">START.md</a></p></body></html>'''

def svg_tiers() -> str:
    return (ROOT / "docs/agentic-uplift/diagrams/routing-tiers.svg").read_text(encoding="utf-8")

DIAGRAMS = {
    "research/routing.html": ("Five-tier routing architecture", svg_tiers),
}

def svg_arch() -> str:
    return '''<svg viewBox="0 0 1280 390" role="img" aria-labelledby="arch-title arch-desc" xmlns="http://www.w3.org/2000/svg"><title id="arch-title">Hermes Pi five-tier routing architecture</title><desc id="arch-desc">Hermes applies deterministic eligibility, multi-label mission profiling, bounded workflow selection and model optimization before an OpenRouter-first gateway selects an eligible physical provider. Coding stages cross the typed Pi boundary and all work is gated by evidence and review.</desc><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs><style>.b{fill:transparent;stroke:#5b4636;stroke-width:2}.t{font:12.5px system-ui;fill:#2d2419}.e{stroke:#5b4636;stroke-width:2;marker-end:url(#a)}@media(prefers-color-scheme:dark){.b{fill:transparent;stroke:#e8dccf}.t{fill:#e8dccf}.e{stroke:#e8dccf}}</style><rect class="b" x="10" y="160" width="90" height="55" rx="8"/><text class="t" x="55" y="192" text-anchor="middle">Hermes</text><rect class="b" x="120" y="40" width="150" height="60" rx="8"/><text class="t" x="195" y="66" text-anchor="middle">LCM + Mnemosyne</text><text class="t" x="195" y="84" text-anchor="middle">local context/memory</text><rect class="b" x="120" y="160" width="135" height="55" rx="8"/><text class="t" x="187" y="183" text-anchor="middle">Tier 0 eligibility</text><text class="t" x="187" y="201" text-anchor="middle">policy/security</text><rect class="b" x="275" y="160" width="135" height="55" rx="8"/><text class="t" x="342" y="183" text-anchor="middle">Tier 1 mission</text><text class="t" x="342" y="201" text-anchor="middle">profile</text><rect class="b" x="430" y="160" width="135" height="55" rx="8"/><text class="t" x="497" y="183" text-anchor="middle">Tier 2 workflow</text><text class="t" x="497" y="201" text-anchor="middle">+ agent</text><rect class="b" x="585" y="160" width="135" height="55" rx="8"/><text class="t" x="652" y="183" text-anchor="middle">Tier 3 model</text><text class="t" x="652" y="201" text-anchor="middle">optimization</text><rect class="b" x="740" y="160" width="120" height="55" rx="8"/><text class="t" x="800" y="183" text-anchor="middle">Tier 4 gateway</text><text class="t" x="800" y="201" text-anchor="middle">OpenRouter-first</text><rect class="b" x="890" y="55" width="135" height="55" rx="8"/><text class="t" x="957" y="79" text-anchor="middle">Research/general/</text><text class="t" x="957" y="97" text-anchor="middle">review executor</text><rect class="b" x="890" y="255" width="135" height="55" rx="8"/><text class="t" x="957" y="279" text-anchor="middle">Typed Pi worker</text><text class="t" x="957" y="297" text-anchor="middle">+ LSP/sandbox</text><rect class="b" x="1060" y="160" width="120" height="55" rx="8"/><text class="t" x="1120" y="183" text-anchor="middle">Evidence /</text><text class="t" x="1120" y="201" text-anchor="middle">review gate</text><rect class="b" x="1060" y="285" width="150" height="55" rx="8"/><text class="t" x="1135" y="309" text-anchor="middle">Outcome telemetry</text><text class="t" x="1135" y="327" text-anchor="middle">research plane</text><line class="e" x1="100" y1="175" x2="120" y2="95"/><line class="e" x1="100" y1="188" x2="120" y2="188"/><line class="e" x1="255" y1="188" x2="275" y2="188"/><line class="e" x1="410" y1="188" x2="430" y2="188"/><line class="e" x1="565" y1="188" x2="585" y2="188"/><line class="e" x1="720" y1="188" x2="740" y2="188"/><line class="e" x1="860" y1="174" x2="890" y2="100"/><line class="e" x1="860" y1="202" x2="890" y2="268"/><line class="e" x1="1025" y1="83" x2="1080" y2="160"/><line class="e" x1="1025" y1="282" x2="1080" y2="215"/><line class="e" x1="1120" y1="215" x2="1135" y2="285"/></svg>'''

def copy_public(out: Path) -> list[dict]:
    manifest=[]
    for src in PUBLIC_FILES:
        path=ROOT/src
        if not path.exists():raise SystemExit(f"missing public source: {src}")
        dst=out/"raw"/src;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dst)
        manifest.append({"path":src,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size})
    return manifest

def write_agent_surface(out: Path, manifest: list[dict]) -> None:
    agent=out/"agent";agent.mkdir()
    (agent/"START.md").write_text(
        "# Agent Start\n\nDo not ingest the whole site. Execution order:\n\n"
        "1. Read `UPLIFT_MISSION.md`.\n2. Read the execution contract and schema-valid durable uplift state.\n"
        "3. Read `skills/hermes-stack-uplift/SKILL.md`.\n4. Load only the current `00-70` phase reference.\n"
        "5. In Phase 30, use `routing-mission.schema.json` and `routing-decision.schema.json`; research/coding are task families, not a closed ontology.\n"
        "6. Fetch only research/evidence required by the current gate.\n\n"
        "Tier 0 deterministic privacy/security/capability eligibility runs before learned routing. The stack then infers a multi-label mission profile, selects a bounded workflow/agent path, optimizes an eligible model role/model, and normally delegates physical-provider execution to OpenRouter. OpenRouter Auto is never privacy/capability/final workflow authority. LCM + Mnemosyne is the required local context/memory baseline. At every phase boundary persist uplift-state/evidence, report to the human, and stop before the next phase.\n",
        encoding="utf-8")
    shutil.copy2(ROOT/"UPLIFT_MISSION.md",agent/"UPLIFT_MISSION.md")
    (agent/"manifest.json").write_text(json.dumps({
        "version":5,"generated_from":"canonical repository sources","progressive_disclosure":True,
        "phase_lifecycle":["00","10","20","30","40","50","60","70"],"default_gateway":"openrouter",
        "bootstrap_mode":"single verified OpenRouter model until Phase 30 shadow gate","context_memory_baseline":"LCM + Mnemosyne",
        "routing_contract":{"mission":"protocols/routing-mission.schema.json","decision":"protocols/routing-decision.schema.json","architecture":"five-tier eligibility/profile/workflow/model/gateway"},
        "files":manifest},indent=2)+"\n",encoding="utf-8")
    shutil.copy2(ROOT/"docs/agentic-uplift/architecture.graph.json",agent/"architecture.graph.json")
    for src in [
        "protocols/routing-mission.schema.json","protocols/routing-decision.schema.json","protocols/pi-task-envelope.schema.json","protocols/uplift-state.schema.json",
        "protocols/examples/routing-mission.example.json","protocols/examples/routing-decision.example.json","protocols/examples/pi-task-envelope.example.json","protocols/examples/uplift-state.example.json",
        "configs/policy.example.yaml","configs/models.example.yaml","configs/hermes-local-context-memory.example.yaml","configs/mnemosyne-local.example.yaml","configs/lcm-baseline.env.example"]:
        dst=agent/src;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/src,dst)
    shutil.copytree(ROOT/"skills/hermes-stack-uplift",agent/"skills/hermes-stack-uplift")

def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument("--output",default="_site");args=ap.parse_args();out=ROOT/args.output
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True);(out/"raw").mkdir();manifest=copy_public(out)
    for page,(title,src) in PAGES.items():
        body=render_md((ROOT/src).read_text(encoding="utf-8"),page)
        if page=="architecture.html":body=svg_arch()+body
        elif page in DIAGRAMS:
            marker,fn=DIAGRAMS[page]
            if marker in body: body=body.replace(f"<h1>{marker}</h1>", f"<h1>{marker}</h1>"+fn(), 1)
        dest=out/page;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(layout(title,body,page,src),encoding="utf-8")
    write_agent_surface(out,manifest)
    (out/"llms.txt").write_text(
        "# Hermes + Pi Agentic Stack\n\n> Staged local-first uplift. Deterministic eligibility precedes learned routing; OpenRouter is the default downstream gateway. Use progressive disclosure.\n\n"
        "## Execute / start\n- [Agent start](agent/START.md)\n- [Uplift mission](agent/UPLIFT_MISSION.md)\n- [Fresh install manual](raw/docs/agentic-uplift/fresh-install-bootstrap.md)\n- [Execution contract](raw/docs/agentic-uplift/agent-execution-contract.md)\n- [00-70 playbook](raw/docs/agentic-uplift/implementation-playbook.md)\n- [Sliced uplift skill](agent/skills/hermes-stack-uplift/SKILL.md)\n- [Uplift state](agent/protocols/uplift-state.schema.json)\n\n"
        "## Routing contracts / architecture\n- [Mission routing architecture](raw/docs/agentic-uplift/research/local-routing-models.md)\n- [Routing mission schema](agent/protocols/routing-mission.schema.json)\n- [Routing decision schema](agent/protocols/routing-decision.schema.json)\n- [Routing mission example](agent/protocols/examples/routing-mission.example.json)\n- [Routing decision example](agent/protocols/examples/routing-decision.example.json)\n- [Router training / ModernBERT](raw/docs/agentic-uplift/research/router-training-control.md)\n- [OpenRouter gateway](raw/docs/agentic-uplift/research/openrouter-routing.md)\n- [Model roles](agent/configs/models.example.yaml)\n- [Router bake-off](raw/tools/router-bench/README.md)\n\n"
        "## Context / security / gates\n- [LCM + Mnemosyne setup](raw/docs/agentic-uplift/local-context-memory-setup.md)\n- [Skill slicing](raw/docs/agentic-uplift/research/skill-slimming-slicing.md)\n- [Mission context](raw/docs/agentic-uplift/research/mission-context-architecture.md)\n- [Legacy state curation](raw/docs/agentic-uplift/research/legacy-state-curation.md)\n- [Security](raw/docs/agentic-uplift/research/security-zero-trust-pii.md)\n- [Adversarial review](raw/docs/agentic-uplift/adversarial-review.md)\n- [Readiness](raw/docs/agentic-uplift/artifact-usability-review.md)\n- [Validation](raw/docs/agentic-uplift/validation-report.md)\n",
        encoding="utf-8")
    (out/"agents.txt").write_text("Start at /llms.txt then /agent/START.md. Do not ingest the whole site. Execute one persisted 00-70 phase at a time. Tier-0 deterministic eligibility precedes mission-profile/workflow/model routing; OpenRouter is downstream physical-provider execution.\n",encoding="utf-8")
    (out/"robots.txt").write_text("User-agent: *\nAllow: /\n",encoding="utf-8");(out/".nojekyll").write_text("",encoding="utf-8")
    urls=["https://thepragmatik.github.io/hermes-pi-agentic-stack/"+p for p in PAGES]
    (out/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"\n".join(f"<url><loc>{html.escape(u)}</loc></url>" for u in urls)+"\n</urlset>\n",encoding="utf-8")
    print(f"Built {len(PAGES)} human pages + agent surface")

if __name__=="__main__":main()
