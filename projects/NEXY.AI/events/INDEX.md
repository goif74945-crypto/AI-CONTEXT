# NEXY.AI Event / Message Registry

`events.jsonl` contains:
- source-defined execution FSM events;
- implementation-observed operational EventLog/AuditLog event kinds.

Every event keeps producer/owner, consumer, schema, ordering, delivery, idempotency, timeout/retry semantics, audit behavior and failure semantics where established.

Source FSM events and OBS operational events are different namespaces.
