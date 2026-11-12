"""Synthetic v5 scorer; expensive structural comparison is cached separately."""
from pathlib import Path
import traceback
import numpy as np
from common import ROOT,CONFIG,read_json,save_json,sha,load_structure,code_hashes
from structure_metrics import parse_submission,strict_assign_phases,fraction_metrics,physical_screen
from soft_matching import cached_pair,assign_quality,SCALES
from bounded_matching import compare_inventory
from replay import replay_prediction
from predictive import evaluate_frozen
from rubric import score_components
from exported_profile import inspect_export


def score_attempt(record):
    out=ROOT/'scores'/record['id'];out.mkdir(parents=True,exist_ok=True)
    case,work=Path(record['case_path']),Path(record['workspace'])
    result={k:record.get(k) for k in ['id','dataset','condition','cohort','replicate','case_id','case_key','split','workspace','case_path']}
    result.update(scorer_version=CONFIG['version'],config_sha256=sha(ROOT/'config.json'),score_100=0.,
                  scientific_score_100=0.,score_interval=[0.,0.],score_status='invalid_submission',
                  score_quadratic_100=0.,independent_atomic_rwp=None,reference_rwp=None,
                  P=0.,P_quadratic=0.,T=0.,F=0.,A=0.,D_poisson=None,D_quadratic=None,D_poisson_infinite=False,
                  implementation_sha256=code_hashes(),
                  input_sha256=read_json(ROOT/'truth_provenance.json').get(str(case.resolve()),{}))
    try:
        elements=read_json(case/'inputs/metadata.json')['elements']
    except Exception as exc:
        result.update(error=str(exc),score_status='verification_error',score_100=None,scientific_score_100=None,
            score_quadratic_100=None,score_interval=None)
        save_json(out/'score.json',result);return result
    try:
        data,rows,notes=parse_submission(work,elements)
    except Exception as exc:
        result['error']=str(exc)
        bad_submission=isinstance(exc,ValueError) or (isinstance(exc,FileNotFoundError) and not (work/'result.json').exists())
        if not bad_submission:
            result.update(score_status='verification_error',score_100=None,scientific_score_100=None,
                score_quadratic_100=None,score_interval=None)
        save_json(out/'score.json',result);return result
    try:
        truth=read_json(case/'private/truth.json');parsing=data['_submission_parsing']
        result['angular_calibration']={'mode':'submitted_project','true_calibration_substituted':False}
        result['solver_measurement_diagnostics']=inspect_export(work,case,data)
        refs=[load_structure(case/'private/references'/(p['id']+'.cif')) for p in truth['phases']]
        pred=[r['structure'] for r in rows];invalid=parsing['invalid_model_records']
        weights=[r['fraction'] for r in rows+invalid];target=truth['true_fractions']
        eligible=bool(rows) and not invalid and parsing['quantification_complete']
        physical=('fail' if parsing['hard_physical_failure'] or any(r['physical']['status']=='fail' for r in rows)
                  else 'needs_adjudication' if any(r['physical']['status']=='needs_adjudication' for r in rows) else 'pass')
        reference_screen=[physical_screen(s) for s in refs]
        partial=bool(invalid or parsing['unresolved_components'] or not parsing['quantification_complete'])
        result.update(submission_parsing=parsing,notes=notes,physical_validity=physical,
            physical_audit=[r['physical'] for r in rows],reference_physical_audit=reference_screen,
            reference_formulas=[s.composition.formula for s in refs],submitted_formulas=[s.composition.formula for s in pred]+['invalid atomic model']*len(invalid),
            reference_fractions=target,submitted_fractions=weights,reported_partial_answer=partial,
            submission_fingerprints={str(p):sha(p) for p in [work/'result.json',*[e['path'] for r in rows for e in r.get('equivalent_exports',[r])]]},
            primary_profile_status='available' if eligible else 'unavailable_incomplete_or_invalid_quantified_model')
        profile_error=None
        try:
            if rows:
                x,y,best,fitmeta=replay_prediction(record,rows,data,out,eligible)
            else:
                x,y=np.loadtxt(case/'inputs/pattern.csv',delimiter=',',skiprows=1).T;best=None;fitmeta={}
            result['fitting']=fitmeta;result['reference_rwp']=fitmeta.get('reference_rwp')
            result['primary_profile_status']=fitmeta.get('status','unavailable')
            if fitmeta.get('project_sha256'):
                result['submission_fingerprints'][str(work/'final.gpx')]=fitmeta['project_sha256']
            if best is not None:
                # Neither this comparison nor the following structural analysis can influence the frozen prediction.
                result.update(evaluate_frozen(case,x,y,best['calculated']))
                result.update(independent_atomic_rwp=best['rwp_percent'],atomic_chi_square=best['chi_square'])
                np.savetxt(out/'independent_fit.csv',np.column_stack([x,y,best['calculated'],y-best['calculated']]),
                    delimiter=',',header='two_theta,observed,calculated,difference',comments='')
            else:result.update(P=0.,P_quadratic=0.,D_poisson=None,D_quadratic=None,D_poisson_infinite=False)
        except Exception as exc:
            profile_error=str(exc);result.update(P=0.,P_quadratic=0.,profile_error=profile_error)
        strict_pairs,strict_matrix,_=strict_assign_phases(refs,pred)
        result['strict_diagnostics']=dict(phase_f1=2*len(strict_pairs)/(len(refs)+len(weights)),
            match_matrix=strict_matrix,**fraction_metrics(target,weights,strict_pairs))
        qualities,pair_reports,registration_errors,bounds=compare_inventory(refs,pred)
        recovery={s:assign_quality(q,target,weights,asserted_count=len(weights)) for s,q in qualities.items()}
        primary=recovery[str(CONFIG['soft_matching']['length_scale_A'])]
        composition=[]
        for i,j in primary['pairs']:
            a=refs[i].composition.fractional_composition.get_el_amt_dict()
            b=pred[j].composition.fractional_composition.get_el_amt_dict()
            delta={e:b.get(e,0.)-a.get(e,0.) for e in sorted(set(a)|set(b))}
            composition.append(dict(reference_index=i,submitted_index=j,
                reference_atomic_fractions=a,submitted_atomic_fractions=b,
                signed_atomic_fraction_errors=delta,total_variation=.5*sum(abs(v) for v in delta.values()),
                basis='Per occupied atom; representation-invariant composition diagnostic, no additional score penalty'))
        result.update(pair_correspondences=pair_reports,quality_matrices={s:q.tolist() for s,q in qualities.items()},
                      recovery_by_scale=recovery,registration_errors=registration_errors,assignment_pruning=bounds,
                      composition_diagnostics=composition)
        result.update(score_components(result['P'],primary['F'],primary['A_interval'][0],result['P_quadratic'],hard_failure=physical=='fail'))
        result['sensitivity']={}
        for s,recover in recovery.items():
            for weight in CONFIG['rubric']['profile_weight_sensitivity']:
                for loss,p in [('poisson',result['P']),('quadratic',result['P_quadratic'])]:
                    lo=weight*p+(100-weight)*recover['T_interval'][0]
                    hi=weight*p+(100-weight)*recover['T_interval'][1]
                    result['sensitivity'][f'{loss}:w{weight}:s{s}']=dict(score=lo if hi-lo<1e-9 else None,
                        interval=[lo,hi]) if physical!='fail' else dict(score=0.,interval=[0.,0.])
        reasons=[]
        reasons.extend(result.get('fitting',{}).get('profile_review_flags',[]))
        if physical=='needs_adjudication':reasons.append('submitted physical interpretation requires review')
        if any(r['status']!='pass' for r in reference_screen):reasons.append('reference physical interpretation requires review')
        if registration_errors:reasons.append('registration unresolved')
        if primary['assignment_ambiguous']:reasons.append('equally optimal phase assignments change abundance credit')
        lo=80*result['P']+20*primary['T_interval'][0];hi=80*result['P']+20*primary['T_interval'][1]
        result['score_interval']=[lo,hi]
        if registration_errors:
            result.update(score_100=None,score_quadratic_100=None,T=None,A=None,F_is_lower_bound=True,
                score_interval=[80*result['P'],80*result['P']+20])
            for key,detail in result['sensitivity'].items():
                loss,weight,_=key.split(':');weight=float(weight[1:])
                p=result['P'] if loss=='poisson' else result['P_quadratic']
                detail.update(score=None,interval=[weight*p,weight*p+100-weight])
        elif primary['assignment_ambiguous']:result.update(score_100=None,score_quadratic_100=None,T=None,A=None)
        if profile_error and eligible:
            result.update(score_100=None,score_quadratic_100=None,score_interval=None,score_status='verification_error',error=profile_error)
            for detail in result['sensitivity'].values():detail.update(score=None,interval=None)
            reasons.append('eligible prediction could not be evaluated')
        else:result['score_status']='needs_adjudication' if reasons else 'partial_submission' if partial or result['primary_profile_status']!='verified' else 'scored'
        if physical=='fail':result.update(score_100=0.,score_quadratic_100=0.,score_interval=[0.,0.],score_status='hard_physical_failure')
        result.update(adjudication_reasons=reasons,score_100_is_provisional=bool(reasons),
            scientific_score_100=result['score_100'] if not reasons else None,
            strict_matching_used_for_total=False,declared_fit_csv_used_for_scoring=False)
    except Exception as exc:
        result.update(score_status='verification_error',error=str(exc),traceback=traceback.format_exc(),score_100=None,
                      score_quadratic_100=None,scientific_score_100=None,score_interval=None)
    save_json(out/'score.json',result)
    return result
