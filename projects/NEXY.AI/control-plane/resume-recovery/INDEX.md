# P4.16 Resume / Recovery

Resume from durable state only after refreshing current HEAD, command status, claim/lease state, supersession lineage, evidence freshness and checkpoint currency.

Recovery never revives an expired claim or silently rewrites an old command.
A resumed action uses a still-valid command or a new superseding command after revalidation.

Files:
- resume.schema.json
- recovery-policy.json
- examples/cases.json
- validation-report.md
