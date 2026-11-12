"""Hidden-mean evaluation of an already frozen, observed-data prediction."""
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.special import xlogy
from common import ROOT, read_json, sha


def prediction_errors(expected, predicted):
    mu, pred = np.asarray(expected, float), np.asarray(predicted, float)
    if mu.ndim != 1 or mu.shape != pred.shape or not len(mu):
        raise ValueError('Expected and predicted counts must be equal-length vectors')
    if not np.all(np.isfinite(mu)) or not np.all(np.isfinite(pred)) or np.any(mu < 0) or np.any(pred < 0):
        raise ValueError('Counts must be finite and nonnegative')
    impossible = bool(np.any((mu > 0) & (pred == 0)))
    # log1p avoids cancellation for predictions near the hidden mean.
    pos = (mu > 0) & (pred > 0)
    terms = pred.copy()
    z = (pred[pos]-mu[pos])/mu[pos]
    near=z>-.99
    vals=np.empty_like(z)
    vals[near]=mu[pos][near]*(z[near]-np.log1p(z[near]))
    vals[~near]=pred[pos][~near]-mu[pos][~near]+mu[pos][~near]*(np.log(mu[pos][~near])-np.log(pred[pos][~near]))
    terms[pos] = vals
    poisson = float('inf') if impossible else max(0., 2*float(np.mean(terms)))
    quad = float(np.mean((pred-mu)**2/np.maximum(mu, 1.)))
    return dict(D_poisson=None if impossible else poisson, D_poisson_infinite=impossible,
                D_quadratic=quad, P=0. if impossible else 1/(1+poisson), P_quadratic=1/(1+quad),
                n_bins=len(mu), noise_model='independent Poisson counts on original fixed grid',
                scope='Expected excess loss; not a statistical equivalence test or probability of correctness')


@lru_cache(maxsize=128)
def load_expected(case_path):
    case = Path(case_path).resolve()
    files = read_json(ROOT/'truth_provenance.json').get(str(case))
    if files is None:
        raise ValueError('Case has no registered synthetic truth provenance')
    for path, expected_hash in files.items():
        if sha(path) != expected_hash:
            raise ValueError('Synthetic source changed: '+path)
    truth=read_json(case/'private/truth.json')
    for name,digest in truth['input_hashes'].items():
        if sha(case/'inputs'/name)!=digest:
            raise ValueError('Input differs from original generation provenance: '+name)
    for phase in truth['phases']:
        if sha(case/'private/references'/(phase['id']+'.cif'))!=phase['model_sha256']:
            raise ValueError('Reference differs from original generation provenance: '+phase['id'])
    with np.load(case/'private/forward.npz', allow_pickle=False) as z:
        x, mu = z['x'].copy(), z['mean'].copy()
        if not np.allclose(mu,z['signal']+z['background'],atol=1e-8,rtol=1e-12):
            raise ValueError('Expected counts do not equal the saved signal plus background')
        signal=np.asarray(truth['true_fractions'])@z['profiles']*z['normalization']
        if not np.allclose(z['signal'],signal,atol=1e-8,rtol=1e-12):
            raise ValueError('Saved signal does not reproduce the generating mixture')
    if x.ndim != 1 or x.shape != mu.shape or not np.all(np.diff(x) > 0):
        raise ValueError('Invalid hidden expected-pattern grid')
    if not np.all(np.isfinite(mu)) or np.any(mu < 0):
        raise ValueError('Invalid hidden expected counts')
    return x, mu, files[str(case/'private/forward.npz')]


def evaluate_frozen(case_path, x, observed, predicted):
    # Call only after project replay and submission consistency checks finish.
    grid, mu, fingerprint = load_expected(str(Path(case_path).resolve()))
    if np.shape(x) != grid.shape or not np.allclose(x, grid, atol=1e-9, rtol=0):
        raise ValueError('Observed and hidden grids differ; no interpolation is permitted')
    public = np.loadtxt(Path(case_path)/'inputs/pattern.csv', delimiter=',', skiprows=1)
    if not np.allclose(public[:,0], x, atol=1e-9, rtol=0) or not np.array_equal(public[:,1], observed):
        raise ValueError('Prediction is not associated with the registered observed scan')
    weights=1/np.maximum(observed,1.)
    reference_rwp=float(100*np.sqrt(np.sum(weights*(observed-mu)**2)/np.sum(weights*observed**2)))
    return {**prediction_errors(mu, predicted), 'expected_mean_sha256':fingerprint,
            'hidden_mean_used_for_fitting':False, 'prediction_selection':'verified submitted-project forward replay; no evaluator refinement',
            'reference_rwp':reference_rwp,'reference_rwp_definition':'unrefined generating mean against observed counts'}
