# Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence |
|---|---|---|---|---|
| R1 | Additive AI-CONTEXT-only implementation | User + task contract | project folder only | GitHub readback |
| R2 | Never mutate NEXY.AI-named repos | User | no connector writes outside AI-CONTEXT | operation log/readback |
| R3 | Deterministic canonical inventory | NEXY principle + design | `canonical.py`, `engine.py` | unit tests |
| R4 | Fail closed on ambiguous/unsupported input | NEXY principle + design | parsers + engine | negative tests |
| R5 | Tamper-evident snapshots | design | snapshot seal verification | tamper tests |
| R6 | Deterministic drift classification | design | `diffing.py` | drift tests |
| R7 | Strict default policy with explicit exceptions | design | `policy.py` | policy tests |
| R8 | No third-party runtime dependencies | design | stdlib Python only | import/static inspection + tests |
| R9 | Machine-readable ALLOW/FREEZE result | design | engine + CLI | unit/CLI tests |
| R10 | Preserve future ideas as proposals only | User | `FUTURE-CONCEPTS.md` | file presence/readback |
| R11 | Do not persist credentials embedded in dependency source URLs | Security boundary + design | parser sanitization + violation | adversarial unit test |
| R12 | Bound raw input size before parsing | Security/resource integrity + design | `Policy.max_input_bytes`, engine pre-parse gate | adversarial unit test |
| R13 | Version drift must not mask registry-origin drift | Fail-closed drift semantics + design | `diffing.py` origin comparison | cross-origin regression test |
