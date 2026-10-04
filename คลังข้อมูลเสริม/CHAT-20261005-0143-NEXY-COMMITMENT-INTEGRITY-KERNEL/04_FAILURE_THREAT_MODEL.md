# 04 — Failure and Threat Model

**Classification:** AI-PROPOSED research model.

## Trust boundary

Treat as untrusted until separately verified:
- model-generated promise text;
- claimed scheduler IDs;
- claimed automation/task state;
- clock/time strings;
- external provider acknowledgements;
- evidence references;
- agent handoff messages;
- UI completion badges;
- retry metadata;
- user identity/role fields not authenticated upstream.

## Threat matrix

| ID | Threat | Required behavior | Reference status |
|---|---|---|---|
| T-01 | Assistant promises future work with no scheduler | FREEZE unbacked commitment | PASS E2 |
| T-02 | Conditional monitoring promised with no watcher | FREEZE binding/capability mismatch | PASS E2 |
| T-03 | Recurring task uses ephemeral session state | FREEZE non-durable future commitment | PASS E2 |
| T-04 | Wrong temporal binding is substituted | FREEZE exact binding mismatch | PASS E2 |
| T-05 | Authority is ambiguous | ASK, not guess | PASS E2 |
| T-06 | Authority sources conflict | FREEZE | PASS E2 |
| T-07 | Scope overlaps protected scope | FREEZE | PASS E2 |
| T-08 | Promise silently widens during execution | require revision + supersedes hash | PASS reference |
| T-09 | Promise silently changes beneficiary | reject revision | PASS E2 |
| T-10 | Promise silently changes issuer | reject revision | PASS E2 |
| T-11 | System says done without evidence | reject completion | PASS E2 |
| T-12 | Stale evidence from old obligation | target fingerprint mismatch | PASS E2 |
| T-13 | Evidence from wrong revision | reject completion | PASS E2 |
| T-14 | Evidence class mismatch | reject exact required-class gap | PASS E2 |
| T-15 | Deployment evidence is used to fake E2E proof | no ordinal substitution | PASS E2 |
| T-16 | Audit event modified after creation | hash-chain verification fails | PASS E2 |
| T-17 | Audit events reordered | sequence/hash-chain verification fails | PASS E2 |
| T-18 | Terminal commitment reopens silently | reject transition | PASS E2 |
| T-19 | Claimed scheduler reference is forged | authenticate binding upstream | NOT_VERIFIED |
| T-20 | Scheduler task deleted after promise issuance | monitor binding liveness / fail user-visible | NOT_VERIFIED |
| T-21 | Cancellation races with dispatch | atomic cancellation/dispatch protocol | NOT_VERIFIED |
| T-22 | Retry performs side effect twice | idempotency + exactly-once receipt law | NOT_VERIFIED |
| T-23 | Condition watcher misses edge transition | durable event cursor / replay | NOT_VERIFIED |
| T-24 | Clock skew expires/executes incorrectly | authoritative time source + tolerance law | NOT_VERIFIED |
| T-25 | Cross-region stale task state | quorum/version/epoch semantics | NOT_VERIFIED |
| T-26 | Cross-agent handoff drops evidence obligation | commitment capsule transfer protocol | NOT_VERIFIED |
| T-27 | User edits/cancels task but old executor proceeds | revocation epoch checked at dispatch | NOT_VERIFIED |
| T-28 | UI paraphrase turns offer into promise | semantic commitment linter | PROPOSED |
| T-29 | Tool capability disappears after acceptance | capability lease/health gate | PROPOSED |
| T-30 | Promise cannot be fulfilled due to provider outage | BLOCKED/FAILED + truthful user notification | PROPOSED |

## Fail-safe law

When NCIK cannot prove that a future commitment is bound to a compatible durable execution capability, it must not label the statement as an accepted commitment.

A product may still explain what it *can* do or offer to create the required automation. That wording layer is outside this reference kernel.

## Production proof obligations

Before adoption, prove at minimum:
1. binding references cannot be forged;
2. acceptance and scheduler creation are transactionally consistent;
3. cancellation/revocation wins against unsafe late dispatch;
4. retries cannot duplicate externally visible effects;
5. service crash/restart preserves obligation state;
6. distributed replicas converge on one legal commitment revision;
7. trigger semantics are replay-safe;
8. evidence references are authenticated and immutable enough for the claim;
9. UI language preserves accepted vs offered vs blocked distinctions;
10. all commitment transitions emit durable attributable audit events.
