# LBCC Integration Contract

## Authority note

This is an **AI-proposed optional adapter contract**. It does not change NEXY.AI authority or current build requirements.

## Input JSON

```json
{
  "bundle_id": "task-123",
  "atoms": [
    {
      "atom_id": "req-1",
      "text": "Never guess missing material facts.",
      "truth_class": "SOURCE_FACT",
      "authority_rank": 100,
      "provenance": ["spec:section-2"],
      "evidence": [],
      "immutable": true,
      "tags": ["law"],
      "valid_from": null,
      "valid_to": null,
      "metadata": {}
    }
  ]
}
```

Unknown fields are rejected by the parser to avoid silent schema drift.

## Policy

CLI flags currently expose:
- `--max-bytes`
- `--max-loss-ppm`
- `--protected-authority-rank`
- `--allow-sensitive`

Library callers can additionally set `protect_unknown_conflict`.

## PASS result

A PASS result contains:
- `capsule`: budget-constrained canonical representation;
- `loss_ledger`: complete omitted-atom references outside capsule budget;
- `metrics`: source/retained/dropped counts, byte size, loss ppm.

## FREEZE result

A FREEZE result contains no trusted capsule. Consumers must not silently downgrade this to PASS.

## Compatibility rules

- schema version `lbcc/0.1` is exact-match for this implementation;
- unknown future schema versions must fail closed;
- canonical JSON is UTF-8, sorted keys, compact separators, Unicode preserved;
- SHA-256 digests are lowercase hex;
- atom IDs are opaque stable strings, not positional indices.

## Suggested NEXY adapter behavior

1. NEXY remains authoritative for admission and scope.
2. Adapter converts approved Vault/context records into atoms.
3. Adapter invokes LBCC with a caller-owned policy.
4. Adapter verifies the result against the original source bundle.
5. Only verified PASS may enter a bounded context surface.
6. FREEZE propagates as a blocking state with the codec reason.
7. Loss ledger remains available for audit/replay.

No direct integration code is written into NEXY.AI by this project.
