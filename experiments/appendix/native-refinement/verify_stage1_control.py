"""Verify a GPU stage-1-only control against its saved two-stage prefix."""
import argparse
import time
from pathlib import Path

import numpy as np
from pymatgen.core import Structure

from common import read_json, write_json


def verify(root):
    plan = read_json(root / 'plan.json')
    if len(plan['ids']) != 1:
        raise ValueError('Expected exactly one implementation-control candidate')
    candidate = root / 'candidates' / plan['ids'][0]
    if not (candidate / 'result.json').exists():
        return None
    old = Path(read_json(root / 'control.json')['original_result'])
    result, original = read_json(candidate / 'result.json'), read_json(old / 'result.json')
    checks = dict(completed=result['status'] == 'completed',
                  source_hash=result.get('code_sha256') == plan['source_hash'],
                  mode=result.get('structsnap_mode') == 'lattice-stage1',
                  single_stage=len(result.get('stages', [])) == 1,
                  same_input=result.get('input_sha256') == original.get('input_sha256'),
                  same_pattern=result.get('pattern_sha256') == original.get('pattern_sha256'))
    if all(checks.values()):
        before, after = Structure.from_file(old / 'stage-1.cif'), Structure.from_file(candidate / 'refined.cif')
        checks['species'] = before.species == after.species
        checks['lattice'] = bool(np.allclose(before.lattice.matrix, after.lattice.matrix, rtol=1e-6, atol=1e-7))
        checks['coordinates'] = bool(np.allclose(before.frac_coords, after.frac_coords, rtol=1e-6, atol=1e-7))
        checks['cosine'] = abs(original['stages'][0]['fresh_negative_cosine'] -
                               result['stages'][0]['fresh_negative_cosine']) < 1e-6
        x, y = np.load(old / 'stage-1-profile.npz'), np.load(candidate / 'stage-1-profile.npz')
        for key in ('two_theta', 'observed', 'calculated'):
            checks['profile_' + key] = bool(np.allclose(x[key], y[key], rtol=1e-6, atol=1e-7))
    report = dict(passed=all(checks.values()), checks=checks, source_hash=plan['source_hash'],
                  original=str(old), control=str(candidate), checked_unix=time.time(),
                  original_gpu=original.get('gpu'), control_gpu=result.get('gpu'))
    write_json(root / 'passed.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--wait', action='store_true')
    args = parser.parse_args()
    while True:
        report = verify(args.root)
        if report is not None:
            print(report, flush=True)
            raise SystemExit(0 if report['passed'] else 1)
        if not args.wait:
            raise SystemExit('Control has not returned yet')
        time.sleep(10)
