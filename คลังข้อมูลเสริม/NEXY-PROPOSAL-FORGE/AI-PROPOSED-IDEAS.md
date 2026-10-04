# AI-Proposed Idea Backlog

Everything in this file is **AI_PROPOSED_CONCEPT / NON-AUTHORITATIVE / NOT A BUILD REQUIREMENT**.

The items below are deliberately separated from canonical NEXY context. They are future review material only.

## 1. NEXY Change Shadow

A read-only preflight simulator that takes a proposed repository change plan and computes the likely requirement, test, evidence, security, and rollback blast radius **before** mutation. It would output a shadow execution graph rather than touching files.

Potential user value: fewer accidental regressions and clearer proof obligations before an expensive implementation starts.

Major constraint: it must never claim that predicted blast radius equals runtime truth.

## 2. Evidence Debt Meter

A ledger that tracks claims whose required evidence class is missing or stale. Instead of a vague “not verified” state, reviewers could see where proof debt accumulates and which exact evidence class is required next.

Potential user value: faster convergence from implementation to verified state.

Major constraint: evidence debt is project metadata, not a license to weaken PASS criteria.

## 3. Concurrent Scope Collision Beacon

A task-manifest comparator for AI-CONTEXT that detects multiple sessions intending to mutate overlapping path scopes or solve the same proposal. It would emit collision warnings before execution.

Potential user value: fewer duplicated multi-agent efforts and less accidental overwrite risk.

Major constraint: stale manifests must never be treated as a live distributed lock.

## 4. Human Proof Lens

A user-facing projection that converts an internal decision/evidence graph into three compact questions: “What is known?”, “What blocked this?”, and “What exact proof/action would unlock the next state?”

Potential user value: users get useful control-room clarity without exposure to internal machinery.

Major constraint: presentation may compress proof but may not change the underlying decision.

## 5. Requirement Drift Sentinel

A read-only comparator between source-normalized requirements, implementation mappings, and evidence records. It would flag when a requirement reference changes authority/scope or when implementation/evidence still points to an obsolete denominator.

Potential user value: prevents historical registries such as the deprecated 215-entry inventory from silently returning as current truth.

Major constraint: it must distinguish source change, code change, and evidence staleness instead of flattening them into one “drift” score.
