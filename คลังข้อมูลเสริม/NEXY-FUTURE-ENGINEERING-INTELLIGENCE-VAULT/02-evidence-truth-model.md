# Evidence & Truth Model
Claim fields: id, statement, evidence type/locator, observed_at, verifier, method, confidence, revalidation condition, status.
States: UNKNOWN -> OBSERVED -> VERIFIED; UNKNOWN -> ASSUMED; ASSUMED requires evidence for VERIFIED; VERIFIED -> STALE; any -> DISPROVEN.
Priority: authoritative user spec; executed tool result; project artifact; official docs; reputable external evidence; inference; assumption. Freshness is independent.
Complete only when artifact exists/readable, required structure exists, critical behavior exercised, acceptance evidence exists, no critical contradiction.
Contradiction: freeze claim; preserve evidence; compare authority/version/time/environment/scope; run discriminating check; unresolved => UNKNOWN. Never average contradictions.
