# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority and scope before reading code.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Use only: PASS / FAIL / PARTIAL / NOT IMPLEMENTED / NOT VERIFIED / UNKNOWN / BLOCKED / CONFLICT / SCOPE where applicable.
5. File existence, docs, mocks, build success, or comments are never runtime proof.
6. Search failure history and known conflicts before declaring a new root cause.
7. Preserve evidence even when verdict is FAIL.

# Workflow: Audit Authority / Supersession

## Sequence
1. Classify question: current build, future domain, implementation truth, runtime truth, deployment or physical.
2. Resolve scope first.
3. Traverse authority graph.
4. Traverse claim/requirement supersession.
5. Inspect unresolved conflict records.
6. Search implementation for lower-authority bypass.
7. Verify descriptive code state is not being used to redefine normative source.

## Attack cases
- future feature treated as current MUST;
- old claim overrides newer claim;
- UI/storage/agent becomes decision authority;
- Owner/Architect generic force path bypasses operational law;
- source-only physical claim reported as proven.

## DONE
Every authority decision is explainable as source + scope + supersession path.
