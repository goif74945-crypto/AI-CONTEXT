import hashlib

from nulf.artifact import ArtifactFile, ConsumerProfile, evaluate


def profile(**kwargs):
    base = dict(
        profile_id="consumer",
        required_files=frozenset({"report.pdf"}),
        allowed_media_types=frozenset({"application/pdf"}),
        required_metadata=frozenset({"title"}),
        forbidden_classifications=frozenset({"SECRET"}),
        max_total_bytes=100,
        require_hash_match=True,
    )
    base.update(kwargs)
    return ConsumerProfile(**base)


def afile(name="report.pdf", content=b"ok", media="application/pdf", classification="INTERNAL", digest=None):
    digest = digest or hashlib.sha256(content).hexdigest()
    return ArtifactFile(name, media, content, digest, classification)


def test_fitness_pass():
    result = evaluate(profile(), (afile(),), {"title": "R"})
    assert result["verdict"] == "PASS"


def test_missing_required_file_freezes():
    result = evaluate(profile(), (), {"title": "R"})
    assert "MISSING_REQUIRED_FILE" in result["reason_codes"]


def test_hash_mismatch_freezes():
    result = evaluate(profile(), (afile(digest="0" * 64),), {"title": "R"})
    assert result["hash_mismatches"] == ["report.pdf"]


def test_forbidden_classification_freezes():
    result = evaluate(profile(), (afile(classification="SECRET"),), {"title": "R"})
    assert "FORBIDDEN_CLASSIFICATION" in result["reason_codes"]


def test_size_and_metadata_enforced():
    result = evaluate(profile(max_total_bytes=1), (afile(content=b"long"),), {"title": ""})
    assert "PACKAGE_TOO_LARGE" in result["reason_codes"]
    assert "MISSING_REQUIRED_METADATA" in result["reason_codes"]


def test_file_input_order_does_not_change_fingerprint():
    p = profile(required_files=frozenset({"report.pdf"}), allowed_media_types=frozenset({"application/pdf", "text/plain"}))
    a = afile()
    extra = afile(name="notes.txt", media="text/plain", content=b"n")
    one = evaluate(p, (a, extra), {"title": "R"})
    two = evaluate(p, (extra, a), {"title": "R"})
    assert one["fingerprint"] == two["fingerprint"]
