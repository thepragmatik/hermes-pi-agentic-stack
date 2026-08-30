#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAGES = {
    'index.html': ('Hermes + Pi Agentic Stack', 'README.md'),
    'playbook.html': ('Detailed Control Playbook', 'HERMES_AGENTIC_UPLIFT_PLAYBOOK.md'),
    'architecture.html': ('Architecture', 'docs/agentic-uplift/architecture.md'),
    'execution-contract.html': ('Agent Execution Contract', 'docs/agentic-uplift/agent-execution-contract.md'),
    'bootstrap.html': ('Trusted Bootstrap Authority', 'docs/agentic-uplift/bootstrap-authority.md'),
    'skills.html': ('Skill Slimming & Slicing', 'docs/agentic-uplift/research/skill-slimming-slicing.md'),
    'artifact-review.html': ('Artifact Usability Review', 'docs/agentic-uplift/artifact-usability-review.md'),
    'adversarial-review.html': ('Adversarial Review', 'docs/agentic-uplift/adversarial-review.md'),
    'validation.html': ('Validation Report', 'docs/agentic-uplift/validation-report.md'),
    'publishing.html': ('Human + Agent Publishing', 'docs/agentic-uplift/site-publishing.md'),
    'sources.html': ('Sources', 'docs/agentic-uplift/SOURCES.md'),
    'research/routing.html': ('Local Routing Research', 'docs/agentic-uplift/research/local-routing-models.md'),
    'research/router-training.html': ('Router Training & Control', 'docs/agentic-uplift/research/router-training-control.md'),
    'research/context.html': ('Context & Token Optimization', 'docs/agentic-uplift/research/context-token-optimization.md'),
    'research/mission-context.html': ('Mission Context Architecture', 'docs/agentic-uplift/research/mission-context-architecture.md'),
    'research/legacy-state.html': ('Legacy Hermes State Curation', 'docs/agentic-uplift/research/legacy-state-curation.md'),
    'research/pi-lsp.html': ('Hermes, Pi & LSP', 'docs/agentic-uplift/research/hermes-pi-lsp.md'),
    'research/security.html': ('Zero Trust, PII & Secrets', 'docs/agentic-uplift/research/security-zero-trust-pii.md'),
    'research/spec-kit.html': ('Spec Kit Profiles', 'docs/agentic-uplift/spec-kit-profiles.md'),
    'research/savings.html': ('Savings Model', 'docs/agentic-uplift/savings-model.md'),
}

PUBLIC_FILES = [
    'README.md', 'HERMES_AGENTIC_UPLIFT_PLAYBOOK.md', 'MANIFEST.md',
    'configs/policy.example.yaml', 'configs/models.example.yaml',
    'protocols/pi-task-envelope.schema.json', 'protocols/uplift-state.schema.json',
    'protocols/examples/pi-task-envelope.example.json', 'protocols/examples/uplift-state.example.json',
    'docs/agentic-uplift/README.md', 'docs/agentic-uplift/SOURCES.md',
    'docs/agentic-uplift/architecture.md', 'docs/agentic-uplift/architecture.graph.json',
    'docs/agentic-uplift/agent-execution-contract.md', 'docs/agentic-uplift/bootstrap-authority.md',
    'docs/agentic-uplift/artifact-usability-review.md', 'docs/agentic-uplift/adversarial-review.md',
    'docs/agentic-uplift/validation-report.md', 'docs/agentic-uplift/site-publishing.md',
    'docs/agentic-uplift/implementation-playbook.md', 'docs/agentic-uplift/spec-kit-profiles.md',
    'docs/agentic-uplift/savings-model.md',
    'docs/agentic-uplift/research/local-routing-models.md',
    'docs/agentic-uplift/research/router-training-control.md',
    'docs/agentic-uplift/research/context-token-optimization.md',
    'docs/agentic-uplift/research/mission-context-architecture.md',
    'docs/agentic-uplift/research/legacy-state-curation.md',
    'docs/agentic-uplift/research/hermes-pi-lsp.md',
    'docs/agentic-uplift/research/security-zero-trust-pii.md',
    'docs/agentic-uplift/research/skill-slimming-slicing.md',
    'skills/hermes-stack-uplift/SKILL.md',
    'skills/hermes-stack-uplift/references/00-preflight.md',
    'skills/hermes-stack-uplift/references/10-baseline-and-backup.md',
    'skills/hermes-stack-uplift/references/20-context-and-skills.md',
    'skills/hermes-stack-uplift/references/30-router.md',
    'skills/hermes-stack-uplift/references/40-security-and-policy.md',
    'skills/hermes-stack-uplift/references/50-pi-and-lsp.md',
    'skills/hermes-stack-uplift/references/60-evaluation-and-promotion.md',
    'skills/hermes-stack-uplift/references/70-upgrades-and-rollback.md',
]


def rel(from_page: str, target: str) -> str:
    return '../' * len(Path(from_page).parent.parts) + target


