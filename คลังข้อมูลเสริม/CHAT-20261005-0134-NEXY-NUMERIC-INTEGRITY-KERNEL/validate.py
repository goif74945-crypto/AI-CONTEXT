from __future__ import annotations
import compileall
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from generate_golden_vectors import build_vectors
ROOT=Path(__file__).resolve().parent

def _run(command):
    return subprocess.run(command,cwd=ROOT,text=True,capture_output=True,check=False)

def run() -> int:
    checks=[]
    details={"python":sys.version.split()[0]}
    compiled=compileall.compile_dir(ROOT/"nnik",quiet=1) and compileall.compile_dir(ROOT/"tests",quiet=1)
    checks.append(("python_compile",compiled))
    json_targets=list((ROOT/"fixtures").glob("*.json"))+[ROOT/"TASK_CONTRACT.json",ROOT/"GOLDEN_VECTORS.json"]
    json_ok=True
    for target in sorted(json_targets):
        try: json.loads(target.read_text(encoding="utf-8"))
        except Exception: json_ok=False
    checks.append(("json_parse",json_ok)); details["json_files_checked"]=len(json_targets)
    unit=_run([sys.executable,"-m","unittest","discover","-s","tests","-v"])
    (ROOT/"evidence"/"unittest.stdout.txt").write_text(unit.stdout,encoding="utf-8")
    (ROOT/"evidence"/"unittest.stderr.txt").write_text(unit.stderr,encoding="utf-8")
    match=re.search(r"Ran (d+) tests",unit.stderr)
    details["unit_test_count"]=int(match.group(1)) if match else None
    checks.append(("unit_tests",unit.returncode==0))
    static=_run([sys.executable,"audit_static.py"])
    (ROOT/"evidence"/"static_audit.stdout.txt").write_text(static.stdout,encoding="utf-8")
    (ROOT/"evidence"/"static_audit.stderr.txt").write_text(static.stderr,encoding="utf-8")
    checks.append(("static_security_audit",static.returncode==0))
    committed_vectors=json.loads((ROOT/"GOLDEN_VECTORS.json").read_text(encoding="utf-8"))
    checks.append(("golden_vectors_regenerate",committed_vectors==build_vectors()))
    details["golden_evaluation_vectors"]=len(committed_vectors["evaluation_vectors"]); details["golden_fixed128_vectors"]=len(committed_vectors["fixed128_vectors"])
    cli=_run([sys.executable,"-m","nnik.cli","evaluate",str(ROOT/"fixtures"/"length_accept.json")])
    (ROOT/"evidence"/"cli_length_accept.json").write_text(cli.stdout,encoding="utf-8")
    checks.append(("cli_integration_accept",cli.returncode==0 and '"verdict":"ACCEPT"' in cli.stdout))
    cli_freeze=_run([sys.executable,"-m","nnik.cli","evaluate",str(ROOT/"fixtures"/"temperature_freeze.json")])
    (ROOT/"evidence"/"cli_temperature_freeze.json").write_text(cli_freeze.stdout,encoding="utf-8")
    checks.append(("cli_integration_freeze",cli_freeze.returncode==0 and '"verdict":"FREEZE"' in cli_freeze.stdout))
    projection=_run([sys.executable,"-m","nnik.cli","project-fixed128","--value","0.85","--quantum","0.01"])
    (ROOT/"evidence"/"cli_fixed128_accept.json").write_text(projection.stdout,encoding="utf-8")
    checks.append(("fixed128_projection_accept",projection.returncode==0 and '"integer":85' in projection.stdout))
    projection_freeze=_run([sys.executable,"-m","nnik.cli","project-fixed128","--value","1/3","--quantum","0.01"])
    (ROOT/"evidence"/"cli_fixed128_freeze.json").write_text(projection_freeze.stdout,encoding="utf-8")
    checks.append(("fixed128_projection_freeze",projection_freeze.returncode==0 and '"verdict":"FREEZE"' in projection_freeze.stdout))
    repeats=[]
    for _ in range(25):
        proc=_run([sys.executable,"-m","nnik.cli","evaluate",str(ROOT/"fixtures"/"length_accept.json")])
        repeats.append(b"PROCESS_FAILURE" if proc.returncode!=0 else proc.stdout.encode("utf-8"))
    hashes=[hashlib.sha256(item).hexdigest() for item in repeats]
    deterministic=len(set(hashes))==1
    (ROOT/"evidence"/"determinism_replay.json").write_text(json.dumps({"runs":len(repeats),"unique_sha256_count":len(set(hashes)),"sha256":hashes[0] if hashes else None,"pass":deterministic},indent=2)+"
",encoding="utf-8")
    checks.append(("determinism_replay_25",deterministic))
    result={"environment":details,"checks":[{"name":name,"status":"PASS" if passed else "FAIL"} for name,passed in checks],"status":"PASS" if all(p for _,p in checks) else "FAIL"}
    (ROOT/"evidence"/"validation.json").write_text(json.dumps(result,indent=2)+"
",encoding="utf-8")
    print(json.dumps(result,indent=2))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(run())
