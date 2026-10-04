import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from collision_guard import (  # noqa: E402
    Candidate,
    ProjectRecord,
    analyze_candidate,
    build_catalog,
    discover_projects,
    normalize_terms,
)


class NormalizeTermsTests(unittest.TestCase):
    def test_removes_generic_noise_but_keeps_domain_terms(self):
        terms = normalize_terms('CHAT-20261005-0122-NEXY-SUPPLEMENTAL-COLLISION-GUARD')
        self.assertIn('collision', terms)
        self.assertIn('guard', terms)
        self.assertNotIn('chat', terms)
        self.assertNotIn('nexy', terms)
        self.assertNotIn('20261005', terms)


class DiscoveryTests(unittest.TestCase):
    def test_discovers_only_immediate_project_directories(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p1 = root / 'CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY'
            p1.mkdir()
            (p1 / 'README.md').write_text('# Knowledge Foundry\nEvidence ledger and provenance.\n', encoding='utf-8')
            nested = p1 / 'src'
            nested.mkdir()
            (nested / 'module.md').write_text('# Internal Module', encoding='utf-8')
            p2 = root / 'NEXY-FUTURE-ASSURANCE-LAB'
            p2.mkdir()
            (p2 / 'README.md').write_text('# Assurance Lab\nFormal proof obligations.\n', encoding='utf-8')
            (root / '00_INDEX.md').write_text('# index', encoding='utf-8')

            records = discover_projects(root)
            names = {r.name for r in records}

            self.assertEqual(
                names,
                {
                    'CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY',
                    'NEXY-FUTURE-ASSURANCE-LAB',
                },
            )


class CandidateAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            ProjectRecord.from_text(
                name='CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY',
                path='CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY',
                text='knowledge foundry evidence ledger provenance architecture',
            ),
            ProjectRecord.from_text(
                name='CHAT-20261005-0121-NEXY-EXPERIENCE-COMPILER',
                path='CHAT-20261005-0121-NEXY-EXPERIENCE-COMPILER',
                text='experience compiler interaction friction delight user journey',
            ),
            ProjectRecord.from_text(
                name='CHAT-20261005-0114-NEXY-KNOWLEDGE-DECAY-LAB',
                path='CHAT-20261005-0114-NEXY-KNOWLEDGE-DECAY-LAB',
                text='knowledge decay freshness temporal validity stale context',
            ),
        ]

    def test_flags_near_duplicate_with_explanation(self):
        candidate = Candidate(
            title='NEXY Knowledge Provenance Foundry',
            summary='evidence ledger provenance architecture for knowledge records',
        )
        result = analyze_candidate(candidate, self.records)

        self.assertEqual(result['classification'], 'HIGH_OVERLAP')
        self.assertEqual(
            result['top_matches'][0]['project'],
            'CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY',
        )
        self.assertIn('provenance', result['top_matches'][0]['shared_terms'])
        self.assertGreaterEqual(result['top_matches'][0]['score'], 0.62)

    def test_marks_orthogonal_candidate_distinct(self):
        candidate = Candidate(
            title='Supplemental Collision Guard',
            summary='detect duplicate parallel chat projects by overlap fingerprints and collision risk',
        )
        result = analyze_candidate(candidate, self.records)

        self.assertEqual(result['classification'], 'DISTINCT')
        self.assertLess(result['top_matches'][0]['score'], 0.38)

    def test_result_order_is_deterministic(self):
        candidate = Candidate(
            title='Knowledge lifecycle',
            summary='knowledge freshness provenance evidence',
        )
        first = analyze_candidate(candidate, list(self.records))
        second = analyze_candidate(candidate, list(reversed(self.records)))
        self.assertEqual(first['top_matches'], second['top_matches'])


class CatalogTests(unittest.TestCase):
    def test_catalog_is_json_serializable_and_has_stable_schema(self):
        records = [
            ProjectRecord.from_text('A', 'A', 'alpha beta gamma'),
            ProjectRecord.from_text('B', 'B', 'delta epsilon'),
        ]
        catalog = build_catalog(records)
        encoded = json.dumps(catalog, sort_keys=True)
        self.assertIn('supplemental-collision-guard/v1', encoded)
        self.assertEqual(catalog['project_count'], 2)
        self.assertEqual([p['name'] for p in catalog['projects']], ['A', 'B'])


