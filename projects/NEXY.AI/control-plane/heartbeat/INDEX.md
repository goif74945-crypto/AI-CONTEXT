# P4.8 Heartbeat

## Binding
Every heartbeat binds exactly:
`worker_id + claim_id + command_id + lease_epoch`.

This prevents a heartbeat from an abandoned worker/old lease epoch from keeping a replacement claim alive.

## Monotonicity
`heartbeat_sequence` strictly increases per claim epoch.
Heartbeat timestamp must remain inside the lease window.

## Lease relationship
Heartbeat may refresh liveness/heartbeat deadline only up to the existing lease expiry.
It cannot silently extend `lease_expiry`; that requires an explicit lease-renewal mutation.

## Files
- `heartbeat.schema.json`
- `heartbeat-policy.json`
- golden + stale-epoch + after-expiry examples
- `validation-report.md`
