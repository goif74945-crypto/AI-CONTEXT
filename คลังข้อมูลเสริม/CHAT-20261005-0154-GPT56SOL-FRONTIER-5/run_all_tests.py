from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).parent
ideas=[
"01_MODEL_DRIFT_SENTINEL","02_SEMANTIC_CAPABILITY_ABI","03_CONTEXT_TAINT_FIREWALL","04_EFFECT_TRANSACTION_COORDINATOR","05_SCOPED_AUTHORITY_LEASE"]
failed=[]
for idea in ideas:
    src=ROOT/idea/"src"; tests=ROOT/idea/"tests"
    for py in sorted(src.glob("*.py")):
        r=subprocess.run([sys.executable,"-m","py_compile",str(py)],capture_output=True,text=True)
        if r.returncode:
            print(f"[E1 FAIL] {idea}: {py.name}\n{r.stderr}"); failed.append((idea,"E1")); continue
    r=subprocess.run([sys.executable,"-m","unittest","discover","-s",str(tests),"-p","test_*.py","-v"],capture_output=True,text=True)
    print(f"=== {idea} ===")
    print(r.stdout,end=""); print(r.stderr,end="")
    if r.returncode: failed.append((idea,"E2"))
    else: print(f"[PASS] {idea} E1+E2")
if not failed:
    ir=subprocess.run([sys.executable,"-m","unittest","discover","-s",str(ROOT/"integration"),"-p","test_*.py","-v"],capture_output=True,text=True)
    print("=== CROSS-SYSTEM INTEGRATION ==="); print(ir.stdout,end=""); print(ir.stderr,end="")
    if ir.returncode: failed.append(("integration","E3-lab"))
if failed:
    print("OVERALL: FAIL",failed); raise SystemExit(1)
print("OVERALL: PASS — 5/5 systems E1+E2; lab integration PASS")
