# NEXY.AI Skill System — Master Specification

**Specification status:** SOURCE-DERIVED / BUILD BASELINE
**Primary source:** `NEXY สกิว.pdf`
**Secondary context:** `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
**Purpose:** canonical build/validation baseline for NEXY Skills; this document does not claim implementation completion.

> **Authority rule:** This specification derives Skill identities, responsibilities, controls, validation, and operating rules from `NEXY สกิว.pdf`. Where the PDF does not specify a concrete mechanism, provider, numeric limit, or implementation detail, the value remains `UNSPECIFIED` / `UNKNOWN` and MUST NOT be invented.

## 1. Objective

Build NEXY.AI Skills as controlled, evidence-producing units whose identity, authority, scope, inputs, outputs, behavior, constraints, failure handling, validation, and evidence are traceable to the NEXY Skill specification.

Every Skill MUST:
- operate within declared authority and scope;
- use current verified context rather than stale context;
- preserve compatibility and data integrity;
- recognize `UNKNOWN` and stop/freeze when critical uncertainty cannot be resolved;
- never fabricate evidence or claim completion without proof;
- expose declared dependencies when invoking another Skill;
- undergo structural, source/spec, behavioral, security, architecture, integration, regression, evidence, and completion validation as applicable.

## 2. Source-of-Truth and Authority

### Primary
`NEXY สกิว.pdf`

### Secondary
`แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx` is contextual material and MUST NOT silently override the Skill specification.

### External Skill archives
`agent-skills-main.zip`, `skills-main.zip`, and `skills-main-2.zip` are reference-only. Their imported Skills MUST NOT be treated as NEXY-native requirements or implementations merely because a similarly named `SKILL.md` exists.

## 3. Universal Skill Contract

### Required Inputs
Every Skill receives at minimum:

- `task`
- `authority`
- `scope`
- `repository`
- `branch`
- `head`
- `source_of_truth`
- `constraints`
- `expected_output`
- `validation_requirements`

If required information is missing: `UNKNOWN`.
If missing information is necessary to execute safely: `BLOCKED`.

### Required Outputs
Every Skill returns at minimum:

- `status`
- `objective`
- `scope`
- `inputs`
- `actions`
- `changed_files`
- `unchanged_files`
- `validation`
- `evidence`
- `errors`
- `unknowns`
- `remaining`
- `next_action`

For modification Skills additionally:

- `diff`
- `impact`
- `tests`
- `rollback`

### Evidence Contract
A statement equivalent to “checked” is insufficient. Evidence MUST identify:

`WHAT → WHERE → HOW → RESULT → EVIDENCE`

Example structure from the specification:
`File → validation method → PASS/FAIL → test result + affected source + diff`.

## 4. Immutable Rules

Every NEXY Skill inherits:

1. DO NOT GUESS.
2. DO NOT INVENT.
3. DO NOT FABRICATE EVIDENCE.
4. DO NOT CLAIM COMPLETION WITHOUT PROOF.
5. DO NOT BYPASS AUTHORITY.
6. DO NOT BYPASS SECURITY.
7. DO NOT BYPASS VALIDATION.
8. DO NOT EXPAND SCOPE.
9. DO NOT HIDE FAILURE.
10. DO NOT TURN UNKNOWN INTO FACT.
11. DO NOT TURN OVERLAP INTO DUPLICATE.
12. FREEZE WHEN CRITICAL UNCERTAINTY REMAINS.
13. PRESERVE COMPATIBILITY.
14. PRESERVE DATA INTEGRITY.
15. VERIFY BEFORE REPORTING.

## 5. API / Tool Policy

The PDF defines Skill permissions and capability boundaries, but does **not** establish a universal concrete external provider/tool list. Therefore:

- only APIs/tools actually authorized by the current repository/runtime/source may be used;
- a provider MUST NOT be invented from a generic capability name;
- `nexy-web-retrieval` MUST NOT assume Google, Bing, Playwright, browser automation, crawler, scraper, or a specific external API as its canonical mechanism because the PDF explicitly marks the retrieval mechanism as a gap;
- tool use MUST remain within the Skill's permission profile and declared scope;
- a Skill MUST NOT bypass Control Skills to obtain a capability.

### Permission vocabulary defined by the PDF

`READ`, `ANALYZE`, `PLAN`, `WRITE`, `DELETE`, `EXECUTE`, `TEST`, `COMMIT`, `DEPLOY`, `RELEASE`.

The PDF gives design examples such as context = READ-only, requirement = READ-only, code = READ/WRITE/TEST, modify = READ/WRITE/TEST, test = READ/TEST, verify = READ/TEST with release capability only through the required authority/release gate, and deploy = READ/limited WRITE/TEST/COMMIT/DEPLOY subject to authority/release gates.

These are permission-model specifications, not proof that the current repository already enforces them.

## 6. Architecture

### Skill hierarchy

```text
GOVERNANCE
    ↓
