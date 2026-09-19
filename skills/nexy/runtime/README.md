# NEXY Skill Runtime — NOT VERIFIED

Runtime root: skills/nexy/runtime
Machine registry: skills/registry/registry.json
Repository: goif74945-crypto/AI-CONTEXT
Execution backend candidate: skills/nexy/runtime/runtime.py

Registry lifecycle:
DISCOVER -> SELECT -> LOAD -> COMPOSE -> EXECUTE -> VERIFY

Scoped execution chain implemented by the candidate runtime:
LOAD -> RESOLVE -> AUTHORIZE -> EXECUTE -> VALIDATE -> EVIDENCE -> RESULT

Target IDs:
GOV-001, GOV-002, CTX-001, CTX-003, REQ-001, ARC-001, ARC-004

Current verification state:
- registry target status: MATERIALIZED / NOT_VERIFIED
- canonical runtime/loader mechanism: UNSPECIFIED by the authoritative Master Specification
- canonicality of runtime.py: NOT VERIFIED
- behavioral evidence: candidate-runtime only; does not prove real source-driven Skill behavior

The candidate runtime is retained for forensic traceability. It MUST NOT be represented as canonical or VERIFIED until an authoritative runtime/loader contract is established and the runtime is proven against it.

Critical failures fail closed:
execution failure -> FAILURE
safety-critical failure -> FREEZE

Every execution, result, evidence, error, authorization token, and checkpoint has a deterministic identifier within the candidate implementation.

Reproducible validation:
PYTHONPATH=. python3 -m unittest discover -s skills/nexy/runtime/tests -p 'test_*.py' -v
PYTHONPATH=. python3 -m skills.nexy.runtime.audit
PYTHONPATH=. python3 skills/nexy/runtime/completion_proof_v2.py
