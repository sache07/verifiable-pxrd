"""Untrusted solver curve/calibration diagnostics, never headline-score inputs."""
from pathlib import Path
import csv
import re
import numpy as np
from common import sha


def inspect_export(work, case, submission):
    work, case = Path(work), Path(case)
    result = {'used_for_score': False, 'status': 'not_supplied',
              'scope': 'Solver-provided curve, not an independent atomic reconstruction.',
              'declared_angular_corrections': []}
    # Record explicit units-bearing declarations without guessing a sign convention
    # or requiring an additional field in historical result.json submissions.
    nodes = [('', submission)]
    for key in ('calibration', 'fit', 'fit_statistics', 'fit_stats', 'measurement'):
        if isinstance(submission.get(key), dict):
            nodes.append((key + '.', submission[key]))
    for prefix, node in nodes:
        for key in ('zero_deg', 'zero_shift_deg', 'zero_offset_deg', 'angular_zero_deg'):
            value = node.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and np.isfinite(value):
                result['declared_angular_corrections'].append({'field': prefix + key, 'degrees': float(value)})
    path = work / 'fit.csv'
    if not path.is_file():
        return result
    if path.is_symlink() or path.stat().st_size > 25_000_000:
        return {**result, 'status': 'unreadable', 'reason': 'unsafe or excessive fit file'}
    try:
        with path.open() as f:
            first = f.readline().strip().lstrip('#').strip()
        normalize = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
        header = [normalize(s) for s in next(csv.reader([first]))]
        aliases = {'x': {'twotheta', '2theta', 'tt', 'tth', 'x'},
                   'obs': {'observed', 'iobs', 'yobs', 'obs', 'intensity'},
                   'calc': {'calculated', 'icalc', 'ycalc', 'calc', 'fitted'}}
        indices = {}
        for key, choices in aliases.items():
            hits = [i for i, name in enumerate(header) if name in choices]
            if len(hits) != 1:
                return {**result, 'status': 'unrecognized_format', 'reason': 'Need identifiable angle, observed and calculated columns'}
            indices[key] = hits[0]
        curve = np.loadtxt(path, delimiter=',', skiprows=1, ndmin=2)
        public = np.loadtxt(case / 'inputs/pattern.csv', delimiter=',', skiprows=1, ndmin=2)
        x, y = public.T
        if len(curve) != len(public) or curve.shape[1] <= max(indices.values()):
            raise ValueError('Curve does not cover the complete measured grid')
        xx, obs, calc = [curve[:, indices[k]] for k in ('x', 'obs', 'calc')]
        if not np.isfinite(curve).all() or np.any(calc < 0):
            raise ValueError('Nonfinite curve or negative predicted counts')
        if not np.allclose(xx, x, atol=1e-7, rtol=0) or not np.allclose(obs, y, atol=1e-5, rtol=0):
            raise ValueError('Curve differs from original observed scan/grid')
        weights = 1 / np.maximum(y, 1.)
        denominator = float(np.sum(weights * y * y))
        if denominator <= 0:
            raise ValueError('Zero observed-data Rwp denominator')
        result.update(status='reported_curve_checked',
                      observed_rwp_percent=float(100 * np.sqrt(np.sum(weights * (y-calc)**2) / denominator)),
                      fit_sha256=sha(path), bins=len(x))
    except (OSError, ValueError, IndexError, UnicodeError, csv.Error) as exc:
        result.update(status='invalid_curve', reason=str(exc))
    return result
