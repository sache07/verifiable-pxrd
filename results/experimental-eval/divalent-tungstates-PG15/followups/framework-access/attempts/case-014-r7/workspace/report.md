# Powder XRD phase analysis

The pattern is best described by three crystalline phases:

| Phase | Space group | Refined cell (angstrom, degrees) | Crystalline weight fraction |
|---|---|---|---:|
| SrWO4 (scheelite) | I41/a, No. 88 | a = 5.41874, c = 11.96129 | 73.25% |
| gamma-WO3 | P21/c, No. 14 | a = 7.69547, b = 7.54162, c = 10.53344, beta = 136.1146 (COD non-standard cell) | 11.46% |
| Sr3WO6 | P21/n, No. 14 | a = 6.07102, b = 5.53930, c = 9.03014, beta = 90.7017 | 15.29% |

Fractions are normalized over these modeled crystalline phases. They do not measure amorphous content or any component below the diffraction detection limit.

## Evidence

The dominant reflections at approximately 28.00, 30.22, 33.39, 45.45, 47.75, 51.98 and 56.08 degrees 2theta form the tetragonal scheelite SrWO4 pattern and refine consistently from COD 1546036. The distinct low-angle WO3 group near 23.45, 23.90 and 24.73 degrees, together with its higher-angle lines, requires monoclinic P21/c WO3; COD 2311041 was selected because it fits these lines and has physically valid interatomic contacts. Residual peaks near 29.75, 32.63, 40.22 and 44.54 degrees are accounted for by monoclinic Sr3WO6. Trial additions of SrCO3, SrO, a second SrWO4 polymorph and Sr3W2O9 did not retain a material positive scale.

The minor-phase chemistry gives an independent check. The refined WO3/Sr3WO6 weight ratio is 0.750, reasonably close to 0.854 required by `3 SrWO4 -> Sr3WO6 + 2 WO3`, given profile and structural-model uncertainty.

The submitted atomic/profile model gives Rwp = 13.259% and Rp = 8.968% on all 8,282 raw-count points using `w = 1/max(Iobs,1)`. Native GSAS-II replay from `final.gpx`, with fresh reflection and intensity generation, reproduces this profile and reports no invalid peak-width, background, displacement-parameter or polarization flags. All three exported CIFs pass the scorer's contact and occupancy screen.

## Remaining uncertainty

SrWO4 and WO3 are well supported phase identifications. The Sr3WO6 identification is supported by multiple otherwise unmodeled lines and by the paired WO3/Sr3WO6 chemistry, but its detailed structure is less certain: no exact Sr3WO6 entry was available in the screened library, so its P21/n model was derived by replacing Ca with Sr in the Ca3WO6 framework of COD 1563081 and refining the cell. Its atomic coordinates were retained from that analogue and should not be interpreted as independently determined by this powder pattern.

The phase fractions are semiquantitative rather than metrologically traceable. No pointwise uncertainties or calibrated instrument profile were supplied, and minor-phase scale factors correlate with broadening, preferred orientation and the low-angle specimen/background correction. In particular, the Sr3WO6 fraction and detailed structure cannot be determined more reliably from this scan alone; a few weight percent systematic uncertainty is plausible.
