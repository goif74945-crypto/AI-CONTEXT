import hashlib
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parent


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative / "src.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


smw = load("smw", "01_schema_migration_witness")
ddb = load("ddb", "02_determinism_divergence_bisector")
arig = load("arig", "03_artifact_referential_integrity_guard")
mch = load("mch", "04_metamorphic_contract_harness")
ams = load("ams", "05_acceptance_mutation_sentinel")


class NoveltyQuintetIntegrationTests(unittest.TestCase):
    def test_release_evolution_guard_pipeline(self):
        migration = smw.evaluate_round_trip(
            [{"legacy_id": 7, "mode": "strict"}],
            [{"op": "rename", "from": "legacy_id", "to": "id"}],
            [{"op": "rename", "from": "id", "to": "legacy_id"}],
        )
        self.assertEqual(migration["status"], "PASS")

        traces = [
            {"id": "migrate", "deps": [], "output": migration["status"], "timestamp": "t1"},
            {"id": "verify", "deps": ["migrate"], "output": "PASS", "timestamp": "t2"},
        ]
        replay = [
            {"id": "migrate", "deps": [], "output": migration["status"], "timestamp": "different"},
            {"id": "verify", "deps": ["migrate"], "output": "PASS", "timestamp": "different2"},
        ]
        self.assertEqual(ddb.bisect_divergence(traces, replay)["status"], "EQUIVALENT")

        evidence_body = "migration=PASS;determinism=EQUIVALENT"
        evidence_hash = hashlib.sha256(evidence_body.encode()).hexdigest()
        manifest = [
            {"id": "REQ-EVOLVE", "kind": "requirement", "refs": ["TEST-EVOLVE"]},
            {"id": "TEST-EVOLVE", "kind": "test", "refs": ["EVID-EVOLVE"]},
            {"id": "EVID-EVOLVE", "kind": "evidence", "refs": [], "sha256": evidence_hash},
        ]
        self.assertEqual(arig.validate_manifest(manifest, {"EVID-EVOLVE": evidence_body})["status"], "PASS")

        relation = mch.Relation(
            name="key-order-invariant",
            mutate=lambda d: dict(reversed(list(d.items()))),
            holds=lambda fn, seed, mutated: fn(seed) == fn(mutated),
        )
        canonicalizer = lambda d: tuple(sorted(d.items()))
        self.assertEqual(mch.evaluate(canonicalizer, [{"b": 2, "a": 1}], [relation])["status"], "PASS")

        gate = lambda x: x["migration"] == "PASS" and x["integrity"] == "PASS" and bool(x["evidence"])
        baseline = {"migration": "PASS", "integrity": "PASS", "evidence": evidence_hash}
        mutators = [
            ams.Mutator("break-migration", lambda x: {**x, "migration": "FAIL"}),
            ams.Mutator("break-integrity", lambda x: {**x, "integrity": "FAIL"}),
            ams.Mutator("erase-evidence", lambda x: {**x, "evidence": ""}),
        ]
        self.assertEqual(ams.evaluate_gate(baseline, gate, mutators)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
