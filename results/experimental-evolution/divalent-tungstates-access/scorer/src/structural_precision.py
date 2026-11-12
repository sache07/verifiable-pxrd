"""Structural precision utilities. No diffraction, hidden-parameter substitution,
or observed-data refinement enters the score. Phase correspondences are inputs
from the separately audited structural registration stage.

The structural term credits inventory, abundance, scattering-weighted site
agreement and fraction accuracy. Cell error is reported but, with cell_cap 0,
earns no separate credit: the profile term already measures it.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from atomic_weighting import NAME as ATOMIC_WEIGHTING

DEFAULT = dict(cell_scale=0.001, position_scale_A=0.03,
               fraction_scale=0.05, cell_cap=0.0, position_cap=0.50,
               fraction_cap=0.25, presence_scale=0.05, inventory_weight=0.50,
               family='compound', atomic_weighting=ATOMIC_WEIGHTING,
               assignment='maximum_total_credited_agreement')

def site_accuracy(feature, scale):
    if feature is None:
        return 0.0
    if any(not np.isfinite(p[k]) or p[k]<0 for p in feature['populations']
           for k in ['coefficient','distance_A']):
        raise ValueError('Invalid transported population or distance')
    if sum(p['coefficient'] for p in feature['populations'])>1+1e-7:
        raise ValueError('Transport exceeds normalized occupied populations')
    return float(np.clip(sum(p['coefficient'] / (1 + (p['distance_A']/scale)**2)
                     for p in feature['populations']),0,1))

def evaluate(row, config=None, details=True):
    cfg = dict(DEFAULT, **(config or {}))
    if cfg['atomic_weighting'] != ATOMIC_WEIGHTING:
        raise ValueError('Unsupported atomic weighting; use the archived scorer for legacy features')
    if row.get('atomic_weighting', ATOMIC_WEIGHTING) != ATOMIC_WEIGHTING:
        raise ValueError('Prepared features use a different atomic weighting')
    q = np.asarray(row['q'], dtype=float)
    w = np.asarray(row['reference_fractions'], dtype=float)
    supplied = list(row['submitted_fractions']) + list(row.get('invalid_fractions', []))
    if q.shape != (len(w), len(row['submitted_fractions'])):
        raise ValueError('Quality matrix dimensions do not match phase lists')
    if not np.all(np.isfinite(q)) or np.any(q < -1e-9) or np.any(q>1+1e-9):
        raise ValueError('Invalid coarse structural quality')
    if len(w)==0 or not np.all(np.isfinite(w)) or np.any(w<=0) or abs(sum(w)-1)>1e-6:
        raise ValueError('Reference fractions must be positive and total one')
    if any(v is not None and (not np.isfinite(v) or v<0) for v in supplied):
        raise ValueError('Negative/nonfinite reported fraction')
    if any(not np.isfinite(cfg[k]) or cfg[k]<=0 for k in
           ('cell_scale','position_scale_A','fraction_scale','presence_scale')):
        raise ValueError('Error scales must be positive')
    if any(not 0<=cfg[k]<=1 for k in
           ('cell_cap','position_cap','fraction_cap','inventory_weight')):
        raise ValueError('Weights and caps must lie in [0,1]')
    if len(supplied)==0:
        return dict(score=0., recovery=0., abundance=0., base_score=0.,
                    cell_accuracy=None, site_accuracy=None, fraction_accuracy=None,
                    assignment=[], status='empty_submission')
    mat = np.zeros((len(w), len(supplied)))
    mat[:, :q.shape[1]] = np.clip(q, 0, 1)
    v = np.array([0. if z is None else z for z in supplied])
    mass_denom = max(1., float(v.sum()))
    gw = -np.expm1(-w/cfg['presence_scale'])
    gv = np.array([1. if z is None else -np.expm1(-z/cfg['presence_scale'])
                   for z in supplied])
    denom = float(gw.sum()+gv.sum())
    im = 2*mat*np.minimum(gw[:,None],gv[None,:])/denom
    am = mat*np.minimum(w[:,None],v[None,:])/mass_denom
    iw=cfg['inventory_weight']; base=iw*im+(1-iw)*am
    # Pairing and grading use the same objective. The maximum of the continuous
    # per-assignment totals stays continuous when the winning assignment changes.
    # This is credited agreement, not a claim to identify phases uniquely.
    if cfg['assignment'] != 'maximum_total_credited_agreement':
        raise ValueError('Unsupported phase-assignment objective')
    edges={}; utility=np.zeros_like(base)
    for i,j in np.ndindex(base.shape):
        b=float(base[i,j]); feature=row['features'][i][j] if j<q.shape[1] else None
        if feature is not None and (not np.isfinite(feature['cell_error']) or feature['cell_error']<0):
            raise ValueError('Invalid registered cell error')
        cell=0. if feature is None else 1/(1+(feature['cell_error']/cfg['cell_scale'])**2)
        site=site_accuracy(feature,cfg['position_scale_A'])
        if feature is not None and feature.get('atomic_weighting',ATOMIC_WEIGHTING)!=ATOMIC_WEIGHTING:
            raise ValueError('Prepared atom transport uses a different weighting')
        overlap=0. if feature is None else sum(p['coefficient'] for p in feature['populations'])
        fraction=0. if supplied[j] is None else 1/(1+((w[i]-v[j])/cfg['fraction_scale'])**2)
        losses=np.array([cfg['cell_cap']*(1-cell),cfg['position_cap']*(1-site),cfg['fraction_cap']*(1-fraction)])
        fam=cfg['family']
        if fam=='broad': mult=1.
        elif fam=='compound': mult=float(np.prod(1-losses))
        elif fam=='additive': mult=float(1-(losses*np.array([.4,.5,.6])).sum())
        elif fam=='exponential': mult=float(np.exp(-losses.sum()))
        elif fam=='pure_product': mult=float(cell*site*fraction)
        elif fam=='clipped': mult=float(max(0.,1-losses.sum()))
        else: raise ValueError('Unknown score family')
        utility[i,j]=b*mult
        edges[i,j]=dict(reference=int(i),submitted=int(j),
            coarse_quality=float(mat[i,j]),reference_fraction=float(w[i]),
            submitted_fraction=supplied[j],base_credit=100*b,
            cell_error=None if feature is None else feature['cell_error'],
            cell_accuracy=100*cell,site_accuracy=100*site,
            composition_occupancy_overlap=100*overlap,
            position_accuracy_on_matched_population=100*site/overlap if overlap else None,
            fraction_accuracy=100*fraction,precision_multiplier=mult,
            score_credit=100*b*mult)
    if '_assignment' in row:
        ii=np.array([a[0]for a in row['_assignment']],int)
        jj=np.array([a[1]for a in row['_assignment']],int)
    else:
        ii,jj=linear_sum_assignment(utility,maximize=True)
    records=[edges[i,j] for i,j in zip(ii,jj)] if details else []
    total=float(utility[ii,jj].sum());weight=float(base[ii,jj].sum())
    weighted=sum((base[i,j]*np.array([edges[i,j][k]/100 for k in
                 ['cell_accuracy','site_accuracy','fraction_accuracy']]) for i,j in zip(ii,jj)),np.zeros(3))
    avg=weighted/weight if weight else [None]*3
    flags=[]
    if any(x is None for x in supplied):flags.append('unknown_fractions')
    if v.sum()>1+1e-8:flags.append('excess_claimed_mass')
    if row.get('physical_invalid'):flags.append('physical_invalid')
    if row.get('physical_review'):flags.append('physical_review')
    return dict(score=0. if row.get('physical_invalid') else 100*total,
                raw_score=100*total, recovery=100*float(im[ii,jj].sum()),
                abundance=100*float(am[ii,jj].sum()),base_score=100*weight,
                cell_accuracy=None if avg[0] is None else 100*avg[0],
                site_accuracy=None if avg[1] is None else 100*avg[1],
                fraction_accuracy=None if avg[2] is None else 100*avg[2],
                assignment=records, pair_credit_matrix=(100*utility).tolist(),
                phase_assignment_rule=cfg['assignment'],
                status=';'.join(flags) if flags else 'scored')


def score(row, config=None):
    """Bounds over incomplete registrations; no factorial assignment search.

    Each unknown edge receives its own admissible coarse-quality upper bound
    and perfect fine precision. Maximizing this matrix gives an upper bound on
    the total even if its winning assignment differs from the lower-bound one.
    """
    import copy
    nominal=evaluate(row,config)
    q=np.asarray(row['q'],float)
    upper=np.asarray(row.get('quality_upper',row['q']),float)
    if upper.shape!=q.shape or np.any(~np.isfinite(upper)) or np.any(upper<q-1e-8) or np.any(upper>1+1e-8):
        raise ValueError('Invalid quality upper bounds')
    optimistic=copy.deepcopy(row);optimistic['q']=upper.tolist()
    for i,j in np.ndindex(q.shape):
        if upper[i,j]>q[i,j]+1e-12:
            optimistic['features'][i][j]=dict(cell_error=0.,populations=[dict(coefficient=1.,distance_A=0.)])
    high=evaluate(optimistic,config)['score']
    low=nominal['score']
    if high<low-1e-7:raise ValueError('Structural score bounds reversed')
    nominal.update(score_interval=[low,max(low,high)],nominal_score=low)
    if high-low>1e-6:
        nominal.update(score=None,status='registration_review_required')
    # An exact objective tie changes attribution, not the scalar. Preserve the
    # selected correspondence and flag equivalent optimal explanations.
    utility=np.asarray(nominal.get('pair_credit_matrix',[]),float)
    if utility.ndim==2 and utility.size:
        best=float(sum(x['score_credit'] for x in nominal['assignment']))
        tied=[]
        selected={(x['reference'],x['submitted']) for x in nominal['assignment']}
        for i,j in np.ndindex(utility.shape):
            if (i,j) in selected or utility[i,j]<=0:continue
            remainder=np.delete(np.delete(utility,i,axis=0),j,axis=1)
            a,b=linear_sum_assignment(remainder,maximize=True)
            alternative=float(utility[i,j]+remainder[a,b].sum())
            if abs(alternative-best)<=1e-8:tied.append([i,j])
        nominal['assignment_ambiguous']=bool(tied)
        nominal['equally_optimal_alternative_edges']=tied
    return nominal
