#!/usr/bin/env python3
"""Framework-neutral router bake-off for the Hermes + Pi stack.

Mission JSONL keeps authoritative constraints separate from expected inferred outputs.
The checked-in fixture may store privacy under expected.privacy for compactness; the harness
passes that privacy object to routers as deterministic constraints and never asks a learned
router to rediscover it.

External adapter protocol: command receives one JSON object on stdin:
  {"id","text","constraints"}
and returns:
  {"tasks":[],"phase":"...","workflow":"...","confidence":0..1,"detail":{...}}

Raw prompts are not persisted unless --include-text is explicitly supplied.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, re, resource, statistics, subprocess, sys, time
from pathlib import Path

TASKS=(
 "research","synthesis","architecture_design","planning_decomposition",
 "coding_implementation","debugging_diagnosis","refactoring","testing",
 "code_review","security_review","devops_configuration","data_analysis",
 "document_generation_transformation","retrieval_memory",
 "agent_supervision_orchestration","long_running_tool_execution",
 "multimodal_analysis","verification_fact_check","other"
)
WORKFLOWS=("hermes_only","research_executor","pi_worker","review_worker","local_tool_runner","multi_stage","local_only","abstain")
PHASES=("discovery","synthesis","design","planning","implementation","diagnosis","testing","review","operation","maintenance","retrieval","supervision","unknown")

PATTERNS={
 "research": r"\b(research|investigate|compare|evaluate|primary[- ]source|gather (?:current )?evidence|survey|literature)\b",
 "synthesis": r"\b(synthesi[sz]e|summari[sz]e|coherent recommendation|trade[- ]?offs?)\b",
 "architecture_design": r"\b(architecture|architectural|design (?:a|the)|trust boundar(?:y|ies))\b",
 "planning_decomposition": r"\b(plan|milestones?|dependencies|decompos|rollout plan|rollback points?)\b",
 "coding_implementation": r"\b(implement|patch|code |edit (?:the )?(?:repository|file)|execute the selected migration|migration in a worktree)\b",
 "debugging_diagnosis": r"\b(debug|diagnos|root cause|stack trace|production bug|exception)\b",
 "refactoring": r"\b(refactor|rename symbol)\b",
 "testing": r"\b(test(?:s|ing| suite)?|regression|compatibility matrix|release workflow syntax)\b",
 "code_review": r"\b(code review|review this pull request|review the diff|pull request for correctness)\b",
 "security_review": r"\b(security review|attack paths?|threat model|vulnerabilit|pii leakage|fields need redaction|client secret)\b",
 "devops_configuration": r"\b(github actions|deployment configuration|configuration for where|devops|ci/cd)\b",
 "data_analysis": r"\b(analy[sz]e (?:the )?(?:benchmark|failure|counts?|cost)|calculate|failure rates?|cost drivers?|cache affinity|provider-switch costs?)\b",
 "document_generation_transformation": r"\b(transform (?:these )?.*notes|operating runbook|generate (?:a )?document|rewrite (?:this|these))\b",
 "retrieval_memory": r"\b(retrieve|durable project memory|memory and summari[sz]e|provenance)\b",
 "agent_supervision_orchestration": r"\b(supervise|agent tasks?|reconcile their evidence|which one should be retried|orchestrat)\b",
 "long_running_tool_execution": r"\b(long[- ]duration|long[- ]running|monitor progress|compatibility matrix)\b",
 "multimodal_analysis": r"\b(attached (?:architecture )?diagram|image|audio|video|passport)\b",
 "verification_fact_check": r"\b(factual claims?|flag unsupported|identify mismatches|independent reviewer verify|fact[- ]?check)\b",
}
RX={k:re.compile(v,re.I) for k,v in PATTERNS.items()}
LOCAL_ONLY=re.compile(r"(?:\b(?:local[- ]only|use only local tools|network access is forbidden|do not (?:upload|send|share)|never send|must stay local|production database dump)\b|\b(?:client secret|access token)\s*[:=])",re.I)

PROTOTYPES={
 "research":["research current sources and gather evidence","compare libraries and investigate alternatives"],
 "synthesis":["synthesize notes into a recommendation","summarize evidence and tradeoffs"],
 "architecture_design":["design system architecture and trust boundaries","propose component architecture"],
 "planning_decomposition":["break objective into milestones dependencies and gates","plan implementation steps and rollback"],
 "coding_implementation":["implement feature edit repository code","patch code in worktree"],
 "debugging_diagnosis":["diagnose root cause from failure","debug stack trace"],
 "refactoring":["refactor module without behavior change","rename and restructure code"],
 "testing":["run regression tests and verify behavior","execute compatibility test suite"],
 "code_review":["review pull request and diff","independent code review"],
 "security_review":["security review attack paths and vulnerabilities","review PII leakage and redaction"],
 "devops_configuration":["update CI deployment configuration","configure build pipeline"],
 "data_analysis":["analyze benchmark data and failure rates","calculate cost and latency statistics"],
 "document_generation_transformation":["transform engineering notes into runbook","generate structured document"],
 "retrieval_memory":["retrieve durable memory with provenance","recall accepted project decision"],
 "agent_supervision_orchestration":["supervise bounded agents and reconcile evidence","orchestrate worker tasks"],
 "long_running_tool_execution":["run long tool job and monitor progress","execute long compatibility matrix"],
 "multimodal_analysis":["inspect image or diagram","analyze attached visual"],
 "verification_fact_check":["verify factual claims against evidence","fact check and flag unsupported statements"],
}

CODINGISH={"coding_implementation","debugging_diagnosis","refactoring","testing","devops_configuration"}
REVIEWISH={"code_review","security_review","verification_fact_check"}
DISCOVERYISH={"research"}

def deterministic_constraints(sample):
 exp=sample.get("expected",{})
 privacy=(sample.get("constraints",{}) or {}).get("privacy") or exp.get("privacy") or {"class":"INTERNAL","cloud_allowed":True}
 return {"privacy":{"class":privacy.get("class","INTERNAL"),"cloud_allowed":bool(privacy.get("cloud_allowed",True))}}

def infer_phase(tasks):
 s=set(tasks)
 if "research" in s:return "discovery"
 if "debugging_diagnosis" in s:return "diagnosis"
 if "architecture_design" in s:return "design"
 if "planning_decomposition" in s:return "planning"
 if "coding_implementation" in s or "refactoring" in s:return "implementation"
 if "testing" in s:return "testing"
 if s & REVIEWISH or "multimodal_analysis" in s:return "review"
 if "long_running_tool_execution" in s or "devops_configuration" in s:return "operation"
 if "retrieval_memory" in s:return "retrieval"
 if "agent_supervision_orchestration" in s:return "supervision"
 if s & {"synthesis","data_analysis","document_generation_transformation"}:return "synthesis"
 return "unknown"

def infer_workflow(tasks,constraints):
 s=set(tasks); privacy=constraints["privacy"]
 if privacy.get("class")=="LOCAL_ONLY" or not privacy.get("cloud_allowed",True):return "local_only"
 if not s:return "abstain"
 if "long_running_tool_execution" in s:return "local_tool_runner"
 if (s & CODINGISH) and (s & (REVIEWISH|DISCOVERYISH|{"architecture_design","planning_decomposition","synthesis"})):return "multi_stage"
 if (s & {"architecture_design","planning_decomposition"}) and (s & REVIEWISH):return "multi_stage"
 if s & CODINGISH:return "pi_worker"
 if s & {"code_review","security_review"} and not (s & DISCOVERYISH):return "review_worker"
 if "research" in s:return "research_executor"
 return "hermes_only"

class Rules:
 name="rules"
 def route(self,sample):
  text=sample["text"]; constraints=deterministic_constraints(sample)
  # Explicit local-only language is an additional deterministic fixture signal.
  if LOCAL_ONLY.search(text):constraints={"privacy":{"class":"LOCAL_ONLY","cloud_allowed":False}}
  tasks=[k for k,rx in RX.items() if rx.search(text)]
  return {"tasks":tasks,"phase":infer_phase(tasks),"workflow":infer_workflow(tasks,constraints),"confidence":1.0 if tasks or not constraints["privacy"].get("cloud_allowed",True) else 0.0,"constraints":constraints,"detail":{"reason":"deterministic rules/state fixture"}}

class Prototype:
 name="prototype"
 def __init__(self,a):
  from sentence_transformers import SentenceTransformer
  self.m=SentenceTransformer(a.embedding_model,trust_remote_code=True)
  self.threshold=a.embedding_threshold; self.embedding_floor=a.embedding_floor; self.max_tasks=a.max_tasks
  labels=[]; texts=[]
  for lab,items in PROTOTYPES.items():
   for text in items:labels.append(lab);texts.append(text)
  vecs=self.m.encode(texts,normalize_embeddings=True)
  self.centroids={}
  for lab in PROTOTYPES:
   xs=[vecs[i] for i,x in enumerate(labels) if x==lab]
   c=sum(xs)/len(xs);self.centroids[lab]=c/((c*c).sum()**.5)
 def route(self,sample):
  constraints=deterministic_constraints(sample)
  if LOCAL_ONLY.search(sample["text"]):constraints={"privacy":{"class":"LOCAL_ONLY","cloud_allowed":False}}
  v=self.m.encode([sample["text"]],normalize_embeddings=True)[0]
  scores={k:float(v@c) for k,c in self.centroids.items()}
  ranked=sorted(scores.items(),key=lambda x:x[1],reverse=True)
  tasks=[k for k,s in ranked if s>=self.threshold][:self.max_tasks]
  if not tasks and ranked and ranked[0][1]>=self.embedding_floor:tasks=[ranked[0][0]]
  conf=max([scores[t] for t in tasks],default=0.0)
  return {"tasks":tasks,"phase":infer_phase(tasks),"workflow":infer_workflow(tasks,constraints),"confidence":float(max(0,min(1,(conf+1)/2))),"constraints":constraints,"detail":{"scores":scores}}

class External:
 def __init__(self,name,cmd):self.name=name;self.cmd=cmd
 def route(self,sample):
  constraints=deterministic_constraints(sample)
  if LOCAL_ONLY.search(sample["text"]):constraints={"privacy":{"class":"LOCAL_ONLY","cloud_allowed":False}}
  # Tier 0 is local and authoritative. Never hand a cloud-ineligible prompt to an
  # external adapter because the benchmark cannot prove that adapter is local.
  if not constraints["privacy"].get("cloud_allowed",True):
   tasks=[k for k,rx in RX.items() if rx.search(sample["text"])]
   return {"tasks":tasks,"phase":infer_phase(tasks),"workflow":"local_only","confidence":1.0,"constraints":constraints,"detail":{"external_skipped":"cloud_allowed=false hard gate"}}
  payload={"id":sample["id"],"text":sample["text"],"constraints":constraints}
  p=subprocess.run(self.cmd,shell=True,input=json.dumps(payload),text=True,capture_output=True,timeout=180)
  if p.returncode:raise RuntimeError(p.stderr[-800:])
  o=json.loads(p.stdout)
  tasks=[x for x in o.get("tasks",[]) if x in TASKS]
  phase=o.get("phase") or infer_phase(tasks); workflow=o.get("workflow") or infer_workflow(tasks,constraints)
  if phase not in PHASES:phase="unknown"
  if workflow not in WORKFLOWS:workflow="abstain"
  return {"tasks":tasks,"phase":phase,"workflow":workflow,"confidence":o.get("confidence"),"constraints":constraints,"detail":o.get("detail",o)}

def rss():
 x=float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 return x/(1024*1024) if sys.platform=="darwin" else x/1024

def load(path):
 out=[]
 for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
  if not line.strip() or line.lstrip().startswith("#"):continue
  o=json.loads(line)
  if "id" not in o or "text" not in o or "expected" not in o:raise SystemExit(f"{path}:{n}: require id/text/expected")
  e=o["expected"]; bad=[x for x in e.get("tasks",[]) if x not in TASKS]
  if bad:raise SystemExit(f"{path}:{n}: bad tasks {bad}")
  if e.get("phase") not in PHASES:raise SystemExit(f"{path}:{n}: bad phase {e.get('phase')}")
  if e.get("workflow") not in WORKFLOWS:raise SystemExit(f"{path}:{n}: bad workflow {e.get('workflow')}")
  out.append(o)
 return out

def load_outcomes(path):
 if not path:return []
 rows=[]
 for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
  if not line.strip() or line.lstrip().startswith("#"):continue
  o=json.loads(line)
  if "id" not in o or "candidate" not in o or "accepted" not in o:raise SystemExit(f"{path}:{n}: require id/candidate/accepted")
  rows.append(o)
 return rows

def make(name,a):
 if name=="rules":return Rules()
 if name=="prototype":return Prototype(a)
 for x in a.external or []:
  n,cmd=x.split("=",1)
  if n==name:return External(n,cmd)
 raise RuntimeError(f"unknown router {name}; use --external name='command' for Aurelio/vLLM/LLMRouter/ModernBERT/RouteLLM/OpenRouter-Auto adapters")

def pct(xs,q):
 s=sorted(xs);return s[min(len(s)-1,max(0,int((len(s)-1)*q)))] if s else 0

def safe_div(a,b):return a/b if b else 0.0

def multilabel_metrics(rows):
 per={}; f1s=[]; TP=FP=FN=0
 for lab in TASKS:
  tp=fp=fn=0
  for row in rows:
   exp=set(row["expected_tasks"]); pred=set(row["predicted_tasks"])
   tp+=int(lab in exp and lab in pred);fp+=int(lab not in exp and lab in pred);fn+=int(lab in exp and lab not in pred)
  if tp+fp+fn:
   pr=safe_div(tp,tp+fp);rc=safe_div(tp,tp+fn);f=safe_div(2*pr*rc,pr+rc);per[lab]={"precision":pr,"recall":rc,"f1":f,"support":tp+fn};f1s.append(f)
  TP+=tp;FP+=fp;FN+=fn
 micro_pr=safe_div(TP,TP+FP);micro_rc=safe_div(TP,TP+FN)
 return {"micro_f1":safe_div(2*micro_pr*micro_rc,micro_pr+micro_rc),"macro_f1":statistics.mean(f1s) if f1s else 0.0,"per_task":per}

def outcome_metrics(outcomes,name):
 xs=[x for x in outcomes if x.get("candidate")==name]
 if not xs:return None
 accepted=[x for x in xs if x.get("accepted")]
 costs=[float(x.get("cost_usd",0) or 0) for x in xs]
 return {
  "missions":len(xs),
  "accepted_rate":safe_div(len(accepted),len(xs)),
  "total_cost_usd":sum(costs),
  "cost_per_accepted_usd":safe_div(sum(costs),len(accepted)) if accepted else None,
  "mean_total_latency_ms":statistics.mean([float(x.get("total_latency_ms",0) or 0) for x in xs]),
  "mean_retries":statistics.mean([float(x.get("retries",0) or 0) for x in xs]),
  "human_override_rate":safe_div(sum(bool(x.get("human_override")) for x in xs),len(xs)),
  "mean_tool_failures":statistics.mean([float(x.get("tool_failures",0) or 0) for x in xs]),
  "mean_model_switches":statistics.mean([float(x.get("model_switches",0) or 0) for x in xs]),
  "mean_provider_switches":statistics.mean([float(x.get("provider_switches",0) or 0) for x in xs]),
  "mean_cache_hit_rate":statistics.mean([float(x.get("cache_hit_rate",0) or 0) for x in xs]),
 }

def metrics(rows):
 ml=multilabel_metrics(rows);lat=[r["latency_ms"] for r in rows]
 by={}
 for r in rows:
  sig=(tuple(sorted(r["predicted_tasks"])),r["predicted_phase"],r["predicted_workflow"]);by.setdefault(r["id"],set()).add(sig)
 local_to_cloud=sum(r["expected_privacy_class"]=="LOCAL_ONLY" and r["predicted_workflow"] not in ("local_only","abstain") for r in rows)
 false_cloud=sum((not r["expected_cloud_allowed"]) and r["predicted_workflow"] not in ("local_only","abstain") for r in rows)
 return {
  "task_family":ml,
  "phase_accuracy":safe_div(sum(r["expected_phase"]==r["predicted_phase"] for r in rows),len(rows)),
  "workflow_accuracy":safe_div(sum(r["expected_workflow"]==r["predicted_workflow"] for r in rows),len(rows)),
  "exact_task_set_accuracy":safe_div(sum(set(r["expected_tasks"])==set(r["predicted_tasks"]) for r in rows),len(rows)),
  "abstain_rate":safe_div(sum(r["predicted_workflow"]=="abstain" for r in rows),len(rows)),
  "determinism_rate":safe_div(sum(len(v)==1 for v in by.values()),len(by)),
  "hard_constraint_violations":{"local_only_to_nonlocal":local_to_cloud,"false_cloud_eligibility":false_cloud},
  "latency_ms":{"mean":statistics.mean(lat),"p50":pct(lat,.5),"p95":pct(lat,.95),"p99":pct(lat,.99)}
 }

def bench(name,a,outcomes):
 data=load(a.dataset);before=rss();t=time.perf_counter();router=make(name,a);startup=(time.perf_counter()-t)*1000;loaded=rss()
 for sample in data[:a.warmup]:router.route(sample)
 rows=[];failures=[]
 for rep in range(a.repeat):
  for sample in data:
   t=time.perf_counter_ns()
   try:pred=router.route(sample)
   except Exception as exc:
    pred={"tasks":[],"phase":"unknown","workflow":"abstain","confidence":0,"constraints":deterministic_constraints(sample),"detail":{"error":f"{type(exc).__name__}: {exc}"}}
    failures.append({"id":sample["id"],"error":pred["detail"]["error"]})
   ms=(time.perf_counter_ns()-t)/1e6;e=sample["expected"];p=e.get("privacy",{})
   rows.append({
    "id":sample["id"],"repeat":rep,"expected_tasks":e.get("tasks",[]),"predicted_tasks":pred.get("tasks",[]),
    "expected_phase":e.get("phase"),"predicted_phase":pred.get("phase","unknown"),
    "expected_workflow":e.get("workflow"),"predicted_workflow":pred.get("workflow","abstain"),
    "expected_privacy_class":p.get("class","INTERNAL"),"expected_cloud_allowed":bool(p.get("cloud_allowed",True)),
    "confidence":pred.get("confidence"),"latency_ms":ms,"text_sha256":hashlib.sha256(sample["text"].encode()).hexdigest(),
    "detail":pred.get("detail",{})
   })
 result={"router":name,"dataset":str(Path(a.dataset).resolve()),"samples":len(data),"repeat":a.repeat,"startup_ms":startup,"max_rss_mb_before":before,"max_rss_mb_after_load":loaded,"max_rss_mb_end":rss(),"metrics":metrics(rows),"outcomes":outcome_metrics(outcomes,name),"failures":failures[:100],"rows":[]}
 for row in rows:
  x={k:v for k,v in row.items() if k not in ("detail",)}
  if a.include_text:x["text"]=next(s["text"] for s in data if s["id"]==row["id"])
  if a.include_detail:x["detail"]=row["detail"]
  result["rows"].append(x)
 return result

def parser():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--dataset",required=True);p.add_argument("--outcomes")
 p.add_argument("--routers",default="rules");p.add_argument("--repeat",type=int,default=3);p.add_argument("--warmup",type=int,default=3)
 p.add_argument("--output");p.add_argument("--pretty",action="store_true");p.add_argument("--include-text",action="store_true");p.add_argument("--include-detail",action="store_true")
 p.add_argument("--fail-on-hard-violations",action="store_true");p.add_argument("--child-router",help=argparse.SUPPRESS)
 p.add_argument("--embedding-model",default=os.getenv("ROUTER_EMBEDDING_MODEL","nomic-ai/modernbert-embed-base"));p.add_argument("--embedding-threshold",type=float,default=.42);p.add_argument("--embedding-floor",type=float,default=.32);p.add_argument("--max-tasks",type=int,default=5)
 p.add_argument("--external",action="append",help="name=command; adapters include aurelio, vllm-semantic-router, modernbert, llmrouter, routellm, openrouter-auto")
 return p

def main():
 a=parser().parse_args();outcomes=load_outcomes(a.outcomes)
 if a.child_router:
  print(json.dumps(bench(a.child_router,a,outcomes),separators=(",",":")));return
 names=[x.strip() for x in a.routers.split(",") if x.strip()];results=[]
 for name in names:
  cmd=[sys.executable,__file__,"--dataset",a.dataset,"--routers",name,"--repeat",str(a.repeat),"--warmup",str(a.warmup),"--child-router",name,"--embedding-model",a.embedding_model,"--embedding-threshold",str(a.embedding_threshold),"--embedding-floor",str(a.embedding_floor),"--max-tasks",str(a.max_tasks)]
  if a.outcomes:cmd += ["--outcomes",a.outcomes]
  for ext in a.external or []:cmd += ["--external",ext]
  if a.include_text:cmd.append("--include-text")
  if a.include_detail:cmd.append("--include-detail")
  proc=subprocess.run(cmd,text=True,capture_output=True)
  result=json.loads(proc.stdout) if proc.returncode==0 else {"router":name,"fatal_error":proc.stderr[-1500:]};results.append(result)
  if "metrics" in result:
   m=result["metrics"];print(f"{name}\ttask-micro-F1={m['task_family']['micro_f1']:.3f}\tworkflow={m['workflow_accuracy']:.3f}\tphase={m['phase_accuracy']:.3f}\thard={sum(m['hard_constraint_violations'].values())}\tp95={m['latency_ms']['p95']:.2f}ms",file=sys.stderr)
 doc={"schema_version":2,"generated_at_epoch":time.time(),"host":{"platform":platform.platform(),"python":sys.version.split()[0],"machine":platform.machine()},"privacy":{"raw_text_included":a.include_text,"note":"Prompt SHA-256 only by default. Tier 0 hard constraints apply before external/cloud adapters."},"evaluation":{"note":"Task/profile inference, hard eligibility, workflow choice, runtime operations and optional outcome economics are reported separately. Not every candidate addresses every tier."},"results":results}
 if a.fail_on-hard-violations:
  bad=sum(sum(r.get("metrics",{}).get("hard_constraint_violations",{}).values()) for r in results)
  if bad:raise SystemExit(f"hard routing constraint violations: {bad}")
 text=json.dumps(doc,indent=2 if a.pretty else None);Path(a.output).write_text(text+"\n",encoding="utf-8") if a.output else print(text)
if __name__=="__main__":main()
