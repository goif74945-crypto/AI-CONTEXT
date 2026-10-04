# RAB Evidence
- Source: `src/index.ts`.
- Focused tests: 5 PASS.
- Verified nested example computes exact worst case 14 attempts.
- Negative: unsafe retry, budget excess, cycle, analysis-cap explosion.
- Property: 200 generated shallow graphs matched an independently computed closed form.
- Stress: repeated retry analysis contributes 10,000 checks in the 55,000-check campaign.
