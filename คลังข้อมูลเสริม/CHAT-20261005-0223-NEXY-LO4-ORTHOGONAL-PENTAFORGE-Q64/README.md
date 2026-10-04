# NEXY Lo4 Orthogonal Pentaforge Q64

**Work trace ID:** `CHAT-20261005-0223-NEXY-LO4-ORTHOGONAL-PENTAFORGE-Q64`  
**Platform internal chat ID:** `UNKNOWN_NOT_EXPOSED_TO_TOOL_RUNTIME`  
**Classification:** `AI-PROPOSED / Lo4 / EXPERIMENTAL / SUPPLEMENTAL / NOT CANON`  
**Storage target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0223-NEXY-LO4-ORTHOGONAL-PENTAFORGE-Q64`  
**Protected implementation repository:** `goif74945-crypto/NEXY.AI-` was used only as a read-only context source and is not a mutation target.

## Authority boundary

This laboratory is additive advisory research. Nothing in this folder is NEXY law, DOC-C build authority, deployment approval, or proof that the NEXY runtime already implements these mechanisms. Promotion into Canon requires a separate authorized decision with exact-revision integration evidence.

The design follows the current AI-CONTEXT execution rules and the source-derived NEXY principles: explicit authority, deterministic behavior where claimed, verification before promotion, and freeze rather than guessing when evidence is insufficient.

## Objective

Build five materially different Lo4 experimental systems that can be connected to NEXY through explicit adapters while remaining isolated from Canon. Each reference implementation is deterministic, standard-library-only, fail-closed on malformed inputs, and uses a shared signed Q64.64 numeric kernel for quantities, ratios, times, distances, utilization, and scores.

Discrete identities, array indexes, iteration counts, priorities, and cardinalities remain integers because they are discrete values rather than fixed-point quantities.

## Five systems

### 1. SQX — Symmetry Quotient Explorer

Collapses states that differ only by permutations inside explicitly declared symmetry groups. It emits deterministic representatives, source-state membership, an orbit upper bound, and a Q64.64 reduction ratio.

Use: reduce redundant finite-state exploration for interchangeable agents/workers/resources without silently declaring semantically different groups equivalent.

### 2. CEFG — Causal Explanation Faithfulness Gate

Checks a structured explanation against an explicit causal-decision trace. It rejects unknown references, known noncausal references, missing mandatory causes, and insufficient causal coverage. Precision and coverage are Q64.64.

Use: prevent a user-facing rationale from becoming a polished post-hoc story that cites facts which did not actually participate in the decision trace.

### 3. RSEK — Robotics Safety Envelope Kernel

Computes a deterministic kinematic advisory envelope using speed, maximum speed, reaction time, maximum deceleration, obstacle distance, and safety margin. It calculates reaction distance, braking distance, stopping distance, clearance, and a Q64.64 clearance ratio.

Use: pre-check motion plans before a lower-level safety boundary. It is deliberately **not** a substitute for a dedicated safety MCU, certified controller, HIL testing, or physical emergency-stop evidence.

### 4. FPSA — Fixed-Priority Schedulability Analyzer

Performs bounded fixed-priority response-time analysis over periodic tasks. Period, WCET, deadline, response time, interference, and utilization are Q64.64. The analyzer distinguishes a proven `DEADLINE_MISS` from `ITERATION_LIMIT`, so budget exhaustion cannot masquerade as a stronger failure claim.

Use: reason about deterministic scheduling budgets for fast/slow loops, robotics control paths, worker queues, or other bounded periodic execution contracts.

### 5. OEWC — Observational Equivalence Witness Compiler

Projects two bounded event traces through an explicit observable-field contract and produces canonical digests, cell-level mismatches, and a Q64.64 match ratio.

Use: test whether a provider swap, runtime rewrite, adapter change, or refactor preserves the behavior that the contract declares observable. This is bounded trace evidence, not a theorem of universal equivalence.

## Shared Q64.64 law

`Q64` stores a signed Q64.64 value as a checked signed 128-bit raw integer:

- 64 integer/sign-side bits and 64 fractional bits;
- `SCALE = 2^64`;
- persisted raw values must fit `[-2^127, 2^127-1]`;
- decimal parsing and division round toward zero;
- no Python float literals occur in the production package;
- no hidden clock, randomness, network, process, or environment access occurs in the production package.

Python arbitrary-precision integers are only the arithmetic vehicle used to calculate intermediate products safely before the resulting Q64 raw value is range-checked.

## Execution and verification

```bash
PYTHONPATH=src python3 verify.py
```

The final local suite includes unit, negative-path, determinism, property/regression, and cross-module composition checks. Raw failure and final verification outputs are retained under `evidence/`.

## Integration contract

A future NEXY adapter may provide already-authorized immutable input objects to these modules and consume their reports as advisory evidence. The modules do not:

- mutate NEXY state;
- call NEXY::JUDGE;
- promote themselves into law;
- perform provider/network calls;
- read secrets;
- deploy or authorize release;
- perform physical actuation.

If required adapter semantics are missing or ambiguous, integration must FREEZE rather than guess.

## Current evidence boundary

Local verification can establish syntax/static properties, module behavior, and local composition only. It cannot establish real NEXY integration, production runtime behavior, deployment readiness, or physical robotics safety.

The complete tested source, tests, evidence, and documents are also sealed in `bundle/nexy_lo4_q64_pentaforge.tar.gz.b64`. Decode with `base64 -d` and verify against `bundle/BUNDLE_SHA256.txt`.

See `EVIDENCE.md`, `NOVELTY_AUDIT.md`, and `FINAL_AUDIT.md` for exact evidence and limitations.
