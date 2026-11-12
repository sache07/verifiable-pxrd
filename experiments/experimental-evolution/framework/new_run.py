"""Create a run folder from this framework and one lab's LAB.md. Operator-only; starts nothing.

python framework/new_run.py --lab labs/NAME/LAB.md --name NAME [--canary LABEL=PATH ...]

The run folder (runs/NAME) holds a copy of the framework, the lab's LAB.md as evolve/LAB.md, its own
settings, researcher permission profile and isolation canaries, and an empty experiment with P0 as
the incumbent. Every run made from the same framework shares PROMPT.md, TOOLS.md, P0.md, the
generator, scorer and controller; only LAB.md differs. Then, from the run folder:
python control/install.py   (freeze and copy to EC2), python control/start_controller.py.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys

FRAMEWORK = Path(__file__).resolve().parent
HOME = FRAMEWORK.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_digest(root):
    files = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    digest = hashlib.sha256()
    for p in files:
        digest.update(str(p.relative_to(root)).encode() + b'\0' + sha(p).encode() + b'\0')
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--lab', type=Path, required=True)
    parser.add_argument('--name', required=True, help='lowercase run name, e.g. divalent-tungstates')
    parser.add_argument('--canary', action='append', default=[], metavar='LABEL=PATH',
                        help='a file the researcher must not be able to read, such as an evaluation label')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9-]{1,40}', args.name):
        raise SystemExit('Run names are lowercase letters, digits and hyphens')
    sys.path.insert(0, str(FRAMEWORK / 'runtime'))
    from labspec import protocol
    protocol(args.lab)  # refuse a lab whose settings do not parse
    run = HOME / 'runs' / args.name
    if run.exists():
        raise SystemExit('Run exists: ' + str(run))
    shutil.copytree(FRAMEWORK, run, ignore=shutil.ignore_patterns('__pycache__', 'new_run.py'))
    evolve, control = run / 'evolve', run / 'control'
    shutil.copy2(args.lab, evolve / 'LAB.md')
    prefix, profile = 'pxrd-' + args.name, 'pxrd-' + args.name
    fill = lambda text: text.replace('{ROOT}', str(run)).replace('{PREFIX}', prefix).replace('{PROFILE}', profile)
    settings = json.loads(fill((control / 'settings.template.json').read_text()))
    (control / 'settings.json').write_text(json.dumps(settings, indent=2) + '\n')
    (control / 'settings.template.json').unlink()
    visible = {k: v for k, v in settings.items() if k not in ('remote_host', 'codex_cli')}
    (evolve / 'settings.json').write_text(json.dumps(visible, indent=2) + '\n')
    (evolve / '.codex').mkdir()
    (evolve / '.codex/config.toml').write_text(fill((evolve / 'codex_config.template.toml').read_text()))
    (evolve / 'codex_config.template.toml').unlink()
    (evolve / 'AGENTS.md').write_text(fill((evolve / 'AGENTS.md').read_text()))
    blocked = {'controller_blocked': str(control / 'private-canary.txt'),
               'credentials_blocked': str(Path.home() / '.codex/auth.json'),
               'operator_labs_blocked': str(Path(args.lab).resolve())}
    for item in args.canary:
        label, _, path = item.partition('=')
        blocked[label + '_blocked'] = str(Path(path).resolve())
    missing = [p for p in blocked.values() if not Path(p).is_file()]
    if missing:
        raise SystemExit('Canaries must be existing files outside the run: ' + ', '.join(missing))
    immutable = [evolve / n for n in ['AGENTS.md', 'PROMPT.md', 'LAB.md', 'TOOLS.md', 'P0.md', 'lab.py',
                                        'verify_environment.py', 'resources.json', 'settings.json', '.codex/config.toml']]
    immutable += [run / 'scorer/config.json', *sorted((run / 'scorer/src').glob('*.py')), *sorted((run / 'scorer/runtime').glob('*.py'))]
    (evolve / 'environment.json').write_text(json.dumps(
        {'status': 'workshop_not_deployed', 'blocked': blocked, 'immutable': {str(p): None for p in immutable},
         'canaries_exist_outside': {}}, indent=2) + '\n')
    for rel in ['attempts', 'batches', 'cases', 'resources', 'evidence/attempts', 'evidence/decisions', 'evidence/groups',
                'evidence/requests', 'evidence/responses', 'evidence/monitor', 'evidence/investigations', 'control/jobs',
                'control/job_status', 'control/staging', 'control/forward_cache', 'control/monitor', 'control/reservations']:
        (run / rel).mkdir(parents=True, exist_ok=True)
    for name in ['.agents', '.aws', '.cache', '.monitor', '.tmp', 'drafts', 'requests', 'investigations', 'packages']:
        (evolve / name).mkdir(exist_ok=True)
    subprocess.run(['git', 'init', '-q', str(evolve)], check=True)
    (run / 'policies/P0/prompt.md').write_bytes((evolve / 'P0.md').read_bytes())
    (run / 'scorer/truth_provenance.json').write_text('{}\n')
    state = {'schema_version': 1, 'paused': False, 'requests': {}, 'batches': {}, 'groups': {}, 'jobs': {},
             'packages': {'P0': {'path': str(run / 'policies/P0'), 'prompt_sha256': sha(run / 'policies/P0/prompt.md')}},
             'current_package': 'P0', 'pause_reason': None}
    (control / 'state.json').write_text(json.dumps(state, indent=2) + '\n')
    (evolve / 'STATE.md').write_text(
        '# Starting state\n\nNo cases, learned packages, investigations or solver attempts have been started. P0 is the incumbent. '
        'Run verify_environment.py directly in the app task, then follow PROMPT.md from the initial curation step.\n')
    record = {'run': args.name, 'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'framework_digest': tree_digest(FRAMEWORK), 'lab_source': str(Path(args.lab).resolve()),
              'lab_sha256': sha(evolve / 'LAB.md'), 'researcher_profile': profile, 'service_prefix': prefix}
    (run / 'RUN.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
