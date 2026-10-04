from __future__ import annotations

from itertools import permutations

from nexy_interchange import canonical_text, fingerprint


def test_all_120_top_level_key_permutations_canonicalize_identically() -> None:
    pairs = [("alpha", 1), ("beta", 2), ("gamma", 3), ("delta", 4), ("epsilon", 5)]
    expected_text = None
    expected_hash = None
    observed = 0
    for permutation in permutations(pairs):
        value = dict(permutation)
        text = canonical_text(value)
        digest = fingerprint(value)
        if expected_text is None:
            expected_text = text
            expected_hash = digest
        assert text == expected_text
        assert digest == expected_hash
        observed += 1
    assert observed == 120


def test_repeated_execution_1000_times_is_byte_identical() -> None:
    value = {
        "task": "T-001",
        "constraints": ["zero-guess", "verify-only"],
        "state": {"status": "FREEZE", "code": 7},
    }
    expected = canonical_text(value)
    expected_hash = fingerprint(value)
    for _ in range(1000):
        assert canonical_text(value) == expected
        assert fingerprint(value) == expected_hash
