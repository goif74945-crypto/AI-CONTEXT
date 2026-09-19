# Canonical NEXY Skill Runtime

Runtime root: `skills/nexy/runtime`
Repository target: `goif74945-crypto/AI-CONTEXT`

## Canonical resolution

The verified current `AI-CONTEXT@main` tree contained 119 tracked paths, 77 non-empty files, and zero executable-source files. The existing Master Specification explicitly leaves the concrete Skill runtime/loader unspecified. This runtime therefore constitutes the first in-repository executable Skill runtime established by the current user command.

## Runtime chain

`LOAD -> RESOLVE -> AUTHORIZE -> EXECUTE -> VALIDATE -> EVIDENCE -> RESULT`

Critical failure is fail-closed:

`SAFETY-CRITICAL FAILURE -> FREEZE`

Non-critical execution errors return `FAILURE`.

## Target bindings

Exactly seven formal Skills are bound:

`GOV-001`, `GOV-002`, `CTX-001`, `CTX-003`, `REQ-001`, `ARC-001`, `ARC-004`.

Every result, evidence, error and checkpoint record has a deterministic identifier. Evidence contains the execution ID, Skill ID, result ID, source HEAD, full chain and SHA-256 content hash.

## Test entry

Run:

`PYTHONPATH=. python3 -m unittest discover -s skills/nexy/runtime/tests -p 'test_*.py' -v`

The tests exercise the real runtime implementation, not a documentation-only check.
