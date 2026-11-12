"""Read-only GSAS-II atomic forward replay. Run in the evaluator's filesystem sandbox.

No refinement, no hidden calibration, no source-project writes, and no cached
calculated intensities. Only numerical reflection lists are regenerated.
"""
from pathlib import Path
import copy
import hashlib
import json
import pickle
import sys
import traceback
import numpy as np
from scipy.interpolate import interp1d
from GSASII import GSASIIstrIO as IO, GSASIIstrMath as M
from GSASII import GSASIIscriptable as G, GSASIIpwd as PW


def plain(value):
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    if isinstance(value, np.ndarray): return plain(value.tolist())
    if isinstance(value, np.generic): return value.item()
    return value


class InvalidProject(ValueError):
    pass


class ProjectUnpickler(pickle.Unpickler):
    """GSAS stores data as pickle; permit data constructors, never arbitrary code."""
    allowed={('GSASII.GSASIIobj','G2VarObj'),('GSASIIobj','G2VarObj'),
             ('builtins','object'),('__builtin__','object'),('builtins','set'),('__builtin__','set'),
             ('builtins','frozenset'),('__builtin__','frozenset'),('builtins','complex'),('__builtin__','complex'),
             ('_codecs','encode'),('copyreg','_reconstructor'),('copy_reg','_reconstructor'),
             ('collections','OrderedDict'),('numpy','dtype'),('numpy','ndarray'),
             ('numpy.core.multiarray','_reconstruct'),('numpy.core.multiarray','scalar'),
             ('numpy._core.multiarray','_reconstruct'),('numpy._core.multiarray','scalar'),
             ('numpy.core.numeric','_frombuffer'),('numpy._core.numeric','_frombuffer'),
             ('numpy.ma.core','MaskedArray'),('numpy.ma.core','_mareconstruct'),
             ('numpy.ma','MaskedArray')}

    def find_class(self,module,name):
        if (module,name) not in self.allowed:
            raise InvalidProject('Disallowed executable object in GSAS project: '+module+'.'+name)
        return super().find_class(module,name)


def restricted_load(file,**kwargs):
    return ProjectUnpickler(file,**kwargs).load()


# All native readers share this pickle module. No project is loaded before here.
pickle.load=restricted_load


def empirical_background(kind, coefficients, x, domain):
    """Preserve the saved fit's background coordinate convention on the full grid."""
    a, b = domain
    t = 2 * (x-a)/(b-a)-1
    if kind == 'chebyschev': return np.polynomial.polynomial.polyval(t, coefficients)
    if kind == 'chebyschev-1': return np.polynomial.chebyshev.chebval(t, coefficients)
    if kind == 'cosine':
        return sum(c*np.cos(np.pi*x*i/b) for i, c in enumerate(coefficients))
    if kind in ['lin interpolate', 'inv interpolate', 'log interpolate']:
        if len(coefficients) == 1: return np.full_like(x, coefficients[0])
        if len(coefficients) == 2: return coefficients[0]+(coefficients[1]-coefficients[0])*(x-a)/(b-a)
        knots = {'lin interpolate': lambda: np.linspace(a,b,len(coefficients)),
                 'inv interpolate': lambda: 1/np.linspace(1/b,1/a,len(coefficients)),
                 'log interpolate': lambda: np.exp(np.linspace(np.log(a),np.log(b),len(coefficients)))}[kind]()
        knots[0],knots[-1]=a,b
        return interp1d(knots, coefficients, bounds_error=False, fill_value='extrapolate')(x)
    return None  # Q-based backgrounds do not depend on the fitting interval.