AUTHORITY
    ↓
CONTEXT
    ↓
REQUIREMENT
    ↓
ARCHITECTURE
    ├── ENGINEERING
    ├── CORE
    └── SECURITY
         ├── WEB / API
         ├── AI
         └── VAULT / DATA
    ↓
TEST
    ↓
VERIFY
    ↓
RELEASE
    ↓
RELEASE / FREEZE
```

### Core dependency flow

```text
nexy-context
    ↓
nexy-authority
    ↓
nexy-requirement
    ↓
nexy-scope-guard
    ↓
nexy-architecture
    ↓
nexy-architecture-impact
    ├───────────────┐
    ↓               ↓
nexy-code       nexy-web
    ↓               ↓
nexy-modify     nexy-api
    └───────┬───────┘
            ↓
    nexy-integration
            ↓
        nexy-test
            ↓
        nexy-verify
            ↓
    nexy-release-gate
         ┌──┴──┐
         ↓     ↓
      RELEASE FREEZE
```

### Skill-to-Skill safety

Dependencies MUST be declared explicitly. Implicit dependencies are forbidden. Recursive Skill execution MUST detect cycles and enforce a maximum execution depth, but the PDF does not specify the numeric maximum; therefore that value remains `UNSPECIFIED` until an authoritative implementation requirement exists.

## 7. Dependencies

Dependencies are governed by the dependency graph above plus each Skill's declared dependency set.

A Skill calling another Skill MUST declare the dependency.

Example specified in the PDF:

`nexy-modify` requires:
- `nexy-context`
- `nexy-authority`
- `nexy-scope-guard`
- `nexy-architecture`
- `nexy-test`

No implicit dependency is permitted.

## 8. Security

Security is a cross-cutting gate, not an optional post-build step.

Required principles:
- authority enforcement;
- backend RBAC enforcement where applicable;
- input/schema validation;
- session/security controls where applicable;
- auditability;
- security review;
- abuse/negative testing;
- freeze on critical security uncertainty or violation;
- no bypass of security gates.

The PDF identifies the roles `OWNER`, `OPERATOR`, `AUDITOR`, `SYSTEM`, and `PUBLIC_USER`; RBAC enforcement is required at the backend for the RBAC Skill.

## 9. Performance

Performance MUST be validated where a Skill's requirement or implementation exposes performance constraints.

The PDF requires performance to be considered by `nexy-code-review` and requires pipeline timeout compliance for `nexy-pipeline`, but it does **not** provide a universal numeric latency/throughput target for every Skill in this Master Specification.

Therefore:
- do not invent universal latency budgets;
- use source-defined timeout/performance requirements when present;
- if a required performance threshold is absent, mark it `UNSPECIFIED` rather than guessing;
- performance failure that is critical under the applicable specification is a validation failure and may trigger FREEZE.

## 10. Failure Conditions / Freeze Protocol

A Skill MUST understand and propagate `FREEZE`.

Freeze triggers defined by the PDF include:
- authority conflict;
- architecture conflict;
- security uncertainty;
- data-integrity risk;
- contract mismatch;
- critical test failure;
- critical agent failure;
- insufficient evidence;
- release-gate failure;
- unresolved source conflict;
- scope violation/expansion;
- unknown architecture where execution requires certainty.

General rule:

```text
UNKNOWN
   ↓
Can resolve?
 ┌──┴──┐
YES   NO
 ↓     ↓
CHECK FREEZE
 ↓
