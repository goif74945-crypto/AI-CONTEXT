#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p evidence
python -m py_compile lo4_foundry.py test_lo4_foundry.py run_demo.py
echo COMPILE_PASS
python - <<'PY'
import ast
from pathlib import Path
p=Path('lo4_foundry.py')
t=ast.parse(p.read_text(encoding='utf-8'))
banned={'requests','httpx','urllib','socket','subprocess','paramiko','ftplib','telnetlib','smtplib','asyncssh'}
viol=[]
for n in ast.walk(t):
    if isinstance(n, ast.Import):
        viol += [a.name for a in n.names if a.name.split('.',1)[0] in banned]
    elif isinstance(n, ast.ImportFrom) and n.module and n.module.split('.',1)[0] in banned:
        viol.append(n.module)
    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {'eval','exec'}:
        viol.append(n.func.id)
assert not viol, viol
print('STATIC_GUARD_PASS banned_imports=0 banned_calls=0')
PY
python -m unittest -v test_lo4_foundry
python - <<'PY'
from lo4_foundry import *

dims=[NoveltyDimension(f'd{i:05d}', i%10001, (i*37)%10001) for i in range(20000)]
p=SurprisePolicy(total_budget=10**9,max_single_dimension_cost=10000)
assert evaluate_surprise_budget(dims,p).fingerprint == evaluate_surprise_budget(reversed(dims),p).fingerprint
alts=[Alternative(f'alt{i:05d}',5000+(i%5000),i%3000,i%2000) for i in range(10000)]
assert refute_feature([BenefitClaim('benefit',8000,3)],8000,4000,alts).fingerprint
constraints=[ConstraintRef(f'e{i:02d}',Authority.EXPERIMENTAL,True,(i%7)+1) for i in range(18)]
conflicts=[ConflictSet(f'c{i:02d}',(f'e{i:02d}',f'e{(i+1)%18:02d}',f'e{(i+7)%18:02d}')) for i in range(12)]
assert propose_minimal_relaxation(constraints,conflicts,RelaxationPolicy(max_relaxations=8,max_search_candidates=20)).fingerprint
scenarios=[f's{i}' for i in range(8)]
actions=[ActionCandidate(f'a{i:05d}',True,False,True,{s:((i*17+j*31)%10000) for j,s in enumerate(scenarios)}) for i in range(5000)]
rp=RegretPolicy(max_worst_case_regret=10000)
assert choose_minimax_regret(actions,rp).fingerprint == choose_minimax_regret(reversed(actions),rp).fingerprint
opts=[FutureOption(f'f{i:02d}',(i+1)*100) for i in range(20)]
choices=[ArchitectureChoice(f'ch{i:05d}',True,tuple(f'f{j:02d}' for j in range(20) if (i+j)%3!=0),i%10001,(i*3)%10001,(i*11)%10001) for i in range(5000)]
op=OptionPolicy(future_weight_bps=5000,switching_penalty_bps=2500,lock_in_penalty_bps=2500)
assert select_option_preserving_choice(opts,choices,op).fingerprint == select_option_preserving_choice(reversed(opts),reversed(choices),op).fingerprint
print('STRESS_PROBE_PASS surprise_dims=20000 alternatives=10000 relaxation_candidates=18 regret_actions=5000 option_choices=5000')
PY
python run_demo.py > evidence/demo-a.json
python run_demo.py > evidence/demo-b.json
cmp evidence/demo-a.json evidence/demo-b.json
echo DEMO_DETERMINISM_PASS
cp evidence/demo-a.json evidence/demo-output.json
rm evidence/demo-a.json evidence/demo-b.json
python - <<'PY'
from pathlib import Path
import hashlib
excluded={'MANIFEST.sha256','evidence/full-verification.txt'}
files=sorted(p for p in Path('.').rglob('*') if p.is_file() and p.as_posix() not in excluded and '__pycache__' not in p.parts and not p.name.endswith('.pyc') and p.name!='static_guard.py')
Path('MANIFEST.sha256').write_text(''.join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.as_posix()}\n" for p in files), encoding='utf-8')
print(f'MANIFEST_PASS entries={len(files)}')
PY
