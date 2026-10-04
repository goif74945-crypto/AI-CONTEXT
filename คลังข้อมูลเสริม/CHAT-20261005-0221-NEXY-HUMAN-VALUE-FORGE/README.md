# NEXY Human Value Forge (HVF)

**Work code:** `CHAT-20261005-0221-NEXY-HUMAN-VALUE-FORGE`  
**Class:** `Lo4 / AI-PROPOSED / NON-CANONICAL`  
**Mutation scope:** `goif74945-crypto/AI-CONTEXT` only.

HVF is a five-system deterministic reference package for translating explicit human value contracts into machine-checkable guards and selectors without giving the AI authority to invent preferences.

## Five concepts
1. **EEC — Expectation Envelope Compiler**: distinguishes expected behavior from merely allowed behavior and hard-forbidden behavior.
2. **SDG — Surprise Delta Governor**: measures candidate deviation from explicit expectation and returns `ALLOW`, `WARN`, or `FREEZE`.
3. **RBP — Regret-Bounded Planner**: chooses among legal verified plans using minimax regret over an explicit scenario/loss matrix.
4. **UFS — Utility Frontier Selector**: computes the deterministic Pareto frontier and optionally selects using an explicit priority order.
5. **SPC — Satisfaction Proof Contract**: proves declared required/desired success criteria using evidence statuses rather than model sentiment.

## Why this is different
Existing supplemental work already covers uncertainty dependencies, reversible probes, capability routing, interruption handling, outcome closure, proof efficiency, preferences, and decision stability. HVF targets a different gap: the formal relationship between **explicit expectations, surprise, regret, multi-objective utility, and provable satisfaction**. A subtree keyword sweep found no existing path names containing `surprise`, `regret`, `expectation`, `utility`, or `satisfaction` at inspection time. That is novelty evidence, not a proof that no semantically related idea exists anywhere.

## Run
```bash
python -m compileall -q src tests examples verify.py
python -m unittest discover -s tests -v
python verify.py
```

The package uses only the Python standard library.
