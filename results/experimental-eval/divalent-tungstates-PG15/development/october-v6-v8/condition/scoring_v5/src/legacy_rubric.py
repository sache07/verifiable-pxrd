"""The approved 35/25/30/10 rubric, independent of the development cases."""
import math
from common import CONFIG

def profile_credit(reference_loss,submitted_loss):
    if not all(math.isfinite(x) and x>=0 for x in [reference_loss,submitted_loss]):
        raise ValueError('Profile losses must be finite and nonnegative')
    if submitted_loss==0:return 1.
    return min(1.,reference_loss/submitted_loss)

def composition_credit(reference_count,matched_pairs):
    if reference_count<1:raise ValueError('At least one reference phase is required')
    indices=[p['reference_index'] for p in matched_pairs]
    if len(set(indices))!=len(indices):raise ValueError('A reference phase was matched more than once')
    known=0.;unknown=[]
    for p in matched_pairs:
        error=p['max_site_occupancy_TV']
        if error is None:
            unknown.append(p['reference_index'])
        else:
            if not math.isfinite(error) or not -1e-10<=error<=1+1e-10:
                raise ValueError('Invalid occupancy error')
            known+=1-min(1.,max(0.,error))
    lower=known/reference_count;upper=(known+len(unknown))/reference_count
    return dict(value=lower if not unknown else None,lower=lower,upper=upper,undefined_reference_indices=unknown)

def total_score(framework_f1,mass_error,reference_count,pairs,reference_loss,submitted_loss,hard_failure=False):
    if not 0<=framework_f1<=1 or not -1e-10<=mass_error<=1+1e-10:
        raise ValueError('Metric outside unit interval')
    w=CONFIG['rubric'];composition=composition_credit(reference_count,pairs)
    components=dict(framework=w['framework_points']*framework_f1,
                    fractions=w['mass_points']*(1-min(1.,max(0.,mass_error))),
                    profile=w['profile_points']*profile_credit(reference_loss,submitted_loss) if submitted_loss is not None else 0.,
                    composition=w['composition_points']*composition['value'] if composition['value'] is not None else None)
    lower=sum(v for v in components.values() if v is not None)
    if composition['value'] is None:lower+=w['composition_points']*composition['lower']
    upper=lower+w['composition_points']*(composition['upper']-composition['lower'])
    raw=dict(component_points=components,score_100=lower if composition['value'] is not None else None,
             score_interval=[lower,upper],composition=composition)
    if hard_failure:
        return dict(component_points={k:0. for k in components},score_100=0.,score_interval=[0.,0.],
                    before_physical_gate=raw,composition=composition)
    return raw
