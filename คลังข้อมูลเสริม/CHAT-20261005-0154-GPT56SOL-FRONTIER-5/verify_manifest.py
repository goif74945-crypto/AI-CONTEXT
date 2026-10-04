from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).parent
manifest=ROOT/'MANIFEST.sha256'
errors=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    digest, rel=line.split('  ',1)
    p=ROOT/rel
    if not p.exists(): errors.append(f"missing:{rel}"); continue
    actual=sha256(p.read_bytes()).hexdigest()
    if actual!=digest: errors.append(f"mismatch:{rel}")
if errors:
    print('MANIFEST: FAIL'); print('\n'.join(errors)); raise SystemExit(1)
print('MANIFEST: PASS')
