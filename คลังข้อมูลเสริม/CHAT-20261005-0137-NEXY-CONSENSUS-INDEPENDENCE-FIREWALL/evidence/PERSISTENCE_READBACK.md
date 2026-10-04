# NCIF AI-CONTEXT Persistence Read-back

Classification: E0 PERSISTENCE EVIDENCE / NON-RUNTIME
Durable session: `CHAT-20261005-0137-NEXY-CONSENSUS-INDEPENDENCE-FIREWALL`

## Target

- Repository: `goif74945-crypto/AI-CONTEXT`
- Isolated authoring branch: `chat-20261005-0137-ncif-lab`
- Branch base observed before authoring: `2a792f13ff42df243d2559003dfd1cb6943296e5`
- Artifact head before this receipt: `1fe5a9879fc1f8b53b4304b5558ad5469e6d0662`

## Exact artifact read-back

The 37-file artifact set was fetched back from the isolated GitHub branch and compared against locally computed Git blob SHA-1 identities for the exact files that were produced/tested.

First comparison found exactly one mismatch:
- `evidence/cli-independent.json`: semantic data matched but formatting bytes differed.

The remote receipt file was replaced with the exact local bytes. GitHub then returned content SHA:
- expected: `dd52de46bcfbbe1ff63f8aaa1f1bcfa83545d9e3`
- observed: `dd52de46bcfbbe1ff63f8aaa1f1bcfa83545d9e3`

Full read-back was then repeated in two bounded batches:
- batch A: 18/18 blob identities matched, 0 missing;
- batch B: 19/19 blob identities matched, 0 missing.

Result: **37/37 exact Git blob identities matched** before this persistence receipt was added.

## Mutation boundary

All repository write calls in this mission targeted `goif74945-crypto/AI-CONTEXT`.
No repository whose name contains `NEXY.AI` was used as a write target.

## Evidence boundary

This proves presence and exact byte identity of the standalone branch artifact (E0). It does not prove NEXY integration/runtime/deployment. Local E1/E2 evidence remains in `verification.json`, `bounded-audit.json`, `stress-audit.json`, and `VALIDATION_REPORT.md`.

This receipt itself is post-test/persistence metadata and is intentionally outside the 37-file pre-publication hash set.
