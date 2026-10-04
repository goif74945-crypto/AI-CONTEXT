# Exact Tested Bundle — SFRC-20

This directory is the persistence bridge for the **exact bytes that were compiled and tested** in the isolated execution workspace.

## Archive identity

- decoded file: `SFRC20-source-evidence.tar.gz`
- decoded bytes: `29747`
- joined base64 length: `39664`
- SHA-256: `71982d0ae740a2158115b9337eda318e1a6c48be884dadec573a088597cd6083`

## Parts

| Part | Bytes | SHA-256 |
|---|---:|---|
| 00 | 4000 | a93bc33867dbffd8c10bab9537a27dad85afec0282619d88522aefd56423b964 |
| 01 | 4000 | 49cd5ff501b784790f3a36460cf01ce179d67093cacfea823851ffea4b8507bb |
| 02 | 4000 | f9f81b89c83b9b62bc05ea472ecc06a61347db223e3a157df9e07489bf10218f |
| 03 | 4000 | 3bad288794e3ee9728f1c8112a4698567b920c50595d61a065d2c6322f6a1334 |
| 04 | 4000 | a5c60ccd44cf077de7c3d9ee39b15f9701e6dae89444f3f4b4c237a612f35faf |
| 05 | 4000 | 39d4edb9eac6e0c1b109b4d8e76f5287d277417c2bcf09affb25015c598d251d |
| 06 | 4000 | 6a2b85c1c0cc74fa9788bed5f431f0a36e68517fc6624d7b7f7bc740dc168ba9 |
| 07 | 4000 | d4ecc67b473502450a4e71b915baf9efca74a31150785f1088b2b990d503990e |
| 08 | 4000 | e25df3fb55e777b7ee4bc3ab9f7d054c9e45eb6f5c54d88268be4eb1c3624e54 |
| 09 | 3664 | 63a6123f92ff20a182e22d0ceefd85d3f4df6694cc8d662b79c6184d326973fd |

## Reconstruct

From this `bundle/` directory:

```bash
cat SFRC20.tar.gz.b64.part-* | base64 -d > SFRC20-source-evidence.tar.gz
printf '%s  %s\n' \
  '71982d0ae740a2158115b9337eda318e1a6c48be884dadec573a088597cd6083' \
  'SFRC20-source-evidence.tar.gz' | sha256sum -c -
mkdir -p SFRC20
tar -xzf SFRC20-source-evidence.tar.gz -C SFRC20
cd SFRC20
npm run check
```

## Read-back proof

After publication, every part was fetched again through the GitHub connector and hashed independently. All ten chunk hashes matched the table above. Their concatenation decoded to exactly 29,747 bytes and the decoded archive hash matched `71982d0a...`.

An earlier publication of part-02 was detected at 3,965 bytes instead of 4,000 and was rejected by this read-back gate. It was repaired from the hashed local source and the full 10/10 + archive verification was rerun successfully. This failure/recovery is intentionally recorded instead of being hidden.

## Authority boundary

The archive contains experimental Lo4 source, tests, design and evidence only. Extraction or a passing standalone test does **not** promote the candidate, change Canon, or modify NEXY.AI.
