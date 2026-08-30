#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import argparse, json
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.alts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='alternate': self.alts.append((a.get('type'),a.get('href')))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--site',default='_site'); args=ap.parse_args(); root=Path(args.site); errors=[]
    required=['index.html','playbook.html','architecture.html','execution-contract.html','skills.html','artifact-review.html','adversarial-review.html','validation.html','publishing.html','sources.html','llms.txt','agent/START.md','agent/manifest.json','agent/architecture.graph.json','agent/protocols/pi-task-envelope.schema.json','agent/protocols/uplift-state.schema.json']
    for r in required:
        if not (root/r).exists(): errors.append(f'missing {r}')
    for p in root.rglob('*.html'):
        h=Links(); h.feed(p.read_text(encoding='utf-8'))
        if not any(t=='text/markdown' for t,_ in h.alts): errors.append(f'{p}: no markdown alternate')
        if not any(t=='text/plain' for t,_ in h.alts): errors.append(f'{p}: no llms.txt alternate')
        for href in h.links:
            if href.startswith(('http://','https://','#','mailto:')): continue
            part=href.split('#',1)[0]
            if part and not (p.parent/part).resolve().exists(): errors.append(f'{p}: broken {href}')
    arch=(root/'architecture.html').read_text(encoding='utf-8')
    if '<title id="arch-title">' not in arch or '<desc id="arch-desc">' not in arch: errors.append('architecture SVG lacks title/desc')
    manifest=json.loads((root/'agent/manifest.json').read_text())
    if not manifest.get('files'): errors.append('empty agent manifest')
    for jf in ['agent/manifest.json','agent/architecture.graph.json','agent/protocols/pi-task-envelope.schema.json','agent/protocols/uplift-state.schema.json']:
        json.loads((root/jf).read_text())
    if errors: raise SystemExit('\n'.join(errors))
    print(f'OK: validated {sum(1 for _ in root.rglob("*.html"))} HTML pages and agent endpoints')
if __name__=='__main__': main()
