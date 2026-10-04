# NEXY EPC Assumption & Identifiability Kernel 20 (AIK20)

CHAT_ID: `CHAT-20261005-0311-GPT56SOL-NEXY-EPC-AIK20-C7F4`

AIK20 is an AI-proposed Lo4 advisory package for the NEXY Evolutionary Proposal Court. It exposes hidden proposal assumptions and detects decision underdetermination: situations where the same verified observations remain compatible with multiple decision-distinct outcomes.

Authority: `Lo4_AI_PROPOSAL_ONLY / NON_CANONICAL / NON_GOVERNING`.
It cannot mutate NEXY.AI, Core/JUDGE/LAW state, promote Canon, authorize release, or physically delete CUT candidates.

## Tested source archive
`AIK20-C7F4.tar.gz`
SHA-256: `d6f666df71d104fa3255285858204572dcfb65604f311d66d56dd57b0847ab0f`

The reproducible archive contains Design + Code + Tests + Evidence + exact SHA-256 manifest:
- 20 AIK modules
- Q64.64 BigInt substrate checked to signed i128 raw bounds
- EPC KEEP/CUT one-round entitlement guards
- strict TypeScript build
- static no-float/no-random/no-wall-clock decision-core scan
- 35 tests PASS / 0 FAIL
- deterministic 4,096-state exhaustive corpus
- semantic collision audit and failure/repair log

NEXY.AI- baseline inspected read-only: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
Canonical NEXY-IGNIS content SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.

Unpack with a standard gzip/tar implementation, then run `npm run verify`.
