import unittest
from dataclasses import replace

from nexy_live_integrity import GateStatus, IntentContract, IntentEquivalenceGate


class MultimodalIntentTests(unittest.TestCase):
    def contract(self, modality):
        return IntentContract(
            modality=modality,
            objective="Create verified artifact",
            operation="build",
            targets=("project:A",),
            mode="strict",
            allow_external=False,
            deterministic_required=True,
            authority_scope="project:A",
            constraints=(("no_delete", "true"),),
        )

    def test_equivalent_text_voice_pass(self):
        result = IntentEquivalenceGate.compare([self.contract("text"), self.contract("voice")], required_modalities=("text", "voice"))
        self.assertEqual(result.status, GateStatus.PASS)

    def test_target_divergence_freezes(self):
        text = self.contract("text")
        voice = replace(self.contract("voice"), targets=("project:B",))
        result = IntentEquivalenceGate.compare([text, voice])
        self.assertEqual(result.code, "INTENT_SEMANTIC_DIVERGENCE")
        self.assertIn("voice:targets", result.mismatches)

    def test_external_permission_divergence_freezes(self):
        text = self.contract("text")
        voice = replace(self.contract("voice"), allow_external=True)
        result = IntentEquivalenceGate.compare([text, voice])
        self.assertIn("voice:allow_external", result.mismatches)

    def test_missing_required_modality_freezes(self):
        result = IntentEquivalenceGate.compare([self.contract("text")], required_modalities=("text", "image"))
        self.assertEqual(result.code, "INTENT_REQUIRED_MODALITY_MISSING")


if __name__ == "__main__":
    unittest.main()
