"""Operator validation: does the frozen D reward modelling the lab's specimen physics?

python reward_sensitivity.py CASES_DIR OUT_DIR [--variants=a,b,...] [CASE ...]

For each generated case, oracle_project.py builds one project per nuisance variant. Each project is
replayed by the frozen scorer's own sandboxed replay worker (scorer, no refinement), then D is
computed against the hidden noise-free mean with the scorer's prediction_errors. No model calls.
"""
from pathlib import Path
import json
import subprocess
import sys

import numpy as np

RUN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RUN / 'scorer/src'))
from replay import isolated_replay  # noqa: E402  (frozen scorer code, unchanged)
from predictive import prediction_errors  # noqa: E402

GSAS = '<HOME>/.local/share/characterizagent/backends/gsas2/venv/bin/python'
VARIANTS = ['oracle', 'no_displacement', 'no_roughness', 'instrument_only', 'no_specimen_model']


def rwp(y, p):
    w = 1 / np.maximum(y, 1.)
    return float(100 * np.sqrt(np.sum(w * (y - p) ** 2) / np.sum(w * y * y)))


def main():
    cases_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    args = sys.argv[3:]
    variants = VARIANTS
    if args and args[0].startswith('--variants='):
        variants = args.pop(0).split('=', 1)[1].split(',')
    names = args or sorted(p.name for p in cases_dir.iterdir() if (p / 'private/truth.json').exists())
    rows = []
    for name in names:
        case = cases_dir / name
        truth = json.loads((case / 'private/truth.json').read_text())
        with np.load(case / 'private/forward.npz') as z:
            mean = z['mean'].copy()
        x, y = np.loadtxt(case / 'inputs/pattern.csv', delimiter=',', skiprows=1).T
        for variant in variants:
            folder = out / name / variant
            p = subprocess.run([GSAS, str(Path(__file__).with_name('oracle_project.py')), str(case), str(folder), variant],
                               capture_output=True, text=True, timeout=900)
            if p.returncode:
                rows.append({'case': name, 'variant': variant, 'error': p.stderr[-800:]})
                continue
            built = json.loads(p.stdout.strip().splitlines()[-1])
            report = isolated_replay(folder / 'final.gpx', case / 'inputs/pattern.csv', folder / 'replay')
            with np.load(folder / 'replay/prediction.npz') as z:
                predicted = z['predicted'].copy()
            errors = prediction_errors(mean, predicted)
            rows.append({'case': name, 'variant': variant, 'D_poisson': errors['D_poisson'],
                         'replay_rwp': rwp(y, predicted), 'gsas_rwp': built['gsas_rwp'],
                         'refined_zero': built['refined_zero'], 'U': built['U'], 'X': built['X'],
                         'replay_status': report['status'], 'review_flags': report.get('profile_review_flags'),
                         'true_shift_um': truth.get('sample_realization', {}).get('shift_um'),
                         'true_zero_deg': truth['measurement']['true_zero_deg'],
                         'true_roughness': [truth.get('sample_realization', {}).get('surf_rough_A'),
                                            truth.get('sample_realization', {}).get('surf_rough_B')]})
            print(json.dumps(rows[-1]), flush=True)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'reward_sensitivity.json').write_text(json.dumps(rows, indent=1) + '\n')


if __name__ == '__main__':
    main()
