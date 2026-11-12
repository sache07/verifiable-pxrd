"""Offline procedure-test checks: request selection, gating and tracking. No services, sandboxes or scoring."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import broker
import procedure_runner
import procedure_test as pt


class ProcedureTestRequests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.work = self.root / 'evolve'
        folder = self.work / 'investigations/p1'
        folder.mkdir(parents=True)
        (folder / 'procedure.py').write_text('print(1)\n')
        (folder / 'helper.py').write_text('X = 1\n')
        (folder / 'big.gpx').write_text('not part of the snapshot\n')
        broker.save(self.root / 'control/settings.json', {
            'service_prefix': 'pxrd-test', 'procedure_test_workers': 2,
            'procedure_test_timeout_seconds': 600, 'procedure_test_max_attempts': 3})
        self.state = {'jobs': {}, 'groups': {'t': {'jobs': ['t1']}}, 'requests': {},
                      'batches': {'b001': {'kind': 'learning', 'cases': ['c1', 'c2']},
                                  'b002': {'kind': 'transfer', 'cases': ['c3'], 'transfer_group': 't'}}}
        self.launched = []
        for name, value in [('ROOT', self.root), ('WORK', self.work), ('launch', self.launch),
                            ('alive', lambda unit: unit.get('alive', True))]:
            p = patch.object(pt, name, value)
            p.start(); self.addCleanup(p.stop)

    def launch(self, rid, folder):
        self.launched.append(rid)
        return {'kind': 'process', 'pid': 1, 'alive': True}

    def attempt(self, jid, case='c1', batch='b001', status='complete', verified=True, gpx=True, at=0):
        self.state['jobs'][jid] = {'id': jid, 'case_id': case, 'batch': batch, 'status': status, 'dispatched_at': at,
                                   'collected': status == 'complete', 'policy': 'P0', 'purpose': 'baseline', 'group': 'g'}
        folder = self.root / 'evidence/attempts' / jid
        if gpx:
            (folder / 'workspace').mkdir(parents=True)
            (folder / 'workspace/final.gpx').write_bytes(b'gpx')
        broker.save(folder / 'score.json', {'profile_status': 'verified' if verified else 'missing_final_project',
                                            'D_poisson': 0.5 if verified else None,
                                            'independent_atomic_rwp': 3.0, 'score_100': 70.0})

    def request(self, **extra):
        return {'id': 'ptest-01', 'script': 'investigations/p1/procedure.py', **extra}

    def test_default_selects_verified_attempts_and_counts_skips(self):
        self.attempt('a1'); self.attempt('a2', case='c2')
        self.attempt('a3', verified=False)
        self.attempt('a4', status='running', gpx=False)
        self.attempt('t1', case='c3', batch='b002', status='running', gpx=False)
        self.attempt('a5', case='c3', batch='b002')  # its prospective comparison is unfinished
        result = pt.start(self.state, self.request())
        self.assertEqual(result['state'], 'running')
        folder = self.root / 'evidence/procedure-tests/ptest-01'
        record = json.loads((folder / 'request.json').read_text())
        self.assertEqual([r['attempt'] for r in record['attempts']], ['a1', 'a2'])
        self.assertEqual(record['skipped'], {'its project replay was not verified': 1, 'not complete and collected': 2,
                                             'its batch has an unfinished prospective comparison': 1})
        self.assertEqual(sorted(p.name for p in (folder / 'procedure').iterdir()), ['helper.py', 'procedure.py'])
        self.assertEqual(record['timeout_seconds'], 600)
        self.assertEqual(self.launched, ['ptest-01'])
        self.assertEqual(self.state['procedure_tests']['ptest-01']['state'], 'running')

    def test_explicit_ineligible_attempt_is_refused(self):
        self.attempt('a1'); self.attempt('a3', verified=False)
        with self.assertRaisesRegex(ValueError, 'a3: its project replay was not verified'):
            pt.start(self.state, self.request(attempts=['a1', 'a3']))
        self.assertEqual(self.launched, [])

    def test_case_filter_and_attempt_cap(self):
        for i in range(4):
            self.attempt(f'a{i}', at=100 + i)
        self.attempt('b1', case='c2')
        with self.assertRaisesRegex(ValueError, 'exceed the cap of 3'):
            pt.start(self.state, self.request(attempts=['a0', 'a1', 'a2', 'a3']))
        with self.assertRaisesRegex(ValueError, 'not both'):
            pt.start(self.state, self.request(cases=['c1'], attempts=['a1']))
        result = pt.start(self.state, self.request(cases=['c1']))
        record = json.loads((self.root / 'evidence/procedure-tests/ptest-01/request.json').read_text())
        self.assertEqual(sorted(r['attempt'] for r in record['attempts']), ['a1', 'a2', 'a3'])
        self.assertEqual(result['skipped'], {'older than the newest 3': 1})

    def test_cancel_stops_a_running_test(self):
        self.attempt('a1')
        self.launch = lambda rid, folder: {'kind': 'process', 'pid': 999999999}
        with patch.object(pt, 'launch', self.launch):
            pt.start(self.state, self.request())
        result = pt.cancel(self.state, {'test': 'ptest-01'})
        self.assertEqual(result['state'], 'cancelled')
        self.assertEqual(self.state['procedure_tests']['ptest-01']['state'], 'cancelled')
        response = json.loads((self.root / 'evidence/responses/ptest-01.json').read_text())
        self.assertEqual(response['status'], 'cancelled')
        with self.assertRaisesRegex(ValueError, 'No running procedure test'):
            pt.cancel(self.state, {'test': 'ptest-01'})

    def test_one_test_at_a_time(self):
        self.attempt('a1')
        pt.start(self.state, self.request())
        with self.assertRaisesRegex(ValueError, 'still running'):
            pt.start(self.state, {'id': 'ptest-02', 'script': 'investigations/p1/procedure.py'})

    def test_script_must_be_python_inside_evolve(self):
        self.attempt('a1')
        for script in ['../control/settings.json', 'investigations/p1/big.gpx', 'investigations/p1/missing.py']:
            with self.assertRaises(ValueError):
                pt.start(self.state, {'id': 'ptest-03', 'script': script})

    def test_timeout_override_is_bounded(self):
        self.attempt('a1')
        result = pt.start(self.state, self.request(timeout_minutes=100))
        self.assertEqual(result['timeout_seconds'], 1200)

    def test_check_closes_finished_tests_and_reports_a_stopped_runner(self):
        done = self.root / 'evidence/procedure-tests/done'
        broker.save(done / 'results.json', {'state': 'complete'})
        self.state['procedure_tests'] = {
            'done': {'state': 'running', 'path': str(done), 'unit': {'kind': 'process', 'pid': 1, 'alive': False}},
            'dead': {'state': 'running', 'path': str(self.root / 'evidence/procedure-tests/dead'),
                     'unit': {'kind': 'process', 'pid': 1, 'alive': False}},
            'busy': {'state': 'running', 'path': str(self.root / 'evidence/procedure-tests/busy'),
                     'unit': {'kind': 'process', 'pid': 1, 'alive': True}}}
        pt.check(self.state)
        tests = self.state['procedure_tests']
        self.assertEqual((tests['done']['state'], tests['dead']['state'], tests['busy']['state']), ('complete', 'error', 'running'))
        response = json.loads((self.root / 'evidence/responses/dead.json').read_text())
        self.assertEqual(response['status'], 'error')

    def test_broker_acknowledges_a_running_test(self):
        self.attempt('a1')
        (self.work / 'requests').mkdir()
        (self.work / 'requests/ptest-01.json').write_text(json.dumps({'command': 'procedure-test', **self.request()}))
        for name, value in [('ROOT', self.root), ('WORK', self.work), ('frozen_code_ok', lambda: None),
                            ('persist', lambda state: None)]:
            p = patch.object(broker, name, value)
            p.start(); self.addCleanup(p.stop)
        broker.requests(self.state)
        response = json.loads((self.root / 'evidence/responses/ptest-01.json').read_text())
        self.assertEqual(response['status'], 'running')
        self.assertEqual(self.state['requests']['ptest-01']['status'], 'accepted')

    def test_lab_wait_follows_a_running_test(self):
        spec = importlib.util.spec_from_file_location('lab', Path(__file__).resolve().parents[2] / 'evolve/lab.py')
        lab = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lab)
        evidence = self.root / 'evidence'
        broker.save(evidence / 'status.json', {'jobs': [], 'groups': {}})
        with patch.object(lab, 'E', evidence):
            broker.save(evidence / 'responses/ptest-01.json', {'id': 'ptest-01', 'status': 'running'})
            self.assertFalse(lab.lookup_progress('ptest-01')[1])
            broker.save(evidence / 'responses/ptest-01.json', {'id': 'ptest-01', 'status': 'complete'})
            self.assertTrue(lab.lookup_progress('ptest-01')[1])

    def test_runner_summary(self):
        row = lambda case, before, after, screen='pass': {
            'case_id': case, 'status': 'scored', 'before': {'D_poisson': before}, 'delta_D': after - before,
            'after': {'D_poisson': after, 'phases': [{'physical_screen': screen}]}}
        rows = [row('c1', 1.0, 0.1), row('c1', 0.5, 0.6, 'fail'), row('c2', 0.1047, 0.1047013),
                {'case_id': 'c2', 'status': 'procedure_failed', 'before': {'D_poisson': 1.0}}]
        s = procedure_runner.summarize(rows)
        self.assertEqual((s['attempts'], s['scored'], s['failed'], s['improved'], s['worse'], s['unchanged'], s['physical_flags_after']),
                         (4, 3, 1, 1, 1, 1, 1))
        self.assertEqual(s['by_case']['c1']['median_D_after'], 0.35)


if __name__ == '__main__':
    unittest.main()