def replay(request):
    gpx=Path(request['project']); before=hashlib.sha256(gpx.read_bytes()).hexdigest()
    # Native readers sometimes replace parsing exceptions with a generic error.
    # Validate the stream first so malformed or executable input is classified
    # as an invalid submission, not a failure of the evaluator.
    with gpx.open('rb') as stream:
        try:
            while stream.read(1):
                stream.seek(-1,1)
                restricted_load(stream)
        except InvalidProject:
            raise
        except (pickle.UnpicklingError, EOFError, ValueError, TypeError) as exc:
            raise InvalidProject('Malformed GSAS project: '+str(exc)) from exc
    public=np.loadtxt(request['observed'], delimiter=',', skiprows=1, ndmin=2)
    x,y=public.T
    hist,phases=IO.GetUsedHistogramsAndPhases(str(gpx))
    candidates=[]
    for name,h in hist.items():
        if not name.startswith('PWDR'): continue
        xx,yy=np.asarray(h['Data'][0]),np.asarray(h['Data'][1])
        # Common eight-significant-digit XYE export rounds 2theta by at most
        # 5e-7 degrees here. Accept exactly that representation (counts and
        # sample count must still agree), never an arbitrary shifted grid.
        grid_agrees = xx.shape == x.shape and (
            np.allclose(xx,x,rtol=0,atol=1e-7) or
            np.allclose(xx,np.asarray([float(format(v,'.8g')) for v in x]),rtol=0,atol=1e-12))
        if grid_agrees and np.allclose(yy,y,rtol=0,atol=1e-5):
            candidates.append(name)
    chosen=request.get('histogram')
    if chosen is not None:
        if chosen not in candidates: raise InvalidProject('Named histogram does not contain the original observed scan')
        name=chosen
    elif len(candidates)==1: name=candidates[0]
    else: raise InvalidProject('Need one histogram matching original observations, or refinement_histogram in result.json')
    h=hist[name]; hist={name:h}
    phases={n:p for n,p in phases.items() if p.get('Histograms',{}).get(name,{}).get('Use',True) and name in p.get('Histograms',{})
            and p['Histograms'][name]['Scale'][0]!=0}
    if not phases: raise InvalidProject('No atomic phases linked to the observed histogram')
    inst=h['Instrument Parameters'][0]
    if inst['Type'][0]!='PXC': raise NotImplementedError('Replay currently supports constant-wavelength laboratory X-ray histograms')
    for n,p in phases.items():
        general=p['General']; hap=p['Histograms'][name]
        if general.get('doPawley') or hap.get('LeBail'):
            raise InvalidProject('Pawley/Le Bail intensities are not an atomic-model prediction')
        if general.get('Modulated') or general['Type']!='nuclear':
            raise NotImplementedError('Unsupported modulated, magnetic or faulted atomic model')
        if not p['Atoms']: raise InvalidProject('An included phase has no atoms')
        if not np.isfinite(hap['Scale'][0]) or hap['Scale'][0]<0:
            raise InvalidProject('Invalid phase scale')
        if any(p.get('RBModels',{}).get(k) for k in ['Residue','Vector','Spin']):
            raise NotImplementedError('Rigid-body replay requires additional validation')
    if h['Background'][1].get('background PWDR',[None])[0]:
        raise NotImplementedError('A separate measured-background histogram requires additional validation')
    old_limits=copy.deepcopy(h['Limits'])
    lo,hi=np.searchsorted(x,old_limits[1])
    hi=min(len(x)-1,hi)
    if hi<=lo: raise InvalidProject('Invalid saved fitting interval')
    background_domain=[float(x[lo]),float(x[hi])]
    # Score the entire original scan, even if the worker narrowed its fit limits.
    # Use GSAS's normal reflection-generation bounds for that grid. Extending
    # them would add boundary tails absent from both its native saved fit and
    # the generator, changing the model convention during verification.
    h['Limits']=[[float(x[0]),float(x[-1])],[float(x[0]),float(x[-1])]]
    controls=dict(IO.GetControls(str(gpx)))
    controls.pop('PhasePartials',None)
    rigid=IO.GetRigidBodies(str(gpx)); ids=rigid.get('RBIds',{'Vector':[],'Residue':[]})
    _,rb=IO.GetRigidBodyModels(rigid,Print=False)
    natoms,atomidx,_,phase,pawley,ff,ef,orb,bl,mf,maxss=IO.GetPhaseData(phases,{},ids,Print=False)
    controls.update(atomIndx=atomidx,Natoms=natoms,FFtables=ff,EFtables=ef,ORBtables=orb,BLtables=bl,MFtables=mf,maxSSwave=maxss)
    _,hap,c=IO.GetHistogramPhaseData(phases,hist,Controls=controls,Print=False);controls.update(c)
    _,hp,hist1,c=IO.GetHistogramData(hist,Print=False);controls.update(c)
    parameters={**rb,**phase,**hap,**hp}; IO.GetFprime(controls,hist)
    frozen=copy.deepcopy(parameters)
    signal,background=M.getPowderProfile(parameters,hist1,x,[],h,phases,controls,pawley,name)
    prefix=f":{h['hId']}:"; kind=controls[prefix+'bakType']
    coefficients=[]
    while prefix+f'Back;{len(coefficients)}' in parameters:
        coefficients.append(parameters[prefix+f'Back;{len(coefficients)}'])
    old=empirical_background(kind,coefficients,x,background_domain)
    if old is not None:
        background=background+old-empirical_background(kind,coefficients,x,[x[0],x[-1]])
    predicted=signal+background
    if not np.all(np.isfinite(predicted)) or np.any(predicted<0):
        raise InvalidProject('The saved atomic/profile model predicts nonfinite or negative counts')
    for k,v in frozen.items():
        if not np.array_equal(np.asarray(v),np.asarray(parameters[k])):
            raise RuntimeError('Forward replay changed a saved parameter: '+k)
    project=G.G2Project(gpxfile=str(gpx))
    # Export the saved atoms, not possibly stale parameter values in covariance.
    project.data['Covariance']['data']={}
    phase_reports=[]; masses=[]; review=[]
    for n,p in phases.items():
        # Displacement tensors describe variances and must be positive
        # semidefinite. Use full-precision saved atoms, not rounded CIF exports.
        cx,ct,cs,cia=p['General']['AtomPtrs']
        for atom in p['Atoms']:
            if atom[cx+3]<=0:continue
            if atom[cia]=='I':
                lowest=float(atom[cia+1])
            else:
                u11,u22,u33,u12,u13,u23=atom[cia+2:cia+8]
                lowest=float(np.linalg.eigvalsh([[u11,u12,u13],[u12,u22,u23],[u13,u23,u33]])[0])
            if lowest < -1e-8:
                review.append('negative atomic displacement tensor: '+n);break
        index=len(phase_reports); ph=project.phase(n)
        ph.data=p
        filename=f'phase_{index}.cif';ph.export_CIF(filename)
        phase_reports.append({'name':n,'cif':filename,'scale':float(p['Histograms'][name]['Scale'][0]),
                              'cell_mass':float(p['General']['Mass'])})
        masses.append(p['General']['Mass']*p['Histograms'][name]['Scale'][0])
        pp=f"{p['pId']}:{h['hId']}:"; pf=f"{p['pId']}::"
        sg=p['General']['SGData']
        from GSASII import GSASIIlattice as LAT
        dij=M.GetDij(pp,sg,parameters)
        avec=[parameters[pf+f'A{j}']+dij[j] for j in range(6)]
        metric,reciprocal=LAT.A2Gmat(avec);_,gb=LAT.Gmat2AB(metric)
        wave=parameters.get(prefix+'Lam1',parameters.get(prefix+'Lam'))
        for refl in h['Reflection Lists'][n]['RefList']:
            pos=refl[5];tan=np.tan(np.deg2rad(pos/2))
            ss,gs=M.GetSampleSigGam(refl,0,wave,metric,gb,sg,prefix,pp,controls,parameters)
            sig=parameters[prefix+'U']*tan*tan+parameters[prefix+'V']*tan+parameters[prefix+'W']+ss
            gam=parameters[prefix+'X']/np.cos(np.deg2rad(pos/2))+parameters[prefix+'Y']*tan+parameters[prefix+'Z']+gs
            if sig<0 or gam<0:
                review.append('negative analytic peak width requiring GSAS numerical clamping: '+n);break
    if sum(masses)<=0: raise InvalidProject('No positive crystalline scale')
    for p,mass in zip(phase_reports,masses):p['weight_fraction']=float(mass/sum(masses))
    if np.min(background)<-1e-6:review.append('negative background counts')
    if h['Background'][1].get('nPeaks',0):review.append('auxiliary background peaks require physical interpretation')
    pol=parameters.get(prefix+'Polariz.')
    if pol is not None and not 0<=pol<=1:review.append('polarization outside [0,1]')
    np.savez('prediction.npz',x=x,observed=y,predicted=predicted,background=background,signal=signal)
    if hashlib.sha256(gpx.read_bytes()).hexdigest()!=before: raise RuntimeError('Source project changed')
    return dict(status='replayed',project_sha256=before,histogram=name,phases=phase_reports,
                parameters_optimized=0,project_unchanged=True,hidden_inputs_read=False,
                original_fit_limits=plain(old_limits),evaluation_grid='entire original observed grid',
                background_domain=background_domain,background_type=kind,background_coefficients=plain(coefficients),
                instrument=plain(inst),profile_review_flags=sorted(set(review)),
                regeneration='Native GSAS atomic structure factors and fresh reflection lists; saved calculated arrays ignored')


if __name__=='__main__':
    try:
        result=replay(json.loads(Path(sys.argv[1]).read_text()))
    except InvalidProject as exc:
        result={'status':'invalid_project','error':str(exc)}
    except Exception as exc:
        result={'status':'verification_error','error':str(exc),'traceback':traceback.format_exc()}
    Path('replay.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    sys.exit(0 if result['status']=='replayed' else 2)
