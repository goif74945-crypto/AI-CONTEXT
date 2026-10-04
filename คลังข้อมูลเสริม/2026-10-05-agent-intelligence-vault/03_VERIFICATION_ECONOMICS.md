# Verification Economics
Verification should scale with impact, uncertainty, reversibility, and blast radius.
Risk score concept: impact * uncertainty * irreversibility * scope.
Low-risk reversible read-only output may use lightweight checks. High-impact mutations require independent postcondition readback and regression checks.
Avoid verification theater: repeating the same model's judgment is correlated, not independent.
Prefer deterministic validators, direct source readback, schema checks, invariant checks, and independent data sources.
Optimization objective: minimize expected failure cost + verification cost, not merely token/tool cost.
