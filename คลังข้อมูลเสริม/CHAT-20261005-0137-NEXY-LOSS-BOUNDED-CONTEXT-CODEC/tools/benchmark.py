from __future__ import annotations

import argparse
import json
import random
import statistics
import time

from lbcc.codec import compact
from lbcc.model import CodecPolicy, ContextAtom, ContextBundle, TruthClass


def make_bundle(count: int, seed: int) -> ContextBundle:
    rng = random.Random(seed)
    atoms = []
    truths = list(TruthClass)
    for i in range(count):
        atoms.append(
            ContextAtom(
                atom_id=f"a-{i:06d}",
                text=(f"synthetic-{i}-" + "x" * rng.randint(40, 220)),
                truth_class=truths[rng.randrange(len(truths))],
                authority_rank=rng.randint(0, 94),
                provenance=(f"synthetic:{i}",),
                immutable=False,
            )
        )
    return ContextBundle(f"bench-{count}-{seed}", tuple(atoms))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--atoms", type=int, default=1000)
    p.add_argument("--runs", type=int, default=5)
    p.add_argument("--max-bytes", type=int, default=100000)
    args = p.parse_args()
    bundle = make_bundle(args.atoms, 20261005)
    policy = CodecPolicy(max_capsule_bytes=args.max_bytes, max_loss_ppm=1_000_000)
    samples = []
    last = None
    for _ in range(args.runs):
        start = time.perf_counter()
        last = compact(bundle, policy)
        samples.append(time.perf_counter() - start)
    print(json.dumps({
        "atoms": args.atoms,
        "runs": args.runs,
        "median_seconds": statistics.median(samples),
        "max_seconds": max(samples),
        "status": last.status.value if last else None,
        "retained_atoms": last.metrics.retained_atoms if last else None,
        "capsule_bytes": last.metrics.capsule_bytes if last else None,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
