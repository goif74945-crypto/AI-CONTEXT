# Failure and Security Model

## Failure semantics

| Condition | Result |
|---|---|
| malformed contract / unknown contract field | compiler error; CLI `FREEZE`, exit 2 |
| missing required observation path | `FREEZE` |
| invalid/non-finite numeric observation | `FREEZE` + `invalid_observations` |
| hard acceptance criterion violated | `FAIL` |
| forbidden effect observed | `FAIL` |
| only soft criteria violated | `PARTIAL` |
| frontier candidate is FAIL/FREEZE | candidate rejected from frontier |
| protected benefit regresses | BRG `FAIL` even if overall soft score rises |
| recovery has conflicting effects | conflicting combination excluded |
| recovery has no full-PASS admissible plan | ORP `FAIL / no_admissible_plan` |
| >16 recovery actions for exact v1 search | planning error; CLI fails closed |

## Threats addressed

### Metric masking
An aggregate score can hide a severe protected-benefit regression. BRG is separate from weighted score and checks guarded criteria directly.

### Unknown-field semantic injection
A caller could attempt to smuggle policy through an ignored JSON key. OCC and compiled-contract reconstruction reject unknown fields.

### Observation poisoning with malformed numeric values
`NaN`, `Infinity`, strings in numeric criteria, and missing paths must not become ordinary hard/soft failures. They are observation-integrity failures and therefore FREEZE.

### Recovery plan escalation
ORP does not run actions. It can require all candidate actions to be reversible and applies cost/risk budgets. A future NEXY adapter must still enforce actual authority/effect controls.

### Hash ambiguity
Canonical JSON rejects non-finite numbers and sorts keys. Contract/report identity is SHA-256 of the canonical representation.

## Non-goals

Reference v1 does not provide:
- cryptographic signatures or key management;
- observation provenance collection;
- distributed consensus;
- probabilistic sensor fusion;
- real side-effect execution;
- production sandboxing;
- external authorization.

Those require separate evidence classes and are not implied by these tests.
