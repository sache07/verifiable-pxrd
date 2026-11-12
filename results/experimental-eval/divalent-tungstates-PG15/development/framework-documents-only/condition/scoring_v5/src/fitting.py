"""Observed-data fitting with protocol-versioned angular calibration."""
from pathlib import Path
from functools import lru_cache
import numpy as np
from common import ROOT, read_json, sha, fit_profiles
from forward import cached_components, serialize_without_model_change
from measurement import uses_known_zero, evaluation_protocol, calibration_diagnostic
from specimen import has_profile_effects, continuous_profiles

OLD=ROOT.parent/'pxrd-family-scoring-v4-20260927'

@lru_cache(maxsize=1)
def original_records():
    rows=read_json(OLD/'attempts.json')+read_json(OLD/'validation_records.json')
    return {r['id']:r for r in rows}

def historical_reuse_matches(record,paths,old):
    original=original_records().get(record['id'])
    if original is None:return False
    if any(Path(record[k]).resolve()!=Path(original[k]).resolve() for k in ['case_path','workspace']):return False
    expected={str(Path(p).resolve()) for p in [Path(record['workspace'])/'result.json',*paths]}
    actual={str(Path(p).resolve()) for p in old.get('submission_fingerprints',{})}
    return expected==actual


def calculate_profiles(paths,weights,protocol,x,y,record,out,eligible):
    if continuous_profiles(protocol):
        if not uses_known_zero(protocol):raise ValueError('Continuous profiles require known-calibration evaluation')
        from continuous_fitting import calculate_continuous_profiles
        try:
            return calculate_continuous_profiles(paths,weights,protocol,x,y,record,out,eligible)
        except (ValueError,RuntimeError) as exc:
            if 'interpretation mismatch' not in str(exc) and 'Native continuous evaluator failed' not in str(exc):raise
            repaired,serialization=serialize_without_model_change(paths,out)
            best,free,evidence,_=calculate_continuous_profiles(repaired,weights,protocol,x,y,record,out,eligible)
            return best,free,evidence,serialization
    if has_profile_effects(protocol):
        if not uses_known_zero(protocol):raise ValueError('Optional profiles require the known-zero protocol')
        from profile_search import calculate_optional_profiles
        return calculate_optional_profiles(paths,weights,protocol,x,y,out,eligible)
    best,free_best,evidence,fallback=None,None,[],False
    serialization=None
    caches=record.get('historical_caches',[record.get('legacy_cache',str(out/'cache'))])
    allow_shift=not uses_known_zero(protocol)
    for size in protocol['generation']['domain_size_um']:
        try:
            xx,profiles,proof=cached_components(paths,protocol,size,caches,out)
        except (ValueError,RuntimeError) as exc:
            if fallback or ('interpretation mismatch' not in str(exc) and 'GSAS forward calculation failed' not in str(exc)):raise
            paths,serialization=serialize_without_model_change(paths,out);fallback=True
            xx,profiles,proof=cached_components(paths,protocol,size,caches,out)
        if not np.allclose(x,xx,atol=1e-7,rtol=0):raise ValueError('Forward grid mismatch')
        if eligible:
            fixed=fit_profiles(x,y,profiles,fixed_fractions=np.asarray(weights),allow_shift=allow_shift)
            fixed['domain_size_um']=size
            if best is None or fixed['chi_square']<best['chi_square']:best=fixed
        free=fit_profiles(x,y,profiles,allow_shift=allow_shift);free['domain_size_um']=size
        if free_best is None or free['chi_square']<free_best['chi_square']:free_best=free
        evidence.append(dict(size_um=size,**proof))
    return best,free_best,evidence,serialization


