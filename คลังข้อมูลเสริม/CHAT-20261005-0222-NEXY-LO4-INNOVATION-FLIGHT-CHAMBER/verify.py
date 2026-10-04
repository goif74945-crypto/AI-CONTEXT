from __future__ import annotations
import hashlib, json, pathlib, subprocess, sys, unittest, io
ROOT=pathlib.Path(__file__).resolve().parent
files=[ROOT/'lo4_flight_chamber.py', ROOT/'test_lo4_flight_chamber.py', ROOT/'verify.py']
r=subprocess.run([sys.executable,'-m','py_compile',*map(str,files)],text=True,capture_output=True)
compile_ok=r.returncode==0
suite=unittest.defaultTestLoader.loadTestsFromName('test_lo4_flight_chamber')
buf=io.StringIO(); result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
summary={'status':'PASS' if compile_ok and result.wasSuccessful() else 'FAIL','compile':'PASS' if compile_ok else 'FAIL','tests':result.testsRun,'failures_or_errors':len(result.failures)+len(result.errors),'authority':'AI_PROPOSED_LO4_NON_CANON'}
print(json.dumps(summary,indent=2,sort_keys=True)); print(buf.getvalue())
raise SystemExit(0 if summary['status']=='PASS' else 1)
