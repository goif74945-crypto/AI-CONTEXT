import subprocess, sys
for cmd in ([sys.executable,'-m','compileall','-q','epistemic_integrity.py','tests'],[sys.executable,'-m','unittest','discover','-s','tests','-v']):
    r=subprocess.run(cmd,check=False)
    if r.returncode: raise SystemExit(r.returncode)
