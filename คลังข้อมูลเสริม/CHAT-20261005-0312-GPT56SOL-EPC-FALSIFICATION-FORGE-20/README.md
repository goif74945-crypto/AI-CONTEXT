# NEXY EPC Falsification & Experimental Design Forge 20

**CHAT_ID:** `CHAT-20261005-0312-GPT56SOL-EPC-FALSIFICATION-FORGE-20`  
**Class:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`  
**Target for possible future adoption:** NEXY.AI  
**Current integration state:** standalone reference implementation; NOT integrated into NEXY.AI.

## Purpose

This package converts Lo4 proposals into deterministic attempts to falsify them before any promotion review. It exists to make a proposal earn evidence by surviving explicit counterexamples, boundary probes, assumption attacks, oracle disagreements, resource probes and deterministic replay.

It deliberately does **not**:
- vote itself into Canon;
- mutate NEXY CORE/JUDGE/LAW/SWARM state;
- decide production release;
- replace NEXY JUDGE;
- physically delete CUT candidates;
- treat WIP/UNKNOWN as failure;
- use binary floating point for authoritative court metrics.

## Core invariant

`PROPOSAL -> HYPOTHESIS -> FALSIFIER -> EXPERIMENT -> EVIDENCE -> ADVISORY DOSSIER`

The terminal dossier can only report readiness for **external review**. `autoPromote` is structurally `false`.

## Numeric model

Authoritative quantitative values use checked signed Q64.64 stored in a signed 128-bit conceptual domain. Ratio construction and signed division truncate toward zero to align with the currently inspected NEXY fixed-point behavior. Overflow and divide-by-zero fail closed.

## Run

Requires Node.js with BigInt support and TypeScript 5.x available as `tsc`.

```text
npm run verify
```

The verification pipeline performs:
1. clean rebuild;
2. strict TypeScript compilation;
3. forbidden nondeterminism/network/float-constructor source scan;
4. unit + negative + property + integration tests;
5. 1,000-run deterministic replay proof.

No runtime package dependency is required.

## Evidence status

Local isolated verification on the exact bytes in `evidence/13_FINAL_MODULAR_TESTED_SHA256.txt`:
- strict TypeScript build: PASS;
- static forbidden-pattern scan: PASS;
- automated tests: 36 PASS / 0 FAIL;
- deterministic replay: 1,000/1,000 identical capsules;
- modular-refactor clean verification: 36 PASS / 0 FAIL + 1,000 deterministic replays;
- NEXY.AI mutation by this mission: forbidden and not performed.

See `05_VERIFICATION_EVIDENCE.md` for exact evidence scope and limitations.
