"""Exact assignment pruning using composition-only upper bounds on atom credit."""
import numpy as np
from scipy.optimize import linear_sum_assignment
from soft_matching import cached_pair,SCALES


def elemental_upper_bound(a,b):
    """Maximal shared occupied population over *any* positive cell multiplier.

    On intervals between a_e/b_e, numerator and denominator are linear, so the
    ratio is monotone or constant. Its maximum occurs at one of these breaks.
    Dropping geometry and lattice restrictions can only increase q.
    """
    a=a.composition.get_el_amt_dict() if hasattr(a,'composition') else a
    b=b.composition.get_el_amt_dict() if hasattr(b,'composition') else b
    shared=set(a)&set(b)
    if not shared:return 0.
    breaks=[a[e]/b[e] for e in shared if a[e]>0 and b[e]>0]
    return min(1.,max(2*sum(min(a.get(e,0.),r*b.get(e,0.)) for e in shared)/(sum(a.values())+r*sum(b.values())) for r in breaks))


def maximum(matrix):
    if not matrix.size:return 0.
    i,j=linear_sum_assignment(matrix,maximize=True)
    return float(matrix[i,j].sum())


def forced_bound(matrix,i,j):
    return float(matrix[i,j]+maximum(np.delete(np.delete(matrix,i,axis=0),j,axis=1)))


def compare_inventory(refs,pred,evaluate=cached_pair):
    n,m=len(refs),len(pred)
    upper=np.array([[elemental_upper_bound(a,b) for b in pred] for a in refs],float).reshape(n,m)
    done=upper<=0
    qualities={str(s):np.zeros((n,m)) for s in SCALES}
    reports=[];errors=[];failed=set()
    while True:
        possible={}
        for scale,lo in qualities.items():
            hi=np.where(done,lo,upper);opt=maximum(lo)
            for i,j in zip(*np.where(~done)):
                bound=forced_bound(hi,i,j)
                if bound>=opt-1e-10:
                    possible[i,j]=max(possible.get((i,j),-1.),bound-opt)
        available=[p for p in possible if p not in failed]
        if not available:break
        # Selection uses only structural/chemical bounds, never mass fractions.
        i,j=max(available,key=lambda ij:(possible[ij],upper[ij],-ij[0],-ij[1]))
        try:
            detail,path=evaluate(refs[i],pred[j])
            for s in SCALES:
                q=detail['quality_by_scale'][str(s)]['q']
                if q>upper[i,j]+1e-8:raise AssertionError('Atom-transport credit exceeded its chemical upper bound')
                qualities[str(s)][i,j]=q
            done[i,j]=True
            reports.append(dict(reference_index=int(i),submitted_index=int(j),cache=path,
                q_by_scale={str(s):float(qualities[str(s)][i,j]) for s in SCALES},
                reference_composition=refs[i].composition.get_el_amt_dict(),submitted_composition=pred[j].composition.get_el_amt_dict()))
        except Exception as exc:
            failed.add((i,j));errors.append(dict(reference_index=int(i),submitted_index=int(j),error=str(exc)))
    unresolved=[e for e in errors if (e['reference_index'],e['submitted_index']) in possible]
    pruned=[]
    for i,j in zip(*np.where(~done)):
        if (i,j) in possible:continue
        pruned.append(dict(reference_index=int(i),submitted_index=int(j),q_upper=float(upper[i,j]),
                          reason='Cannot participate in an optimal assignment at any audited geometric scale'))
    return qualities,reports,unresolved,dict(pruned_edges=pruned,all_evaluation_errors=errors,
        evaluated_pairs=int(done.sum()),total_pairs=n*m,assignment_certified=not unresolved,
        unknown_edge_upper_bounds=upper.tolist(),uncomputed_mask=(~done).tolist())
