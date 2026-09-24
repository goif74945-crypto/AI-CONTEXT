# Case: API coverage metric authority ambiguity

Evidence from Railway deployment `aedd277b-38b8-4811-875a-bba1468a0d5f`:

`[FREEZE] coverage metric authority is ambiguous for api; metrics straddle 85%: lines=82.00% statements=80.38% functions=91.26% branches=71.98%`

Classification: SPEC/AUTHORITY AMBIGUITY, not a proven implementation defect.

Safe action: FREEZE coverage policy decision. Do not weaken threshold, choose a metric, or modify tests/source merely to force PASS.