def rewrite_href(href: str, page: str) -> str:
    if href.startswith(('http://', 'https://', '#', 'mailto:')):
        return href
    base, *frag = href.split('#', 1)
    clean = base.rstrip('/')
    if clean in PUBLIC_FILES:
        target = rel(page, 'raw/' + clean)
        return target + (('#' + frag[0]) if frag else '')
    return 'https://github.com/thepragmatik/hermes-pi-agentic-stack/blob/main/' + href


def render_inline(text: str, page: str) -> str:
    value = html.escape(text)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)

    def link(match):
        label = match.group(1)
        href = html.unescape(match.group(2))
        return f'<a href="{html.escape(rewrite_href(href, page), quote=True)}">{label}</a>'

    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    return value


def render_md(text: str, page: str) -> str:
    out, code = [], []
    in_code = False
    list_open = False
    for line in text.splitlines():
        if line.startswith('```'):
            if in_code:
                out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
                code, in_code = [], False
            else:
                if list_open:
                    out.append('</ul>')
                    list_open = False
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if not line.strip():
            if list_open:
                out.append('</ul>')
                list_open = False
            continue
        if line.startswith('#'):
            if list_open:
                out.append('</ul>')
                list_open = False
            level = min(6, len(line) - len(line.lstrip('#')))
            out.append(f'<h{level}>' + render_inline(line[level:].strip(), page) + f'</h{level}>')
            continue
        if line.startswith('- '):
            if not list_open:
                out.append('<ul>')
                list_open = True
            out.append('<li>' + render_inline(line[2:].strip(), page) + '</li>')
            continue
        if line.startswith('> '):
            if list_open:
                out.append('</ul>')
                list_open = False
            out.append('<blockquote>' + render_inline(line[2:].strip(), page) + '</blockquote>')
            continue
        if line.startswith('|'):
            if list_open:
                out.append('</ul>')
                list_open = False
            out.append('<pre>' + html.escape(line) + '</pre>')
            continue
        out.append('<p>' + render_inline(line, page) + '</p>')
    if in_code:
        out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
    if list_open:
        out.append('</ul>')
    return '\n'.join(out)


