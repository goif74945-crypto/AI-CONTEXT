from __future__ import annotations

import json
from pathlib import Path

import pytest

from nexy_interchange import canonical_text, fingerprint, loads_strict
from nexy_interchange.errors import InterchangeError

ROOT = Path(__file__).resolve().parents[1]


def test_valid_conformance_vectors() -> None:
    vectors = json.loads((ROOT / "conformance" / "valid-vectors.json").read_text(encoding="utf-8"))
    assert vectors
    for vector in vectors:
        assert canonical_text(vector["input"]) == vector["canonical"], vector["name"]
        assert fingerprint(vector["input"]) == vector["fingerprint"], vector["name"]


def test_invalid_conformance_vectors() -> None:
    vectors = json.loads((ROOT / "conformance" / "invalid-vectors.json").read_text(encoding="utf-8"))
    assert vectors
    for vector in vectors:
        with pytest.raises(InterchangeError) as exc_info:
            loads_strict(vector["input_json"])
        assert exc_info.value.code == vector["expected_error"], vector["name"]
