# Publication Evidence

Execution code: `CHAT-20261005-0224-NEXY-LO4-REALITY-FIVE`
Repository mutated by this execution: `goif74945-crypto/AI-CONTEXT` only.
Target folder: `คลังข้อมูลเสริม/CHAT-20261005-0224-NEXY-LO4-REALITY-FIVE`.

## Primary publication

Primary publication commit:
`a00741833e1b5430a4eec83634b1a067aca28cee`

The publication used a non-force branch update. A prior candidate was abandoned when another concurrent writer advanced `main`; the tree was rebuilt on the newer head rather than overwriting concurrent work.

## Post-write readback

Readback from `main` returned all 14 initially published files and **0 blob-SHA mismatches**.

Human-readable files matched their locally computed Git blob SHA:
- `README.md` → `b583ba5b1c440e1989a3d5437de32ad04a7ae31e`
- `DESIGN.md` → `fa2f8a866ebdc52b7ea21569d02c4e61ce972b5f`
- `EVIDENCE.md` → `ae3ca9e6f224ced16bc03a2eb8872fbe4c2fe262`
- `00_TEMP_MEMORY.md` → `8b13b2f766d89b011c41c9d495180c4e7d4a0b35`
- `NOVELTY_SCAN.md` → `6bc6717fbf4c29e3d5309294b2d9e6ecbc828cc2`
- `BUNDLE_README.md` → `0af97d82a6b06912645aee5fee147e7666bc0d7e`

Source bundle part sizes read back as:
`5000, 5000, 5000, 5000, 5000, 5000, 3880` bytes.

Source bundle part Git blob SHAs matched the exact local base64 slices:
1. `ec1caa00c910867a84f8a75ca489d6a5cd5ae51b`
2. `d81a6b64b516ba33ffb9fd23db69f06ee55c2bc6`
3. `0c257e44c26eb43923729761f7683b4ab2e35396`
4. `b94a73877c22ff87ec12ebab8a12c008339d1e53`
5. `b1696ff6092effef555ee6520222130b03b3ab7f`
6. `ee584589afcb2e1863744cc8932c9d6d5bc217f8`
7. `8f0850a3d3001bec2bb38d35197dc9228bc62e20`

Therefore the published base64 sequence is byte-identical to the locally generated sequence. The reconstructed local archive SHA-256 is:
`9af0a004884662fb62396869f83f35fa5b96a57f738cd72dd6b8026c76cc93ae`.

## Ancestry proof

After publication, concurrent work advanced `main`. A GitHub compare from publication commit `a0074183...` to observed later head `dc99132e...` returned:
- status: `ahead`
- ahead_by: `3`
- behind_by: `0`
- merge base: exactly `a00741833e1b5430a4eec83634b1a067aca28cee`

This proves the observed later `main` head descended from the publication commit rather than replacing it.

## Mutation boundary

All write-tool calls in this execution targeted `goif74945-crypto/AI-CONTEXT`. No repository whose repository name contains `NEXY.AI` was mutated.

## Truth boundary

This proves artifact publication and isolated reference-test evidence only. It does not prove current NEXY.AI runtime integration, deployment, legal compliance, accessibility-standard conformance, production performance, or Canon promotion.
