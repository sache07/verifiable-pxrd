"""Operator setup, not exposed to the research agent. Never launches a model.

python install.py              freeze P0, the environment manifest and infrastructure hashes; copy to EC2
python install.py --no-deploy  the same, without copying (local checks and tests)
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
from common import CORE, require_scoring_alignment
from tree_digest import tree_digest

R = Path(__file__).resolve().parents[1]
W = R / 'evolve'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare():
    require_scoring_alignment()
    sys.path.insert(0, str(R / 'runtime'))
    from labspec import protocol
    protocol(W / 'LAB.md')  # the lab settings must parse before anything is frozen
    # P0.md is the baseline source; package freezing inherits its deployed copy.
    (R / 'policies/P0').mkdir(parents=True, exist_ok=True)
    (R / 'policies/P0/prompt.md').write_bytes((W / 'P0.md').read_bytes())
    freeze = json.loads((R / 'scorer/config_freeze.json').read_text())
    if freeze.get('status') != 'frozen_for_synthetic_evaluation':
        raise ValueError('Finish scientific validation and freeze this version before deployment')
    scorer_files = [R / 'scorer/config.json', *sorted((R / 'scorer/src').glob('*.py')), *sorted((R / 'scorer/runtime').glob('*.py'))]
    if {str(p.relative_to(R / 'scorer')): sha(p) for p in scorer_files} != freeze['code_hashes']:
        raise ValueError('Validate and freeze changed scoring code before deployment')
    manifest = json.loads((W / 'environment.json').read_text())
    manifest['canaries_exist_outside'] = {name: Path(path).is_file() for name, path in manifest['blocked'].items()}
    manifest['immutable'] = {path: sha(path) for path in manifest['immutable']}
    manifest['status'] = 'prepared_not_deployed'
    (W / 'environment.json').write_text(json.dumps(manifest, indent=2) + '\n')
    files = [*R.glob('control/*.py'), *R.glob('runtime/*.py'), R / 'runtime/generator_defaults.json',
             *R.glob('control/harness/src/**/*.py'), R / 'control/harness/experiments/agent-adaptation/conditions/pxrd-codex.toml',
             R / 'control/settings.json', R / 'control/MONITOR.md', R / 'control/monitor_schema.json',
             W / 'lab.py', W / 'LAB.md', W / 'P0.md', R / 'policies/P0/prompt.md',
             *([R / 'policies/P0/base_layer.json'] if (R / 'policies/P0/base_layer.json').exists() else [])]
    (R / 'control/infrastructure_freeze.json').write_text(
        json.dumps({'files': {str(p.relative_to(R)): sha(p) for p in sorted(set(files))}}, indent=2) + '\n')


def deploy():
    host = json.loads((R / 'control/settings.json').read_text())['remote_host']
    subprocess.run(['rsync', '-a', '--exclude=__pycache__', '--exclude=.git', '--exclude=.cache', '--exclude=.tmp',
                    '--exclude=probe_home', '--exclude=auth', '--exclude=attempts', '--exclude=resources',
                    '--exclude=state.json', '--exclude=evidence', '--exclude=scores', '--exclude=cache', '--exclude=jobs',
                    '--exclude=job_status', '--exclude=tests', '--exclude=/control/validation/', '--exclude=/control/monitor/',
                    '--exclude=/control/evaluator.lock', '--exclude=staging', '--exclude=drafts', '--exclude=packages',
                    '--exclude=investigations', '--exclude=requests', '--', str(R) + '/', host + ':' + str(R) + '/'], check=True)
    if (R / 'policies/P0/helpers').is_dir():
        # The baseline folder may hold subfolders named like the excluded ones; copy it whole and check the digest there.
        subprocess.run(['rsync', '-a', '--exclude=__pycache__', '--', str(R / 'policies/P0') + '/', host + ':' + str(R / 'policies/P0') + '/'], check=True)
        expected = json.loads((R / 'policies/P0/base_layer.json').read_text())['tree_digest']
        remote = subprocess.run(['ssh', '-o', 'BatchMode=yes', host, CORE, str(R / 'control/tree_digest.py'), str(R / 'policies/P0/helpers')],
                                capture_output=True, text=True, check=True)
        if remote.stdout.strip() != expected or tree_digest(R / 'policies/P0/helpers') != expected:
            raise ValueError('Baseline folder digest mismatch after deployment: ' + remote.stdout.strip() + ' vs ' + expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--no-deploy', action='store_true')
    args = parser.parse_args()
    prepare()
    if not args.no_deploy:
        deploy()
        manifest = json.loads((W / 'environment.json').read_text())
        manifest['status'] = 'deployed_ready'
        (W / 'environment.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Frozen' + ('' if args.no_deploy else ' and deployed') + '; no model calls.')
