"""Bridge to a native continuous fit; no hidden profile realization is used."""
from pathlib import Path
import hashlib
import fcntl
import json
import os
import subprocess
import numpy as np
from common import ROOT, sha, load_structure
from specimen import effect_settings, continuous_bounds


def calculate_continuous_profiles(paths, weights, protocol, x, y, record, out, eligible):
    settings = effect_settings(protocol)
    bounds = continuous_bounds(protocol)
    common_sizes = protocol['generation']['domain_size_um'] if bounds['size_um'] is None else [None]
    request = {'cifs':[str(Path(p).resolve()) for p in paths],
               'cif_sha256':[sha(p) for p in paths], 'instrument':protocol['instrument'], 'grid':protocol['grid'],
               'bounds':bounds,
               'axes':settings['preferred_orientation']['axes'] if settings.get('preferred_orientation',{}).get('enabled') else [[0,0,1]],
               'observed_path':str((Path(record['case_path'])/'inputs/pattern.csv').resolve()),
               'search':protocol['verification']['continuous_profile_search']}
    request['observed_sha256'] = sha(request['observed_path'])
    worker = ROOT/'runtime/continuous_worker.py'
    request['worker_sha256'] = sha(worker)
    request['native_memory_sha256'] = sha(ROOT/'runtime/native_memory.py')
    request['instrument_writer_sha256'] = sha(ROOT/'runtime/gsas_worker_text.py')
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2', MKL_NUM_THREADS='2', PYTHONDONTWRITEBYTECODE='1')
    # Free quantitation is a separately optimized diagnostic, never a starting
    # state or selection criterion for the primary fixed-fraction prediction.
    results, evidence = {}, []
    conditions = [('fixed', list(map(float,weights)))]*int(eligible)
    # Free-fraction refinement is not part of the score and no longer runs in
    # its critical path. Missing fractions retain P=0; structure credit remains.
    for label, fractions in conditions:
        if label == 'free' and len(paths) == 1 and eligible:
            results['free'] = dict(results['fixed'], fractions=np.array([1.]))
            evidence.append({'condition':'free','mode':'identical one-phase model reused; no fraction degree of freedom'})
            continue
        for common_size in common_sizes:
            req = {**request, 'fractions':fractions}
            if common_size is not None:
                req['bounds'] = {**bounds, 'size_um':[common_size,common_size]}
            token = hashlib.sha256(json.dumps(req,sort_keys=True).encode()).hexdigest()
            folder = out/'continuous_cache'/token; folder.mkdir(parents=True,exist_ok=True)
            result = folder/'prediction.npz'
            # Concurrent attempts can share a reference diagnostic. A lock
            # protects the native GPX/request/result files from overlapping fits.
            with (folder/'compute.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                if not (result.is_file() and result.with_suffix('.json').is_file()):
                    (folder/'request.json').write_text(json.dumps(req,indent=2)+'\n')
                    python = '<HOME>/.local/share/characterizagent/backends/gsas2/venv/bin/python'
                    with (folder/'worker.log').open('w') as log:
                        proc = subprocess.run([python,str(worker),str(folder/'request.json'),str(result)],
                                              cwd=folder,env=env,stdout=log,stderr=subprocess.STDOUT)
                    if proc.returncode:
                        raise RuntimeError('Native continuous evaluator failed; see '+str(folder/'worker.log'))
            info = json.loads(result.with_suffix('.json').read_text())
            expected = np.array([float(load_structure(p).composition.weight) for p in paths])
            actual = np.array(info['unit_cell_masses_amu'])
            if actual.shape != expected.shape or np.any(abs(actual-expected)/expected > .001):
                raise ValueError('GSAS-II/pymatgen CIF interpretation mismatch in continuous evaluator')
            with np.load(result,allow_pickle=False) as data:
                if data['x'].shape != x.shape or not np.allclose(data['x'],x,atol=1e-7,rtol=0):
                    raise ValueError('Continuous prediction grid mismatch')
                info.update(calculated=data['calculated'].copy(),background=data['background'].copy())
            # Verify the returned weighted error directly on observed counts.
            loss = float(np.sum((y-info['calculated'])**2/np.maximum(y,1)))
            if not np.isclose(loss,info['chi_square'],rtol=1e-9,atol=1e-7):
                raise ValueError('Native continuous objective reconstruction failed')
            info['fractions'] = np.asarray(info['fractions'])
            if label not in results or info['chi_square'] < results[label]['chi_square']:
                results[label] = info
            evidence.append({'condition':label,'request_sha256':token,'prediction_sha256':sha(result),
                             'selection':'observed counts only; true instrument fixed, true specimen settings unavailable',
                             'path':str(folder), 'search':info['profile_search']})
    return results.get('fixed'), results.get('free'), evidence, None