class GuardrailTests(unittest.TestCase):
    def test_exact_duplicate_is_likely_duplicate(self):
        record = ProjectRecord.from_text(
            'NEXY-COLLISION-GUARD',
            'NEXY-COLLISION-GUARD',
            'collision guard duplicate overlap parallel registry coordination',
        )
        candidate = Candidate(
            title='NEXY Collision Guard',
            summary='collision guard duplicate overlap parallel registry coordination',
        )
        result = analyze_candidate(candidate, [record])
        self.assertEqual(result['classification'], 'LIKELY_DUPLICATE')

    def test_generated_directory_does_not_change_project_fingerprint(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / 'CHAT-ONE'
            project.mkdir()
            (project / 'README.md').write_text('# Collision Registry\nparallel project overlap\n', encoding='utf-8')
            first = discover_projects(root)[0]
            generated = project / 'generated'
            generated.mkdir()
            (generated / 'catalog.json').write_text('{"volatile":"content"}', encoding='utf-8')
            second = discover_projects(root)[0]
            self.assertEqual(first.content_hash, second.content_hash)
            self.assertEqual(first.terms, second.terms)

    def test_missing_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / 'missing'
            with self.assertRaisesRegex(ValueError, 'does not exist'):
                discover_projects(missing)

class CliPolicyTests(unittest.TestCase):
    def _seed_root(self, root: Path) -> None:
        project = root / 'CHAT-20261005-0111-NEXY-KNOWLEDGE-FOUNDRY'
        project.mkdir()
        (project / 'README.md').write_text(
            '# Knowledge Foundry\nknowledge evidence ledger provenance architecture\n',
            encoding='utf-8',
        )

    def test_fail_at_high_overlap_returns_policy_exit_code_2(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_root(root)
            cmd = [
                sys.executable,
                str(ROOT / 'src' / 'collision_guard.py'),
                'check', '--root', str(root),
                '--title', 'Knowledge Provenance Foundry',
                '--summary', 'knowledge evidence ledger provenance architecture records',
                '--fail-at', 'HIGH_OVERLAP',
            ]
            completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertIn(payload['classification'], {'HIGH_OVERLAP', 'LIKELY_DUPLICATE'})

    def test_fail_at_high_overlap_allows_distinct_candidate(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._seed_root(root)
            cmd = [
                sys.executable,
                str(ROOT / 'src' / 'collision_guard.py'),
                'check', '--root', str(root),
                '--title', 'Supplemental Collision Guard',
                '--summary', 'duplicate parallel collision overlap registry coordination',
                '--fail-at', 'HIGH_OVERLAP',
            ]
            completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload['classification'], 'DISTINCT')

class FingerprintIntegrityTests(unittest.TestCase):
    def test_relative_file_path_changes_content_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / 'CHAT-ONE'
            (project / 'docs').mkdir(parents=True)
            (project / 'docs' / 'same.md').write_text('same content', encoding='utf-8')
            first = discover_projects(root)[0].content_hash

            (project / 'specs').mkdir()
            (project / 'specs' / 'same.md').write_text('same content', encoding='utf-8')
            (project / 'docs' / 'same.md').unlink()
            second = discover_projects(root)[0].content_hash

            self.assertNotEqual(first, second)

class SecurityBoundaryTests(unittest.TestCase):
    def test_symlinked_file_outside_project_is_not_read(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'supplemental'
            root.mkdir()
            project = root / 'CHAT-ONE'
            project.mkdir()
            (project / 'README.md').write_text('collision coordination registry', encoding='utf-8')

            outside = Path(td) / 'outside-secret.txt'
            outside.write_text('ultrasecret external payload', encoding='utf-8')
            link = project / 'leak.txt'
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest('symlink creation not supported in this environment')

            record = discover_projects(root)[0]
            self.assertNotIn('ultrasecret', record.terms)
            self.assertNotIn('external', record.terms)
            self.assertEqual(record.files_read, 1)


class CandidateValidityTests(unittest.TestCase):
    def test_blank_candidate_title_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'title'):
            Candidate(title='   ')

    def test_candidate_without_discriminating_terms_is_rejected(self):
        candidate = Candidate(title='NEXY AI CHAT 20261005')
        with self.assertRaisesRegex(ValueError, 'discriminating'):
            analyze_candidate(candidate, [])

class AdditionalBoundaryTests(unittest.TestCase):
    def test_symlinked_project_directory_is_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / 'supplemental'
            root.mkdir()
            real = base / 'external-project'
            real.mkdir()
            (real / 'README.md').write_text('external private project', encoding='utf-8')
            link = root / 'CHAT-LINKED'
            try:
                link.symlink_to(real, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('directory symlink creation not supported in this environment')

            records = discover_projects(root)
            self.assertEqual(records, [])

    def test_cli_rejects_candidate_without_discriminating_terms_without_traceback(self):
        import subprocess
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cmd = [
                sys.executable,
                str(ROOT / 'src' / 'collision_guard.py'),
                'check', '--root', str(root),
                '--title', 'NEXY AI CHAT 20261005',
            ]
            completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 2)
            self.assertIn('discriminating', completed.stderr.lower())
            self.assertNotIn('Traceback', completed.stderr)


if __name__ == '__main__':
    unittest.main()
