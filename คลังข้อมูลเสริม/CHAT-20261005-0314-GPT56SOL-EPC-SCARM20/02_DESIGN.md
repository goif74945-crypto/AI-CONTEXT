# SCARM-20 Design — Social-Choice & Strategic Manipulation Resistance for NEXY EPC

## Classification
`Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`

SCARM-20 is an external advisory pre-review layer for the proposed NEXY Evolutionary Proposal Court. It detects process manipulation patterns. It does not decide Canon, change NEXY state, cast KEEP/CUT, or promote anything.

## Design laws
1. Quantitative metrics use checked signed i128-domain Q64.64.
2. Binary floating-point is not used for authoritative scoring.
3. Logical ticks are explicit inputs; wall-clock time cannot affect a verdict.
4. Canonical ordering uses exact deterministic text comparison, not locale collation or Unicode normalization.
5. Hard findings are non-compensatory. A high score elsewhere cannot cancel a hard manipulation failure.
6. Missing required mechanism evidence or `UNKNOWN` yields `DEFER_REVIEW`, never an invented PASS.
7. Identity-sensitive detectors consume explicit provenance only; SCARM never infers hidden identity or Sybil ownership.
8. WIP/DEFER/INSUFFICIENT_EVIDENCE are not CUT reasons.
9. All outputs remain advisory: `ALLOW_REVIEW`, `DEFER_REVIEW`, or `BLOCK_REVIEW`.

## Mechanisms
| # | ID | Executable symbol | Purpose | Critical failure behavior |
|---:|---|---|---|---|
| 1 | SPLIT64 | `detectSplitGaming` | Detect same-owner/same-lineage proposal fragmentation with high semantic-atom overlap. | Flag for review; never CUT automatically. |
| 2 | MERGE64 | `detectMergeGaming` | Detect undeclared recombination of multiple independent lineages. | Missing parent evidence -> UNKNOWN; undeclared high-coverage merge -> hard finding. |
| 3 | LAUNDER64 | `detectRevisionVoteLaundering` | Detect reuse of a spent round through a substantively unchanged revision. | Hard finding; no right is regranted. |
| 4 | FRONT64 | `detectFrontRunning` | Detect high-similarity later proposal copied within an explicit logical-tick window without declared lineage. | Soft finding; no hidden intent inference. |
| 5 | CLONE64 | `detectCloneFlood` | Detect exact semantic clone flooding of the active candidate set. | Soft finding; prevents count inflation from silently looking like diversity. |
| 6 | IIA64 | `checkIIA` | Test independence of irrelevant alternatives by preserving pairwise order among unchanged candidates. | UNKNOWN if no common pair; order reversal flags. |
| 7 | CLONEINV64 | `checkCloneIndependence` | Verify adding a declared clone does not reorder non-clone candidates. | Missing clone reference -> UNKNOWN. |
| 8 | ORDER64 | `verifyBallotOrderIndependence` | Verify ballot presentation order cannot change canonical ballot content. | Any content divergence under replay is hard. |
| 9 | EVIDORDER64 | `verifyEvidenceOrderIndependence` | Verify evidence set order/duplicate presentation cannot change the canonical set. | Set divergence is hard. |
| 10 | TIE64 | `deterministicTieBreak` / `proveDeterministicTieBreak` | Provide exact replay-stable tie ordering. | Divergent replay is hard. |
| 11 | OSC64 | `detectStatusOscillation` | Detect A→B→A status churn under unchanged evidence. | Soft finding; does not interpret WIP as failure. |
| 12 | DEFERCHURN64 | `detectDeferChurn` | Detect repeated DEFER/WIP cycling without evidence growth. | Soft process warning only; never CUT. |
| 13 | SCOPE64 | `detectScopeExpansionGaming` | Detect scope expansion that outruns new supporting evidence. | Soft finding; preserves explicit new dimensions as evidence IDs. |
| 14 | APPEAL64 | `guardAppealNonRegrant` | Ensure appeal/revision cannot restore a spent KEEP/CUT entitlement. | Hard finding; consumes an external entitlement snapshot but does not own the rights ledger. |
| 15 | COALITION64 | `measureCoalitionConcentration` | Measure concentration (HHI) using explicit provenance clusters. | Incomplete provenance -> UNKNOWN, never inferred identity. |
| 16 | RECIPROCITY64 | `detectReciprocityRings` | Detect explicit cross-chat KEEP reciprocity cycles. | Soft finding; only explicit voter/owner edges are used. |
| 17 | BURST64 | `detectCoordinatedBurst` | Detect dense same-provenance voting bursts in logical-tick space. | Missing explicit provenance -> UNKNOWN. |
| 18 | COUNTERARG64 | `checkCounterargumentCompleteness` | Enforce reason + counterargument + evidence + final justification completeness. | Missing required record content is hard. |
| 19 | DISSENT64 | `checkDissentPreservation` | Ensure explicit opposing evidence survives dossier compilation. | Dropped dissent is hard. |
| 20 | MANIPGATE64 | `manipulationRiskGate` | Non-compensatory aggregation of the first 19 mechanisms. | Hard finding -> BLOCK_REVIEW; unknown/missing or soft risk above threshold -> DEFER_REVIEW. Never KEEP/CUT/promotion. |

## Semantic input boundary
SCARM does not perform free-form NLP similarity. `semanticAtoms` are an explicit normalized input contract supplied by an upstream evidence/semantic adapter. This prevents model-dependent embeddings from becoming hidden authority. Phrase/name similarity alone is not sufficient duplicate proof.

## Numeric boundary
SCARM uses its own checked Q64.64 helper whose carrier is conceptually signed i128. Overflow and divide-by-zero throw. This choice is aligned to the inspected Lo3 governor fail-closed arithmetic. It does not claim to redefine NEXY-wide numeric law; inspected G15 simulation code has a separate deterministic saturation policy.

## Composition boundary
SCARM complements, rather than replaces, existing EPC work:
- external Vote Rights Ledger owns entitlement truth;
- semantic duplicate/novelty systems own semantic evidence production;
- evidence maturity/freshness systems own evidence qualification;
- JUDGE/LAW/CORE retain final authority;
- SCARM consumes explicit evidence and emits manipulation-review findings only.