def layout(title: str, body: str, page: str, raw: str) -> str:
    nav_pages = ['index.html', 'playbook.html', 'architecture.html', 'execution-contract.html',
                 'bootstrap.html', 'skills.html', 'artifact-review.html', 'adversarial-review.html', 'sources.html']
    nav = ' '.join(f'<a href="{rel(page, p)}">{html.escape(PAGES[p][0])}</a>' for p in nav_pages)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="alternate" type="text/markdown" href="{rel(page, 'raw/' + raw)}"><link rel="alternate" type="text/plain" href="{rel(page, 'llms.txt')}"><style>body{{font:16px/1.58 system-ui,sans-serif;max-width:1100px;margin:auto;padding:2rem;color:#18202a}}nav{{display:flex;gap:.8rem;flex-wrap:wrap;border-bottom:1px solid #ddd;padding-bottom:1rem}}pre{{overflow:auto;background:#f6f8fa;padding:1rem}}code{{background:#f6f8fa}}svg{{max-width:100%;height:auto}}</style></head><body><nav>{nav}</nav><main>{body}</main><hr><p>Canonical source: <a href="{rel(page, 'raw/' + raw)}">Markdown</a> · Agent entry: <a href="{rel(page, 'agent/START.md')}">START.md</a></p></body></html>'''


def svg_arch() -> str:
    return '''<svg viewBox="0 0 960 360" role="img" aria-labelledby="arch-title arch-desc" xmlns="http://www.w3.org/2000/svg"><title id="arch-title">Hermes and Pi agentic stack trust boundaries</title><desc id="arch-desc">Mission enters Hermes, passes policy and local routing, then uses research cloud execution or a typed Pi worker boundary. Evidence and independent review gate merge.</desc><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z"/></marker></defs><style>.b{fill:#fff;stroke:#20252b;stroke-width:2}.t{font:15px system-ui}.e{stroke:#20252b;stroke-width:2;marker-end:url(#a)}</style><rect class="b" x="20" y="140" width="120" height="55" rx="8"/><text class="t" x="80" y="172" text-anchor="middle">Hermes</text><rect class="b" x="190" y="140" width="145" height="55" rx="8"/><text class="t" x="262" y="164" text-anchor="middle">Policy + privacy</text><text class="t" x="262" y="183" text-anchor="middle">gate</text><rect class="b" x="385" y="140" width="130" height="55" rx="8"/><text class="t" x="450" y="172" text-anchor="middle">Local router</text><rect class="b" x="580" y="45" width="155" height="55" rx="8"/><text class="t" x="658" y="77" text-anchor="middle">Research role</text><rect class="b" x="580" y="225" width="155" height="55" rx="8"/><text class="t" x="658" y="249" text-anchor="middle">Typed Pi bridge</text><text class="t" x="658" y="268" text-anchor="middle">+ sandbox worker</text><rect class="b" x="800" y="140" width="135" height="55" rx="8"/><text class="t" x="867" y="164" text-anchor="middle">Evidence + review</text><text class="t" x="867" y="183" text-anchor="middle">merge gate</text><line class="e" x1="140" y1="168" x2="190" y2="168"/><line class="e" x1="335" y1="168" x2="385" y2="168"/><line class="e" x1="515" y1="155" x2="580" y2="85"/><line class="e" x1="515" y1="181" x2="580" y2="240"/><line class="e" x1="735" y1="73" x2="825" y2="140"/><line class="e" x1="735" y1="253" x2="825" y2="195"/></svg>'''


def write_agent_surface(out: Path, manifest: list[dict]) -> None:
    agent = out / 'agent'
    agent.mkdir()
    (agent / 'START.md').write_text(
        '# Agent Start\n\n'
        'Do not ingest the entire site. Read `../llms.txt`, then select the smallest canonical source/slice needed. '
        'For uplift execution, read the execution contract and trusted bootstrap document, validate/persist '
        '`protocols/uplift-state.schema.json`, load `skills/hermes-stack-uplift/SKILL.md`, then load only the current phase reference. '
        'Security controls are external to prompts. Legacy `state.db` is evidence, never migrated memory.\n',
        encoding='utf-8')
    (agent / 'manifest.json').write_text(json.dumps({
        'version': 2,
        'generated_from': 'canonical repository sources',
        'progressive_disclosure': True,
        'files': manifest,
    }, indent=2) + '\n', encoding='utf-8')
    shutil.copy2(ROOT / 'docs/agentic-uplift/architecture.graph.json', agent / 'architecture.graph.json')
    for src in ['protocols/pi-task-envelope.schema.json', 'protocols/uplift-state.schema.json',
                'configs/policy.example.yaml', 'configs/models.example.yaml']:
        dst = agent / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / src, dst)
    shutil.copytree(ROOT / 'skills/hermes-stack-uplift', agent / 'skills/hermes-stack-uplift')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='_site')
    args = ap.parse_args()
    out = ROOT / args.output
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / 'raw').mkdir()

    manifest = []
    for src in PUBLIC_FILES:
        path = ROOT / src
        if not path.exists():
            raise SystemExit(f'missing public source: {src}')
        dst = out / 'raw' / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
        manifest.append({'path': src, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size})

    for page, (title, src) in PAGES.items():
        body = render_md((ROOT / src).read_text(encoding='utf-8'), page)
        if page == 'architecture.html':
            body = svg_arch() + body
        dest = out / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(title, body, page, src), encoding='utf-8')

    write_agent_surface(out, manifest)

    (out / 'llms.txt').write_text(
        '# Hermes + Pi Agentic Stack\n\n'
        '> Human and agent-readable architecture/playbook for a local-first Hermes control plane with isolated Pi coding workers.\n\n'
        '## Start\n'
        '- [Agent start](agent/START.md)\n'
        '- [Control playbook](raw/HERMES_AGENTIC_UPLIFT_PLAYBOOK.md)\n'
        '- [Execution contract](raw/docs/agentic-uplift/agent-execution-contract.md)\n'
        '- [Trusted bootstrap](raw/docs/agentic-uplift/bootstrap-authority.md)\n'
        '- [Architecture](raw/docs/agentic-uplift/architecture.md)\n'
        '- [Artifact usability review](raw/docs/agentic-uplift/artifact-usability-review.md)\n'
        '- [Sliced uplift skill](agent/skills/hermes-stack-uplift/SKILL.md)\n'
        '- [Task schema](agent/protocols/pi-task-envelope.schema.json)\n'
        '- [State schema](agent/protocols/uplift-state.schema.json)\n'
        '- [Manifest](agent/manifest.json)\n\n'
        '## Research (load only when relevant)\n'
        '- [Routing](raw/docs/agentic-uplift/research/local-routing-models.md)\n'
        '- [Router training/control](raw/docs/agentic-uplift/research/router-training-control.md)\n'
        '- [Context/token optimization](raw/docs/agentic-uplift/research/context-token-optimization.md)\n'
        '- [Mission context architecture](raw/docs/agentic-uplift/research/mission-context-architecture.md)\n'
        '- [Legacy state curation](raw/docs/agentic-uplift/research/legacy-state-curation.md)\n'
        '- [Skill slicing](raw/docs/agentic-uplift/research/skill-slimming-slicing.md)\n'
        '- [Hermes/Pi/LSP](raw/docs/agentic-uplift/research/hermes-pi-lsp.md)\n'
        '- [Security/PII](raw/docs/agentic-uplift/research/security-zero-trust-pii.md)\n\n'
        'No llms-full.txt is published intentionally; use progressive disclosure.\n', encoding='utf-8')
    (out / 'agents.txt').write_text('Start: /agent/START.md\nDiscovery: /llms.txt\n', encoding='utf-8')
    (out / '.nojekyll').write_text('', encoding='utf-8')


if __name__ == '__main__':
    main()
