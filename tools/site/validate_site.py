#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
PHASES=["00-preflight","10-baseline-and-backup","20-context-and-skills","30-router","40-security-and-policy","50-pi-and-lsp","60-evaluation-and-promotion","70-upgrades-and-rollback"]
TASKS={"research","synthesis","architecture_design","planning_decomposition","coding_implementation","debugging_diagnosis","refactoring","testing","code_review","security_review","devops_configuration","data_analysis","document_generation_transformation","retrieval_memory","agent_supervision_orchestration","long_running_tool_execution","multimodal_analysis","verification_fact_check","other"}
REQUIRED=[
 "index.html","architecture.html","fresh-install.html","start-uplift.html","playbook.html","execution-contract.html","bootstrap.html","context-memory-setup.html","skills.html","routing-openrouter.html","research/routing.html","research/router-training.html","pi-lsp.html","security.html","adversarial-review.html","artifact-review.html","validation.html","upgrade-rollback.html","publishing.html","sources.html",
 "llms.txt","agents.txt","agent/START.md","agent/UPLIFT_MISSION.md","agent/manifest.json","agent/architecture.graph.json",
 "agent/protocols/routing-mission.schema.json","agent/protocols/routing-decision.schema.json","agent/protocols/pi-task-envelope.schema.json","agent/protocols/uplift-state.schema.json",
 "agent/protocols/examples/routing-mission.example.json","agent/protocols/examples/routing-decision.example.json","agent/protocols/examples/pi-task-envelope.example.json","agent/protocols/examples/uplift-state.example.json",
 "agent/configs/models.example.yaml","agent/configs/hermes-local-context-memory.example.yaml","agent/configs/lcm-baseline.env.example","agent/configs/mnemosyne-local.example.yaml",
 "raw/UPLIFT_MISSION.md","raw/docs/agentic-uplift/fresh-install-bootstrap.md","raw/docs/agentic-uplift/research/local-routing-models.md","raw/docs/agentic-uplift/research/openrouter-routing.md","raw/tools/router-bench/README.md","raw/tools/router-bench/sample_missions.jsonl"
]

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.alts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="a" and "href" in a:self.links.append(a["href"])
        if tag=="link" and a.get("rel")=="alternate":self.alts.append((a.get("type"),a.get("href")))

def load_json(path,errors):
    try:return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:errors.append(f"{path}: invalid JSON: {exc}");return {}

