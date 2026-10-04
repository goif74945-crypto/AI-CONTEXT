# Dependency & Supply-Chain Intelligence

Status: PROPOSAL_AI

## Goal
Model dependencies as operational contracts, not merely package names.

## Dependency dossier
For every critical direct dependency, record:
- identity + exact version/digest
- why it exists
- authority surface it can influence
- runtime privilege
- network/filesystem/process reach
- serialization boundary
- upgrade owner
- rollback path
- deterministic impact
- license/security constraints
- substitute candidates
- minimum verification suite after change

## Risk dimensions
R = exposure × authority × mutability × opacity × recovery_cost

This is a prioritization heuristic, not a security fact.

High-risk examples include dependencies that parse authoritative input, execute code, alter persistence, sign/verify evidence, or control deployment behavior.

## Upgrade classes
U0 cosmetic/dev-only
U1 internal behavior, no contract change expected
U2 serialization/API behavior may shift
U3 persistence/security/authority boundary shift
U4 toolchain/runtime/platform shift

PROPOSAL_AI: U3/U4 upgrades should require explicit migration + rollback evidence and cannot inherit prior release proof.

## Supply-chain evidence
Useful artifacts:
- lockfile diff
- package provenance
- immutable artifact digest
- SBOM snapshot
- vulnerability scan timestamp
- license delta
- build reproducibility result
- focused contract regression result

## Failure semantics
If a critical dependency's provenance cannot be established, mark UNKNOWN or BLOCKED according to project authority. Do not substitute popularity, maintainer reputation, or model confidence for provenance.

## Future design
HYPOTHESIS: build a Dependency Authority Graph linking package → executable surface → project invariant → tests → release evidence. This allows a dependency diff to select the smallest defensible regression suite automatically.
