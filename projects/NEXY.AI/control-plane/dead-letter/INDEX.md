# P4.10 Dead Letter / Quarantine

## Purpose
Contain terminal or unsafe command outcomes without silent requeue or history rewriting.

## Core rules
- Dead-letter and quarantine records are immutable provenance records.
- Retry exhaustion routes to DEAD_LETTER unless a stricter policy requires BLOCKED or QUARANTINED.
- Security violations route to QUARANTINED.
- Authority conflicts and human gates remain BLOCKED, not automatically retried.
- No record may return to READY without an explicit new/superseding command after revalidation.
- Release from quarantine requires an authorized release decision with evidence; the original record remains immutable.

## Integration
Consumes command identity, retry decisions, claim/lease state, expected-HEAD guard and supersession lineage.
Produces terminal routing evidence for scheduler, convergence and human escalation.

## Files
- `dead-letter.schema.json`
- `routing-policy.json`
- golden and negative examples
- `validation-report.md`
