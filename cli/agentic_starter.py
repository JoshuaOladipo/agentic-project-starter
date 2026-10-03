#!/usr/bin/env python3
import argparse,shutil,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent; F=R/"framework"; B=R/"bootstrap"; V=(R/"VERSION").read_text().strip()
def ver(p):
 q=p/".agentic/VERSION"; return q.read_text().strip() if q.exists() else None
def install_managed(p):
 d=p/".agentic"
 if d.exists(): shutil.rmtree(d)
 shutil.copytree(F,d)
def init(p):
 p.mkdir(parents=True,exist_ok=True)
 if (p/".agentic").exists(): print("ERROR: .agentic exists; use update.",file=sys.stderr); return 2
 install_managed(p)
 for rel in ["AGENTS.md","agentic.yaml","architecture/CONTRACT.yaml",".agentic-local/AGENTS.md"]:
  dst=p/rel
  if dst.exists(): print("Preserved:",rel)
  else: dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(B/rel,dst); print("Created:",rel)
 for rel in ["architecture/decisions","tasks/active","tasks/completed","docs"]: (p/rel).mkdir(parents=True,exist_ok=True)
 print("Installed framework",V)
 if (p/"AGENTS.md").read_text()!= (B/"AGENTS.md").read_text(): print("ACTION: ensure existing AGENTS.md directs agents to .agentic/AGENTS.md and architecture/CONTRACT.yaml.")
 return 0
def status(p):
 x=ver(p)
 if not x: print("Framework not installed."); return 1
 print("Installed:",x);print("Available:",V);print("Up to date." if x==V else "Update available.");return 0
def files(b): return {x.relative_to(b) for x in b.rglob("*") if x.is_file()}
def update(p,dry):
 x=ver(p)
 if not x: print("ERROR: use init first.",file=sys.stderr);return 2
 d=p/".agentic"; old,new=files(d),files(F)
 for label,items in [("ADD",new-old),("REMOVE",old-new),("UPDATE",{q for q in old&new if (d/q).read_bytes()!=(F/q).read_bytes()})]:
  for q in sorted(items): print(f"{label}: .agentic/{q}")
 print(f"Framework {x} -> {V}")
 if dry: print("Dry run: no files changed.");return 0
 install_managed(p);print("Applied only to .agentic/. Review with: git diff -- .agentic");return 0
a=argparse.ArgumentParser();s=a.add_subparsers(dest="cmd",required=True)
for n in ["init","status"]:
 q=s.add_parser(n);q.add_argument("project",nargs="?",default=".")
q=s.add_parser("update");q.add_argument("project",nargs="?",default=".");q.add_argument("--dry-run",action="store_true")
z=a.parse_args();p=Path(z.project).resolve()
raise SystemExit(init(p) if z.cmd=="init" else status(p) if z.cmd=="status" else update(p,z.dry_run))
