import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'systems' / 'skill_compiler'))
from skill_compiler import ExecutionRecord, compile_skill


def rec(i, *, steps=('inspect', 'verify'), passed=True, evidence=2):
    return ExecutionRecord(f'r{i}', 'verify artifact', steps, ('artifact',), ('report',), evidence, passed, 'sandbox')


class SkillCompilerTests(unittest.TestCase):
    def test_compiles_consistent_records(self):
        result = compile_skill([rec(1), rec(2), rec(3)])
        self.assertEqual(result.status, 'PASS')
        self.assertEqual(result.name, 'verify-artifact')
        self.assertEqual(result.provenance_record_ids, ('r1', 'r2', 'r3'))

    def test_rejects_step_drift(self):
        result = compile_skill([rec(1), rec(2), rec(3, steps=('inspect', 'mutate'))])
        self.assertEqual(result.status, 'FREEZE')

    def test_rejects_weak_evidence(self):
        result = compile_skill([rec(1), rec(2), rec(3, evidence=1)])
        self.assertEqual(result.status, 'FREEZE')

    def test_rejects_secret_literal(self):
        bad = ExecutionRecord('r3', 'verify artifact', ('inspect', 'token=TEST_ONLY_NON_SECRET_LITERAL'), ('artifact',), ('report',), 2, True, 'sandbox')
        result = compile_skill([rec(1), rec(2), bad])
        self.assertEqual(result.status, 'FREEZE')
        self.assertIn('secret', result.reason)


if __name__ == '__main__':
    unittest.main()
