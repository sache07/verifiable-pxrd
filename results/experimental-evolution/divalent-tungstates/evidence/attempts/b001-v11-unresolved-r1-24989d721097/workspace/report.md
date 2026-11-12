# Crystalline phase analysis

The pattern is described by three crystalline phases. Fractions are normalized over those phases only.

| Phase | Space group | Weight fraction |
|---|---:|---:|
| CaWO4 (scheelite) | I 41/a | 77.717% |
| WO3 | P 21/n (No. 14) | 12.193% |
| Ca3WO6 | P 21/n (No. 14) | 10.090% |

The final full-range GSAS-II replay converged at Rwp = 2.6119%, Rp = 2.0438%, and goodness of fit = 1.1652 (8301 points, 40 variables; final maximum shift/e.s.d. = 0.0035). The formal GSAS-II fraction e.s.d.'s are 0.057, 0.034, and 0.049 weight-percentage points, respectively, but these do not include model-selection and specimen-systematic uncertainty.

## Evidence and model selection

The dominant scheelite CaWO4 model indexes the major families across the full angular range. Monoclinic WO3 accounts for the characteristic clustered reflections near 23–25 degrees and their higher-angle families. After fitting those phases, coherent split residual families remained, including approximately 18.71/19.28 degrees and 30.71/31.39/32.13 degrees, with additional independent matches near 22.01, 45.13, 57.00, and 65.77 degrees. A positive, replay-stable Ca3WO6 scale accounts for these families and remains near 10.1 wt% through the final profile challenges. CaO re-challenges drove its scale effectively to zero with an unphysical cell collapse, so no crystalline CaO is retained.

The retained sources were health-screened before use. CaWO4 is based on COD 7219229 and WO3 on the powder-equivalent reduced setting of COD 2311041. No exact Ca3WO6 record was available in the supplied index, so charge-balanced non-1:1 products were searched. The retained P 21/n Ca3WO6 model uses the Ca3OsO6 topology (COD 1562666) with the chemically direct Os6+ to W6+ substitution. Its lower-symmetry P 21 competitor received the same converged profile loop and remained worse (best Rwp 2.6190% versus 2.6119%); a cubic competitor gave Rwp about 8.11%. WO3 P-1 and Pnma alternatives and a C2/c CaWO4 record were also inferior. All three submitted CIFs pass `learned/cif_health.py`; independent distance checks give plausible shortest W–O distances of 1.76, 1.71, and 1.92 Å for CaWO4, WO3, and Ca3WO6.

The retained nuisance model has a 12-term smooth background, one specimen shift, refined polarization, and nonnegative U/W/X profile terms. CaWO4 requires [110] March-Dollase texture plus [001] size and strain anisotropy. WO3 retains [010] strain anisotropy, and Ca3WO6 retains [010] size anisotropy with isotropic strain. A repeated final coordinate-descent loop rejected extra texture, 16 background terms, WO3 size, and Ca3WO6 strain anisotropy. Surface roughness lowered Rwp but was rejected as a scale surrogate because it correlated 96% with the dominant CaWO4 scale (and over 91% with the polarization/scale trend). No repeated directional asymmetry was found, so SH/L stayed fixed. Representative isolated low/mid-angle families had observed/calculated FWHM ratios around 0.95–1.06; individual high-angle widths are less diagnostic because of dense overlap.

## Remaining uncertainty

The identities and normalized crystalline fractions are well supported by the profile. The detailed Ca3WO6 internal coordinates cannot be determined reliably from this powder pattern: they remain fixed to the Ca3OsO6 analogue, so the submitted CIF is a topology-level structural model rather than an independent atomic-structure solution. WO3 and CaWO4 atomic coordinates were likewise not released because the data constrain cells and profiles much more strongly than individual coordinates.

No precursor amounts or CaO:WO3 ratio were reported in the metadata, so no mass-balance constraint could be imposed. Without an internal standard, amorphous content and therefore absolute bulk phase fractions cannot be determined. Preferred orientation, absorption/roughness ambiguity, peak overlap, and the analogue-derived Ca3WO6 structure make the true systematic fraction uncertainty larger than the formal e.s.d.'s above.
