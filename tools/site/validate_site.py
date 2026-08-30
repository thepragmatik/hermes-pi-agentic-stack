#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json

PHASES = [
    "00-preflight",
    "10-baseline-and-backup",
    "20-context-and-skills",
    "30-router",
    "40-security-and-policy",
    "50-pi-and-lsp",
    "60-evaluation-and-promotion",
    "70-upgrades-and-rollback",
]

REQUIRED = [
    "index.html","architecture.html","fresh-install.html","start-uplift.html","playbook.html",
    "execution-contract.html","bootstrap.html","context-memory-setup.html","skills.html",
    "routing-openrouter.html","pi-lsp.html","security.html","adversarial-review.html",
    "artifact-review.html","validation.html","upgrade-rollback.html","publishing.html","sources.html",
    "llms.txt","agents.txt","agent/START.md","agent/UPLIFT_MISSION.md","agent/manifest.json",
    "agent/architecture.graph.json","agent/protocols/pi-task-envelope.schema.json",
    "agent/protocols/uplift-state.schema.json","agent/protocols/examples/pi-task-envelope.example.json",
    "agent/protocols/examples/uplift-state.example.json","agent/configs/models.example.yaml",
    "agent/configs/hermes-local-context-memory.example.yaml","agent/configs/lcm-baseline.env.example",
    "agent/configs/mnemosyne-local.example.yaml","raw/UPLIFT_MISSION.md",
    "raw/docs/agentic-uplift/fresh-install-bootstrap.md","raw/docs/agentic-uplift/research/openrouter-routing.md",
]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.alts=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == "a" and "href" in a: self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "alternate": self.alts.append((a.get("type"), a.get("href")))

