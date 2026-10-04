import math

import pytest

from nexy_mvk.canonical import CanonicalizationError, canonical_json, stable_hash
from nexy_mvk.model import Case


def test_mapping_order_does_not_change_hash():
    assert stable_hash({"b": 2, "a": 1}) == stable_hash({"a": 1, "b": 2})


def test_set_order_does_not_change_hash():
    assert stable_hash({"x", "y", "z"}) == stable_hash({"z", "x", "y"})


def test_case_hash_is_stable_for_permission_order():
    left = Case(prompt="x", permissions=frozenset({"read", "write"}))
    right = Case(prompt="x", permissions=frozenset({"write", "read"}))
    assert stable_hash(left) == stable_hash(right)


def test_non_finite_float_rejected():
    with pytest.raises(CanonicalizationError):
        canonical_json(math.inf)


def test_unknown_object_rejected_instead_of_repr_fallback():
    with pytest.raises(CanonicalizationError):
        canonical_json(object())

from enum import Enum


def test_enum_is_canonicalized_by_value():
    class Mode(str, Enum):
        SAFE = "safe"
    assert canonical_json(Mode.SAFE) == '"safe"'


def test_non_string_mapping_key_rejected():
    with pytest.raises(CanonicalizationError, match="mapping keys must be strings"):
        canonical_json({1: "bad"})
