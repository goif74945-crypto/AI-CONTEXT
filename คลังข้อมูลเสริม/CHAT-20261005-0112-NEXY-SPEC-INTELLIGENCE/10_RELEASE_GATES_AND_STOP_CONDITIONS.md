# Release Gates and Stop Conditions
Hard gates: no critical requirement orphan; no unresolved critical contradiction; immutable invariants verified; forbidden behaviors negatively tested where observable; durable artifacts exist; evidence reproducible; critical failures closed; scope audit clean; checkpoint current; completion predicate true.

STOP_AND_FREEZE on critical requirement conflict, ambiguous mutation surface, missing required credential/approval, unobtainable critical evidence, destructive/out-of-scope risk, or unexpected repository change during writes.

COMPLETE only when gates pass. INCOMPLETE when work remains. BLOCKED for external dependency/authority. NOT VERIFIED when evidence is insufficient.