"""Profile agreement primary: the verified final.gpx replay is scored against the hidden
noise-free pattern (D), gated by physical validity, with a secondary structural term that
credits inventory, fractions and scattering-weighted site agreement.

Interplay: a solution is good when its predicted pattern matches the data to the noise
floor and every structure is physically valid. Fitting noise cannot lower D, and misplacing
atoms the pattern barely sees costs little structural credit."""
from pathlib import Path
import traceback
import numpy as np
from common import ROOT,CONFIG,read_json,save_json,sha,load_structure,code_hashes,allowed_elements
from structure_metrics import parse_submission,strict_assign_phases,fraction_metrics,physical_screen
from structural_inventory import compare_inventory
from replay import replay_prediction
from predictive import evaluate_frozen
from exported_profile import inspect_export


def score_attempt(record):
    out=ROOT/'scores'/record['id'];out.mkdir(parents=True,exist_ok=True)
    case,work=Path(record['case_path']),Path(record['workspace'])
    result={k:record.get(k)for k in ['id','dataset','condition','cohort','replicate','case_id','case_key','split','workspace','case_path']}
    headline=CONFIG['headline']
    result.update(scorer_version=CONFIG['version'],headline_metric=headline['metric'],
        config_sha256=sha(ROOT/'config.json'),implementation_sha256=code_hashes(),
        score_100=None,score_interval=None,score_status='verification_error',
        independent_atomic_rwp=None,reference_rwp=None,D_poisson=None,D_quadratic=None,
        D_poisson_infinite=False,P=None,P_quadratic=None,profile_status='not_evaluated',
        profile_used_for_primary_score=False,declared_fit_csv_used_for_scoring=False)
    try:
        # Registered provenance must cover this case, including structural truth.
        provenance=read_json(ROOT/'truth_provenance.json').get(str(case.resolve()))
        if not provenance:raise ValueError('Case has no registered synthetic truth provenance')
        for path,digest in provenance.items():
            if sha(path)!=digest:raise ValueError('Frozen case changed: '+path)
        result['input_sha256']=provenance
        truth=read_json(case/'private/truth.json')
        elements=allowed_elements(truth,read_json(case/'inputs/metadata.json'))
        refs=[load_structure(case/'private/references'/(p['id']+'.cif'))for p in truth['phases']]
        target=truth['true_fractions']
    except Exception as exc:
        result['error']=str(exc);save_json(out/'score.json',result);return result
    try:
        data,rows,notes=parse_submission(work,elements)
    except Exception as exc:
        bad=isinstance(exc,ValueError)or(isinstance(exc,FileNotFoundError)and not(work/'result.json').exists())
        result.update(error=str(exc),score_status='invalid_submission' if bad else 'verification_error',
            score_100=0. if bad else None,score_interval=[0.,0.]if bad else None)
        save_json(out/'score.json',result);return result
    try:
        parsing=data['_submission_parsing'];pred=[r['structure']for r in rows]
        invalid=parsing['invalid_model_records'];weights=[r['fraction']for r in rows+invalid]
        physical=('fail'if parsing['hard_physical_failure']or any(r['physical']['status']=='fail'for r in rows)
                  else 'needs_adjudication'if any(r['physical']['status']=='needs_adjudication'for r in rows)else 'pass')
        reference_screen=[physical_screen(s)for s in refs]
        partial=bool(invalid or parsing['unresolved_components']or not parsing['quantification_complete'])
        result.update(submission_parsing=parsing,notes=notes,physical_validity=physical,
            physical_audit=[r['physical']for r in rows],reference_physical_audit=reference_screen,
            reference_formulas=[s.composition.formula for s in refs],
            submitted_formulas=[s.composition.formula for s in pred]+['invalid atomic model']*len(invalid),
            reference_fractions=target,submitted_fractions=weights,reported_partial_answer=partial,
            submission_fingerprints={str(p):sha(p)for p in [work/'result.json',*[e['path']for r in rows for e in r.get('equivalent_exports',[r])]]})
        eligible=bool(rows)and not invalid and parsing['quantification_complete']
        # Existing replay is unchanged: the complete submitted calibration/model
        # is retained, and the hidden expected signal is consulted only after
        # independent prediction. Its success never selects a structural match.
        try:
            result['solver_measurement_diagnostics']=inspect_export(work,case,data)
            if rows:
                x,y,best,meta=replay_prediction(record,rows,data,out,eligible)
                result['fitting']=meta;result['profile_status']=meta.get('status','unavailable')
                result['reference_rwp']=meta.get('reference_rwp')
                if meta.get('project_sha256'):result['submission_fingerprints'][str(work/'final.gpx')]=meta['project_sha256']
                if best is not None:
                    result.update(evaluate_frozen(case,x,y,best['calculated']))
                    result.update(independent_atomic_rwp=best['rwp_percent'],atomic_chi_square=best['chi_square'])
                    np.savetxt(out/'independent_fit.csv',np.column_stack([x,y,best['calculated'],y-best['calculated']]),delimiter=',',
                               header='two_theta,observed,calculated,difference',comments='')
            else:result['profile_status']='unavailable_no_atomic_models'
        except Exception as exc:
            result.update(profile_status='verification_error',profile_error=str(exc),profile_traceback=traceback.format_exc())
        # Independent structure score survives a missing/invalid/unreplayable
        # project. A complete scientific solution still needs a valid profile;
        # the status and missing diagnostics remain explicit for the researcher.
        structural,features,registration=compare_inventory(refs,pred,target,[r['fraction']for r in rows],
            [r['fraction']for r in invalid],physical=='fail',physical=='needs_adjudication')
        save_json(out/'structural_features.json',features)
        # Headline: profile agreement with the hidden noise-free pattern is primary and
        # requires a verified project; the structural term is secondary. A hard physical
        # failure scores zero. An unresolved registration keeps its interval.
        D=result.get('D_poisson')
        verified=result['profile_status']=='verified' and D is not None and not result.get('D_poisson_infinite')
        profile=1/(1+D/headline['profile_scale_D']) if verified else 0.
        combine=lambda s:100*(headline['profile_weight']*profile+headline['structure_weight']*s/100)
        lo,hi=structural['score_interval']
        gate=physical=='fail'
        result.update(structural_components=structural,pair_correspondences=registration,
            score_100=0. if gate else (None if structural['score'] is None else combine(structural['score'])),
            score_interval=[0.,0.] if gate else [combine(lo),combine(hi)],
            structural_status=structural['status'],structural_feature_file=str(out/'structural_features.json'),
            profile_used_for_primary_score=verified,
            headline_components=dict(profile_score=100*profile,profile_available=verified,D_poisson=D,
                structural_score=structural['score'],structural_score_interval=[lo,hi],
                profile_weight=headline['profile_weight'],structure_weight=headline['structure_weight'],
                profile_scale_D=headline['profile_scale_D'],physical_gate='fail' if gate else 'pass'))
        try:
            pairs,matrix,_=strict_assign_phases(refs,pred)
            result['strict_diagnostics']=dict(phase_f1=2*len(pairs)/(len(refs)+len(weights)),match_matrix=matrix,
                                              **fraction_metrics(target,weights,pairs))
        except Exception as exc:result['strict_diagnostics_error']=str(exc)
        reasons=[]
        if physical=='needs_adjudication':reasons.append('submitted physical interpretation requires review')
        if any(r['status']!='pass'for r in reference_screen):reasons.append('reference physical interpretation requires review')
        reasons.extend(result.get('fitting',{}).get('profile_review_flags',[]))
        if structural['score']is None:reasons.append('structural registration unresolved; score interval retained')
        result['score_status']=('hard_physical_failure'if physical=='fail'else 'needs_adjudication'if reasons
            else 'partial_submission'if partial or result['profile_status']!='verified'else 'scored')
        result.update(adjudication_reasons=reasons,score_100_is_provisional=bool(reasons),
            scientific_score_100=result['score_100']if not reasons else None,
            angular_calibration={'mode':'submitted_project','true_calibration_substituted':False},
            scientific_caveat='Agreement with the synthetic generating pattern and model, not proof of experimental identifiability. Inspect the profile and structural components and physical flags separately.')
    except Exception as exc:
        result.update(score_status='verification_error',error=str(exc),traceback=traceback.format_exc(),score_100=None,score_interval=None)
    save_json(out/'score.json',result);return result
