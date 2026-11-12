"""Offline scheduling/deployment checks. No scientist, solver, SSH or service calls."""
from pathlib import Path
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'control'))
from progression import check_candidate_capacity, development_cycle, require_transfer_complete
import common


CASES = [f'c{i}' for i in range(1, 7)]


def empty_state():
    return {'groups': {}, 'jobs': {}, 'batches': {'b1': {'kind': 'learning'}}}


def solves(policy, cases, repeats=1):
    """Slots in schedule order: every case once before any repeat."""
    return [{'policy': policy, 'case_id': c} for _ in range(repeats) for c in cases]


def add(state, gid, purpose, slots, **job):
    group = state['groups'][gid] = {'id': gid, 'purpose': purpose, 'jobs': [],
        'created_at': f"{len(state['groups']):03}", 'policies': sorted({s['policy'] for s in slots})}
    for k, slot in enumerate(slots):
        group['jobs'].append(f'{gid}-{k}')
        state['jobs'][f'{gid}-{k}'] = {**slot, 'status': 'queued', **job}


def learning_state():
    s = empty_state()
    add(s, 'p0', 'baseline', solves('P0', CASES, 3))
    return s


class AlignmentTests(unittest.TestCase):
    def test_package_solves_count_except_evaluation_repeats(self):
        s = learning_state()
        add(s, 'v1', 'development', solves('v1', CASES))
        cycle = development_cycle(s)
        self.assertEqual((cycle['development_solves_used'], cycle['evaluation_solves_free']), (6, 0))
        # The 3-rollout evaluation: a package's 2nd and 3rd solve on a case are free.
        check_candidate_capacity(s, solves('v1', CASES, 2), 'evaluation')
        add(s, 'v1-eval', 'evaluation', solves('v1', CASES, 2))
        cycle = development_cycle(s)
        self.assertEqual((cycle['development_solves_used'], cycle['evaluation_solves_free']), (6, 12))
        with self.assertRaisesRegex(ValueError, 'already has three'):
            check_candidate_capacity(s, solves('v1', ['c1']), 'evaluation')
        # A 1st solve counts even under evaluation, so evaluation cannot screen for free;
        # reruns outside evaluation, diagnostics and package baselines all count.
        add(s, 'v2', 'evaluation', solves('v2', ['c1'], 3))
        add(s, 'v2-rerun', 'development', solves('v2', ['c1']))
        add(s, 'v2-diag', 'diagnostic', solves('v2', ['c2']))
        add(s, 'mixed', 'baseline', solves('P0', ['c3']) + solves('v2', ['c3']))
        cycle = development_cycle(s)
        self.assertEqual((cycle['development_solves_used'], cycle['evaluation_solves_free']), (10, 14))
        self.assertFalse(cycle['budget_reached'])

    def test_spent_budget_completes_one_package(self):
        s = learning_state()
        for v in ['v1', 'v2', 'v3', 'v4']:
            add(s, v, 'development', solves(v, CASES))
        add(s, 'v5', 'development', solves('v5', ['c1', 'c2']))
        with self.assertRaisesRegex(ValueError, 'Development budget: 26 of 30 .* needs 5'):
            check_candidate_capacity(s, solves('v6', CASES[:5]), 'development')
        # An evaluation that crosses the limit completes its package uncounted.
        check_candidate_capacity(s, solves('v6', CASES, 3), 'evaluation')
        add(s, 'v6', 'development', solves('v6', CASES[:4]))
        self.assertTrue(development_cycle(s)['budget_reached'])
        with self.assertRaisesRegex(ValueError, 'Development budget: 30 of 30'):
            check_candidate_capacity(s, solves('v7', ['c1']), 'development')
        check_candidate_capacity(s, solves('P0', ['c1']), 'baseline')
        # The most promising package reaches three solves per case, including
        # set-aside cases it never ran on, without counting.
        add(s, 'v6-eval', 'evaluation', solves('v6', CASES[:4], 2) + solves('v6', CASES[4:], 3))
        cycle = development_cycle(s)
        self.assertEqual((cycle['development_solves_used'], cycle['evaluation_solves_free'],
                          cycle['package_completed_after_budget']), (30, 14, 'v6'))
        with self.assertRaisesRegex(ValueError, 'v6 is the package being completed'):
            check_candidate_capacity(s, solves('v5', ['c1']), 'evaluation')
        with self.assertRaisesRegex(ValueError, 'c7 has not been run in this cycle'):
            check_candidate_capacity(s, solves('v6', ['c7']), 'evaluation')

    def test_pending_transfer_does_not_close_cycle(self):
        s = learning_state()
        for v in ['v1', 'v2', 'v3', 'v4', 'v5']:
            add(s, v, 'development', solves(v, CASES))
        add(s, 'transfer', 'transfer', solves('P0', ['n1']) + solves('v4', ['n1']),
            status='complete', collected=False)
        self.assertTrue(development_cycle(s)['budget_reached'])
        with self.assertRaisesRegex(ValueError, 'Development budget'):
            check_candidate_capacity(s, solves('v6', ['c1']), 'development')
        for j in s['groups']['transfer']['jobs']:
            s['jobs'][j]['collected'] = True
        cycle = development_cycle(s)
        self.assertEqual((cycle['cycle'], cycle['development_solves_used']), (2, 0))
        check_candidate_capacity(s, solves('v6', CASES), 'development')

    def test_new_case_learning_waits_for_whole_transfer(self):
        s = empty_state()
        s['batches']['b2'] = {'kind': 'transfer', 'transfer_group': 'g'}
        s['groups']['g'] = {'jobs': ['a', 'b']}
        s['jobs'] = {'a': {'status': 'complete', 'collected': True},
                     'b': {'status': 'running', 'collected': False}}
        require_transfer_complete(s, 'b1')
        with self.assertRaises(ValueError):
            require_transfer_complete(s, 'b2')
        for status in ['interrupted', 'evaluator_error', 'complete']:
            s['jobs']['b']['status'] = status
            with self.assertRaises(ValueError):
                require_transfer_complete(s, 'b2')
        s['jobs']['b']['collected'] = True
        require_transfer_complete(s, 'b2')

    def test_no_fallback_to_old_score(self):
        # Test the guard on an isolated bad configuration. Never execute the
        # real installer from a unit test, including after deployment is ready.
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'control').mkdir();(p/'scorer').mkdir()
            (p/'control/settings.json').write_text('{"primary_metric":"profile_primary_agreement"}')
            (p/'scorer/config.json').write_text('{"headline_metric":"old_profile_score"}')
            with patch.object(common,'ROOT',p):
                with self.assertRaisesRegex(ValueError, 'Scoring deployment incomplete'):
                    common.require_scoring_alignment()
        common.require_scoring_alignment()

    def test_not_deployed_verifier_explains_blocker(self):
        with tempfile.TemporaryDirectory() as d:
            w=Path(d)
            (w/'verify_environment.py').write_bytes((ROOT/'evolve/verify_environment.py').read_bytes())
            (w/'environment.json').write_text('{"status":"workshop_not_deployed"}')
            p = subprocess.run([sys.executable, str(w/'verify_environment.py')],
                               capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(json.loads(p.stdout)['checks']['deployment_complete'])
        self.assertNotIn('Traceback', p.stderr)

    def test_no_implicit_target_and_lab_settings_parse(self):
        for name in ['control/settings.json', 'evolve/settings.json']:
            c = json.loads((ROOT / name).read_text())
            self.assertNotIn('case_target', c)
            self.assertEqual(c['primary_metric'], 'profile_primary_agreement')
            self.assertEqual(c['solver_timeout_seconds'], 14400)
            self.assertIsNone(c['total_solver_budget'])
            self.assertEqual(c['max_guidance_words'], 600)
        sys.path.insert(0, str(ROOT / 'runtime'))
        from labspec import protocol
        self.assertEqual(protocol(ROOT / 'evolve/LAB.md')['generation']['training_cases'], 6)

    def test_reporting_has_separate_diagnostics_no_cutoff(self):
        broker = importlib.import_module('broker')
        s = empty_state()
        s.update(paused=False, current_package='P0', requests={})
        s['jobs'] = {'a': {'id': 'a', 'case_id': 'c1', 'policy': 'P0',
            'group': 'g', 'purpose': 'baseline', 'status': 'complete'}}
        s['jobs']['b'] = dict(s['jobs']['a'], id='b')
        s['jobs']['c'] = dict(s['jobs']['a'], id='c')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            for sub in ['control', 'scorer', 'evidence/attempts/a', 'evidence/attempts/b', 'evidence/attempts/c']:
                (p / sub).mkdir(parents=True)
            (p / 'control/settings.json').write_text((ROOT / 'control/settings.json').read_text())
            (p / 'scorer/config.json').write_text('{"version":"test-structural"}')
            (p / 'evidence/attempts/a/score.json').write_text(json.dumps({
                'score_100': 91., 'score_status': 'scored', 'D_poisson': .4,
                'independent_atomic_rwp': 3.2}))
            (p / 'evidence/attempts/b/score.json').write_text(json.dumps({
                'score_100': None, 'score_status': 'needs_adjudication',
                'score_interval': [36.2, 85.5], 'D_poisson': .6,
                'independent_atomic_rwp': 4.2}))
            (p / 'evidence/attempts/c/score.json').write_text(json.dumps({
                'score_100': 40., 'score_status': 'needs_adjudication', 'D_poisson': 9.0,
                'independent_atomic_rwp': 9.5}))
            with patch.object(broker, 'ROOT', p):
                broker.report(s)
            report = (p / 'evidence/STATUS.md').read_text()
            self.assertNotIn('≥80', report)
            self.assertIn('91.0', report)
            self.assertIn('0.400', report)
            self.assertIn('3.20', report)
            self.assertIn('36.2–85.5†', report)
            self.assertIn('2/3', report)
            self.assertIn('| 65.5 | 91.0 |', report)
            self.assertEqual(json.loads((p / 'evidence/status.json').read_text())['primary_metric'],
                             'profile_primary_agreement')


if __name__ == '__main__':
    unittest.main()
