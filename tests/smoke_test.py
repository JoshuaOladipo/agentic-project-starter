import subprocess,tempfile
from pathlib import Path
r=Path(__file__).resolve().parent.parent;c=r/"cli/agentic_starter.py"
with tempfile.TemporaryDirectory() as t:
 p=Path(t)/"app";p.mkdir();(p/"README.md").write_text("# Existing\n")
 subprocess.run(["python3",str(c),"init",str(p)],check=True)
 assert (p/".agentic/AGENTS.md").exists() and (p/"README.md").read_text()=="# Existing\n"
 subprocess.run(["python3",str(c),"status",str(p)],check=True)
 subprocess.run(["python3",str(c),"update",str(p),"--dry-run"],check=True)
 subprocess.run(["python3",str(p/".agentic/scripts/validate_project.py")],cwd=p,check=True)
print("Smoke test PASS")
