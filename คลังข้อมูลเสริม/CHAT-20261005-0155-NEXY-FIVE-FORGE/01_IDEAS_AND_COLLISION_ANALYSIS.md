# Five Proposed Systems and Collision Analysis

All items below are **AI-proposed concepts**, not existing NEXY requirements unless separately promoted by authoritative project sources.

## 1. Context Budget Optimizer (CBO)
Problem: long-running agents repeatedly face context/token limits. Naive truncation can discard authority, dependencies or fresh evidence.
Proposal: deterministic context packing that scores authority, relevance and freshness, always closes dependencies, and freezes if mandatory context cannot fit.
Why it adds value: makes NEXY-style zero-guess operation possible under constrained context windows without pretending omitted facts still exist.

## 2. Tool Evidence Router (TER)
Problem: selecting a tool because it is available does not prove it can produce the evidence class required for a claim.
Proposal: enumerate bounded tool combinations and choose a route satisfying capability, evidence, reliability, latency and cost constraints.
Why it adds value: turns tool choice into a verifiable planning problem rather than model intuition.

## 3. Recovery Recipe Distiller (RRD)
Problem: failure catalogs describe what went wrong, but repeated successful repairs are often not converted into reusable, evidence-bound procedures.
Proposal: cluster verified episodes by subsystem/error/root-cause, preserve both successes and failed attempts, and publish a recipe only after evidence thresholds are met.
Why it adds value: creates a durable self-improving recovery library without promoting one lucky fix into doctrine.

## 4. Skill Compiler (SKC)
Problem: repeated high-quality workflows are often copied manually or encoded as prompts with weak provenance.
Proposal: compile consistent successful execution traces into portable declarative skills only after evidence, consistency, failure-rate and secret-safety gates pass.
Why it adds value: converts demonstrated behavior into reusable capability while preventing silent skill drift.

## 5. Assumption Burn-down Planner (ABP)
Problem: autonomous work often accumulates assumptions that remain hidden until a mutation fails.
Proposal: represent assumptions explicitly, rank their expected damage, and solve for the smallest probe set that covers all mutation-blocking assumptions within cost/risk limits.
Why it adds value: operationalizes “do not guess” into a pre-mutation planning primitive.

## Collision policy
The existing supplemental tree was scanned before design. Many adjacent assurance, proof, context, tool-drift, resource, semantic and recovery projects exist. These five concepts were retained only because their direct path-name themes were absent. Similar underlying primitives may still exist elsewhere; therefore novelty is claimed as **non-colliding package scope**, not as universal invention priority.