VALIDATE
```

A failure MUST NOT be converted into success merely to satisfy a count.

## 11. Master Skill Inventory

The following formal identities are extracted from the PDF. The formal ID is the identity key. Similar names across families remain separate identities and MUST NOT be merged without authoritative resolution.

### Family 00 — GOVERNANCE

| ID | Skill | Objective / responsibility |
|---|---|---|
| GOV-001 | `nexy-authority` | Determine which source has authority over a decision; distinguish AUTHORITATIVE / SUPPORTING / HISTORICAL / UNKNOWN. |
| GOV-002 | `nexy-scope-guard` | Prevent feature creep, out-of-scope refactor, rename/delete, architecture change, and unauthorized dependency additions. |
| GOV-003 | `nexy-change-control` | Control modifications and record CHANGE_ID, request, affected files/modules, contract/security/test impact, rollback. |
| GOV-004 | `nexy-risk-gate` | Assess data-loss, security, compatibility, architecture, determinism, and release risks; critical unknown freezes. |

### Family 01 — CONTEXT

| ID | Skill | Objective / responsibility |
|---|---|---|
| CTX-001 | `nexy-context` | Load required current project, architecture, requirements, repository, branch, HEAD, files, registry, and validation state. |
| CTX-002 | `nexy-repository-context` | Inspect repository, branch, HEAD, working state, and relevant tree before code changes. |
| CTX-003 | `nexy-source-inspector` | Inspect real source and identify file, path, type, dependencies, callers, callees, contracts, and tests. |
| CTX-004 | `nexy-context-diff` | Compare previous/current/expected state to prevent stale context. |

### Family 02 — REQUIREMENT

| ID | Skill | Objective / responsibility |
|---|---|---|
| REQ-001 | `nexy-requirement` | Convert a command into objective, in-scope, out-of-scope, input, output, constraint, acceptance, and validation. |
| REQ-002 | `nexy-requirement-decomposer` | Decompose requirements into functional, technical, security, data, UI, test, and release aspects. |
| REQ-003 | `nexy-requirement-trace` | Trace Requirement → Design → File → Implementation → Test → Evidence; missing test/evidence remains UNVERIFIED. |
| REQ-004 | `nexy-conflict-resolution` | Detect requirement conflict and resolve only through authoritative source; unresolved conflict is BLOCKED. |

### Family 03 — ARCHITECTURE

| ID | Skill | Objective / responsibility |
|---|---|---|
| ARC-001 | `nexy-architecture` | Understand actual NEXY architecture including core-kernel, packages, apps, contracts, auth, API, web, tests, deployment. |
| ARC-002 | `nexy-boundary` | Verify module boundaries and prevent invalid dependencies across boundaries. |
| ARC-003 | `nexy-dependency-analysis` | Analyze direct/transitive dependencies, cycles, API compatibility, build impact, and test impact. |
| ARC-004 | `nexy-architecture-impact` | Report affected modules, contracts, state, tests, security, and release impact of a change. |

### Family 04 — ENGINEERING

| ID | Skill | Objective / responsibility |
|---|---|---|
| ENG-001 | `nexy-code` | Create code supported by inspected source; do not assume a language/stack is canonical unless source supports it. |
| ENG-002 | `nexy-modify` | Controlled code modification: Inspect → Understand → Impact → Plan → Modify → Compile → Test → Diff → Evidence. |
| ENG-003 | `nexy-debug` | Failure → Reproduce → Observe → Evidence → Localize → Hypothesis → Verify → Root Cause → Fix → Regression. Root cause requires proof. |
| ENG-004 | `nexy-refactor` | Refactor only when scope permits; preserve behavior, API, contracts, state semantics, security, tests, compatibility. |
| ENG-005 | `nexy-code-review` | Review correctness, architecture, security, performance, maintainability, tests, and scope. |
| ENG-006 | `nexy-migration` | Gate schema/data/API/dependency/module/architecture migrations with migration and applicable rollback/evidence. |
| ENG-007 | `nexy-dependency` | Govern dependency additions/changes: why, source, version, license, required location, security, compatibility, build, lockfile. |

### Family 05 — WEB

| ID | Skill | Objective / responsibility |
|---|---|---|
| WEB-001 | `nexy-web` | Create/modify the web application according to source/spec. |
| WEB-002 | `nexy-ui` | Create UI while preserving state truth, permissions, loading, error, freeze, and success behavior. |
| WEB-003 | `nexy-page` | Create page according to route specification. |
| WEB-004 | `nexy-form` | Create forms with schema validation, authorization, error, submission, and state handling. |
| WEB-005 | `nexy-ui-truth` | Ensure UI reflects actual backend state; backend FREEZE must be represented as UI FREEZE, not fake success. |
| WEB-006 | `nexy-web-integration` | Integrate UI → API → contracts and verify response, error, loading, authorization. |
| WEB-007 | `nexy-web-validation` | Validate type, build, route, API, integration, state, permissions, freeze, and error behavior. |

### Family 06 — API

| ID | Skill | Objective / responsibility |
|---|---|---|
| API-001 | `nexy-api` | Create/modify API endpoint through Request → Schema → Auth → RBAC → Validation → Business Rule → Core → Response → Audit. |
| API-002 | `nexy-contract` | Manage API contracts and inspect consumers before changing a contract. |
| API-003 | `nexy-api-validation` | Validate request, response, errors, auth, RBAC, schema, and status. |
| API-004 | `nexy-api-integration` | Validate UI/API/Core integration. |
| API-005 | `nexy-api-security` | Test API abuse: unauthorized access, invalid input, rate limit, CSRF where applicable, session, and RBAC. |

### Family 07 — CORE

| ID | Skill | Objective / responsibility |
|---|---|---|
| CORE-001 | `nexy-core` | Work with core-kernel without bypassing core law. |
| CORE-002 | `nexy-state-machine` | Manage state transitions; each transition must be valid, authorized, deterministic, and auditable. |
| CORE-003 | `nexy-law` | Check law/policy before execution. |
| CORE-004 | `nexy-freeze` | Manage FREEZE triggered by critical failure, contradiction, insufficient evidence, timeout, policy violation, or consensus failure. |
| CORE-005 | `nexy-determinism` | Verify deterministic execution according to requirements. |
| CORE-006 | `nexy-recovery` | Manage recovery after FREEZE without converting a freeze into success without evidence. |

### Family 08 — AI / SWARM

| ID | Skill | Objective / responsibility |
|---|---|---|
| AI-001 | `nexy-agent` | Manage agent execution contract. |
| AI-002 | `nexy-agent-adapter` | Connect an agent to the canonical interface. |
| AI-003 | `nexy-swarm` | Orchestrate Decompose → Parallel → Adversarial → Cross Verify → Consensus. |
| AI-004 | `nexy-consensus` | Evaluate consensus. |
| AI-005 | `nexy-adversarial` | Check counter-evidence and contradiction. |
| AI-006 | `nexy-agent-failure` | Handle timeout, error, invalid output, contradiction, and missing evidence. |
| AI-007 | `nexy-pipeline` | Control end-to-end execution and obey specification-defined timeouts. |

### Family 09 — DATA / EVIDENCE

| ID | Skill | Objective / responsibility |
|---|---|---|
| DATA-001 | `nexy-data` | Manage data lifecycle. |
| DATA-002 | `nexy-evidence` | Manage Evidence objects and supported source categories such as DOCUMENT, WEB, MODEL, USER_INPUT, INTERNAL. |
| DATA-003 | `nexy-provenance` | Ensure important evidence records source, origin, description, hash, and verification. |
| DATA-004 | `nexy-integrity` | Verify hash/content integrity. |
| DATA-005 | `nexy-evidence-verifier` | Classify evidence as VERIFIED, UNVERIFIED, CONTRADICTED, or UNKNOWN. |
| DATA-006 | `nexy-web-retrieval` | Define web retrieval as an interface/policy capability only until an authoritative retrieval mechanism is established. PDF status: DESIGN/GAP. |
| DATA-007 | `nexy-data-transform` | Transform data while preserving provenance: INPUT → TRANSFORM → OUTPUT → PROVENANCE. |

### Family 10 — SECURITY

| ID | Skill | Objective / responsibility |
|---|---|---|
| SEC-001 | `nexy-auth` | Support authentication according to implementation/spec, including OTAC, session, and logout where applicable. |
| SEC-002 | `nexy-session` | Verify session lifecycle, expiry, cookie/security, and revocation. |
| SEC-003 | `nexy-rbac` | Verify OWNER, OPERATOR, AUDITOR, SYSTEM, PUBLIC_USER and enforce RBAC at backend. |
| SEC-004 | `nexy-security` | General security engineering. |
| SEC-005 | `nexy-security-review` | Review authentication, authorization, input, data, dependencies, secrets, and logging. |
| SEC-006 | `nexy-audit` | Create/verify audit events. |
| SEC-007 | `nexy-incident` | Manage security, system, and freeze incidents. |
| SEC-008 | `nexy-abuse-test` | Test abuse scenarios. |

### Family 11 — VAULT / STATE

| ID | Skill | Objective / responsibility |
|---|---|---|
| VLT-001 | `nexy-vault` | Manage Vault. |
| VLT-002 | `nexy-artifact` | Manage Artifact lifecycle. |
| VLT-003 | `nexy-revision` | No overwrite; new content creates a new revision with monotonic revision/hash semantics. |
| VLT-004 | `nexy-commit` | Manage commit semantics. |
| VLT-005 | `nexy-integrity` | Verify artifact integrity. |
| VLT-006 | `nexy-concurrency` | Verify optimistic concurrency and revision conflicts. |

### Family 12 — TEST / VERIFICATION

| ID | Skill | Objective / responsibility |
|---|---|---|
| TEST-001 | `nexy-test` | Test orchestration. |
| TEST-002 | `nexy-unit-test` | Unit-level validation. |
| TEST-003 | `nexy-contract-test` | Validate API/schema contracts. |
| TEST-004 | `nexy-integration-test` | Validate module boundaries. |
| TEST-005 | `nexy-e2e-test` | Validate real flows. |
| TEST-006 | `nexy-security-test` | Security regression testing. |
| TEST-007 | `nexy-regression` | After modification, validate the affected regression surface. |
| TEST-008 | `nexy-build-test` | Validate compile, typecheck, and build. |

### Verification

| ID | Skill | Objective / responsibility |
|---|---|---|
| VER-001 | `nexy-verify` | Final verification controller: Requirement, Scope, Architecture, Security, Tests, Evidence. |
| VER-002 | `nexy-evidence-verify` | Verify evidence itself, not merely file existence. |
| VER-003 | `nexy-determinism-verify` | Verify deterministic requirement. |
| VER-004 | `nexy-consensus-verify` | Verify consensus result. |
| VER-005 | `nexy-release-gate` | Gate release. |
| VER-006 | `nexy-completion-proof` | Answer what evidence permits a completion declaration; if it cannot, status is NOT COMPLETE. |

### Family 13 — BUILD / RELEASE

| ID | Skill | Objective / responsibility |
|---|---|---|
| REL-001 | `nexy-build` | Build orchestration. |
| REL-002 | `nexy-ci` | Validate CI pipeline. |
| REL-003 | `nexy-deploy` | Deployment only after tests, verification, release policy, and evidence. |
| REL-004 | `nexy-migration` | Migration gate. |
| REL-005 | `nexy-release` | Release orchestration. |
| REL-006 | `nexy-recovery` | Deployment/release recovery. |

## 12. Identity Integrity

The PDF contains name collisions across formal IDs:

- `nexy-migration`: `ENG-006` and `REL-004`
- `nexy-recovery`: `CORE-006` and `REL-006`
- `nexy-integrity`: `DATA-004` and `VLT-005`

These MUST remain distinct formal identities unless an authoritative source resolves them. Do not merge, rename, or split them merely because names are equal.

The PDF also uses `nexy-integration` in the wave/graph context without a separate formal numbered identity in the extracted formal inventory. Do not invent a new ID to resolve this.

## 13. Skill Integrity Record

Each Skill identity is required by the PDF to contain:

- `id`
- `name`
- `version`
- `family`
- `authority`
- `dependencies`
- `status`
- `source_basis`

No two Skills may have the same identity.

## 14. SKILL.md Creation Pipeline

The required creation pipeline is:

```text
SOURCE
  ↓
