"""Numerical serialization precision, independent of experimental uncertainty.

An uncertainty in parentheses does not enlarge the permitted rounding interval.
Bare integers/rational constants do not imply a half-unit error bar.
"""
from decimal import Decimal, InvalidOperation
import re
import numpy as np


def half_last_digit(token):
    text=re.sub(r'\(\d+\)', '', str(token).strip())
    if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',text):
        return 0.
    if '.' not in text and 'e' not in text.lower():return 0.
    try:
        value=Decimal(text)
        step=float(Decimal('0.5').scaleb(value.as_tuple().exponent)) if value.is_finite() else 0.
        return step if np.isfinite(step) else 0.
    except ArithmeticError:return 0.


def tensor_bound(transform, uncertainty):
    """Conservative component-wise propagation through A U A-transpose."""
    a=np.abs(np.asarray(transform,float))
    return a@np.asarray(uncertainty,float)@a.T


def occupancy_tolerance(a,b,element,floor):
    return max(floor,a.properties.get('occupancy_rounding',{}).get(element,0.)+
                     b.properties.get('occupancy_rounding',{}).get(element,0.))+1e-12


def adps_agree(native,submitted,floor,occupancy_floor):
    aa=native.properties.get('declared_adps',[])
    bb=submitted.properties.get('declared_adps',[])
    ea=native.properties.get('adp_rounding_A2',[np.zeros((3,3)).tolist() for _ in aa])
    eb=submitted.properties.get('adp_rounding_A2',[np.zeros((3,3)).tolist() for _ in bb])
    for k,(element,occupancy,tensor) in enumerate(bb):
        available=0.
        for j,(e,pop,m) in enumerate(aa):
            allowance=np.maximum(floor,np.asarray(ea[j])+np.asarray(eb[k]))+1e-12
            if e==element and np.all(np.abs(np.asarray(m)-tensor)<=allowance):available+=pop
        if available+occupancy_tolerance(native,submitted,element,occupancy_floor)<occupancy:return False
    return True


def position_bound(site):
    return np.asarray(site.properties.get('position_rounding_A',[0.,0.,0.]),float)


def cell_tolerances(a,b,settings):
    def bounds(st):
        props=st.properties
        steps=np.asarray(props.get('cell_rounding',[0.]*6))
        values=np.asarray(props.get('cell_declared',list(st.lattice.abc)+list(st.lattice.angles)))
        return float(max(steps[:3]/values[:3])),float(max(steps[3:]))
    ar,aa=bounds(a);br,ba=bounds(b)
    return max(settings['lattice_relative_tolerance'],ar+br),max(settings['angle_tolerance_deg'],aa+ba)
