# Architecture

**Classification: AI-PROPOSED future tooling. Not current NEXY law or implementation.**

## Components

1. **Decision Record Adapter**: converts an external stable/candidate decision result into the narrow lab schema. Adapter ownership remains outside the lab.
2. **Canonicalizer**: stable JSON serialization + SHA-256 digest for structural replay checks.
3. **Pair Comparator**: compares same-case proof contexts and emits typed findings.
4. **Dataset Gate**: coverage, duplicate, nondeterminism and promotion status logic.
5. **CLI Reporter**: machine-readable JSON output with fail-closed exit codes.
6. **Evidence Pack**: fixtures, test output and explicit limitations.

## Trust boundary

The prototype is read/compare/report only. It accepts pre-generated decision records. It has no credentials, no network client, no command executor and no pathway to promote itself.

## Data minimization

The record schema uses `input_fingerprint` rather than raw prompts/user data. Reports contain case IDs, finding codes and bounded messages, not original payloads. An integrating system should still treat case IDs and references as potentially sensitive metadata.

## Determinism model

Canonicalization sorts mapping keys and forbids NaN. Candidate duplicates for one `case_id` are hashed structurally. Different hashes are a blocking nondeterminism signal. Identical duplicate records are not a safety failure, but remain `NOT_VERIFIED` because repetition can indicate replay/collection defects.

## Promotion semantics

`PASS`: no blocking findings and no warnings.  
`NOT_VERIFIED`: no blocking finding, but at least one warning remains.  
`FAIL`: at least one blocking finding.

The lab intentionally does not emit an automatic "promote" action. A PASS report is evidence input, not authorization.
