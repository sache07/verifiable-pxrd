"""Offline controller queue tests: no SSH, services, or model requests."""
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import broker


class CapacityQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        broker.save(self.root / 'control/settings.json', {
            'capacity_retry_seconds': 60, 'max_concurrent_solvers': 10, 'development_solves_per_cycle': 30, 'solver_timeout_seconds': 14400,
            'model': 'gpt-5.6-sol', 'solver_effort': 'max', 'tmux_socket': 'test', 'tmux_session': 'test'})
        self.state = {'paused': False, 'jobs': {}, 'groups': {'g': {'id': 'g', 'jobs': []}}}
        self.info = {'usage_pause': None, 'jobs': {}}
        self.now = 1000
        self.launched = []
        self.mode = 'fresh'
        self.recovery_error = False
        for name, value in [('ROOT', self.root), ('remote', self.remote),
                            ('collect', lambda job: None), ('sync_up', lambda path: None)]:
            p = patch.object(broker, name, value)
            p.start(); self.addCleanup(p.stop)
        p = patch.object(broker.time, 'time', lambda: self.now)
        p.start(); self.addCleanup(p.stop)

    def remote(self, *args, **kwargs):
        if args[0] == 'tmux':
            return SimpleNamespace(stdout='')
        action = args[2]
        if action == 'rescore':
            return SimpleNamespace(stdout=json.dumps({'id': args[3], 'status': 'complete'}))
        if action == 'status':
            return SimpleNamespace(stdout=json.dumps(self.info))
        if action == 'recovery-mode':
            if self.recovery_error:
                raise RuntimeError('old scope still active')
            return SimpleNamespace(stdout=json.dumps({'mode': self.mode}))
        self.assertEqual(action, 'launch')
        jid = args[3]
        self.launched.append(jid)
        self.info['jobs'][jid] = {'status': 'running', 'work_started': False}
        return SimpleNamespace(stdout='{"status":"dispatched"}')

    def job(self, jid, status='interrupted', capacity=True, failure=None):
        payload = {'id': jid, 'group': 'g', 'replicate': len(self.state['jobs']) + 1,
                   'policy': 'P0', 'case_id': 'c1'}
        broker.save(self.root / 'control/jobs' / (jid + '.json'), payload)
        self.state['jobs'][jid] = {**payload, 'status': status}
        self.state['groups']['g']['jobs'].append(jid)
        if status != 'queued':
            self.info['jobs'][jid] = {'status': status, 'detail': {
                'capacity_limited': capacity, 'infrastructure_failure': failure}}

    def confirm(self, jid):
        self.info['jobs'][jid]['work_started'] = True

    def reject(self, jid):
        self.info['jobs'][jid] = {'status': 'interrupted', 'detail': {'capacity_limited': True, 'infrastructure_failure': None}}

    def poll(self):
        broker.poll_and_dispatch(self.state)

    def test_one_launch_at_a_time_up_to_the_limit(self):
        for i in range(12):
            self.job('q' + str(i), 'queued')
        self.poll(); self.poll()
        self.assertEqual(self.launched, ['q0'])
        for i in range(1, 10):
            self.confirm(self.launched[-1]); self.poll()
            self.assertEqual(self.launched[-1], 'q' + str(i))
        self.confirm('q9'); self.poll()
        self.assertEqual(len(self.launched), 10)
        self.info['jobs']['q0'] = {'status': 'complete'}; self.poll()
        self.assertEqual(self.launched[-1], 'q10')

    def test_rejected_head_retried_every_minute_before_the_queue(self):
        self.job('a', 'queued'); self.job('b', 'queued')
        self.poll(); self.reject('a'); self.poll()
        self.assertEqual(self.state['jobs']['a']['status'], 'retry_wait')
        self.now = 1059; self.poll()
        self.assertEqual(self.launched, ['a'])
        self.now = 1060; self.poll()
        child = self.state['jobs']['a']['superseded_by']
        self.assertEqual(self.launched, ['a', child])
        self.assertEqual(self.state['jobs'][child]['replicate'], 1)
        self.assertEqual(self.state['groups']['g']['jobs'], [child, 'b'])
        self.state = broker.read(self.root / 'control/state.json')
        self.reject(child); self.poll()
        self.now = 1119; self.poll()
        self.assertEqual(len(self.launched), 2)
        self.now = 1120; self.poll()
        grandchild = self.state['jobs'][child]['superseded_by']
        self.assertEqual(self.launched[-1], grandchild)
        self.poll()
        self.assertEqual(self.launched[-1], grandchild)
        self.confirm(grandchild); self.poll()
        self.assertEqual(self.launched[-1], 'b')
        self.assertEqual(len(set(self.launched)), 4)

    def test_silent_launch_stops_blocking_after_15_minutes(self):
        self.job('a', 'queued'); self.job('b', 'queued')
        self.poll()
        self.now += 899; self.poll()
        self.assertEqual(self.launched, ['a'])
        self.now += 1; self.poll()
        self.assertEqual(self.launched, ['a', 'b'])

    def test_pause_quota_and_other_failures_are_not_retried(self):
        self.job('capacity'); self.poll()
        self.state['paused'] = True
        self.now += 60; self.poll()
        self.assertEqual(self.launched, [])
        self.state['paused'] = False
        self.info['usage_pause'] = {'reason': 'usage limit'}
        self.poll()
        self.assertTrue(self.state['paused'])
        self.assertEqual(self.launched, [])
        for detail in [{'capacity_limited': False},
                       {'capacity_limited': True, 'infrastructure_failure': 'immutable_inputs_modified'}]:
            self.state['paused'] = False; self.info['usage_pause'] = None
            self.info['jobs']['capacity'] = {'status': 'interrupted', 'detail': detail}
            self.poll()
            self.assertEqual(self.launched, [])

    def test_resume_and_pending_recovery_survive_restart(self):
        self.job('parent'); self.poll(); self.now += 60
        self.mode = 'resume'
        jid = broker.next_launch(self.state)['id']
        payload = broker.read(self.root / 'control/jobs' / (jid + '.json'))
        self.assertTrue(payload['infrastructure_recovery'])
        self.assertEqual(payload['continuation_of'], 'parent')
        self.state = broker.read(self.root / 'control/state.json')
        self.poll(); self.poll()
        self.assertEqual(self.launched, [jid])
        self.assertEqual(self.state['groups']['g']['jobs'], [jid])

    def test_recovery_safety_error_does_not_fresh_restart(self):
        self.job('parent'); self.poll(); self.now += 60
        self.recovery_error = True
        self.poll(); self.poll()
        self.assertEqual(self.launched, [])
        self.assertIn('capacity_retry_blocked', self.state['jobs']['parent'])

    def test_disabled_retry_still_admits_one_at_a_time(self):
        settings = broker.read(self.root / 'control/settings.json')
        settings['capacity_retry_seconds'] = 0
        broker.save(self.root / 'control/settings.json', settings)
        self.job('failed')
        for i in range(3):
            self.job('new' + str(i), 'queued')
        self.poll(); self.confirm('new0'); self.poll()
        self.assertEqual(self.launched, ['new0', 'new1'])
        self.assertEqual(self.state['jobs']['failed']['status'], 'interrupted')

    def test_schedule_is_breadth_first_with_conditions_interleaved(self):
        cases = ['c1', 'c2', 'c3']
        for policy in ['P0', 'P1']:
            (self.root / 'policies' / policy).mkdir(parents=True)
            (self.root / 'policies' / policy / 'prompt.md').write_text(policy)
        state = {'batches': {'b': {'kind': 'development', 'cases': cases}}, 'packages': {'P0': {}, 'P1': {}},
                 'groups': {}, 'jobs': {}}
        request = {'id': 'run1', 'batch': 'b', 'policies': ['P0', 'P1'], 'repeats': 3}
        _, jobs = broker.make_jobs(state, request)
        self.assertEqual([j['replicate'] for j in jobs], [1] * 6 + [2] * 6 + [3] * 6)
        for r in range(3):
            self.assertEqual(sorted((j['case_id'], j['policy']) for j in jobs[6 * r:6 * r + 6]),
                             sorted((c, p) for c in cases for p in ['P0', 'P1']))
        self.assertEqual([j['id'] for j in broker.make_jobs(state, request)[1]], [j['id'] for j in jobs])

    def test_failed_collection_does_not_block_other_jobs(self):
        self.job('done1', 'complete'); self.job('done2', 'complete'); self.job('next', 'queued')
        def collect(job):
            if job['id'] == 'done1':
                raise RuntimeError('rsync failed')
        with patch.object(broker, 'collect', collect):
            self.poll()
        self.assertIn('collection_error', self.state['jobs']['done1'])
        self.assertFalse(self.state['jobs']['done1'].get('collected'))
        self.assertTrue(self.state['jobs']['done2']['collected'])
        self.assertEqual(self.launched, ['next'])
        self.poll()
        self.assertTrue(self.state['jobs']['done1']['collected'])
        self.assertNotIn('collection_error', self.state['jobs']['done1'])

    def test_rescore_only_after_an_evaluator_error(self):
        self.job('bad', 'evaluator_error')
        self.state['jobs']['bad']['collected'] = True
        result = broker.handle(self.state, {'command': 'rescore', 'id': 'r1', 'attempt': 'bad'})
        self.assertEqual(result['status'], 'complete')
        self.assertEqual((self.state['jobs']['bad']['status'], self.state['jobs']['bad']['collected']), ('complete', False))
        with self.assertRaises(ValueError):
            broker.handle(self.state, {'command': 'rescore', 'id': 'r2', 'attempt': 'bad'})

    def test_continue_command_is_gone(self):
        with self.assertRaisesRegex(ValueError, 'Unknown command'):
            broker.handle(self.state, {'command': 'continue', 'id': 'c1', 'parent': 'x'})


if __name__ == '__main__':
    unittest.main()