def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--site", default="_site"); args=ap.parse_args()
    root=Path(args.site); errors=[]

    for r in REQUIRED:
        if not (root/r).exists(): errors.append(f"missing {r}")

    html_pages=list(root.rglob("*.html"))
    if len(html_pages) != 26:
        errors.append(f"expected 26 HTML pages, found {len(html_pages)}")

    for p in html_pages:
        h=Links(); h.feed(p.read_text(encoding="utf-8"))
        if not any(t == "text/markdown" for t,_ in h.alts): errors.append(f"{p}: no markdown alternate")
        if not any(t == "text/plain" for t,_ in h.alts): errors.append(f"{p}: no llms.txt alternate")
        for href in h.links:
            if href.startswith(("http://","https://","#","mailto:")): continue
            part=href.split("#",1)[0]
            if part and not (p.parent/part).resolve().exists(): errors.append(f"{p}: broken {href}")

    arch=(root/"architecture.html").read_text(encoding="utf-8") if (root/"architecture.html").exists() else ""
    if '<title id="arch-title">' not in arch or '<desc id="arch-desc">' not in arch:
        errors.append("architecture SVG lacks title/desc")
    for token in ["OpenRouter","Model-role","Deterministic policy"]:
        if token not in arch: errors.append(f"architecture missing {token}")

    llms=(root/"llms.txt").read_text(encoding="utf-8") if (root/"llms.txt").exists() else ""
    for token in ["OpenRouter","agent/UPLIFT_MISSION.md","fresh-install-bootstrap.md","openrouter-routing.md"]:
        if token not in llms: errors.append(f"llms.txt missing {token}")

    start=(root/"agent/START.md").read_text(encoding="utf-8") if (root/"agent/START.md").exists() else ""
    for token in ["UPLIFT_MISSION.md","OpenRouter","current `00-70` phase reference","stop before the next phase"]:
        if token not in start: errors.append(f"agent/START.md missing {token}")

    manifest=load_json(root/"agent/manifest.json", errors)
    if manifest.get("version") != 4: errors.append("agent manifest version must be 4")
    if manifest.get("default_gateway") != "openrouter": errors.append("agent manifest default gateway is not openrouter")
    if manifest.get("context_memory_baseline") != "LCM + Mnemosyne": errors.append("agent manifest context/memory baseline mismatch")
    if manifest.get("phase_lifecycle") != ["00","10","20","30","40","50","60","70"]: errors.append("agent manifest phase lifecycle mismatch")
    files=manifest.get("files") or []
    if not files: errors.append("empty agent manifest")
    for item in files:
        rel=item.get("path")
        if not rel: errors.append("manifest item missing path"); continue
        raw=root/"raw"/rel
        if not raw.exists(): errors.append(f"manifest raw file missing: {rel}"); continue
        digest=hashlib.sha256(raw.read_bytes()).hexdigest()
        if digest != item.get("sha256"): errors.append(f"manifest hash mismatch: {rel}")
        if raw.stat().st_size != item.get("bytes"): errors.append(f"manifest byte count mismatch: {rel}")

    graph=load_json(root/"agent/architecture.graph.json", errors)
    node_ids={n.get("id") for n in graph.get("nodes", [])}
    for node in ["policy","router","model_role","openrouter","physical_provider","pi_bridge","state"]:
        if node not in node_ids: errors.append(f"architecture graph missing node {node}")

    pi_schema=load_json(root/"agent/protocols/pi-task-envelope.schema.json", errors)
    pi_example=load_json(root/"agent/protocols/examples/pi-task-envelope.example.json", errors)
    if pi_schema.get("properties",{}).get("version",{}).get("const") != "2.1": errors.append("Pi schema version must be 2.1")
    if pi_schema.get("properties",{}).get("phase",{}).get("enum") != PHASES: errors.append("Pi schema phase lifecycle mismatch")
    if "model_role" not in pi_schema.get("required",[]): errors.append("Pi schema does not require model_role")
    if len(pi_schema.get("allOf",[])) < 2: errors.append("Pi schema missing conditional safety constraints")
    for key in pi_schema.get("required",[]):
        if key not in pi_example: errors.append(f"Pi example missing required key {key}")
    if pi_example.get("version") != "2.1": errors.append("Pi example version mismatch")
    if pi_example.get("phase") != "50-pi-and-lsp": errors.append("Pi example must demonstrate Phase 50 worker activation")
    if pi_example.get("model_role") != "coding.default": errors.append("Pi example model_role mismatch")

    uplift_schema=load_json(root/"agent/protocols/uplift-state.schema.json", errors)
    uplift_example=load_json(root/"agent/protocols/examples/uplift-state.example.json", errors)
    if uplift_schema.get("properties",{}).get("version",{}).get("const") != "1.1": errors.append("uplift-state schema version must be 1.1")
    if uplift_schema.get("$defs",{}).get("phaseId",{}).get("enum") != PHASES: errors.append("uplift-state phase lifecycle mismatch")
    if uplift_example.get("version") != "1.1": errors.append("uplift-state example version mismatch")
    if [p.get("id") for p in uplift_example.get("phases",[])] != PHASES: errors.append("uplift-state example phases mismatch")
    if uplift_example.get("runtime",{}).get("gateway") != "openrouter": errors.append("uplift-state example gateway mismatch")

    for src in [
        "UPLIFT_MISSION.md",
        "protocols/pi-task-envelope.schema.json",
        "protocols/uplift-state.schema.json",
        "protocols/examples/pi-task-envelope.example.json",
        "protocols/examples/uplift-state.example.json",
        "configs/models.example.yaml",
        "configs/hermes-local-context-memory.example.yaml",
        "configs/lcm-baseline.env.example",
        "configs/mnemosyne-local.example.yaml",
    ]:
        agent=root/"agent"/src
        raw=root/"raw"/src
        if agent.exists() and raw.exists() and agent.read_bytes() != raw.read_bytes(): errors.append(f"agent/raw copy mismatch: {src}")

    if errors: raise SystemExit("\n".join(errors))
    print("OK: validated 26 HTML pages, progressive-disclosure agent surface, hashed raw manifest, OpenRouter architecture, and 00-70 lifecycle contracts")

if __name__ == "__main__": main()
