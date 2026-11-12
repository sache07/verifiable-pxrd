"""Evaluate only phase pairs that can affect maximum credited agreement."""
import copy,time
import numpy as np
from scipy.optimize import linear_sum_assignment
from common import CONFIG
from structural_precision import score,evaluate
from structural_registration import cached_pair
from atomic_weighting import NAME as ATOMIC_WEIGHTING


def maximum(a):
    if not a.size:return 0.
    i,j=linear_sum_assignment(a,maximize=True);return float(a[i,j].sum())


def compare_inventory(refs,pred,target,fractions,invalid_fractions=(),physical_invalid=False,physical_review=False):
    start=time.monotonic();n,m=len(refs),len(pred)
    q=np.zeros((n,m));up=np.ones((n,m));features=[[None]*m for _ in refs]
    reports=[];failed=set();attempted=set();errors=[]
    row=dict(q=q.tolist(),features=features,reference_fractions=list(target),submitted_fractions=list(fractions),
             invalid_fractions=list(invalid_fractions),physical_invalid=physical_invalid,physical_review=physical_review,
             atomic_weighting=ATOMIC_WEIGHTING)
    if physical_invalid:
        row['quality_upper']=up.tolist();return score(row,CONFIG['structural_precision']),row,dict(pairs=[],errors=[])
    while True:
        row.update(q=q.tolist(),quality_upper=up.tolist(),features=features)
        result=score(row,CONFIG['structural_precision'])
        if result['score'] is not None:break
        remaining=CONFIG['structural_registration']['inventory_deadline_seconds']-(time.monotonic()-start)
        if remaining<=0:
            errors.append(dict(error='Inventory registration time budget reached'));break
        optimistic=copy.deepcopy(row);optimistic['q']=up.tolist()
        for i,j in np.ndindex(q.shape):
            if up[i,j]>q[i,j]+1e-12:
                optimistic['features'][i][j]=dict(cell_error=0.,populations=[dict(coefficient=1.,distance_A=0.)])
        hi=np.asarray(evaluate(optimistic,CONFIG['structural_precision'])['pair_credit_matrix'])
        best=result['nominal_score'];possible=[]
        for i,j in np.ndindex(q.shape):
            if (i,j) in attempted:continue
            remainder=np.delete(np.delete(hi,i,axis=0),j,axis=1)
            bound=float(hi[i,j]+maximum(remainder))
            if bound<=best+1e-7:continue
            a=refs[i].composition.fractional_composition.get_el_amt_dict()
            b=pred[j].composition.fractional_composition.get_el_amt_dict()
            similarity=sum(min(a.get(e,0.),b.get(e,0.)) for e in set(a)|set(b))
            possible.append((similarity,bound,-i,-j))
        if not possible:break
        _,_,ni,nj=max(possible);i,j=-ni,-nj;attempted.add((i,j))
        try:
            detail,path=cached_pair(refs[i],pred[j],min(remaining,CONFIG['structural_registration']['pair_deadline_seconds']))
            q[i,j]=detail['q'];features[i][j]=detail['feature']
            up[i,j]=detail['q_upper'] if detail['status']=='incomplete_search' else detail['q']
            reports.append(dict(reference=i,submitted=j,cache=path,**detail))
            if detail['status']=='incomplete_search':errors.append(dict(reference=i,submitted=j,error=detail['error']))
        except Exception as exc:
            errors.append(dict(reference=i,submitted=j,error=repr(exc)))
    row.update(q=q.tolist(),quality_upper=up.tolist(),features=features)
    result=score(row,CONFIG['structural_precision'])
    return result,row,dict(pairs=reports,errors=errors,attempted_pairs=len(attempted),total_pairs=n*m,
                          seconds=time.monotonic()-start,search='Finite deterministic registration; explicit bounds for unfinished evaluator work.')
