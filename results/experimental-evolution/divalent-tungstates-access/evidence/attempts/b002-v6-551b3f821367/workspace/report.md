# Powder XRD phase analysis

## Result

The crystalline pattern is modeled with three phases. Fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO4 | wolframite, P 2/c, COD 1520200 | a=4.79497, b=5.70113, c=4.97042, beta=91.1078 | 64.24% |
| WO3 | monoclinic, P 21/c, neutron model COD 2311041 | a=7.68224, b=7.53529, c=10.50616, beta=136.0438 | 21.42% |
| Mn2WO6 | orthorhombic, P 21 21 21, Mn-substituted Y2WO6 analogue (COD 1541070 parent) | a=5.06631, b=8.67682, c=9.43066 | 14.35% |

Fresh forward replay of `final.gpx` over all 8301 points gives Rwp=15.244%, Rp=9.715%, Rexp=1.990%, and goodness-of-fit=7.660. The relatively high goodness-of-fit reflects systematic profile/intensity mismatch and the absence of supplied pointwise uncertainties; counting-statistics weights, 1/max(Iobs,1), were used.

## Evidence

- The precursor context (Mn3O4 + WO3, heated at 800 °C in reflection geometry with Cu Kalpha radiation) restricts the ordinary chemistry to Mn-W-O. Wolframite MnWO4 indexes the dominant sharp reflection family and refines to a conventional wolframite cell.
- Residual peaks at approximately 23.1, 23.6, 26.5, 28.6-28.9, 33.5, and 34.1° are accounted for by monoclinic WO3. The submitted neutron-derived COD 2311041 model was chosen over a coarse older coordinate set that produced an implausible 1.58 Å fully occupied O-O contact; all submitted CIFs pass the contact and occupancy screen.
- A broad, coherent family at approximately 19.86, 20.41, 28.64, 35.11, 46.49, 54.45, 55.30, 56.49, 59.35, and 66.41° requires the third phase. It is indexed by an orthorhombic P 21 21 21 Mn2WO6 cell obtained by chemically supported Mn-for-Y transfer from Y2WO6 (COD 1541070). Exact Mn oxides/precursors tested against this family did not retain a stable, broadly supported positive contribution.
- The remaining major difference features are centered on accepted reflections or fall inside the broad Mn2WO6 profiles; no additional coherent reflection family remains. Preferred-orientation trials were non-unique or bound-limited and were not retained.

## Uncertainty and model limits

The MnWO4 and WO3 identifications and cells are reliable. The formal one-sigma mass-fraction uncertainties from the least-squares covariance matrix are 0.29, 0.18, and 0.32 percentage points, respectively, but they omit phase-model and profile-systematic error.

The detailed Mn2WO6 atomic coordinates cannot be determined reliably from this pattern. Its isotropic size is at the imposed 0.040 micrometre floor and its microstrain is about 7168 ppm; coordinate and texture trials were bound-limited. Thus the P 21 21 21 indexing and an approximately 14% crystalline contribution are supported, while the submitted analogue-derived coordinates are provisional and the fraction should be regarded as semiquantitative (systematic uncertainty of several absolute percentage points is plausible).

The supplied staged polish was run once. Its valid branches agreed after rollback of clipped atoms; small physical MnWO4 coordinate shifts were retained. A polished branch using the coarse WO3 reference was rejected on geometry, and the final project was re-settled with the physical neutron WO3 model without repeating the staged polish. No amorphous fraction can be obtained without an internal standard, so the reported fractions sum to 100% only over modeled crystalline material.
