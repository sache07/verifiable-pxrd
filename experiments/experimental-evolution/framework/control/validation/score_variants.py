"""Operator validation: full frozen 6.0.0 scoring of the reward-sensitivity projects.

python score_variants.py SCORER_COPY CASES_DIR VARIANTS_DIR

SCORER_COPY is a disposable copy of scorer (its truth_provenance.json and scores/ are written).
Each variant project from reward_sensitivity.py becomes a complete submission: the CIFs and weight
fractions the replay worker exported from final.gpx, result.json, fit.csv and report.md.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys

import numpy as np

scorer, cases_dir, variants_dir = map(lambda p: Path(p).resolve(), sys.argv[1:4])
sys.path.insert(0, str(scorer / 'src'))
from score import score_attempt  # noqa: E402  (frozen scorer code)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def register(case):
    path = scorer / 'truth_provenance.json'
    data = json.loads(path.read_text()) if path.exists() else {}
    files = [*(case / 'inputs').iterdir(), case / 'private/truth.json', case / 'private/forward.npz',
             *(case / 'private/references').glob('*.cif')]
    data[str(case.resolve())] = {str(p.resolve()): sha(p) for p in files}
    path.write_text(json.dumps(data, indent=2) + '\n')


rows = []
for case_dir in sorted(p for p in variants_dir.iterdir() if p.is_dir()):
    case = cases_dir / case_dir.name
    register(case)
    for folder in sorted(p for p in case_dir.iterdir() if (p / 'replay/replay.json').exists()):
        report = json.loads((folder / 'replay/replay.json').read_text())
        work = folder / 'submission'
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir()
        shutil.copy2(folder / 'final.gpx', work / 'final.gpx')
        phases = []
        for p in report['phases']:
            shutil.copy2(folder / 'replay' / p['cif'], work / p['cif'])
            phases.append({'name': p['name'], 'cif_path': p['cif'], 'weight_fraction': p['weight_fraction']})
        with np.load(folder / 'replay/prediction.npz') as z:
            x, y, c = z['x'], z['observed'], z['predicted']
        np.savetxt(work / 'fit.csv', np.column_stack([x, y, c, y - c]), delimiter=',',
                   header='two_theta,observed,calculated,difference', comments='')
        (work / 'result.json').write_text(json.dumps({'phases': phases}, indent=1) + '\n')
        (work / 'report.md').write_text('Operator validation project: ' + folder.name + '\n')
        rid = case.name + '-' + folder.name
        result = score_attempt({'id': rid, 'case_path': str(case), 'workspace': str(work), 'condition': folder.name})
        comp = result.get('structural_components') or {}
        rows.append({'case': case.name, 'variant': folder.name, 'score_100': result.get('score_100'),
                     'score_status': result.get('score_status'), 'D_poisson': result.get('D_poisson'),
                     'independent_atomic_rwp': result.get('independent_atomic_rwp'),
                     'components': {k: comp.get(k) for k in comp if k not in {'pairs', 'phase_credits'}},
                     'adjudication_reasons': result.get('adjudication_reasons'), 'error': result.get('error')})
        print(json.dumps(rows[-1])[:900], flush=True)
(variants_dir / 'full_scores.json').write_text(json.dumps(rows, indent=1) + '\n')
