from __future__ import annotations

import pytest

from nexy_interchange import (
    CanonicalLimits,
    CycleError,
    DuplicateKeyError,
    InvalidUnicodeError,
    NonStringKeyError,
    NormalizationCollisionError,
    ResourceLimitError,
    UnsafeIntegerError,
    UnsupportedTypeError,
    canonical_text,
    canonicalize_json_text,
    fingerprint,
    loads_strict,
)


def test_key_order_is_irrelevant() -> None:
    a = {"z": 1, "a": 2, "nested": {"b": True, "a": None}}
    b = {"nested": {"a": None, "b": True}, "a": 2, "z": 1}
    assert canonical_text(a) == canonical_text(b)
    assert fingerprint(a) == fingerprint(b)


def test_unicode_nfc_produces_same_value_and_hash() -> None:
    decomposed = {"name": "Cafe\u0301"}
    composed = {"name": "Caf\u00e9"}
    assert canonical_text(decomposed) == canonical_text(composed)
    assert fingerprint(decomposed) == fingerprint(composed)


def test_unicode_key_normalization_collision_is_rejected() -> None:
    value = {"Caf\u00e9": 1, "Cafe\u0301": 2}
    with pytest.raises(NormalizationCollisionError):
        canonical_text(value)


def test_float_is_rejected() -> None:
    with pytest.raises(UnsupportedTypeError):
        canonical_text({"x": 0.1})


def test_non_string_key_is_rejected() -> None:
    with pytest.raises(NonStringKeyError):
        canonical_text({1: "x"})


def test_unsafe_integer_is_rejected() -> None:
    with pytest.raises(UnsafeIntegerError):
        canonical_text({"x": 2**53})


def test_safe_integer_boundaries_are_accepted() -> None:
    assert canonical_text({"lo": -(2**53 - 1), "hi": 2**53 - 1})


def test_duplicate_raw_json_key_is_rejected() -> None:
    with pytest.raises(DuplicateKeyError):
        loads_strict('{"a":1,"a":2}')


def test_json_float_is_rejected_during_parse() -> None:
    with pytest.raises(UnsupportedTypeError):
        loads_strict('{"a":1.0}')


def test_non_standard_nan_is_rejected_during_parse() -> None:
    with pytest.raises(Exception) as exc_info:
        loads_strict('{"a":NaN}')
    assert "NaN" in str(exc_info.value)


def test_cyclic_list_is_rejected() -> None:
    value: list[object] = []
    value.append(value)
    with pytest.raises(CycleError):
        canonical_text(value)


def test_cyclic_dict_is_rejected() -> None:
    value: dict[str, object] = {}
    value["self"] = value
    with pytest.raises(CycleError):
        canonical_text(value)


def test_depth_limit_is_enforced() -> None:
    with pytest.raises(ResourceLimitError):
        canonical_text([[[0]]], limits=CanonicalLimits(max_depth=2))


def test_node_limit_is_enforced() -> None:
    with pytest.raises(ResourceLimitError):
        canonical_text([1, 2, 3], limits=CanonicalLimits(max_nodes=3))


def test_output_byte_limit_is_enforced() -> None:
    with pytest.raises(ResourceLimitError):
        canonical_text("abcdef", limits=CanonicalLimits(max_output_bytes=4))


def test_strict_json_canonicalization() -> None:
    assert canonicalize_json_text(' { "b": 2, "a": [true, null] } ') == '{"a":[true,null],"b":2}'



def test_unpaired_surrogate_is_rejected() -> None:
    with pytest.raises(InvalidUnicodeError):
        canonical_text({"x": "\ud800"})


def test_surrogate_in_key_is_rejected() -> None:
    with pytest.raises(InvalidUnicodeError):
        canonical_text({"\udfff": 1})


def test_domain_separation_changes_fingerprint() -> None:
    value = {"x": 1}
    assert fingerprint(value, domain="A") != fingerprint(value, domain="B")
