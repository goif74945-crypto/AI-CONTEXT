from __future__ import annotations

import unittest

from lbcc.codec import compact
from lbcc.model import CodecPolicy, CodecStatus, ContextAtom, ContextBundle, TruthClass


class SecurityTests(unittest.TestCase):
    def test_openai_key_shape_freezes_by_default(self) -> None:
        a = ContextAtom("s", "key sk-proj-1234567890abcdefghijklmnop", TruthClass.SOURCE_FACT)
        result = compact(ContextBundle("b", (a,)), CodecPolicy(max_capsule_bytes=3000))
        self.assertEqual(result.status, CodecStatus.FREEZE)
        self.assertIn("sensitive content detected", result.reason or "")

    def test_private_key_header_freezes(self) -> None:
        a = ContextAtom("s", "-----BEGIN PRIVATE KEY-----", TruthClass.SOURCE_FACT)
        result = compact(ContextBundle("b", (a,)), CodecPolicy(max_capsule_bytes=3000))
        self.assertEqual(result.status, CodecStatus.FREEZE)

    def test_secret_in_metadata_freezes(self) -> None:
        a = ContextAtom(
            "s", "normal text", TruthClass.SOURCE_FACT,
            metadata={"credential": "AKIA1234567890ABCDEF"},
        )
        result = compact(ContextBundle("b", (a,)), CodecPolicy(max_capsule_bytes=3000))
        self.assertEqual(result.status, CodecStatus.FREEZE)

    def test_explicit_allow_sensitive_permits_processing(self) -> None:
        a = ContextAtom("s", "-----BEGIN PRIVATE KEY-----", TruthClass.SOURCE_FACT)
        result = compact(
            ContextBundle("b", (a,)),
            CodecPolicy(max_capsule_bytes=3000, allow_sensitive=True),
        )
        self.assertEqual(result.status, CodecStatus.PASS)


if __name__ == "__main__":
    unittest.main()
