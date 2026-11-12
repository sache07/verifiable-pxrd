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
from comparison import case_state, paired_comparison, solve_flags
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
    def test_three_versions_per_cycle_three_solves_each(self):
        s = learning_state()
        with self.assertRaisesRegex(ValueError, 'three solves per case in one request'):
            check_candidate_capacity(s, solves('v1', CASES), 'development')
        for v in ['v1', 'v2']:
            check_candidate_capacity(s, solves(v, CASES, 3), 'development')
            add(s, v, 'development', solves(v, CASES, 3))
        with self.assertRaisesRegex(ValueError, 'v1 already has three fresh solves on c1'):
            check_candidate_capacity(s, solves('v1', ['c1'], 3), 'evaluation')
        # A version may still be evaluated on a case it has not run on, without counting again.
        check_candidate_capacity(s, solves('v1', ['c7'], 3), 'development')
        add(s, 'v3', 'development', solves('v3', CASES, 3))
        cycle = development_cycle(s)
        self.assertEqual((cycle['candidates_used'], cycle['candidates'], cycle['candidates_spent']), (3, ['v1', 'v2', 'v3'], True))
        self.assertEqual(cycle['cycle_cases']['v2'], CASES)
        with self.assertRaisesRegex(ValueError, '3 package versions have been evaluated this cycle'):
            check_candidate_capacity(s, solves('v4', CASES, 3), 'development')
        check_candidate_capacity(s, solves('P0', ['c1']), 'baseline')

    def test_pending_transfer_does_not_close_cycle(self):
        s = learning_state()
        for v in ['v1', 'v2', 'v3']:
            add(s, v, 'development', solves(v, CASES, 3))
        add(s, 'transfer', 'transfer', solves('P0', ['n1'], 3) + solves('v2', ['n1'], 3),
            status='complete', collected=False)
        self.assertTrue(development_cycle(s)['candidates_spent'])
        with self.assertRaisesRegex(ValueError, 'package versions have been evaluated'):
            check_candidate_capacity(s, solves('v4', ['c1'], 3), 'development')
        for j in s['groups']['transfer']['jobs']:
            s['jobs'][j]['collected'] = True
        cycle = development_cycle(s)
        self.assertEqual((cycle['cycle'], cycle['candidates_used']), (2, 0))
        # The comparison's incumbent does not count as a version in the next cycle.
        add(s, 'v2-old', 'development', solves('v2', ['c7'], 3))
        for v in ['v4', 'v5', 'v6']:
            check_candidate_capacity(s, solves(v, CASES, 3), 'development')
            add(s, v, 'development', solves(v, CASES, 3))
        self.assertEqual(development_cycle(s)['candidates'], ['v4', 'v5', 'v6'])

    def test_promotion_rule_on_the_november_record(self):
        def rows(policy, scores):
            return [{'case_id': c, 'policy': policy, 'purpose': 'evaluation', 'status': 'complete',
                     'score_100': x} for c, xs in scores.items() for x in xs]
        p0 = {'c01': [95.8, 83.5, 78.3], 'c02': [57.9, 62.9, 51.7], 'c03': [46.3, 50.0, 42.6],
              'c04': [41.2, 35.1, 46.6], 'c05': [28.8, 24.1, 26.3], 'c06': [38.3, 52.4, 39.1]}
        v6 = {'c01': [95.7, 99.0, 97.7], 'c02': [80.9, 78.9, 85.2], 'c03': [83.8, 67.6, 69.3],
              'c04': [93.4, 52.6, 39.6], 'c05': [60.3, 26.2, 70.6], 'c06': [79.1, 63.8, 89.5],
              'b002-c01': [85.1, 11.6, 83.8], 'b002-c02': [84.3, 85.6, 84.3]}
        v12 = {'c03': [70.7, 76.1, 72.4], 'c04': [37.4, 33.1, 33.1], 'c05': [76.5, 67.2, 76.3],
               'c06': [79.8, 51.6, 43.1], 'b002-c01': [58.5, 56.4, 58.3], 'b002-c02': [93.2, 35.6, 89.1]}
        data = rows('P0', p0) + rows('v6', v6) + rows('v12', v12)
        r = paired_comparison(data, 'P0', {'v6': list(p0)})['packages']['v6']
        self.assertTrue(r['meets_rule'])
        self.assertAlmostEqual(r['delta'], 24.0, delta=0.1)
        r = paired_comparison(data, 'v6', {'v12': list(v12)})['packages']['v12']
        self.assertFalse(r['meets_rule'])
        self.assertAlmostEqual(r['delta'], -6.8, delta=0.1)
        self.assertAlmostEqual(r['lowest_difference'], -27.4, delta=0.1)
        # Fewer than six cases, or a case without three solves of each, cannot promote.
        r = paired_comparison(data, 'P0', {'v6': ['c01', 'c02', 'c03', 'c04', 'c05']})['packages']['v6']
        self.assertFalse(r['meets_rule'])
        r = paired_comparison(data, 'P0', {'v6': list(p0) + ['b002-c01']})['packages']['v6']
        self.assertEqual((r['meets_rule'], r['not_comparable']), (False, ['b002-c01']))

    def test_case_states(self):
        def score(d, overlaps=(100, 100), submitted=2, gate='pass', value=80.):
            return {'score_100': value, 'D_poisson': d, 'reference_fractions': [.5, .5],
                    'submitted_fractions': [.5] * submitted, 'headline_components': {'physical_gate': gate},
                    'structural_components': {'assignment': [{'composition_occupancy_overlap': o} for o in overlaps]}}
        self.assertEqual(solve_flags(score(0.05)), (True, True))
        self.assertEqual(solve_flags(score(0.5)), (True, False))
        self.assertEqual(solve_flags(score(1.5)), (False, False))
        self.assertEqual(solve_flags(score(0.05, overlaps=(100,))), (False, False))
        self.assertEqual(solve_flags(score(0.05, submitted=3)), (False, False))
        self.assertEqual(solve_flags(score(0.05, overlaps=(100, 40))), (False, False))
        self.assertEqual(solve_flags(score(0.05, gate='fail', value=0.)), (False, False))
        solve = lambda r, f: {'recovered': r, 'at_floor': f}
        self.assertEqual(case_state([solve(True, True)] * 3), 'at floor')
        self.assertEqual(case_state([solve(True, True), solve(True, False), solve(True, True)]), 'recovered')
        self.assertEqual(case_state([solve(True, True), solve(False, False), solve(True, False)]), 'inconsistent')
        self.assertEqual(case_state([solve(False, False)] * 3), 'unrecovered')

    def test_promote_refused_unless_rule_met(self):
        broker = importlib.import_module('broker')
        s = empty_state()
        s.update(paused=False, current_package='P0', requests={}, packages={'P0': {}, 'v1': {}, 'v2': {}})
        add(s, 'p0', 'baseline', solves('P0', CASES, 3), status='complete', collected=True)
        add(s, 'v1', 'development', solves('v1', CASES, 3), status='complete', collected=True)
        add(s, 'v2', 'development', solves('v2', CASES[:5], 3), status='complete', collected=True)
        scores = {'P0': [50., 60., 70.], 'v1': [70., 75., 80.], 'v2': [90., 95., 99.]}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'control').mkdir(); (p / 'work').mkdir(); (p / 'evidence/decisions').mkdir(parents=True)
            (p / 'control/settings.json').write_text((ROOT / 'control/settings.json').read_text())
            (p / 'work/notes.md').write_text('decision')
            for jid, job in s['jobs'].items():
                job.update(id=jid, purpose=s['groups'][jid.rsplit('-', 1)[0]]['purpose'])
                (p / 'evidence/attempts' / jid).mkdir(parents=True)
                value = scores[job['policy']][int(jid.rsplit('-', 1)[1]) // 6]
                (p / 'evidence/attempts' / jid / 'score.json').write_text(json.dumps({'score_100': value, 'score_status': 'scored'}))
            with patch.object(broker, 'ROOT', p), patch.object(broker, 'WORK', p / 'work'):
                with self.assertRaisesRegex(ValueError, 'v2 does not meet the promotion rule'):
                    broker.handle(s, {'command': 'promote', 'id': 'choose-v2', 'package': 'v2', 'notes': 'notes.md'})
                record = broker.handle(s, {'command': 'promote', 'id': 'choose-v1', 'package': 'v1', 'notes': 'notes.md'})
            self.assertEqual((s['current_package'], record['comparison']['cases']), ('v1', 6))
            self.assertAlmostEqual(record['comparison']['delta'], 15.0)

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
