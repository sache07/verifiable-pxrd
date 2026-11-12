# PXRD phase analysis

The stable crystalline model contains scheelite PbWO4, monoclinic WO3, and Pb3O4. Fractions are normalized over these modeled crystalline phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| PbWO4 (scheelite) | I4_1/a | 0.61365 (formal s.u. 0.00173) |
| WO3 (monoclinic) | P2_1/c | 0.20916 (formal s.u. 0.00131) |
| Pb3O4 | P4_2/mbc | 0.17718 (formal s.u. 0.00172) |

The reopened full-range refinement gives Rwp = 4.6713%, Rp = 3.0496%, and GOF = 1.8829 over 9.9034–100.0946 degrees 2-theta. The formal fraction uncertainties do not include source choice, profile model, preferred orientation, or amorphous material, so practical uncertainty is larger. No precursor quantities or numerical precursor ratio were present in `metadata.json`; consequently no mass-balance constraint was invented. Pb3O4 is consistent with unreacted precursor.

## Evidence and model selection

PbWO4 accounts for the scheelite families near 27.8, 33.2, 45.1, 51.6, 55.6, and 72.4 degrees. WO3 is anchored by the characteristic 23.5/24.0/24.8-degree group and families near 33.7/34.6, 41.9, and 50.4 degrees. Pb3O4 has independent support near 14.66, 26.81, 31.25/32.55, 50.37/52.52, 58.53, and 63.64 degrees. Its scale stayed positive through profile rebuilds and broadening/texture challenges.

The submitted sources all pass `learned/cif_health.py`: PbWO4 COD 9009811, WO3 COD 2311041, and Pb3O4 COD 9012124. Matched source loops rejected raspite and lower-symmetry/alternate WO3 models without diagnostic splitting. For Pb3O4, COD 9012124 gave Rwp 4.671%; reviewed tetragonal COD 1537983 gave 4.798%, while orthorhombic COD 9003043 gave 8.198%, collapsed to about 0.7 wt%, and drove polarization above one.

The retained nuisance model uses nonnegative common W+X profile terms, 10 smooth background coefficients, specimen shift, and bounded polarization. PbWO4 has symmetry-compatible uniaxial size broadening (about 71/51 nm) and weak [100] March-Dollase texture (1.052); Pb3O4 has approximately 33 nm isotropic size broadening. WO3 remains at the neutral size/strain/texture state. Roughness, unsupported strain, and collapsed broadening/texture terms were pruned.

## Peak-family audit

Positions and widths below are measured from smoothed local observed/calculated profiles after background subtraction. L/R are observed left/right half-widths in degrees.

| Phase | Range | Position obs/calc | FWHM obs/calc | L/R |
|---|---|---:|---:|---:|
| PbWO4 | low | 30.028/30.028 | 0.252/0.270 | 0.120/0.133 |
| PbWO4 | middle | 68.962/68.973 | 0.391/0.362 | 0.121/0.270 |
| PbWO4 | high | 84.338/84.241 | 0.435/0.439 | 0.207/0.228 |
| WO3 | low | 24.019/24.019 | 0.132/0.139 | 0.058/0.074 |
| WO3 | middle | 48.664/48.664 | 0.221/0.213 | 0.086/0.135 |
| WO3 | high | 97.237/97.280 | 0.071/0.101 | 0.027/0.045 |
| Pb3O4 | low | 31.245/31.202 | 0.340/0.332 | 0.207/0.133 |
| Pb3O4 | middle | 52.522/52.522 | 0.396/0.417 | 0.208/0.188 |
| Pb3O4 | high | 92.749/92.749 | 0.035/0.049 | 0.021/0.014 |

The low/middle-angle agreement supports the phase inventory. Some high-angle families are weak or partly overlapping, and the correlated residuals (Durbin-Watson 0.591) plus GOF above one mean this model is not adequate for fine topology decisions from small Rwp differences alone.

## Remaining uncertainty

A health-passing Pb3WO6 model adapted isovalently from Pb3UO6 (U6+ to W6+, Pnma) matched positive residual families near 29.49 and 45.63 degrees. However, repeated four-phase loops moved its apparent fraction between roughly 2 and 6 wt%, exchanged size and strain, and produced texture/scale or polarization boundary behavior. A Pb2WO5 analogue was driven mainly by one residual family; raspite improved Rwp only marginally and split the PbWO4 scale; PbO and the reviewed defect scheelite refined to effectively zero scale. None satisfies the required replay-stable scale plus two-family gate, so no fourth phase is quantified. The 29.5/45.6-degree residual component remains unresolved; its exact structure and weight fraction cannot be determined reliably from this pattern.

Atomic coordinates were not refined. The CIFs therefore combine passing literature coordinates with refined unit cells. Fractions apply only to modeled crystalline material; an amorphous fraction cannot be obtained from these data without an internal standard.
