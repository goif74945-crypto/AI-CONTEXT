# Canonical NEXY Skill Runtime

Runtime root: skills/nexy/runtime
Canonical machine registry: skills/registry/registry.json
Repository: goif74945-crypto/AI-CONTEXT
Execution backend: skills/nexy/runtime/runtime.py

Registry lifecycle:
DISCOVER -> SELECT -> LOAD -> COMPOSE -> EXECUTE -> VERIFY

Scoped NEXY execution chain:
LOAD -> RESOLVE -> AUTHORIZE -> EXECUTE -> VALIDATE -> EVIDENCE -> RESULT

The canonical registry provides identity and routing. The runtime backend enforces Skill-level permissions and executes the seven scoped NEXY Skills.

Target IDs:
GOV-001, GOV-002, CTX-001, CTX-003, REQ-001, ARC-001, ARC-004

Each target registry entry binds:
ID -> source_path -> load_path -> locator -> permissions -> validator -> evidence_handler -> tests

Critical failures fail closed:
execution failure -> FAILURE
safety-critical failure -> FREEZE

Every execution, result, evidence, error, authorization token, and checkpoint has a deterministic identifier.

Reproducible validation:
PYTHONPATH=. python3 -m unittest discover -s skills/nexy/runtime/tests -p 'test_*.py' -v
PYTHONPATH=. python3 -m skills.nexy.runtime.audit
PYTHONPATH=. python3 skills/nexy/runtime/completion_proof_v2.py
