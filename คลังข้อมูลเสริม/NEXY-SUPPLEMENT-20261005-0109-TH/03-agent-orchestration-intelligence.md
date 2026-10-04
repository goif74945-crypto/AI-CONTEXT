# Agent Orchestration Intelligence
Status: ADVISORY DESIGN

Agent count is not evidence. Consensus is not truth. Correlated agents can amplify one mistake.

## Roles
SCOPER: task contract.
AUTHORITY_RESOLVER: governing sources.
STATE_OBSERVER: current state.
BUILDER: candidate.
ADVERSARY: falsification.
EVIDENCE_COLLECTOR: proof.
JUDGE: evidence-bound acceptance.
HISTORIAN: provenance/checkpoint.

## Independence budget
Record diversity across model/provider, prompt strategy, source subset, verification method, environment and tool path. Quorum should reflect failure independence, not headcount.

## Claim-level merge
Return normalized claims: proposition, authority refs, evidence refs, objections, status. Never merge by prose voting.

## Deterministic tie-break
Among candidates satisfying all hard requirements: fewer assumptions -> stronger evidence -> smaller mutation -> lower irreversible impact -> simpler dependency surface -> stable canonical order. If uniqueness is required and a material tie remains, FREEZE.

## Work packet
objective; target revision; read scope; mutation scope; protected scope; authority; outputs; evidence; forbidden assumptions; stop conditions; return schema.

## Checkpoint DAG
Long parallel work should preserve parent checkpoints, requirements, revision, artifacts, evidence, invalidations, conflicts and next work packets.

Treat every agent output as untrusted until evidence is checked. "Another agent verified it" is not proof.
