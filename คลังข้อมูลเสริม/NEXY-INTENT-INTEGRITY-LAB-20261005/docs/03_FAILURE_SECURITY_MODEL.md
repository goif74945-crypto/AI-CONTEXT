# 03 — Failure and Security Model

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Threats this prototype attempts to expose

| Threat | Prototype behavior | Residual risk |
|---|---|---|
| Worker omits a mandatory requirement | `REQUIREMENT_COVERAGE_GAP` → FREEZE | Worker may falsely claim coverage without doing the work |
| Worker targets protected repository | `PROTECTED_REPOSITORY_TARGET` → FREEZE | Repository string is not cryptographic identity |
| Worker touches protected path | `PROTECTED_SCOPE_TOUCH` → FREEZE | Path model is not an OS sandbox |
| Worker expands scope | `UNAUTHORIZED_SCOPE_EXPANSION` → FREEZE | Repository identity is not cryptographically bound |
| Worker weakens evidence | `EVIDENCE_DOWNGRADE` → FREEZE | Global evidence ordering is simplified |
| Worker claims unverified completion | `UNVERIFIED_COMPLETION_CLAIM` → FREEZE | Truth-class labels themselves can be dishonest |
| Contract objective changes | transition drift → FREEZE unless exact approval | Approval envelope is not authenticated |
| Approval for A reused to approve B | exact change IDs prevent blanket use | Replay protection is not implemented |
| Key/order serialization changes | canonical digest remains stable | Canonicalizer policy may be wrong for future ordered arrays |

## Fail-closed principles

1. Unknown requirement references block the proposal.
2. Path traversal attempts are invalid input.
3. Missing required evidence blocks the proposal.
4. Protected and out-of-scope patterns take precedence over in-scope convenience.
5. Contract changes freeze unless explicitly approved by exact semantic change ID.

## Attacks not solved

### Dishonest proposal metadata
A malicious agent could mark a requirement as “covered” without actually implementing it. The guard needs external evidence binding to solve this.

### Forged approval JSON
The research prototype does not authenticate the human or spec owner. A real system would require signed/verified authority tokens.

### TOCTOU
A proposal can pass and the repository can change before execution. Production use would need repository/ref/commit binding and re-validation at mutation time.

### Symlink/filesystem escape
String path checks are not equivalent to secure filesystem confinement. A real executor needs OS/container-level isolation and canonical filesystem checks.

### Prompt injection
The guard consumes structured JSON. It does not sanitize untrusted content for downstream language models. Prompt-injection defense remains a separate layer.

### Semantic laundering
A requirement can be rewritten to hide weakened meaning while retaining an ID. The transition guard detects object inequality, but deciding whether an explicitly approved rewrite is safe remains an authority problem.

## Recommended adversarial test classes for future work

- Unicode normalization edge cases;
- Windows/Unix path separator mixtures;
- deep path traversal attempts;
- wildcard ambiguity;
- duplicate ID collision;
- stale approval replay;
- evidence-rank boundary cases;
- contract schema migration;
- concurrent contract revisions;
- mismatched repository identity;
- forged worker claims;
- partial multi-agent handoff loss.
