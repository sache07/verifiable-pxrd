"""Frozen-model experimental diagnostics. No refinement, truth fit or synthetic score."""
import argparse
import csv
import json
from pathlib import Path
import sys
import warnings
import numpy as np

R=Path(__file__).resolve().parent
BENCH=R.parent
sys.path.insert(0,str(R/'scoring_v5/src'))
from common import sha,save_json,load_structure,code_hashes
from structure_metrics import parse_submission,matcher,occupancy_neutral
from replay import replay_prediction
from pymatgen.core import Element
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

def rwp(observed,predicted):
    w=1/np.maximum(observed,1.)
    return float(100*np.sqrt(np.sum(w*(observed-predicted)**2)/np.sum(w*observed**2)))

def export_curve(work,x,y):
    with (work/'fit.csv').open() as f:
        reader=csv.DictReader(f);names=reader.fieldnames;records=list(reader)
    cn=next(n for n in names if ('calc' in n.lower() or n.lower() in ['yc','yfit','fit','model']) and 'background' not in n.lower())
    xx=np.asarray([float(row[names[0]]) for row in records])
    cc=np.asarray([float(row[cn]) if row[cn].strip() else np.nan for row in records])
    good=np.flatnonzero(np.isfinite(cc))
    if not len(good) or not np.array_equal(good,np.arange(good[0],good[-1]+1)):
        raise ValueError('Missing interior calculated intensities')
    bad=np.flatnonzero(~np.isfinite(cc))
    if len(bad) and any(records[i].get('used_in_refinement','').lower()!='false' for i in bad):
        raise ValueError('Blank curve rows not declared inactive')
    xx,cc=xx[good],cc[good]
    if not np.isfinite(xx).all() or not (np.diff(xx)>0).all():raise ValueError('Invalid curve grid')
    mask=(x>=10)&(x<=100)&(x>=xx[0])&(x<=xx[-1])
    if mask.sum()<100:raise ValueError('Insufficient profile coverage')
    calc=np.interp(x[mask],xx,cc)
    result={'export_rwp':rwp(y[mask],calc),'export_coverage':float(mask.sum()/((x>=10)&(x<=100)).sum()),
            'export_range':[float(x[mask][0]),float(x[mask][-1])], 'export_points':int(mask.sum())}
    on=next((n for n in names if 'observ' in n.lower() or n.lower() in ['yobs','y_obs','yo']),None)
    if on:
        obs=np.asarray([float(records[i][on]) for i in good])
        result['export_observation_max_error']=float(np.max(np.abs(np.interp(x[mask],xx,obs)-y[mask])))
    return result,(xx,cc)

