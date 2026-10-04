# Research Backlog

All items are AI_PROPOSED and outside the completed prototype scope.

## P0 before any real integration
- recipient trust registry with revocation/freshness;
- data classification provenance and conflict handling;
- multi-tenant object-level authorization integration;
- provider-specific logging/training/retention metadata;
- unavoidable egress enforcement point;
- cryptographic tokenization/key rotation design;
- deletion/expiry evidence model;
- purpose registry with versioning.

## P1 correctness research
- mixed-purpose batch tasks;
- derived data sensitivity propagation;
- aggregation/k-anonymity style transform choices where appropriate;
- field-level regional constraints;
- transformation utility loss measurement;
- policy evolution and backward compatibility;
- policy snapshot pinning to task execution.

## P1 user/product research
- compact disclosure receipts;
- when consent prompt is actually necessary;
- interruption cost vs privacy value;
- defaults that preserve user control without consent fatigue;
- clear explanation of FREEZE without leaking sensitive metadata.

## P2 advanced future concepts
- information-flow labels propagated through SWARM subtask graphs;
- automatic taint tracking from source → derived artifact;
- privacy-preserving consensus where agents see different minimal views;
- cryptographic proof that a gateway applied a specific disclosure plan;
- provider attestation that retention/training settings match the plan;
- privacy budget across a long-running project, not only one task.
