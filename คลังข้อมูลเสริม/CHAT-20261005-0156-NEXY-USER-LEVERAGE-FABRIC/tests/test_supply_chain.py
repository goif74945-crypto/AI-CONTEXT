from nulf.supply_chain import Dependency, TrustPolicy, audit


def policy(**kwargs):
    base = dict(
        allowed_sources=frozenset({"internal"}),
        allowed_signature_states=frozenset({"VERIFIED"}),
        allowed_permissions=frozenset({"read"}),
        allowed_network_domains=frozenset({"api.example.com"}),
        require_pinned=True,
        require_sha256=True,
    )
    base.update(kwargs)
    return TrustPolicy(**base)


def dep(**kwargs):
    base = dict(
        name="tool",
        version="1.0.0",
        source="internal",
        sha256="a" * 64,
        pinned=True,
        signature_state="VERIFIED",
        permissions=frozenset({"read"}),
        network_domains=frozenset({"api.example.com"}),
    )
    base.update(kwargs)
    return Dependency(**base)


def test_trusted_dependency_passes():
    assert audit(policy(), (dep(),))["verdict"] == "PASS"


def test_unpinned_freezes():
    result = audit(policy(), (dep(pinned=False),))
    assert "UNPINNED_VERSION" in result["reason_codes"]


def test_permission_violation_freezes():
    result = audit(policy(), (dep(permissions=frozenset({"read", "admin"})),))
    assert "PERMISSION_NOT_ALLOWED" in result["reason_codes"]


def test_network_violation_freezes():
    result = audit(policy(), (dep(network_domains=frozenset({"evil.example"})),))
    assert "NETWORK_DOMAIN_NOT_ALLOWED" in result["reason_codes"]


def test_invalid_digest_and_source_freeze():
    result = audit(policy(), (dep(source="unknown", sha256="nope"),))
    assert "INVALID_SHA256" in result["reason_codes"]
    assert "UNTRUSTED_SOURCE" in result["reason_codes"]


def test_dependency_input_order_does_not_change_result_or_fingerprint():
    a = dep(name="a")
    b = dep(name="b", sha256="b" * 64)
    assert audit(policy(), (a, b)) == audit(policy(), (b, a))
