# AI-Proposed Future Ideas

Everything in this file is **proposal only**. None is a current NEXY requirement.

## A. Metamorphic Shadow Worlds
Generate controlled transformations of the same task: reorder irrelevant metadata, perturb timestamps outside semantics, swap equivalent provider formatting, and verify the candidate keeps the same decision class.

## B. Authority Mutation Testing
Automatically remove/reorder one authority edge at a time in a synthetic candidate and require the gate to detect every mutation. Useful as a self-test of the assurance layer itself.

## C. Proof-Closure Fingerprints
Instead of binding evidence only to revision, compute a fingerprint over files/config/policies actually relevant to a claim. This could reduce unnecessary revalidation while still preventing stale proof reuse. Requires rigorous dependency discovery before trust.

## D. Shadow Budget Governor
Run only high-information comparison cases under cost/latency constraints: freeze boundaries, policy edges, prior incidents, high-risk actions, and changed dependency closures first.

## E. Divergence Triage Capsules
For each blocked case, emit a minimal capsule containing fingerprints, authority delta, evidence delta and behavior delta so a reviewer can resolve the divergence without raw user content.

## F. Promotion Confidence Is Forbidden
Do not collapse assurance into a single opaque probability. Keep typed findings and explicit evidence. If a future UI wants a score, the score must never override blocking findings.