def observed_prediction(record,paths,weights,protocol,out,eligible):
    case=Path(record['case_path']);x,y=np.loadtxt(case/'inputs/pattern.csv',delimiter=',',skiprows=1).T
    oldfile=OLD/'scores'/record['id']/'score.json'
    old=read_json(oldfile) if oldfile.exists() else None
    if not uses_known_zero(protocol) and record.get('reuse_v4',True) and old is not None and historical_reuse_matches(record,paths,old):
        protected=read_json(ROOT/'source_hashes.json')
        if protected.get(str(oldfile))!=sha(oldfile):raise ValueError('Historical score changed')
        for f,digest in old.get('submission_fingerprints',{}).items():
            if sha(f)!=digest:raise ValueError('Historical submission changed: '+f)
        if eligible:
            curve=oldfile.parent/'independent_fit.csv'
            if not curve.exists():raise RuntimeError('Eligible historical prediction is unavailable')
            if protected.get(str(curve))!=sha(curve):raise ValueError('Historical fitted curve changed')
            a=np.loadtxt(curve,delimiter=',',skiprows=1)
            if not np.allclose(a[:,0],x,atol=1e-9,rtol=0) or not np.array_equal(a[:,1],y):raise ValueError('Historical observed scan mismatch')
            pred=a[:,2];q=1/np.maximum(y,1.)
            rwp=100*np.sqrt(np.sum(q*(y-pred)**2)/np.sum(q*y*y))
            if not np.isclose(rwp,old['independent_atomic_rwp'],rtol=1e-10,atol=1e-9):raise ValueError('Historical Rwp cannot be reproduced')
            best=dict(calculated=pred,rwp_percent=float(rwp),chi_square=float(np.sum(q*(y-pred)**2)),
                      **old.get('submitted_nuisance',{}))
        else:best=None
        return x,y,best,dict(mode='verified immutable v4 curve',source=str(oldfile),
            curve_sha256=sha(oldfile.parent/'independent_fit.csv') if best is not None else None,
            candidate_quality=old.get('candidate_quality'),reference_rwp=old.get('reference_rwp'),
            v4_score=old.get('score_100'),v4_status=old.get('score_status'),
            v4_reference_physical_validity=old.get('reference_physical_validity'),
            v4_strict_fraction_error=old.get('mass_fraction_error'))
    best,free,evidence,serialization=calculate_profiles(paths,weights,protocol,x,y,record,out,eligible)
    if free is not None:
        np.savetxt(out/'diagnostic_free_fraction_fit.csv',np.column_stack([x,y,free['calculated'],y-free['calculated']]),
                   delimiter=',',header='two_theta,observed,calculated,difference',comments='')
    return x,y,best,dict(mode='known-zero observed-data fitting' if uses_known_zero(protocol) else 'unchanged observed-data fitting',
        angular_calibration=calibration_diagnostic(protocol),
        fitted_nuisance=None if best is None else {k:best[k] for k in ['zero_shift_deg','domain_size_um','phase_profile_settings','profile_search'] if k in best},
        forward_evidence=evidence,
        serialization_repair=serialization,candidate_quality=None if free is None else dict(rwp_percent=free['rwp_percent'],
        refitted_fractions=free['fractions'].tolist(),primary_profile_credit=False),reference_rwp=None)


@lru_cache(maxsize=128)
def reference_diagnostic(case_path):
    """Observed-scan reference fit, calculated only after candidate freezing.

    This diagnostic cannot choose the candidate's nuisance settings or credit.
    Historical attempts already provide the identical v4 diagnostic.
    """
    case=Path(case_path);truth=read_json(case/'private/truth.json')
    x,y=np.loadtxt(case/'inputs/pattern.csv',delimiter=',',skiprows=1).T
    paths=[case/'private/references'/(p['id']+'.cif') for p in truth['phases']]
    out=ROOT/'reference_diagnostics'/sha(case/'private/truth.json')
    out.mkdir(parents=True,exist_ok=True)
    best,_,_,_=calculate_profiles(paths,truth['true_fractions'],evaluation_protocol(truth),x,y,
                                 {'case_path':str(case),'_reference_diagnostic':True},out,True)
    return float(best['rwp_percent'])
