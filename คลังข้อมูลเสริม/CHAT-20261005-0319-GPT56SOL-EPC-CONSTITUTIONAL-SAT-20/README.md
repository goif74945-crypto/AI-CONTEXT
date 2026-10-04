# NEXY EPC Constitutional Satisfiability & Contradiction Lab 20

CHAT_ID: `CHAT-20261005-0319-GPT56SOL-EPC-CONSTITUTIONAL-SAT-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
STATUS: `VERIFIED_STANDALONE / NON_CANONICAL / NOT_RUNTIME_INTEGRATED`
CLASSIFICATION: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / ADVISORY_ONLY`

## Purpose
A deterministic proof laboratory for checking whether explicit proposal constraints can coexist with explicit Canon constraints before a proposal reaches any authoritative NEXY promotion/release process.

It can prove SAT/UNSAT for its bounded boolean constraint language, produce deterministic model witnesses, bounded exact minimal UNSAT cores, implication/equivalence/redundancy evidence, forced-atom/dead-state evidence, proposal conflict attribution, Q64.64 conflict-density metrics, proof capsules and a court consistency dossier.

## Authority boundary
This project has **zero authority** over NEXY Canon, LAW, CORE, JUDGE, SWARM or runtime state.

- It does not emit NEXY `accepted` or `rejected` events.
- It does not auto-promote a proposal.
- It does not mutate `goif74945-crypto/NEXY.AI-`.
- Its strongest positive result is advisory compatibility evidence.
- UNKNOWN / WIP / INSUFFICIENT_EVIDENCE never becomes CUT by coercion.

## Evidence pins
- Spec: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20261001-010334).docx`
- Spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- NEXY repo: `goif74945-crypto/NEXY.AI-`
- NEXY branch: `NEXY.ai`
- NEXY inspected commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- inspected state matrix blob: `27e1281fba330784cc3bf2c30e9e1e82f951479b`
- inspected judge consensus blob: `d4ab4821182ab896b2c76941253d35111eb1f77c`
- inspected LAW prerelease blob: `f0ae1b06774e11cb2c0f417bc36c0d398347b036`
- inspected Q64.64 core blob: `e0e1d4b3fa47d40ac9b30ae14ea8b7ae0ac58313`

## Verified artifact
The exact tested 40-file project is preserved in `bundle/VERIFIED_ARTIFACT.tar.xz.b64.part-00..04`.

Archive SHA-256:
`33fc410780ebfb819130453f0995c8e45c692c18fb321662745b9371ef47c90f`

Reconstruction:
```bash
cat bundle/VERIFIED_ARTIFACT.tar.xz.b64.part-* | base64 -d > VERIFIED_ARTIFACT.tar.xz
echo "33fc410780ebfb819130453f0995c8e45c692c18fb321662745b9371ef47c90f  VERIFIED_ARTIFACT.tar.xz" | sha256sum -c -
mkdir recovered
tar -xJf VERIFIED_ARTIFACT.tar.xz -C recovered
cd recovered
sha256sum -c MANIFEST.sha256
npm run verify
```

## Verification summary
- TypeScript strict compile: PASS
- tests: 28/28 PASS
- static forbidden-surface audit: PASS, 0 hits
- SAT solver vs independent brute-force truth-table: 180 deterministic formulas PASS
- implication prover vs independent brute-force check: 576 formula pairs PASS
- replay safe case SHA-256: `9178c7c029a89e8d62d282abb4d6ea354e5c6a9ebbef6376335ce16416365763`
- replay conflict case SHA-256: `e9b2949531cd288af4e805b31ce1d8e56656879da513b11d48e061abd0ce40e6`

## Honest evidence ceiling
Local isolated verification proves this supplemental implementation at its tested bytes. It does **not** prove NEXY runtime integration, E2E deployment, Canon acceptance, or production readiness.