IDENTITY
  ↓
REQUIREMENT
  ↓
BEHAVIOR
  ↓
INPUT / OUTPUT
  ↓
CONSTRAINT
  ↓
FAILURE
  ↓
VALIDATION
  ↓
EVIDENCE
  ↓
SKILL.md
```

A Skill MUST NOT be generated from its name alone.

## 15. SKILL.md Master Structure

The PDF presents the following proposed master structure:

```text
# NEXY Skill
## Identity
## Objective
## Authority
## Source of Truth
## Scope
### In Scope
### Out of Scope
## Inputs
### Required
### Optional
## Preconditions
## Outputs
## Workflow
### Phase 1 — Context
### Phase 2 — Authority
### Phase 3 — Requirement
### Phase 4 — Inspection
### Phase 5 — Execution
### Phase 6 — Validation
### Phase 7 — Evidence
## Required Behavior
## Forbidden Behavior
## Architecture Constraints
## Security Constraints
## Compatibility Constraints
## Data Integrity
## Failure Handling
## Freeze Conditions
## Validation
### Structural
### Functional
### Integration
### Regression
### Evidence
## Completion Criteria
## Stop Conditions
## Checkpoint
## Resume
## Error Reporting
## Examples
## Non-Goals
## Version
```

**Important:** the PDF labels this as a proposed standard structure. It is therefore the build baseline from the supplied Skill document, but any field that is not otherwise mandatory in authoritative requirements MUST NOT acquire invented semantics.

## 16. Quality Gates

Before a Skill is admitted as VERIFIED:

```text
GATE 0 — Identity
      ↓