def evaluate(root,job,output_dir=None,grid_tolerance=1e-7):
    a=root/'attempts'/job['id'];work=a/'workspace'
    launch=json.loads((a/'run/launch.json').read_text()) if (a/'run/launch.json').exists() else json.loads((a/'dispatch_error.json').read_text())
    out=Path(output_dir) if output_dir is not None else root/'analysis/attempts'/job['id']
    out.mkdir(parents=True,exist_ok=True)
    sources=[a/'job.json',a/'prompt.txt',a/'run/launch.json',work/'result.json',work/'report.md',work/'fit.csv',work/'final.gpx',work/'inputs/pattern.csv',work/'inputs/metadata.json']
    sources += list(work.rglob('*.cif'))
    before={str(p):sha(p) for p in sources if p.is_file()}
    evaluator_hashes={**code_hashes(), 'evaluate_attempt.py':sha(__file__)}
    cached=out/'result.json'
    if cached.exists():
        prior=json.loads(cached.read_text())
        if prior.get('source_hashes')==before and prior.get('evaluator_hashes')==evaluator_hashes:return prior
    row={'id':job['id'],'condition':job['policy'],'case':job['case_id'],'replicate':job['replicate'],
         'workspace':str(work),'execution_status':launch['status'],'minutes':launch.get('elapsed_seconds',0)/60,
         'inputs_unchanged':launch.get('inputs_unchanged'),'errors':[],'source_hashes':before,
         'evaluator_hashes':evaluator_hashes}
    x,y=np.loadtxt(work/'inputs/pattern.csv',delimiter=',',skiprows=1).T
    standard=(x>=10)&(x<=100)
    interior=(x>=10.1)&(x<=99.9)
    reference=json.loads((BENCH/'references'/f"{job['case_id']}-reference-data.json").read_text())['plot_data']
    cm=standard&(x>=min(reference['x']))&(x<=max(reference['x']))
    row['ceder_rwp']=rwp(y[cm],np.interp(x[cm],reference['x'],reference['y_calc']))
    row['ceder_coverage']=float(cm.sum()/standard.sum())
    row['ceder_interior_rwp']=rwp(y[interior],np.interp(x[interior],reference['x'],reference['y_calc']))
    exported=None
    try:
        metrics,exported=export_curve(work,x,y);row.update(metrics)
        xx,cc=exported
        if xx[0]<=x[interior][0] and xx[-1]>=x[interior][-1]: row['export_interior_rwp']=rwp(y[interior],np.interp(x[interior],xx,cc))
        lo,hi=metrics['export_range'];mask=cm&(x>=lo)&(x<=hi)
        row['ceder_rwp_on_export_range']=rwp(y[mask],np.interp(x[mask],reference['x'],reference['y_calc']))
    except Exception as exc:row['errors'].append('fit.csv: '+repr(exc))
    try:
        data,phases,notes=parse_submission(work,[e.symbol for e in Element])
        row['parsing']=data['_submission_parsing'];row['parsing_notes']=notes
        row['reported_statistics']=data.get('fit_statistics');row['phases']=[]
        targets={n:load_structure(BENCH/'references/diagnostic_structures'/f'{n}_canonical.cif') for n in ['Pb2WO5','Pb3WO6','Sr2WO5']}
        for ph in phases:
            st=ph['structure'];p={'formula':st.composition.reduced_formula,'composition':st.composition.get_el_amt_dict(),
              'weight_fraction':ph['fraction'],'cif':str(ph['path']),'physical_screen':ph['physical'],
              'reported':ph['reported'],'target_matches':{}}
            try:p['space_group']=SpacegroupAnalyzer(st,symprec=.1).get_space_group_symbol()
            except Exception as exc:p['space_group_error']=str(exc)
            for n,target in targets.items():
                if set(target.composition.get_el_amt_dict())==set(p['composition']):
                    p['target_matches'][n]=bool(matcher().fit(occupancy_neutral(target),occupancy_neutral(st),symmetric=True))
            row['phases'].append(p)
        eligible=bool(phases) and not row['parsing']['invalid_model_records'] and row['parsing']['quantification_complete']
        try:
            _,_,prediction,meta=replay_prediction({'workspace':str(work),'case_path':str(root/'cases'/job['case_id']), 'grid_tolerance_degrees':grid_tolerance},phases,data,out,eligible)
            row['replay']=meta
            if prediction is not None:
                pred=prediction['calculated']
                row['replay_rwp_full']=prediction['rwp_percent']
                row['replay_rwp']=rwp(y[standard],pred[standard])
                row['replay_interior_rwp']=rwp(y[interior],pred[interior])
                np.savez(out/'curves.npz',x=x,observed=y,calculated=pred)
                if exported is not None:
                    xx,cc=exported;mask=standard&(x>=xx[0])&(x<=xx[-1])
                    row['replay_rwp_on_export_range']=rwp(y[mask],pred[mask])
                    row['export_replay_rms_count_difference']=float(np.sqrt(np.mean((np.interp(x[mask],xx,cc)-pred[mask])**2)))
            else:row['errors'].append('Replay unavailable: '+meta.get('status','unknown'))
        except Exception as exc:row['replay']={'status':'evaluator_error','error':repr(exc)};row['errors'].append('Replay evaluator: '+repr(exc))
    except Exception as exc:row['errors'].append('Atomic submission: '+repr(exc))
    row['protected_sources_unchanged']=all(Path(p).is_file() and sha(p)==h for p,h in before.items())
    assert row['protected_sources_unchanged'],'Assessment modified a protected source'
    save_json(cached,row)
    return row

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('job');args=p.parse_args()
    root=Path(args.root);job=next(j for j in json.loads((root/'jobs/experimental45.json').read_text()) if j['id']==args.job)
    with warnings.catch_warnings():warnings.simplefilter('ignore');result=evaluate(root,job)
    print(json.dumps({'id':result['id'],'replay_rwp':result.get('replay_rwp'),'errors':result['errors']}))
