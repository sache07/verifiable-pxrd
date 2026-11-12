"""Instrument-file rendering without importing the GSAS-only environment."""


def instrument_text(p):
    if p.get('wavelength_ka2_A') is None:
        spectrum = f"Lam:{p['wavelength_ka1_A']}\n"  # one wavelength (monochromated or synchrotron)
    else:
        spectrum = f"Lam1:{p['wavelength_ka1_A']};Lam2:{p['wavelength_ka2_A']};I(L2)/I(L1):{p['ka2_ka1_ratio']}\n"
    return (
        '# Synthetic laboratory instrument; GSAS-II convention\n'
        'Type:PXC;Bank:1\n'
        + spectrum +
        f"Zero:{p.get('zero_deg',0.0)};Polariz.:{p['polarization']};Azimuth:0.0\n"
        f"U:{p['U']};V:{p['V']};W:{p['W']};X:{p['X']};Y:0.0;Z:0.0;SH/L:{p['SH_L']}\n"
    )
