from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ONE=1<<64
p=subprocess.run(['node','scripts/export_vectors.mjs'],cwd=ROOT,check=True,capture_output=True,text=True)
rows=json.loads(p.stdout)
def ceil_div(a:int,b:int)->int:
    return 0 if a==0 else 1+(a-1)//b
for i,row in enumerate(rows):
    b=int(row['b']); r=int(row['r']); R=int(row['R']); T=int(row['T'])
    expected_backlog=(b+r*T)*ONE
    expected_delay=T*ONE + ceil_div(b*ONE,R)
    expected_chain_rate=R*ONE
    expected_chain_latency=(T+3)*ONE
    got=(int(row['backlog']),int(row['delay']),int(row['chainRate']),int(row['chainLatency']))
    exp=(expected_backlog,expected_delay,expected_chain_rate,expected_chain_latency)
    if got!=exp:
        raise SystemExit(f'FAIL vector={i} got={got} expected={exp}')
print(f'PASS: independent Python integer oracle matched {len(rows)} TypeScript Q64.64 vectors')
