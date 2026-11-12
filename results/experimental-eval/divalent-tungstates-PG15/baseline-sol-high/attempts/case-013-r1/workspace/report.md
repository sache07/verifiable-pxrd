# Quantitative phase analysis

The crystalline model contains three phases. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Structure | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| PbWO4 | scheelite, *I*4_1/*a* | a = 5.46553, c = 12.06100 | 78.40 wt% |
| PbO | massicot, *Pbcm* | a = 5.89733, b = 5.49559, c = 4.75949 | 10.11 wt% |
| WO3 | monoclinic, *P*2_1/*n* | a = 7.30543, b = 7.54673, c = 7.70269, beta = 90.3555° | 11.49 wt% |

## Evidence

Scheelite PbWO4 accounts for the dominant line series at approximately 27.70, 33.06, 45.03, 47.28, 51.49, 55.54, 56.82, and 72.27° 2theta. Monoclinic WO3 is required by its diagnostic low-angle group near 23.39, 23.89, and 24.64°, with supporting lines near 33.52–34.83°. Orthorhombic PbO is supported by lines near 29.35, 38.09, 53.38, and 63.28°. These assignments are chemically consistent with PbWO4 formation from incompletely reacted PbO and WO3 at 500 °C.

Raspite PbWO4 and Pb3O4 were tested but rejected. Raspite overpredicts its strong 24.5° group when scaled to the 25.9° residual, while Pb3O4 gives only a marginal profile improvement, a poorly matching intensity distribution, and an implausibly distorted refined cell. No additional crystalline phase can therefore be assigned reliably.

## Refinement and uncertainty

The GSAS-II refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, Poisson counting weights (sigma = sqrt(counts)), a 15-term Chebyshev background, a common constrained pseudo-Voigt profile, phase scales, unit cells, and a common zero offset. Atomic coordinates and occupancies were held at reference-structure values. The final fit has Rwp = 16.05%, Rp = 11.55%, Rexp = 3.50%, and goodness of fit = 4.58.

GSAS-II covariance estimates correspond to 0.32, 0.19, and 0.30 percentage-point standard uncertainties for PbWO4, PbO, and WO3, respectively. They do not include model systematics. The raw profile contains a repeated unmatched satellite series (roughly constant sin(theta) ratio near 0.89 relative to stronger lines), compatible with an unmodeled shorter-wavelength/instrumental contribution but not uniquely attributable from the supplied metadata. Together with the absence of a calibrated instrument profile, this limits the fractions to semi-quantitative accuracy; a realistic uncertainty is several relative percent (about 2–3 absolute percentage points for the minor phases), not the smaller formal errors. The three structure types are well supported, but more precise fractions and any phase below roughly 1–2 wt% cannot be determined reliably from this dataset.
