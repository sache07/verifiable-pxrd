"""Generate and audit curator-selected synthetic mixtures; makes no model calls."""
from pathlib import Path
import argparse
import json
import shutil
import sys
import numpy as np
from physics import components,sha,save_json,bernstein,fit_profiles
from backgrounds import realize_background, sample_background
from measurement import generate_measurement, offset_settings, uses_known_zero
from specimen import effect_settings, realize_specimen, forward_spec, apply_uiso, has_profile_effects, enabled, profile_options, continuous_profiles
from specimen import CASE_KEYS, realize_sample, sample_spec, realize_mismatch
from perturb_model import mismatch_model
from solver_inputs import check_sample, write_inputs

def recipe_check(recipe,catalog,protocol):
    if set(recipe)-{'id','phases','principal_id','availability','withhold_ids','peak_counts','background_counts','background_family','domain_size_um','seed','rationale','sample','angular_offset_control','measurement_session','specimen_control'}:
        raise ValueError('unrecognized recipe fields')
    import re
    if not re.fullmatch(r'[a-z][a-z0-9-]{1,39}',recipe['id']):
        raise ValueError('id must be a short lowercase opaque identifier')
    phases=recipe['phases']
    if not 1<=len(phases)<=protocol['generation'].get('max_components',16):
        raise ValueError('phase count exceeds the configured resource ceiling')
    ids=[p['id'] for p in phases]
    if len(set(ids))!=len(ids):raise ValueError('duplicate source IDs')
    rows=[catalog[i] for i in ids]
    fractions=np.array([p['weight_fraction'] for p in phases],float)
    if not np.all(np.isfinite(fractions)) or abs(fractions.sum()-1)>1e-8:
        raise ValueError('mass fractions must sum to one')
    if np.any(fractions<=0) or np.any(fractions>1):
        raise ValueError('each mass fraction must be positive and at most one')
    if len(phases)==1 and fractions[0]!=1:raise ValueError('single-phase fraction must be 1')
    if recipe['availability'] not in ['full','withhold_principal_composition','withhold_ids']:
        raise ValueError('unsupported availability condition')
    principal=recipe.get('principal_id')
    if principal is not None and principal not in ids:
        raise ValueError('principal_id must identify an included component')
    if recipe['availability']=='withhold_principal_composition' and principal is None:
        raise ValueError('withholding requires principal_id to select the excluded composition')
    withhold=recipe.get('withhold_ids')
    if (withhold is not None)!=(recipe['availability']=='withhold_ids'):
        raise ValueError('withhold_ids is required with, and only with, availability "withhold_ids"')
    if withhold is not None:
        if not isinstance(withhold,list) or not withhold or len(set(withhold))!=len(withhold) or any(not isinstance(w,str) or not w.isdigit() for w in withhold):
            raise ValueError('withhold_ids must be a nonempty list of distinct COD record IDs as strings')
        # Never hide a library entry that another phase of the same case was registered from.
        import re
        for r in rows:
            found=set(re.findall(r'\b(\d{7})\b',str(r.get('provenance',''))+' '+str(r.get('cif_path',''))+' '+str(r.get('source_path',''))))
            clash=found&set(withhold)
            if clash and (principal is None or r['id']!=principal):
                raise ValueError('withhold_ids would hide the library entry of included phase '+r['id']+': '+', '.join(sorted(clash)))
    for field,allowed in [('peak_counts',protocol['generation']['peak_counts']),('domain_size_um',protocol['generation']['domain_size_um'])]:
        if recipe[field] not in allowed:raise ValueError(f'{field} must be selected from {allowed}')
    if isinstance(recipe['seed'],bool) or not isinstance(recipe['seed'],int) or not 0<=recipe['seed']<2**32:
        raise ValueError('seed must be uint32')
    realize_background(recipe,protocol)
    generate_measurement(recipe,protocol)
    settings=offset_settings(protocol)
    effect_settings(protocol)
    realize_specimen(recipe,protocol)
    realize_sample(recipe,protocol)
    if not continuous_profiles(protocol):profile_options(protocol,recipe['domain_size_um'])
    if settings and settings['enabled'] and not uses_known_zero(protocol):
        raise ValueError('Hidden offsets require known-generating-zero evaluation')
    if has_profile_effects(protocol):
        if not uses_known_zero(protocol):raise ValueError('Optional specimen profiles require the known-zero protocol')
        if continuous_profiles(protocol):
            from specimen import continuous_bounds
            continuous_bounds(protocol)
            search=protocol.get('verification',{}).get('continuous_profile_search',{})
            if set(search)!={'starts','max_nfev','ftol','xtol','gtol','seed'} or any(type(search.get(k)) is not int or search[k]<1 for k in ['starts','max_nfev','seed']):
                raise ValueError('Continuous profiles require a frozen observed-data search policy')
            if any(type(search[k]) not in (int,float) or not np.isfinite(search[k]) or not 0<search[k]<1 for k in ['ftol','xtol','gtol']):
                raise ValueError('Invalid continuous-profile numerical tolerance')
        else:
            search=protocol.get('verification',{}).get('optional_profile_search',{})
            if set(search)!={'exhaustive_max_combinations','coordinate_starts','coordinate_max_passes'} or any(type(v) is not int or v<1 for v in search.values()):
                raise ValueError('Optional specimen profiles require a valid frozen observed-data search policy')
    if not str(recipe['rationale']).strip():raise ValueError('rationale required')
    # Solvers see the stated sample description, as on the lab's experimental scans; it must account for every phase's elements.
    stated,allowed=check_sample(recipe,rows,protocol)
    return rows,fractions,stated,allowed

