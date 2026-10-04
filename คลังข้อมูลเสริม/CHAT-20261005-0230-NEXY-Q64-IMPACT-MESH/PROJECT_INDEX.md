# NEXY Q64 Impact Mesh - Project Index

Classification: `Lo4_AI_PROPOSAL_ONLY / NON_GOVERNING / REFERENCE_IMPLEMENTATION`
Execution ID: `CHAT-20261005-0230-NEXY-Q64-IMPACT-MESH`
Platform chat ID: `UNKNOWN_NOT_EXPOSED_TO_TOOL_RUNTIME`

This task contains a byte-preserved tested project snapshot split into four binary XZ parts to make concurrent GitHub persistence safer.

## Reassemble
```bash
cat artifact/nqim_project.tar.xz.part00 \
    artifact/nqim_project.tar.xz.part01 \
    artifact/nqim_project.tar.xz.part02 \
    artifact/nqim_project.tar.xz.part03 > nqim_project.tar.xz
sha256sum nqim_project.tar.xz
# expected: 6958bc0713c95b334fc0597d6a6f59f7db0ab29bc439f48de584f87e3f5e740f
tar -xJf nqim_project.tar.xz
```

## Twenty engines
OCL, RRG, BRB, DDI, RDM, UFB, LVD, FSS, CRI, CSD, RPG, PSM, BSA, SME, VLD, IGO, SRE, DCA, ECG, CMB.

## Verified local commands
```bash
python -m py_compile src/nqim/*.py tests/*.py tools/*.py
PYTHONHASHSEED=1 python -W error -X dev tests/test_nqim.py
PYTHONHASHSEED=999 python -W error -X dev tests/test_nqim.py
PYTHONHASHSEED=1 python tests/stress_nqim.py
PYTHONHASHSEED=999 python tests/stress_nqim.py
PYTHONHASHSEED=1 python tools/deep_validation.py
PYTHONHASHSEED=999 python tools/deep_validation.py
python tools/static_audit.py
```

The archive includes Design, Architecture, Failure Log, Novelty Audit, Integration Contract, Test Plan, Evidence, source, tests, tools and raw evidence. It does not mutate or integrate with any `NEXY.AI` repository.
