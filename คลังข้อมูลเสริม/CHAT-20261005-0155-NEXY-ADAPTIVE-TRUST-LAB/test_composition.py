from __future__ import annotations

import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

ROOT = Path(__file__).parent


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel / "reference.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


mcae = load("mcae_ref", "01_multimodal_claim_arbitration")
cpac = load("cpac_ref", "02_consent_purpose_action_compiler")
emcr = load("emcr_ref", "03_empirical_model_calibration_router")
ivs = load("ivs_ref", "04_incremental_verification_scheduler")
cdhc = load("cdhc_ref", "05_cross_device_handoff_capsule")


class TestComposition(unittest.TestCase):
    def test_reference_components_can_coexist_in_fail_closed_flow(self):
        claims = [
            mcae.Claim("c1", "artifact_ready", True, "tool", "test-a", "verified", 1.0),
            mcae.Claim("c2", "artifact_ready", True, "text", "review-a", "observed", 0.9),
        ]
        self.assertEqual(mcae.arbitrate(claims).status, "ALLOW")

        now = datetime(2026, 10, 5, 2, 0, tzinfo=timezone.utc)
        grant = cpac.ConsentGrant(
            "g1", "u1", ("publish_verified_artifact",), ("publish",), ("artifact:1",),
            now - timedelta(minutes=1), now + timedelta(minutes=5), False,
        )
        req = cpac.ActionRequest("r1", "u1", "publish_verified_artifact", "publish", "artifact:1", now)
        self.assertEqual(cpac.evaluate([grant], req).status, "ALLOW")

        observations = [
            emcr.Observation("model-a", "summarize", True, 0.9, 100, 10),
            emcr.Observation("model-a", "summarize", True, 0.9, 110, 10),
            emcr.Observation("model-a", "summarize", True, 0.8, 120, 10),
        ]
        self.assertEqual(emcr.route(observations, "summarize").status, "ROUTE")

        deps = {"api": {"core"}}
        tests = [ivs.TestSpec("core_api", frozenset({"core", "api"}), 1.0)]
        self.assertEqual(ivs.schedule(deps, ["core"], tests).status, "PLAN")

        state = {"objective": "continue verified publish task", "verified_state": {"status": "PARTIAL"}, "next_action": "run superior NEXY gates"}
        capsule = cdhc.build_capsule(state, b"composition-test-secret", "trusted-target", 100, 60)
        self.assertEqual(cdhc.verify_capsule(capsule, b"composition-test-secret", "trusted-target", 110)[0], "ALLOW")


if __name__ == "__main__":
    unittest.main()
