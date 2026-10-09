#!/usr/bin/env python3
"""Decode this proposal's complete gzip+Base64 Git patch without overwrites."""
import argparse, base64, gzip, hashlib, pathlib, re, sys
EXPECTED="7ff3a856b1eba7dac7d745c04463fc8c4ac5934d85eb30f4271e29ac20ae3234"
def run(snapshot: pathlib.Path, output: pathlib.Path) -> int:
    raw=snapshot.read_text(encoding="utf-8")
    m=re.search(r"```base64\n([A-Za-z0-9+/=]+)\n```",raw)
    if m is None: raise ValueError("Missing complete Base64 archive")
    packed=base64.b64decode(m[1],validate=True)
    data=gzip.decompress(packed)
    if hashlib.sha256(data).hexdigest()!=EXPECTED: raise ValueError("Patch SHA-256 mismatch")
    if output.exists() or output.is_symlink(): raise FileExistsError("Refusing overwrite")
    if output.parent.is_symlink() or not output.parent.is_dir(): raise ValueError("Unsafe destination")
    with output.open("xb") as stream: stream.write(data)
    print("VERIFIED",EXPECTED,"bytes",len(data),"->",str(output));return 0
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("archive",type=pathlib.Path)
    parser.add_argument("output",type=pathlib.Path)
    args=parser.parse_args()
    try: sys.exit(run(args.archive,args.output))
    except (OSError,ValueError) as e: print("FAIL:",str(e),file=sys.stderr);sys.exit(1)
