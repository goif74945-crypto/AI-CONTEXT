# Integration Evidence

Two E3-style local integration scenarios execute cross-module behavior:

1. All configured critical gates clear. Result PASS but proposal/non-promotion advisories remain.
2. Authority expansion + stale proof + capability exfiltration path + replay divergence occur together. Result FREEZE with all four blocker codes.

Executed in `tests/test_integration.py`; included in the 27-test PASS record.
