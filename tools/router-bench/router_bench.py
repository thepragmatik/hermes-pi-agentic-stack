#!/usr/bin/env python3
"""Isolated-process local router benchmark for the Hermes + Pi stack.

Dataset JSONL: {"id":"x","text":"...","label":"deepseek|glm|hybrid|local_only|abstain"}.
Raw prompts are not persisted unless --include-text is explicitly supplied.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, re, resource, statistics, subprocess, sys, time
from pathlib import Path

LABELS=("deepseek","glm","hybrid","local_only","abstain"); CLOUD=("deepseek","glm","hybrid")
PROTOTYPES={
 "deepseek":["research technical evidence and synthesize tradeoffs","compare architectures and recommend a strategy","investigate libraries standards papers and approaches"],
 "glm":["implement a feature edit files run tests","debug code and patch repository","refactor code using language server diagnostics"],
 "hybrid":["research an approach then implement and test it","compare libraries select one integrate it and verify code"]}

class Rules:
 name="rules"
 LOCAL_ONLY=re.compile(r"(?:\b(?:local[- ]only|do not (?:upload|send|share)|never (?:upload|send|share)|contains? (?:real |actual )?(?:pii|personal data|customer data)|my (?:passport|ssn|tfn|tax file number)|private key|seed phrase|production database dump)\b|\b(?:client secret|access token)\s*[:=])",re.I)
 CODE=re.compile(r"\b(implement|code|fix|debug|refactor|compile|build|test|rename symbol|edit (?:the )?file|patch|pull request|commit|typescript|javascript|python|java|kotlin|gradle|maven|npm|pnpm|pytest|junit|stack trace|exception|terminal|shell command|cli|api endpoint|migration)\b",re.I)
 RESEARCH=re.compile(r"\b(research|investigate|compare|evaluate|architecture|strategy|ideat|brainstorm|landscape|trade[- ]?off|design options|literature|survey|systems map|recommend|decision memo)\b",re.I)
 def route(self,text):
  if self.LOCAL_ONLY.search(text): return ("local_only",1.0,{"reason":"privacy/security rule"})
  c=bool(self.CODE.search(text)); r=bool(self.RESEARCH.search(text))
  if c and r:return ("hybrid",.90,{"reason":"code + research"})
  if c:return ("glm",.93,{"reason":"coding/tool"})
  if r:return ("deepseek",.93,{"reason":"research/design"})
  return ("abstain",0.0,{"reason":"no deterministic signal"})

class Prototype:
 name="prototype"
 def __init__(self,a):
  from sentence_transformers import SentenceTransformer
  self.m=SentenceTransformer(a.embedding_model,trust_remote_code=True); self.t=a.embedding_threshold; self.margin=a.embedding_margin
  labs=[]; texts=[]
  for lab,items in PROTOTYPES.items():
   for x in items: labs.append(lab); texts.append(x)
  v=self.m.encode(texts,normalize_embeddings=True); self.c={}
  for lab in PROTOTYPES:
   xs=[v[i] for i,x in enumerate(labs) if x==lab]; c=sum(xs)/len(xs); self.c[lab]=c/((c*c).sum()**.5)
 def route(self,text):
  if Rules.LOCAL_ONLY.search(text):return ("local_only",1.0,{})
  v=self.m.encode([text],normalize_embeddings=True)[0]; s={k:float(v@c) for k,c in self.c.items()}; q=sorted(s.items(),key=lambda x:x[1],reverse=True)
  if q[0][1]<self.t or q[0][1]-q[1][1]<self.margin:return ("abstain",max(0,min(1,(q[0][1]+1)/2)),{"scores":s})
  return (q[0][0],max(0,min(1,(q[0][1]+1)/2)),{"scores":s})

class Semantic:
 name="semantic-router"
 def __init__(self,a):
  from semantic_router import Route
  from semantic_router.routers import SemanticRouter
  try: from semantic_router.encoders import HuggingFaceEncoder
  except ImportError: from semantic_router.encoders.huggingface import HuggingFaceEncoder
  try:e=HuggingFaceEncoder(name=a.semantic_model)
  except TypeError:e=HuggingFaceEncoder(model_name=a.semantic_model)
  rs=[Route(name=k,utterances=v) for k,v in PROTOTYPES.items()]
  try:self.r=SemanticRouter(encoder=e,routes=rs,auto_sync="local")
  except TypeError:self.r=SemanticRouter(encoder=e,routes=rs)
  self.t=a.semantic_threshold
 def route(self,text):
  if Rules.LOCAL_ONLY.search(text):return ("local_only",1.0,{})
  x=self.r(text); name=getattr(x,"name",None); score=getattr(x,"similarity_score",None)
  if not name or (score is not None and score<self.t):return ("abstain",float(score or 0),{})
  return (name,float(score) if score is not None else None,{})

class ModernBERT:
 name="modernbert"
 def __init__(self,a):
  from transformers import pipeline
  if not a.modernbert_model:raise RuntimeError("--modernbert-model is required")
  self.p=pipeline("text-classification",model=a.modernbert_model,tokenizer=a.modernbert_model,top_k=None); self.t=a.modernbert_threshold
 def route(self,text):
  if Rules.LOCAL_ONLY.search(text):return ("local_only",1.0,{})
  rows=self.p(text)[0]; best=max(rows,key=lambda x:x["score"]); lab=best["label"].lower().replace("label_","")
  if lab.isdigit(): lab={"0":"deepseek","1":"glm","2":"hybrid","3":"local_only","4":"abstain"}.get(lab,"abstain")
  return (lab if best["score"]>=self.t else "abstain",float(best["score"]),{"scores":rows})

class RouteLLM:
 name="routellm"
 def __init__(self,a):
  from routellm.controller import Controller
  self.c=Controller(routers=["mf"],strong_model=a.routellm_strong_model,weak_model=a.routellm_weak_model); self.a=a
 def route(self,text):
  if Rules.LOCAL_ONLY.search(text):return ("local_only",1.0,{})
  model=self.c.route(prompt=text,router="mf",threshold=self.a.routellm_threshold)
  lab=self.a.routellm_strong_label if model==self.a.routellm_strong_model else self.a.routellm_weak_label
  return (lab,None,{"model":model})

class External:
 def __init__(self,name,cmd):self.name=name;self.cmd=cmd
 def route(self,text):
  if Rules.LOCAL_ONLY.search(text):return ("local_only",1.0,{})
  p=subprocess.run(self.cmd,shell=True,input=text,text=True,capture_output=True,timeout=120)
  if p.returncode:raise RuntimeError(p.stderr[-500:])
  o=json.loads(p.stdout);return (o["label"],o.get("confidence"),o)

def rss():
 x=float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);return x/(1024*1024) if sys.platform=="darwin" else x/1024

def load(p):
 out=[]
 for n,line in enumerate(Path(p).read_text().splitlines(),1):
  if not line.strip() or line.lstrip().startswith("#"):continue
  o=json.loads(line);lab=o["label"].lower()
  if lab not in LABELS:raise SystemExit(f"{p}:{n}: bad label {lab}")
  out.append((str(o["id"]),str(o["text"]),lab))
 return out

def make(name,a):
 if name=="rules":return Rules()
 if name=="prototype":return Prototype(a)
 if name=="semantic-router":return Semantic(a)
 if name=="modernbert":return ModernBERT(a)
 if name=="routellm":return RouteLLM(a)
 for x in a.external or []:
  n,cmd=x.split("=",1)
  if n==name:return External(n,cmd)
 raise RuntimeError(f"unknown router {name}")

def pct(xs,q):
 s=sorted(xs);return s[min(len(s)-1,max(0,int((len(s)-1)*q)))] if s else 0

def metrics(rows):
 f=[]; per={}
 for lab in LABELS:
  tp=sum(r[2]==lab and r[3]==lab for r in rows); fp=sum(r[2]!=lab and r[3]==lab for r in rows); fn=sum(r[2]==lab and r[3]!=lab for r in rows)
  if tp+fp+fn:
   pr=tp/(tp+fp) if tp+fp else 0; rc=tp/(tp+fn) if tp+fn else 0; z=2*pr*rc/(pr+rc) if pr+rc else 0; f.append(z); per[lab]={"precision":pr,"recall":rc,"f1":z}
 by={}
 for r in rows:by.setdefault(r[0],set()).add(r[3])
 lat=[r[5] for r in rows]
 return {"accuracy":sum(r[2]==r[3] for r in rows)/len(rows),"macro_f1":statistics.mean(f),"abstain_rate":sum(r[3]=="abstain" for r in rows)/len(rows),"determinism_rate":sum(len(v)==1 for v in by.values())/len(by),"latency_ms":{"mean":statistics.mean(lat),"p50":pct(lat,.5),"p95":pct(lat,.95),"p99":pct(lat,.99)},"high_severity_errors":{"local_only_to_cloud":sum(r[2]=="local_only" and r[3] in CLOUD for r in rows),"glm_to_deepseek":sum(r[2]=="glm" and r[3]=="deepseek" for r in rows),"deepseek_to_glm":sum(r[2]=="deepseek" and r[3]=="glm" for r in rows)},"per_label":per}

def bench(name,a):
 data=load(a.dataset); before=rss(); t=time.perf_counter(); r=make(name,a); startup=(time.perf_counter()-t)*1000; loaded=rss()
 for _,text,_ in data[:a.warmup]:r.route(text)
 rows=[]; failures=[]
 for rep in range(a.repeat):
  for id,text,exp in data:
   t=time.perf_counter_ns()
   try:pred,conf,detail=r.route(text)
   except Exception as e:pred,conf,detail="abstain",0,{"error":f"{type(e).__name__}: {e}"};failures.append({"id":id,"error":detail["error"]})
   ms=(time.perf_counter_ns()-t)/1e6; rows.append((id,rep,exp,pred,conf,ms,text,detail))
 result={"router":name,"dataset":str(Path(a.dataset).resolve()),"samples":len(data),"repeat":a.repeat,"startup_ms":startup,"max_rss_mb_before":before,"max_rss_mb_after_load":loaded,"max_rss_mb_end":rss(),"metrics":metrics(rows),"failures":failures[:100],"rows":[]}
 for id,rep,exp,pred,conf,ms,text,detail in rows:
  x={"id":id,"repeat":rep,"expected":exp,"predicted":pred,"confidence":conf,"latency_ms":ms,"text_sha256":hashlib.sha256(text.encode()).hexdigest()}
  if a.include_text:x["text"]=text
  if a.include_detail:x["detail"]=detail
  result["rows"].append(x)
 return result

def args_parser():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--dataset",required=True);p.add_argument("--routers",default="rules,prototype,semantic-router");p.add_argument("--repeat",type=int,default=5);p.add_argument("--warmup",type=int,default=3);p.add_argument("--output");p.add_argument("--pretty",action="store_true");p.add_argument("--include-text",action="store_true");p.add_argument("--include-detail",action="store_true");p.add_argument("--child-router",help=argparse.SUPPRESS);p.add_argument("--embedding-model",default=os.getenv("ROUTER_EMBEDDING_MODEL","Qwen/Qwen3-Embedding-0.6B"));p.add_argument("--embedding-threshold",type=float,default=.35);p.add_argument("--embedding-margin",type=float,default=.03);p.add_argument("--semantic-model",default=os.getenv("SEMANTIC_ROUTER_MODEL","sentence-transformers/all-MiniLM-L6-v2"));p.add_argument("--semantic-threshold",type=float,default=.5);p.add_argument("--modernbert-model",default=os.getenv("MODERNBERT_ROUTER_MODEL",""));p.add_argument("--modernbert-threshold",type=float,default=.65);p.add_argument("--routellm-strong-model",default=os.getenv("ROUTELLM_STRONG_MODEL","gpt-4-1106-preview"));p.add_argument("--routellm-weak-model",default=os.getenv("ROUTELLM_WEAK_MODEL","mixtral-8x7b-instruct-v0.1"));p.add_argument("--routellm-strong-label",choices=LABELS,default="deepseek");p.add_argument("--routellm-weak-label",choices=LABELS,default="glm");p.add_argument("--routellm-threshold",type=float,default=.5);p.add_argument("--external",action="append");return p

def main():
 a=args_parser().parse_args()
 if a.child_router:print(json.dumps(bench(a.child_router,a),separators=(",",":")));return
 names=[x.strip() for x in a.routers.split(",") if x.strip()]; results=[]
 for name in names:
  cmd=[sys.executable,__file__,"--dataset",a.dataset,"--routers",name,"--repeat",str(a.repeat),"--warmup",str(a.warmup),"--child-router",name]
  for opt in ("embedding_model","semantic_model","modernbert_model","routellm_strong_model","routellm_weak_model","routellm_strong_label","routellm_weak_label"):
   v=getattr(a,opt);cmd += ["--"+opt.replace("_","-"),str(v)] if v else []
  for opt in ("embedding_threshold","embedding_margin","semantic_threshold","modernbert_threshold","routellm_threshold"):cmd += ["--"+opt.replace("_","-"),str(getattr(a,opt))]
  for x in a.external or []:cmd += ["--external",x]
  if a.include_text:cmd.append("--include-text")
  if a.include_detail:cmd.append("--include-detail")
  p=subprocess.run(cmd,text=True,capture_output=True)
  results.append(json.loads(p.stdout) if p.returncode==0 else {"router":name,"fatal_error":p.stderr[-1000:]})
 doc={"schema_version":1,"generated_at_epoch":time.time(),"host":{"platform":platform.platform(),"python":sys.version.split()[0],"machine":platform.machine()},"privacy":{"raw_text_included":a.include_text,"note":"Prompt SHA-256 only by default; apply egress policy before third-party routers."},"results":results}
 for r in results:
  if "metrics" in r:
   m=r["metrics"];print(f"{r['router']}\tacc={m['accuracy']:.3f}\tmacro-F1={m['macro_f1']:.3f}\tabstain={m['abstain_rate']:.3f}\tp50={m['latency_ms']['p50']:.2f}ms\tp95={m['latency_ms']['p95']:.2f}ms",file=sys.stderr)
 text=json.dumps(doc,indent=2 if a.pretty else None);Path(a.output).write_text(text+"\n") if a.output else print(text)
if __name__=="__main__":main()
