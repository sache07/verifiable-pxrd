"""Small deterministic bridge from manifests to GSAS-II and comparable fits."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import tempfile

import numpy as np
from scipy.optimize import nnls, minimize_scalar

GSAS_PYTHON=Path('<HOME>/.local/share/characterizagent/backends/gsas2/venv/bin/python')
RUNTIME=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.partial')
    temp.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n')
    temp.replace(path)

def components(cifs,protocol,size_um,cache,combined=None,instrument_override=None,phase_profiles=None,profile_variants=None,sample_parameters=None):
    cache=Path(cache).resolve();cache.mkdir(parents=True,exist_ok=True)
    instrument={**protocol['instrument'],**(instrument_override or {})}
    content={'cif_hashes':[sha(c) for c in cifs],'instrument':instrument,'grid':protocol['grid'],
             'domain_size_um':float(size_um),'worker_sha256':sha(RUNTIME/'gsas_worker.py'),
             'instrument_writer_sha256':sha(RUNTIME/'gsas_worker_text.py'),
             'combined_fractions':None if combined is None else list(map(float,combined))}
    if phase_profiles is not None:
        if len(phase_profiles)!=len(cifs):raise ValueError('One specimen profile required per phase')
        content['phase_profiles']=phase_profiles
    if profile_variants is not None:
        if phase_profiles is not None or combined is not None or len(profile_variants)!=len(cifs):
            raise ValueError('Invalid profile-bank request')
        content['profile_variants']=profile_variants
    if sample_parameters is not None:
        # Omitted when absent, so cache keys of runs without whole-specimen effects are unchanged.
        content['sample_parameters']={k:float(v) for k,v in sample_parameters.items()}
    token=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    target=cache/token
    result=target/'profiles.npz'
    if not result.exists():
        # Atomic directory publication makes caches reusable across interrupted runs.
        with tempfile.TemporaryDirectory(prefix='forward-',dir=cache) as temp:
            work=Path(temp)
            request={**content,'cifs':[str(Path(c).resolve()) for c in cifs]}
            save_json(work/'request.json',request)
            env=os.environ.copy()
            for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
                env[name]='2'
            env['PYTHONDONTWRITEBYTECODE']='1'
            proc=subprocess.run([str(GSAS_PYTHON),str(RUNTIME/'gsas_worker.py'),str(work/'request.json'),str(work/'profiles.npz')],
                                cwd=work,env=env,capture_output=True,text=True,timeout=120)
            (work/'gsas.log').write_text(proc.stdout+'\n'+proc.stderr)
            if proc.returncode:
                failure=cache/f'failed-{token}'
                if not failure.exists():
                    import shutil
                    shutil.copytree(work,failure)
                raise RuntimeError('GSAS forward calculation failed; see '+str(failure/'gsas.log')+'\n'+proc.stderr[-1800:])
            target.mkdir(exist_ok=True)
            import shutil
            for p in work.iterdir():
                if p.is_file():shutil.copy2(p,target/p.name)
    with np.load(result) as d:
        x,profiles=d['x'].copy(),d['profiles'].copy()
    info=json.loads(result.with_suffix('.json').read_text())
    # A CIF can parse successfully but be expanded in a different origin/setting
    # by GSAS-II. Never silently quantify a different occupied atom model.
    from pymatgen.core import Structure
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        expected=np.array([float(Structure.from_file(c,primitive=False).composition.weight) for c in cifs])
    actual=np.asarray(info['unit_cell_masses_amu'])
    if actual.shape!=expected.shape or np.any(np.abs(actual-expected)/expected>.001):
        raise ValueError('GSAS-II/pymatgen CIF interpretation mismatch: unit-cell masses differ. Review space-group setting before generating or scoring; this is not a solver failure.')
    return x,profiles,info

def bernstein(x):
    t=(np.asarray(x)-x[0])/(x[-1]-x[0])
    return np.column_stack(((1-t)**2,2*t*(1-t),t**2))

def fit_profiles(x,y,profiles,weights=None,fixed_fractions=None,allow_shift=True,background_basis=None):
    """Nonnegative linear intensity/background fit, plus bounded common zero."""
    q=1/np.maximum(y,1.) if weights is None else np.asarray(weights)
    rootq=np.sqrt(q)
    background=bernstein(x) if background_basis is None else np.asarray(background_basis,float)
    if (background.ndim!=2 or background.shape[0]!=len(x) or background.shape[1]<1
            or not np.all(np.isfinite(background)) or np.any(background<0)):
        raise ValueError('Invalid nonnegative generation-audit background basis')
    if fixed_fractions is not None:
        fractions=np.asarray(fixed_fractions,float)
        profiles=np.asarray([fractions @ profiles])
    norm=float(np.max(profiles))
    if norm<=0:raise ValueError('zero diffraction intensity')
    basis=profiles.T/norm
    def solve(shift):
        shifted=np.column_stack([np.interp(x-shift,x,basis[:,i],left=0,right=0) for i in range(basis.shape[1])])
        A=np.column_stack((shifted,background))
        coef,_=nnls(A*rootq[:,None],y*rootq,maxiter=1000)
        calculated=A@coef
        loss=float(np.sum(q*(y-calculated)**2))
        return loss,coef,calculated,A
    best=(0.,solve(0.))
    if allow_shift:
        # Include zero explicitly: bounded minimization alone can miss a narrow minimum.
        trial=minimize_scalar(lambda s:solve(float(s))[0],bounds=(-.05,.05),method='bounded',options={'xatol':1e-6,'maxiter':50})
        value=solve(float(trial.x))
        if value[0]<best[1][0]:best=(float(trial.x),value)
    shift,(loss,coef,calculated,A)=best
    amplitude=coef[:basis.shape[1]]
    fractions=amplitude/amplitude.sum() if amplitude.sum()>0 else np.zeros_like(amplitude)
    denominator=float(np.sum(q*y*y))
    return {'chi_square':loss,'rwp_percent':100*np.sqrt(loss/denominator),'fractions':fractions,
            'calculated':calculated,'background':background@coef[basis.shape[1]:],
            'zero_shift_deg':shift,'coefficients':coef,'weighted_design':A*rootq[:,None]}

def compare_structures(reference,candidate):
    from pymatgen.analysis.structure_matcher import StructureMatcher,ElementComparator
    matcher=StructureMatcher(ltol=.2,stol=.3,angle_tol=5,primitive_cell=True,scale=False,attempt_supercell=True,allow_subset=False,comparator=ElementComparator())
    return bool(matcher.fit(reference,candidate,symmetric=True))
