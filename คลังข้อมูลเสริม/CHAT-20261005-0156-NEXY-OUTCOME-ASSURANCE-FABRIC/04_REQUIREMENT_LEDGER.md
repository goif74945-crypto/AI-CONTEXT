# Requirement Ledger

| ID | Requirement | Implementation | Evidence |
|---|---|---|---|
| OAF-R001 | Exactly five engines must be callable independently. | compiler/verifier/frontier/regression/recovery modules | unit + CLI tests |
| OAF-R002 | Contract compilation must reject unknown fields. | `compiler.py` | adversarial unit |
| OAF-R003 | Contract IDs and reports must use canonical deterministic hashing. | `canonical.py` | unit + 100 replay test |
| OAF-R004 | Hard criteria cannot be masked by soft criteria. | `verifier.py` | property test |
| OAF-R005 | Forbidden effects cannot be masked by other success. | `verifier.py` | unit + property test |
| OAF-R006 | Missing material observation must FREEZE. | `verifier.py` | unit |
| OAF-R007 | Invalid numeric observation must FREEZE and remain canonicalizable. | `verifier.py` | adversarial unit; repaired defect |
| OAF-R008 | Soft-only failure must be distinguishable as PARTIAL. | `verifier.py` | unit |
| OAF-R009 | OSF must preserve nondominated tradeoffs. | `frontier.py` | Pareto test |
| OAF-R010 | OSF must reject FAIL/FREEZE candidates. | `frontier.py` | unit + property test |
| OAF-R011 | Duplicate candidate IDs must be rejected. | `frontier.py` | unit |
| OAF-R012 | BRG must detect protected benefit regression independently of weighted score. | `regression.py` | unit + property test |
| OAF-R013 | BRG must support bounded directional regression tolerance. | `regression.py` | unit |
| OAF-R014 | Recovery search must respect max cost/risk. | `recovery.py` | unit paths + code invariant |
| OAF-R015 | Recovery can require reversibility. | `recovery.py` | unit |
| OAF-R016 | Conflicting repair effects must not be combined. | `recovery.py` | unit/adversarial |
| OAF-R017 | Recovery result must simulate to full PASS. | `recovery.py` | unit/integration |
| OAF-R018 | Exact search must be explicitly bounded. | `recovery.py` max 16 actions | unit |
| OAF-R019 | NaN/Infinity budgets/actions must be rejected. | `recovery.py` | adversarial unit |
| OAF-R020 | Core must use no network/model/clock/random/filesystem/env/subprocess I/O. | core source | static source audit |
| OAF-R021 | CLI malformed input must fail closed. | `cli.py` | CLI integration |
| OAF-R022 | All five engines must compose in one integration pipeline. | `pipeline.py` | integration test |
| OAF-R023 | JSON schemas must be syntactically valid. | `schemas/` | `python -m json.tool` |
| OAF-R024 | No write to NEXY.AI repositories is allowed. | mission scope | repository mutation audit |
| OAF-R025 | Every OAF concept must remain advisory/not canon. | docs/integration contract | document audit |
