# Bundle Index

The full executable source tree is preserved as a gzip tar archive encoded into eight text blobs so it can be persisted atomically through the connected GitHub interface.

## Archive identity
- decoded filename: `lo4_verified_skill_foundry.tar.gz`
- decoded size: **23,105 bytes**
- decoded SHA-256: `66b1876dd724af961282fe19373283b75979de75f133036e70c0f578e82a7a22`
- concatenated base64 length: **30,808 characters**
- archive inventory: **28 entries**
- transient `EVIDENCE.local.json`, `STRESS_EVIDENCE.local.json`, bytecode caches, and nested archive copies: excluded

## Part identities
| Part | chars | Git blob SHA-1 | content SHA-256 |
|---|---:|---|---|
| 00 | 4096 | `532834058875728d26c0986324529d20d476808e` | `23e60298cbbf45fca341523f521678b7f9b3947c387750809a9754038da2afd4` |
| 01 | 4096 | `dbad1affa125bdeebc8f0189757e2021075b190d` | `909983d661df1af1f6373cc1f3faf5c1bbbde897495c1a28a4834e1da6c1de73` |
| 02 | 4096 | `c7dd5f48eab6bc3f0e769b3ccd5be82a1014bd1b` | `4396cc81a774e18e3f22107fbbb8f9d0f787ef5297fa5344d077bbe4e1a5901b` |
| 03 | 4096 | `49830423b88410ea29f7ac3dc0697cf5ddeacaad` | `97717056f2e009707773ac0f0af5aa8e0729541d3df687cb05eeb315c6ee978e` |
| 04 | 4096 | `b6bb5de6c180590d7407dd7a7affb5bad73ffe33` | `324088a1e8634abd52c89df57e9127f27c4fca4564eae26bc7e80db81cb2869d` |
| 05 | 4096 | `8161aeb4b30c95c6d028a2f703bcb26dbb112024` | `22a0bf87b2e6a7704c5f71657683b2339e2efea2efee03c00d63e71f0ed60ee9` |
| 06 | 4096 | `ebead018c1b281d58971b9ea2c9bb932a845082c` | `2499bffe48ee7a70cdb14ff8bb64b696831b801104d74fd24facc7961f69c8a5` |
| 07 | 2136 | `fbe8ea4fc63c2d9ffec43d0f1a67ba864b856b89` | `b45221644261f69c624512ab9229c30795a134c08cf90ece8c68edce8cb1d781` |

Each Git blob SHA above matched the SHA returned by GitHub when the blob was created.

## Source tree inside the archive
The archive includes:
- `README.md`
- `00_SESSION_MEMORY.md`
- `01_TASK_CONTRACT.json`
- `02_ARCHITECTURE.md`
- `03_REQUIREMENT_LEDGER.md`
- `04_COLLISION_REVIEW.md`
- `05_INTEGRATION_PROPOSAL.md`
- `06_VALIDATION_REPORT.md`
- `BUNDLE_INDEX.md`
- `EVIDENCE.json`
- `STRESS_EVIDENCE.json`
- `MANIFEST.sha256`
- `src/lo4foundry/*.py`
- `tests/test_foundry.py`
- `static_guard.py`
- `verify.py`
- `stress_verify.py`

## Reconstruct and verify
Run `RECONSTRUCT.sh`, then enter the extracted `lo4_verified_skill_foundry` directory and execute:
```bash
sha256sum -c MANIFEST.sha256
python static_guard.py
python verify.py
python stress_verify.py
```

Archive identity and local test evidence do not imply NEXY runtime integration or Canon approval.
