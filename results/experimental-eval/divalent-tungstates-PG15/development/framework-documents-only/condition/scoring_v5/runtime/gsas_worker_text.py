"""Instrument-file rendering without importing the GSAS-only environment."""
def instrument_text(p):
    return (
        '# Synthetic laboratory Cu Kalpha template; GSAS-II convention\n'
        'Type:PXC;Bank:1\n'
        f"Lam1:{p['wavelength_ka1_A']};Lam2:{p['wavelength_ka2_A']};I(L2)/I(L1):{p['ka2_ka1_ratio']}\n"
        f"Zero:{p.get('zero_deg',0.0)};Polariz.:{p['polarization']};Azimuth:0.0\n"
        f"U:{p['U']};V:{p['V']};W:{p['W']};X:{p['X']};Y:0.0;Z:0.0;SH/L:{p['SH_L']}\n"
    )