def router_smoke(errors):
    cmd=[sys.executable,str(ROOT/"tools/router-bench/router_bench.py"),"--dataset",str(ROOT/"tools/router-bench/sample_missions.jsonl"),"--routers","rules","--repeat","3","--fail-on-hard-violations"]
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:
        errors.append("router smoke failed: "+(p.stderr[-1000:] or p.stdout[-1000:]))
        return None
    try:doc=json.loads(p.stdout)
    except Exception as exc:errors.append(f"router smoke invalid JSON: {exc}");return None
    result=(doc.get("results") or [{}])[0];m=result.get("metrics",{});hard=m.get("hard_constraint_violations",{})
    if sum(hard.values())!=0:errors.append(f"router smoke hard violations: {hard}")
    if m.get("determinism_rate")!=1.0:errors.append("router smoke is not deterministic")
    return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--site",default="_site");args=ap.parse_args();root=Path(args.site);errors=[]
    for r in REQUIRED:
        if not (root/r).exists():errors.append(f"missing {r}")
    html_pages=list(root.rglob("*.html"))
    if len(html_pages)!=26:errors.append(f"expected 26 HTML pages, found {len(html_pages)}")
    for p in html_pages:
        h=Links();h.feed(p.read_text(encoding="utf-8"))
        if not any(t=="text/markdown" for t,_ in h.alts):errors.append(f"{p}: no markdown alternate")
        if not any(t=="text/plain" for t,_ in h.alts):errors.append(f"{p}: no llms.txt alternate")
        for href in h.links:
            if href.startswith(("http://","https://","#","mailto:")):continue
            part=href.split("#",1)[0]
            if part and not (p.parent/part).resolve().exists():errors.append(f"{p}: broken {href}")

    arch=(root/"architecture.html").read_text(encoding="utf-8") if (root/"architecture.html").exists() else ""
    if '<title id="arch-title">' not in arch or '<desc id="arch-desc">' not in arch:errors.append("architecture SVG lacks title/desc")
    for token in ["Tier 0 eligibility","Tier 1 mission","Tier 2 workflow","Tier 3 model","Tier 4 gateway","OpenRouter"]:
        if token not in arch:errors.append(f"architecture missing {token}")

    llms=(root/"llms.txt").read_text(encoding="utf-8") if (root/"llms.txt").exists() else ""
    for token in ["agent/UPLIFT_MISSION.md","routing-mission.schema.json","routing-decision.schema.json","local-routing-models.md","openrouter-routing.md","Router bake-off"]:
        if token not in llms:errors.append(f"llms.txt missing {token}")
    start=(root/"agent/START.md").read_text(encoding="utf-8") if (root/"agent/START.md").exists() else ""
    for token in ["UPLIFT_MISSION.md","routing-mission.schema.json","multi-label mission profile","OpenRouter","phase boundary"]:
        if token not in start:errors.append(f"agent/START.md missing {token}")

    manifest=load_json(root/"agent/manifest.json",errors)
    if manifest.get("version")!=5:errors.append("agent manifest version must be 5")
    if manifest.get("default_gateway")!="openrouter":errors.append("agent manifest default gateway is not openrouter")
    if manifest.get("context_memory_baseline")!="LCM + Mnemosyne":errors.append("agent manifest context/memory baseline mismatch")
    if manifest.get("phase_lifecycle")!=["00","10","20","30","40","50","60","70"]:errors.append("agent manifest phase lifecycle mismatch")
    rc=manifest.get("routing_contract",{})
    if rc.get("mission")!="protocols/routing-mission.schema.json" or rc.get("decision")!="protocols/routing-decision.schema.json":errors.append("agent manifest routing contract mismatch")
    files=manifest.get("files") or []
    if not files:errors.append("empty agent manifest")
    for item in files:
        rel=item.get("path")
        if not rel:errors.append("manifest item missing path");continue
        raw=root/"raw"/rel
        if not raw.exists():errors.append(f"manifest raw file missing: {rel}");continue
        if hashlib.sha256(raw.read_bytes()).hexdigest()!=item.get("sha256"):errors.append(f"manifest hash mismatch: {rel}")
        if raw.stat().st_size!=item.get("bytes"):errors.append(f"manifest byte count mismatch: {rel}")

    graph=load_json(root/"agent/architecture.graph.json",errors);nodes={n.get("id") for n in graph.get("nodes",[])}
    for node in ["eligibility","mission_profile","workflow_selector","model_optimizer","gateway_adapter","openrouter","physical_provider","pi_bridge","outcome_telemetry","research_plane","state"]:
        if node not in nodes:errors.append(f"architecture graph missing node {node}")
    if graph.get("version")!=3:errors.append("architecture graph version must be 3")

    mission_schema=load_json(root/"agent/protocols/routing-mission.schema.json",errors)
    decision_schema=load_json(root/"agent/protocols/routing-decision.schema.json",errors)
    mission_example=load_json(root/"agent/protocols/examples/routing-mission.example.json",errors)
    decision_example=load_json(root/"agent/protocols/examples/routing-decision.example.json",errors)
    if mission_schema.get("properties",{}).get("version",{}).get("const")!="1.0":errors.append("routing mission schema version mismatch")
    task_enum=set(mission_schema.get("$defs",{}).get("taskFamily",{}).get("enum",[]))
    if task_enum!=TASKS:errors.append("routing mission task-family vocabulary mismatch")
    if decision_schema.get("properties",{}).get("version",{}).get("const")!="1.0":errors.append("routing decision schema version mismatch")
    if set(mission_example.get("mission_profile",{}).get("tasks",[]))-TASKS:errors.append("routing mission example has unknown tasks")
    if decision_example.get("execution",{}).get("workflow")!="multi_stage":errors.append("routing decision example must demonstrate multi-stage workflow")
    if "routing" not in (root/"raw/docs/agentic-uplift/research/local-routing-models.md").read_text(encoding="utf-8").lower():errors.append("routing research raw missing")

    pi_schema=load_json(root/"agent/protocols/pi-task-envelope.schema.json",errors);pi_example=load_json(root/"agent/protocols/examples/pi-task-envelope.example.json",errors)
    if pi_schema.get("properties",{}).get("version",{}).get("const")!="2.2":errors.append("Pi schema version must be 2.2")
    if pi_schema.get("properties",{}).get("phase",{}).get("enum")!=PHASES:errors.append("Pi schema phase lifecycle mismatch")
    for key in ["model_role","routing"]:
        if key not in pi_schema.get("required",[]):errors.append(f"Pi schema does not require {key}")
    for key in pi_schema.get("required",[]):
        if key not in pi_example:errors.append(f"Pi example missing required key {key}")
    if pi_example.get("version")!="2.2":errors.append("Pi example version mismatch")
    if pi_example.get("phase")!="50-pi-and-lsp" or pi_example.get("model_role")!="coding.default":errors.append("Pi example phase/model role mismatch")
    if not pi_example.get("routing",{}).get("stage_id"):errors.append("Pi example lacks routing stage traceability")

    uplift_schema=load_json(root/"agent/protocols/uplift-state.schema.json",errors);uplift_example=load_json(root/"agent/protocols/examples/uplift-state.example.json",errors)
    if uplift_schema.get("properties",{}).get("version",{}).get("const")!="1.1":errors.append("uplift-state schema version must be 1.1")
    if uplift_schema.get("$defs",{}).get("phaseId",{}).get("enum")!=PHASES:errors.append("uplift-state phase lifecycle mismatch")
    if uplift_example.get("version")!="1.1" or [p.get("id") for p in uplift_example.get("phases",[])]!=PHASES:errors.append("uplift-state example mismatch")
    if uplift_example.get("runtime",{}).get("gateway")!="openrouter":errors.append("uplift-state example gateway mismatch")

    for src in ["UPLIFT_MISSION.md","protocols/routing-mission.schema.json","protocols/routing-decision.schema.json","protocols/pi-task-envelope.schema.json","protocols/uplift-state.schema.json","protocols/examples/routing-mission.example.json","protocols/examples/routing-decision.example.json","protocols/examples/pi-task-envelope.example.json","protocols/examples/uplift-state.example.json","configs/models.example.yaml","configs/hermes-local-context-memory.example.yaml","configs/lcm-baseline.env.example","configs/mnemosyne-local.example.yaml"]:
        agent=root/"agent"/src;raw=root/"raw"/src
        if agent.exists() and raw.exists() and agent.read_bytes()!=raw.read_bytes():errors.append(f"agent/raw copy mismatch: {src}")

    smoke=router_smoke(errors)
    if errors:raise SystemExit("\n".join(errors))
    summary=""
    if smoke:summary=f", rules smoke task-micro-F1={smoke['task_family']['micro_f1']:.3f}, workflow={smoke['workflow_accuracy']:.3f}, hard=0"
    print("OK: validated 26 HTML pages, routing contracts, progressive-disclosure agent surface, hashed raw manifest, five-tier OpenRouter architecture, Pi routing traceability, 00-70 lifecycle"+summary)

if __name__=="__main__":main()