GATE 1 — Specification
      ↓
GATE 2 — Implementation
      ↓
GATE 3 — Behavior
      ↓
GATE 4 — Security
      ↓
GATE 5 — Integration
      ↓
GATE 6 — Evidence
      ↓
VERIFIED
```

Failure at any gate = `NOT VERIFIED`.

## 17. Validation Matrix

Every important Skill is validated across:

| Layer | Validation |
|---|---|
| V0 | File integrity |
| V1 | `SKILL.md` structure |
| V2 | Source/spec alignment |
| V3 | Behavior |
| V4 | Security |
| V5 | Architecture |
| V6 | Integration |
| V7 | Regression |
| V8 | Evidence |
| V9 | Completion proof |

Passing a build or test suite alone does not satisfy the matrix.

## 18. Negative Testing

Important Skills require negative testing.

Examples explicitly defined by the PDF:

### `nexy-code`
- missing requirement → BLOCK
- unknown architecture → BLOCK
- invalid contract → BLOCK
- security violation → BLOCK
- test failure → NOT VERIFIED
- scope expansion → STOP

### `nexy-web`
- unauthorized UI action → BLOCK
- backend FREEZE → UI FREEZE
- invalid API response → ERROR
- fake success → FAIL

### `nexy-data`
- missing provenance → UNVERIFIED
- invalid hash → FAIL
- contradiction → BLOCK
- unknown source → UNKNOWN

## 19. Operating Model

Skills are not invoked as uncontrolled isolated workers when a task requires gates.

### Example: create web page

```text
nexy-context
↓
nexy-requirement
↓
nexy-scope-guard
↓
nexy-architecture
↓
nexy-web
↓
nexy-api (if required)
↓
nexy-test
↓
nexy-verify
```

### Example: fix bug

```text
nexy-context
↓
nexy-debug
↓
nexy-architecture-impact
↓
nexy-modify
↓
nexy-test
↓
nexy-regression
↓
nexy-verify
```

### Example: add API

```text
nexy-requirement
↓
nexy-contract
↓
nexy-api
↓
nexy-api-security
↓
nexy-contract-test
↓
nexy-integration-test
↓
nexy-verify
```

### Example: add AI Agent

```text
nexy-requirement
↓
nexy-architecture
↓
nexy-agent
↓
nexy-agent-adapter
↓
nexy-swarm
↓
nexy-adversarial
↓
nexy-consensus
↓
nexy-test
↓
nexy-verify
```

### Example: release

```text
build
↓
typecheck
↓
contract tests
↓
integration tests
↓
security tests
↓
evidence verification
↓
determinism verification
↓
release policy
↓
release gate
↓
DEPLOY / FREEZE
```

## 20. Wave Build Order

The PDF specifies this build order:

### Wave 1 — Foundation
`nexy-authority`, `nexy-context`, `nexy-source-inspector`, `nexy-requirement`, `nexy-scope-guard`, `nexy-architecture`, `nexy-architecture-impact`

### Wave 2 — Engineering
`nexy-code`, `nexy-modify`, `nexy-debug`, `nexy-code-review`, `nexy-dependency`, `nexy-refactor`

### Wave 3 — Application
`nexy-web`, `nexy-ui`, `nexy-page`, `nexy-form`, `nexy-ui-truth`, `nexy-api`, `nexy-contract`, `nexy-integration`

### Wave 4 — Core
`nexy-core`, `nexy-state-machine`, `nexy-law`, `nexy-freeze`, `nexy-determinism`, `nexy-recovery`

### Wave 5 — AI
`nexy-agent`, `nexy-agent-adapter`, `nexy-swarm`, `nexy-adversarial`, `nexy-consensus`, `nexy-pipeline`

### Wave 6 — Data
`nexy-data`, `nexy-evidence`, `nexy-provenance`, `nexy-integrity`, `nexy-evidence-verifier`, `nexy-data-transform`, `nexy-web-retrieval` `[GAP]`

### Wave 7 — Security
`nexy-auth`, `nexy-session`, `nexy-rbac`, `nexy-security`, `nexy-security-review`, `nexy-audit`, `nexy-incident`, `nexy-abuse-test`

### Wave 8 — Vault
`nexy-vault`, `nexy-artifact`, `nexy-revision`, `nexy-commit`, `nexy-concurrency`

### Wave 9 — Test
`nexy-test`, `nexy-unit-test`, `nexy-contract-test`, `nexy-integration-test`, `nexy-e2e-test`, `nexy-security-test`, `nexy-regression`, `nexy-build-test`

### Wave 10 — Verification
`nexy-verify`, `nexy-evidence-verify`, `nexy-determinism-verify`, `nexy-consensus-verify`, `nexy-release-gate`, `nexy-completion-proof`

### Wave 11 — Release
`nexy-build`, `nexy-ci`, `nexy-deploy`, `nexy-migration`, `nexy-release`, `nexy-recovery`

## 21. Repository Architecture Boundary

The PDF proposes the following Skill repository architecture after design approval:

```text
nexy-skills/
├── governance/
├── context/
├── requirements/
├── architecture/
├── engineering/
├── web/
├── api/
├── core/
├── ai-swarm/
├── data/
├── security/
├── vault/
├── testing/
├── verification/
├── release/
├── registry/
│   ├── skills.json
│   ├── dependencies.json
│   └── validation.json
├── schemas/
├── evidence/
└── checkpoints/
```

The PDF explicitly states that this is a suitable proposed structure after design and authorization; it is **not by itself an instruction to create this exact repository structure**.

## 22. Registry Specification

The proposed registry records:

- `id`
- `name`
- `family`
- `version`
- `status`
- `authority`
- `source_basis`
- `dependencies`
- `dependents`
- `permissions`
- `validation_level`
- `last_verified`
- `evidence`

Registry status MUST correspond to actual files and evidence. A stub MUST NOT be counted as complete.

## 23. Acceptance Criteria

A Skill is `VERIFIED` only when all applicable criteria are proven:

- `SKILL.md` exists and has the required structure;
- identity is correct;
- objective is correct;
- authority is declared;
- source of truth is declared;
- scope is explicit;
- required/optional inputs are explicit;
- outputs are explicit;
- workflow is defined;
- required behavior is defined;
- forbidden behavior is defined;
- architecture constraints are respected;
- security constraints are respected;
- compatibility/data-integrity constraints are respected;
- failure handling is defined;
- freeze conditions are defined;
- validation is executed;
- evidence is real and traceable;
- behavioral validation exists;
- required negative testing exists;
- dependencies are explicit;
- no unresolved critical conflict remains;
- no completion claim depends on unsupported assumptions.

## 24. Completion / Stop Criteria

### COMPLETE / VERIFIED is forbidden when
- evidence is missing;
- a required test has not run;
- behavior is unverified;
- a critical source conflict remains;
- required identity is unresolved;
- implementation differs from the source requirement;
- a placeholder is being counted as implementation;
- a required dependency is missing;
- a security gate failed;
- integration/regression evidence is missing.

### STOP / FREEZE when
- critical uncertainty cannot be resolved;
- source of truth cannot be established;
- scope is ambiguous in a way that affects architecture/data;
- authority conflicts remain unresolved;
- implementation would require inventing a provider/mechanism not specified by the source;
- validation cannot prove completion.

## 25. Checkpoint / Resume Contract

Large builds MUST maintain:

- `expected`
- `processed`
- `verified`
- `failed`
- `skipped`
- `blocked`
- `remaining`
- `current_item`
- `resume_point`
- `last_verified_source`
- `last_verified_head`

A checkpoint is evidence of progress, not evidence of completion.

## 26. Error Reporting Contract

Every material failure reports:

- `ERROR`
- `LOCATION`
- `IMPACT`
- `ROOT_CAUSE` — only when proven
- `RECOVERY`
- `CURRENT_STATUS`

## 27. Explicit Scope Fence

The PDF explicitly identifies capabilities that should **not** be promoted into NEXY Core Skills merely because they appear in vision/concept material:

- voice orchestration
- blockchain
- AR
- VR
- XR
- real-time 3D UI
- IoT
- quantum-safe crypto layer
- holographic UI
- self-patch
- auto-heal
- runtime public anonymous write

A future authoritative requirement may introduce additional Skill families; this specification does not invent them.

## 28. Web Retrieval Special Case

`nexy-web-retrieval` is explicitly a `DESIGN/GAP` in the PDF.

The source confirms the need to distinguish:

`DATA ≠ RETRIEVAL`

`EVIDENCE ≠ SOURCE ACQUISITION`

Until an authoritative source specifies the real retrieval mechanism, this Skill remains an interface/policy specification. Do not hard-code Google, Bing, Playwright, browser automation, crawler, scraper, or another specific provider as canonical.

## 29. Master Build Rule

The implementation process is:

```text
PDF SPEC
  ↓
