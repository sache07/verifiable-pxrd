# PXRD phase analysis

The crystalline pattern is modeled as wolframite ZnWO4, wurtzite ZnO, and monoclinic WO3. The quantitative result, normalized over these modeled crystalline phases, is:

| Phase | Space group | Weight fraction | Refined cell (angstrom, degrees) |
|---|---:|---:|---|
| ZnWO4 (wolframite) | P2/c (13) | 73.8 wt% | a=4.69114, b=5.71872, c=4.92673, beta=90.6320 |
| ZnO (wurtzite) | P6_3mc (186) | 7.0 wt% | a=3.25005, c=5.20796 |
| WO3 (monoclinic) | P2_1/c (14) | 19.2 wt% | a=7.69174, b=7.53782, c=10.53093, beta=136.0930 |

The WO3 cell is the valid non-reduced setting used by the source structure; it is equivalent to the familiar near-orthogonal monoclinic metric under a cell transformation. The final fit has Rwp=5.151%, Rp=4.018%, Rexp=3.782%, and goodness-of-fit=1.362 for all 8,301 measured points.

## Evidence

The 900 C ZnO/WO3 reaction context supports ZnWO4 formation with residual precursors. Atomistic models from COD 1520641 (ZnWO4), 9004178 (ZnO), and 2311041 (WO3) reproduce multiple distinct line families across 9.90-100.09 degrees 2-theta. In matched leave-one-out refinements from the mature model, Rwp increased from 5.15% to 6.75% without ZnO and about 14.4% without WO3; removing ZnWO4 destroyed the fit (Rwp about 40% and an unstable nuisance solution).

The monoclinic WO3 assignment was tested against materially distinct alternatives with the same companion phases and nuisance model. Rwp was 5.15% for P2_1/c, 5.35% for a near-metric triclinic model, 8.09% for orthorhombic WO3, and 12.49% for tetragonal WO3. The monoclinic model was therefore retained. The largest remaining residuals lie on shoulders of modeled ZnWO4/WO3 reflections, especially near 30.7 degrees, rather than forming a coherent new peak family.

All imported and final CIFs passed the supplied composition, occupancy, symmetry-expansion, duplicate-site, and contact audit. The selected GPX passed fresh-profile regeneration, total-width, convergence, and dropped-variable checks. A simple surface-roughness envelope was strongly preferred; unconstrained polarization ran outside its physical range, and axial-divergence and extra profile branches were unstable, correlated, or inferior. The retained minor terms are weak [001] March-Dollase corrections for ZnWO4 (ratio 0.990) and ZnO (1.049), plus approximately 0.0031 isotropic microstrain for WO3. Crystallite-size terms were not retained after the final ADP/profile pass.

## Remaining uncertainty

The phase identities are well supported, but the fractions should be quoted to about one decimal wt% rather than at their formal covariance precision. Pointwise uncertainties, a calibrated instrumental profile, effective polarization, and an internal standard were not supplied, so the small formal fraction esds in `result.json` exclude important profile/envelope systematics. The values are crystalline-phase-normalized; amorphous content cannot be determined from this data set.

ZnWO4 independent coordinates and the two independent W positions in WO3 refined stably with plausible contacts. ZnO's oxygen coordinate did not improve the fit materially, and refinement of the WO3 oxygen coordinates oscillated rather than converging. The WO3 source lacked usable ADPs: a constrained W/O ADP trial was strongly coupled to W coordinates, so chemically modest values were fixed at Uiso(W)=0.004 and Uiso(O)=0.008 angstrom squared rather than reported as measured. Detailed ZnO/WO3 oxygen geometry and WO3 ADPs are consequently not determined independently by this powder pattern, even though the phase families, cells, and crystalline fractions are supported.
