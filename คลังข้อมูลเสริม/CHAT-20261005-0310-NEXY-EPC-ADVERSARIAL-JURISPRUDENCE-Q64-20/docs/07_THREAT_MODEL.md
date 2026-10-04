# Threat Model

| Threat | Control | Failure state |
|---|---|---|
| Correlated sources inflate confidence | SIC-01 | DEFER |
| Reviewer cartel/collusion | CTG-02 | BLOCK |
| Majority suppresses strong minority proof | MPS-03 | DEFER |
| Strawman / absent counterargument | CSG-04 | DEFER |
| Single decisive evidence item | SPEF-05 | DEFER |
| Verdict unstable under evidence removal | CVS-06 | DEFER |
| Homogeneous quorum | QDG-07 | DEFER |
| Candidate-linked reviewer influence | COIF-08 | BLOCK |
| AI invents an easy proof threshold | BPR-09 external authority requirement | FREEZE/DEFER |
| CUT interpreted as deletion | RAC-10 | BLOCK |
| Appeals used to reset vote entitlement | AEC-11 only marks eligibility | no entitlement mutation |
| Reconsideration used as sham second vote | EDRG-12 | BLOCK |
| Same facts/law yield unexplained divergent precedent | PCM-13 | DEFER |
| Winner deletes dissent | DIL-14 | DEFER/BLOCK |
| Tie broken arbitrarily | PDR-15 | DEFER |
| Empty justification | ECG-16 | BLOCK |
| One evidence family dominates impact | ECL-17 | DEFER |
| Assumption/UNKNOWN converted into proof | ACF-18 | BLOCK/DEFER |
| Evidence arrives after claimed decision | TCT-19 | BLOCK/FREEZE |
| Labels/order manipulate outcome | FIH-20 + canonical projection | FREEZE on malformed, invariant otherwise |
| Float/random/time causes cross-host drift | Q64 bigint + token gate | build verification failure |
| EPC output mutates NEXY | adapter capability boundary | rejected by type/runtime invariant |