def generate_one(recipe,pool,protocol,out,cache):
    catalog={r['id']:r for r in json.loads((pool/'catalog.json').read_text())['records']}
    rows,fractions,stated,allowed=recipe_check(recipe,catalog,protocol)
    case=out/recipe['id']
    token=sha(pool/'catalog.json')
    if case.exists():
        old=json.loads((case/'private/truth.json').read_text()) if (case/'private/truth.json').exists() else None
        if old and old['recipe']==recipe and old['protocol']==protocol and old['source_pool_sha256']==token:
            return json.loads((case/'checks.json').read_text())
        raise ValueError(f'refusing to overwrite different or incomplete case: {case}')
    cifs=[pool/r['model_path'] for r in rows]
    for p,r in zip(cifs,rows):
        if sha(p)!=r['model_sha256']:raise ValueError('source model checksum mismatch')
    # The registered pool remains immutable. Mismatched and thermal variants are separate case
    # references with their own hashes and parent-model provenance.
    references=case/'private/references'
    mismatch=realize_mismatch(recipe,protocol)
    if any(mismatch):
        references.mkdir(parents=True,exist_ok=True)
        changed=[];derived=[]
        for source,row,draw in zip(cifs,rows,mismatch):
            if draw is None:
                changed.append(source);derived.append(row);continue
            destination=references/(row['id']+'.cif')
            record=mismatch_model(source,destination,draw['cell_strain'],draw['position_rms_A'],draw['seed'],
                                  rms_by_element=draw.get('position_rms_A_by_element'))
            changed.append(destination)
            derived.append({**row,'parent_model_sha256':row['model_sha256'],'registered_model_path':str(source.resolve()),
                            'model_sha256':sha(destination),'reference_mismatch':record})
        cifs,rows=changed,derived
    specimen=realize_specimen(recipe,protocol)
    if enabled(protocol,'displacement_parameters'):
        references.mkdir(parents=True,exist_ok=True)
        changed=[];derived=[]
        for source,row,spec in zip(cifs,rows,specimen):
            destination=references/(row['id']+'.cif')
            apply_uiso(source,destination,spec['uiso_A2'])
            changed.append(destination)
            derived.append({**row,'parent_model_sha256':row.get('parent_model_sha256',row['model_sha256']),
                            'model_sha256':sha(destination),'case_uiso_A2':spec['uiso_A2']})
        cifs,rows=changed,derived
    measurement=generate_measurement(recipe,protocol)
    instrument = measurement.get('true_instrument', {'zero_deg':measurement['true_zero_deg']})
    # Whole-specimen effects (displacement, low-angle deficit) are shared by all phases.
    sample=realize_sample(recipe,protocol)
    case_effects=any(enabled(protocol,k) for k in CASE_KEYS)
    x,profiles,forward=components(cifs,protocol,recipe['domain_size_um'],cache,
        instrument_override=instrument,
        phase_profiles=[forward_spec(r) for r in specimen] if has_profile_effects(protocol) else None,
        sample_parameters=sample_spec(sample) if case_effects else None)
    raw=fractions@profiles
    normalization=float(recipe['peak_counts'])/float(np.max(raw))
    signal=normalization*raw
    background,bg_basis,bg_realization=sample_background(x,recipe,protocol)
    mean=signal+background
    observed=np.random.default_rng(recipe['seed']).poisson(mean).astype(float)
    allow_shift=not uses_known_zero(protocol)
    oracle=fit_profiles(x,observed,profiles,allow_shift=allow_shift,background_basis=bg_basis)
    weights=1/np.maximum(mean,1.)
    omissions=[]
    for i,r in enumerate(rows):
        left=np.delete(profiles,i,axis=0)
        if len(left):
            fit=fit_profiles(x,mean,left,weights=weights,allow_shift=allow_shift,background_basis=bg_basis)
            rms=np.sqrt(fit['chi_square']/len(x))
        else:
            from scipy.optimize import nnls
            A=bg_basis;sq=np.sqrt(weights)
            coef,_=nnls(A*sq[:,None],mean*sq)
            rms=np.sqrt(np.mean(weights*(mean-A@coef)**2))
        omissions.append({'id':r['id'],'omission_rms_noise_units':float(rms)})
    fraction_error=float(np.max(np.abs(oracle['fractions']-fractions)))
    min_signal=min(o['omission_rms_noise_units'] for o in omissions)
    eligible=fraction_error<=protocol['verification']['oracle_max_fraction_error'] and min_signal>=protocol['verification']['minimum_omission_rms_noise_units']
    public=case/'inputs';private=case/'private'
    public.mkdir(parents=True);(private/'references').mkdir(parents=True,exist_ok=True)
    write_inputs(public,x,observed,recipe,stated,protocol)
    for r,cif in zip(rows,cifs):
        destination=private/'references'/f"{r['id']}.cif"
        if cif.resolve()!=destination.resolve():shutil.copy2(cif,destination)
    np.savez_compressed(private/'forward.npz',x=x,profiles=profiles,mean=mean,background=background,signal=signal,normalization=normalization)
    truth={'schema_version':1,'recipe':recipe,'protocol':protocol,'source_pool_sha256':token,'phases':rows,'true_fractions':fractions.tolist(),'forward':forward,
           'generation_code_sha256':sha(Path(__file__)),'worker_sha256':sha(Path(__file__).with_name('gsas_worker.py')),
           'runtime_sha256':{p.name:sha(p) for p in sorted(Path(__file__).parent.glob('*.py'))},
           'input_hashes':{p.name:sha(p) for p in public.iterdir()},
           'withhold_composition':catalog[recipe['principal_id']]['composition_key'] if recipe['availability']=='withhold_principal_composition' else None,
           'withhold_ids':sorted(recipe['withhold_ids']) if recipe['availability']=='withhold_ids' else None}
    truth['background_realization']=bg_realization
    truth['allowed_elements']=allowed
    if offset_settings(protocol) is not None or uses_known_zero(protocol):
        truth['measurement']=measurement
    if protocol['generation'].get('specimen_effects') is not None:
        truth['specimen_realization']=specimen
    if case_effects:
        truth['sample_realization']=sample
    save_json(private/'truth.json',truth)
    checks={'case_id':recipe['id'],'eligible_for_strict_recovery':bool(eligible),
            'oracle_max_fraction_error':fraction_error,'oracle_fractions':oracle['fractions'].tolist(),
            'oracle_rwp_percent':float(oracle['rwp_percent']),'omissions':omissions,
            'background_audit':'Generating background family and shape parameters known; its nonnegative amplitudes refitted. This is an oracle generation check, not a solver fit or proof of experimental identifiability.',
            'scope':'known-structure quantitation and omission detectability screen; not a proof of unique structure or a complete competing-polymorph audit'}
    save_json(case/'checks.json',checks)
    return checks

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest',type=Path);p.add_argument('--pool',type=Path,default=Path('outputs/pool'))
    p.add_argument('--lab',type=Path,default=Path('LAB.md'),help='LAB.md with the lab settings block')
    p.add_argument('--out',type=Path,default=Path('outputs/cases'))
    p.add_argument('--cache',type=Path,default=Path('.cache/forward'))
    p.add_argument('--finalize',action='store_true',help='validate at least the configured initial-batch case count; supplementary cases are allowed')
    args=p.parse_args()
    manifest=json.loads(args.manifest.read_text())
    if manifest.get('schema_version')!=1:raise ValueError('manifest schema_version must be 1')
    from labspec import protocol as lab_protocol
    protocol=lab_protocol(args.lab)
    if manifest.get('source_pool_sha256')!=sha(args.pool/'catalog.json'):
        raise ValueError('manifest source_pool_sha256 must match the selected pool/catalog.json')
    if manifest.get('lab_sha256')!=sha(args.lab):
        raise ValueError('manifest lab_sha256 must match LAB.md')
    cases=manifest['cases']
    if len({c['id'] for c in cases})!=len(cases):raise ValueError('duplicate case IDs')
    reports=[]
    for case in cases:
        report=generate_one(case,args.pool.resolve(),protocol,args.out.resolve(),args.cache.resolve())
        reports.append(report)
        print(json.dumps(report),flush=True)
    save_json(args.out/'generation_summary.json',{'case_count':len(reports),'strict_eligible_count':sum(r['eligible_for_strict_recovery'] for r in reports),'cases':reports})
    if args.finalize:
        checks={
            'case_count':len(cases)>=protocol['generation']['training_cases'],
            'all_cases_generated':len(reports)==len(cases),
        }
        save_json(args.out/'handoff_check.json',{'passed':all(checks.values()),'checks':checks,'manifest_sha256':sha(args.manifest),
             'strict_eligible_count':sum(r['eligible_for_strict_recovery'] for r in reports),
             'scope':'Mechanical generation checks only. Scientific coverage, ambiguity, and evaluation sampling are reviewed separately; no category or eligibility quota.'})
        if not all(checks.values()):raise ValueError('panel handoff requirements failed: '+json.dumps(checks))

if __name__=='__main__':
    main()
