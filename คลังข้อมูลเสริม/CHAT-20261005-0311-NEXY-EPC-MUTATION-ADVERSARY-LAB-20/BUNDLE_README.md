# EPC Mutation Adversary Laboratory 20 — Bundle Reconstruction

Truth class: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

The exact standalone Design + Code + Tests + Evidence are preserved as eight base64 text parts under `bundle/`.

## Reconstruct

```bash
cat bundle/BUNDLE.part-*.b64 | base64 -d > EPC_MUTATION_ADVERSARY_LAB_20.tar.gz
sha256sum EPC_MUTATION_ADVERSARY_LAB_20.tar.gz
# expected: a4ce20cd6d25bb1170017de8cab1e59a17ff0f2a1be61f0b1d88050a7cb1fc89
tar -xzf EPC_MUTATION_ADVERSARY_LAB_20.tar.gz
cd epc_mutation_lab
sha256sum MANIFEST.sha256
# expected: 55d96963950a5db3bc8896b9b267bf8ee81dbbf2818d87f5f76ec7a7b14fab38
python run_verification.py
python independent_verify.py evidence/campaign.json
```

## Verified local seal before publication
- archive SHA-256: `a4ce20cd6d25bb1170017de8cab1e59a17ff0f2a1be61f0b1d88050a7cb1fc89`
- manifest SHA-256: `55d96963950a5db3bc8896b9b267bf8ee81dbbf2818d87f5f76ec7a7b14fab38`
- manifest-tracked files: 35
- unit/adversarial tests: 39 PASS
- pairwise mutant compositions: 190
- mutation campaign: 20/20 killed, 0 escaped
- mutation score Q64.64 raw: `18446744073709551616` = exact 1.0
- NEXY integration/runtime/deployment: NOT_VERIFIED

This bundle contains no authorized mutation to any repository whose name contains `NEXY.AI`.
