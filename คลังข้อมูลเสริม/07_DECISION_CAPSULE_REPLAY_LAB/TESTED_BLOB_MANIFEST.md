# Tested Blob Manifest

Status: VERIFIED TEST BASELINE  
Branch: `dcrl-20261005-0121`

These are Git blob object IDs for the exact Python source and test files that correspond byte-for-byte to the local baseline on which the latest 30/30 test suite and compile checks passed.

| Git blob | Path |
|---|---|
| `ef0a45e4c9a47f9246311062318a8717441edec4` | `src/nexy_dcr/__init__.py` |
| `6a75e6c52a088b92da60a20d8983e663b096c060` | `src/nexy_dcr/builder.py` |
| `5a54828c716b21347ab6fe5ba76595779a52fa60` | `src/nexy_dcr/canonical.py` |
| `c2e2593852c8858f4a596e5bb587a550ecad1ee2` | `src/nexy_dcr/cli.py` |
| `b6578c85917440e874eaef7e740a393cf6e70538` | `src/nexy_dcr/diff.py` |
| `1837251b6ad13df3abaeec9d4d8fe4ad45b9776d` | `src/nexy_dcr/errors.py` |
| `f8f05532ff56d6811fd86fbfa0b94c1baa34dff8` | `src/nexy_dcr/io.py` |
| `353599ece5bda1e62403596a46cebda18a211a91` | `src/nexy_dcr/model.py` |
| `9fd85b4389873e834a364aa38c6f043bf2a9bcbd` | `src/nexy_dcr/receipt.py` |
| `a13e36622e0b2b053f70faa184247bfbb02caf7e` | `src/nexy_dcr/replay.py` |
| `9cc7dd28aec8536d8be020c796f22c6543b745a0` | `tests/helpers.py` |
| `d16c24a7ee2258bd95d9b30fbb12dfb1d9ef4ef5` | `tests/test_canonical.py` |
| `30f224422842d2e66adaf1548ef04ef790d0658b` | `tests/test_diff.py` |
| `17817450c83ce841dcb837b52b8ae9181558cc18` | `tests/test_integrity.py` |
| `0fff7a4812ee5cdca88075c0676de4b0763e2906` | `tests/test_io_cli.py` |
| `e524881b211f965cf6cb4cbb5eb80eb3db6a6113` | `tests/test_receipt.py` |
| `361695f4569f0881be0ed38eac5fe3c4693c0e2e` | `tests/test_replay.py` |

## Verification meaning

Matching a Git blob ID proves repository file content is byte-for-byte identical to the tested file content under Git's blob identity algorithm. It does **not** by itself prove a deployment, external evidence truthfulness, cryptographic signer identity or NEXY runtime integration.
