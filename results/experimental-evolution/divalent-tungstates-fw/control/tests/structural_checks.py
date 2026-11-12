"""Analytic and raw-structure checks; run separately from controller imports."""
from pathlib import Path
import sys,json,time,copy,tempfile
import numpy as np
from pymatgen.core import Structure,Lattice
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scorer/src'))
from structural_precision import score,evaluate
from structural_registration import pair_quality,Objective
from atomic_weighting import exact_population_feature
from structure_metrics import parse_submission
checks=[]
def check(name,ok,**detail):
    checks.append(dict(name=name,passed=bool(ok),**detail));print(json.dumps(checks[-1]),flush=True)
f=exact_population_feature({'Ca':1,'W':1,'O':4})
def row(w,v,q=None):
    n,m=len(w),len(v)
    return dict(reference_fractions=w,submitted_fractions=v,q=q if q is not None else np.eye(n,m).tolist(),features=[[copy.deepcopy(f)for j in range(m)]for i in range(n)])
values=[]
for epsilon in [-1e-7,0,1e-7]:
    q=[[.9+epsilon,.9],[.9,.9]]
    r=row([.9,.1],[.9,.1],q)
    r['features']=[[dict(cell_error=0.,populations=[dict(coefficient=v,distance_A=0.)])for v in rr]for rr in q]
    values.append(score(r)['score'])
check('assignment_switch_continuity',max(values)-min(values)<.0001,scores=values)
r=row([.5,.5],[.5,.5],[[1,1],[1,1]])
z=score(r);check('equal_objective_tie_reported',z['assignment_ambiguous']and abs(z['score']-100)<1e-9)
for n in [1,2,16]:
    r=row([1/n]*n,[1/n]*n);s=score(r)
    check(f'exact_{n}_phases',abs(s['score']-100)<1e-9)
r=row([.6,.4],[.6]);check('missing_phase_not_renormalized',0<score(r)['score']<80,value=score(r)['score'])
r=row([1.],[1.,.2],[[1,0]]);check('false_phase_penalty',score(r)['score']<100,value=score(r)['score'])
r=row([1.],[None]);check('unknown_fraction_partial_credit',0<score(r)['score']<50,value=score(r)['score'])
r=row([1.],[.6]);check('missing_mass_partial_credit',0<score(r)['score']<70,value=score(r)['score'])
r=row([1.],[1.]);r['physical_invalid']=True;check('hard_physical_failure_zero',score(r)['score']==0)
r=row([1.],[1.],[[0.]]);r['features']=[[None]];r['quality_upper']=[[1.]]
z=score(r);check('unknown_registration_bounds',z['score']is None and z['score_interval']==[0.,100.])
scores=[]
for v in [0,.0002,.0005,.001,.002,.005]:
    r=row([1.],[1.]);r['features'][0][0]['cell_error']=v;scores.append(score(r)['score'])
check('cell_error_reported_not_credited',max(scores)-min(scores)<1e-9,scores=scores)
scores=[]
for v in [0,.005,.01,.03,.06,.1]:
    r=row([1.],[1.])
    for p in r['features'][0][0]['populations']:p['distance_A']=v
    scores.append(score(r)['score'])
check('distance_A_smooth_monotone',all(a>b for a,b in zip(scores,scores[1:])),scores=scores)
# Scattering weighting: a displaced tungsten costs more than a displaced oxygen, and
# displacing all four oxygens together costs less than the one tungsten.
def displaced(element):
    r=row([1.],[1.]);r['features'][0][0]=exact_population_feature({'Ca':1,'W':1,'O':4},distances={element:.03});return score(r)['score']
check('scattering_weighted_sites',displaced('W')<displaced('O')<100,W=displaced('W'),O=displaced('O'))
base=Structure(Lattice.from_parameters(7.1,7.7,8.3,88,97,103),['Ca','W','O','O','O','O'],
               [[.03,.12,.22],[.42,.52,.61],[.15,.76,.31],[.65,.21,.87],[.72,.73,.19],[.24,.31,.46]])
def runpair(name,b,expected=None):
    z=pair_quality(base,b);ok=z['status']=='registered'
    if expected is not None:ok=ok and abs(z['unit_credit']-expected)<1e-7
    gap=None if z['feature']is None else z['feature']['transport_log_duality_gap']
    check(name,ok,unit=z['unit_credit'],q=z['q'],seconds=z['seconds'],gap=gap,status=z['status'])
    return z
runpair('exact_raw',base,1)
b=Structure.from_sites(list(base)[::-1]);runpair('atom_order',b,1)
b=base.copy();b.translate_sites(range(len(b)),[.314,.228,.491],frac_coords=True,to_unit_cell=True);runpair('origin_shift',b,1)
b=base.copy();b.make_supercell([[1,1,0],[0,1,0],[0,0,1]]);runpair('equivalent_cell_setting',b,1)
b=base.copy();b.make_supercell([2,1,1]);runpair('supercell',b,1)
b=base.copy();sp=b[0];b.replace(0,{'Ca':.4});b.append({'Ca':.6},sp.frac_coords);runpair('split_occupancy',b,1)
b=base.copy();b.replace(0,{'Ca':.95,'Sr':.05});s=runpair('small_substitution',b);check('substitution_proportional_credit',.7<s['unit_credit']<1)
b=base.copy();b.remove_sites([5]);s=runpair('missing_atom',b);check('missing_atom_partial_credit',.5<s['unit_credit']<1)
b=base.copy();b.translate_sites([2],[.035,0,0],frac_coords=False);a=runpair('one_atom_displaced',b)
z=pair_quality(b,base);check('direction_symmetry',abs(a['unit_credit']-z['unit_credit'])<1e-6,forward=a['unit_credit'],reverse=z['unit_credit'])
# Parser duplicate collapsing should preserve total absolute abundance.
with tempfile.TemporaryDirectory()as d:
    w=Path(d);base.to(filename=w/'a.cif');b=base.copy();b.make_supercell([2,1,1]);b.to(filename=w/'b.cif')
    (w/'result.json').write_text(json.dumps({'phases':[{'cif':'a.cif','weight_fraction':.4},{'cif':'b.cif','weight_fraction':.6}]}))
    try:
        data,rs,notes=parse_submission(w,['Ca','W','O']);check('duplicate_parser',len(rs)==1 and abs(rs[0]['fraction']-1)<1e-9,rows=len(rs),notes=notes)
    except Exception as exc:check('duplicate_parser',False,error=repr(exc))
path=R/'control/validation/results/structural_checks.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(checks,indent=2)+'\n')
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
