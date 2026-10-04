# Evidence Architecture for NEXY.AI
Status: PROPOSAL grounded in FACT_PROJECT

## Objective
ทำให้คำว่า “ผ่าน” หมายถึงหลักฐานที่ผูกกับ source identity, toolchain, inputs, environment และ verifier ไม่ใช่ข้อความจาก agent

## Evidence graph
Node types:
- Requirement
- SourceIdentity(commit/tree)
- BuildEnvironment
- Toolchain
- TestCase
- Execution
- Artifact
- Hash
- Verification
- Exception/Freeze
- ReleaseDecision

Edges:
REQUIREMENT -> PROVED_BY -> TEST
TEST -> EXECUTED_AS -> EXECUTION
EXECUTION -> USED_SOURCE -> SOURCE_IDENTITY
EXECUTION -> USED_ENV -> ENVIRONMENT
EXECUTION -> PRODUCED -> ARTIFACT
ARTIFACT -> SEALED_BY -> HASH
VERIFICATION -> VERIFIED -> HASH/ARTIFACT
RELEASE -> REQUIRES -> VERIFICATION

## Mandatory evidence properties
PROPOSAL:
1. immutable source identity
2. test command identity
3. tool/runtime versions
4. input/config identity
5. exit status
6. machine-readable result
7. artifact hash
8. verifier identity
9. timestamp as metadata only, never authority
10. explicit missing-evidence state

## Anti-false-completion rules
- PASS without source identity = NOT VERIFIED
- PASS from stale source = INVALID
- generated report without execution provenance = INVALID
- agent prose saying “tested” = zero proof
- partial suite cannot satisfy whole-suite requirement
- cached result must prove cache identity or be treated as stale
- changed authority/spec invalidates dependent evidence until revalidated

## Evidence freshness
Freshness should be dependency-based, not merely time-based.
An old proof remains relevant only when all authority/source/toolchain/input dependencies remain identical under the contract.
A recent proof is invalid if it targets the wrong tree.

## Evidence closure
A release claim has closure only if every required claim reaches at least one valid terminal verification node and no required edge terminates in UNKNOWN.

## Failure behavior
Missing, contradictory, unverifiable, or source-mismatched evidence -> FREEZE release claim.

## Project grounding
FACT_PROJECT: Dockerfile checks provider source identity, tested SHA/tree, rerun nonce and executes Rust + TS/product gates.
FACT_PROJECT: package scripts include seal and seal:verify.
PROPOSAL: represent those proofs as a queryable graph to expose orphan requirements and stale evidence automatically.
