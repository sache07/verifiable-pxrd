"""80 prediction + 10 soft structural inventory + 10 attributed abundance."""
import math


def score_components(P, F, A, P_quadratic=None, hard_failure=False, profile_weight=80):
    for name, value in [('P',P),('F',F),('A',A)]:
        if not math.isfinite(value) or not -1e-9 <= value <= 1+1e-9:
            raise ValueError(name+' outside unit interval')
    P,F,A = [min(1.,max(0.,x)) for x in (P,F,A)]
    T=(F+A)/2
    points={'profile':profile_weight*P, 'structure':(100-profile_weight)*F/2,
            'abundance':(100-profile_weight)*A/2}
    out=dict(P=P,T=T,F=F,A=A,component_points=points,score_100=sum(points.values()),
             score_quadratic_100=None if P_quadratic is None else profile_weight*P_quadratic+(100-profile_weight)*T)
    if hard_failure:
        out=dict(out,before_physical_gate=out.copy(),score_100=0.,score_quadratic_100=0.,
                 component_points={k:0. for k in points})
    return out