MASTER REGISTRY
  ↓
SKILL IDENTITY
  ↓
SKILL REQUIREMENT
  ↓
SKILL.md
  ↓
IMPLEMENTATION
  ↓
BEHAVIOR VALIDATION
  ↓
SECURITY / INTEGRATION / REGRESSION
  ↓
EVIDENCE
  ↓
GATE 0–6
  ↓
VERIFIED
```

No shortcut is permitted.

## 30. Current Specification Limitations

This document intentionally does **not** invent:

- a universal numeric performance target;
- a concrete web-search provider;
- a browser/crawler/scraper provider;
- a Skill runtime/loader implementation;
- a Skill-to-Skill protocol beyond the declared dependency rule;
- a numeric recursive execution-depth limit;
- a concrete permission-enforcement implementation;
- a new Skill identity to resolve naming ambiguity.

These remain `UNSPECIFIED` / `UNKNOWN` until an authoritative source defines them.

## 31. Source Traceability

Primary traceability sections in `NEXY สกิว.pdf`:

- Skill families / formal identities: sections 5–19
- dependency graph: section 20
- Control vs Worker Skills: section 21
- permission model: section 22
- universal input contract: section 23
- universal output contract: section 24
- evidence contract: section 25
- FREEZE protocol: section 26
- checkpoint protocol: section 27
- Skill creation pipeline: section 28
- `SKILL.md` master structure: section 29
- completion criteria: section 30
- validation matrix: section 31
- negative testing: section 32
- Skill-to-Skill safety: section 33
- recursive execution: section 34
- Skill integrity: section 35
- duplicate/overlap classification: section 36
- operating model: sections 37–41
- web retrieval gap: section 42
- scope fence: section 43
- proposed repository architecture: section 44
- registry: section 45
- quality gates: section 46
- hierarchy: section 47
- immutable rules: section 48
- anti-placeholder rule: section 49
- wave build order: section 50

## 32. Status of This File

`MASTER-SPECIFICATION.md` is a **specification artifact**, not proof that all listed Skills have been implemented.

Implementation status MUST be established separately by file-level forensic inspection and validation evidence.
