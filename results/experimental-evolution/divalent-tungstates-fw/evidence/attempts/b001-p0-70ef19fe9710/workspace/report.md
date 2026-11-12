# Powder XRD phase analysis

The pattern is explained by three crystalline phases: 65.23 wt% PbWO4, 18.86 wt% residual PbCO3, and 15.91 wt% residual WO3. Fractions are normalized over modeled crystalline material only. The final atomic Rietveld model gives Rwp = 3.3735%, Rp = 2.6650%, and Rexp = 3.3643% (goodness-of-fit chi-squared = 1.0054), so the fit is essentially at the counting-statistical limit.

| Phase | Structural assignment | Crystalline wt% |
|---|---|---:|
| PbWO4 | tetragonal stolzite/scheelite, I41/a | 65.23 |
| PbCO3 | orthorhombic cerussite, Pnma | 18.86 |
| WO3 | monoclinic, P21/c | 15.91 |

## Evidence

The strongest family at 27.90, 30.11, 33.26, 45.21, 51.67, and 55.68 degrees 2-theta is the scheelite PbWO4 pattern. The exact PbWO4 composition was absent from the supplied reference subset, so its model was constructed by isovalent adaptation of the I41/a SrWO4 framework (COD 1546036), cross-checked against the PbMoO4 scheelite analogue, and then refined in GSAS-II. The refined W-O distance is 1.779 A and the heavy-atom framework remains the standard stolzite arrangement.

Residual-precursor assignments are independently supported by complete peak families. Monoclinic WO3 accounts for the 23.64/24.12/24.91 degree triplet and its higher-angle splittings; the selected physically valid P21/c model is based on COD 2311041. PbCO3 accounts for the 25.36/26.05 degree doublet and peaks near 36.74 and 44.09 degrees; its model is based on COD 1010956. Adding PbO drove its scale to zero and made its cell terms singular, so no fourth crystalline phase is justified. Modest March-Dollase terms for PbCO3 [100] (1.141) and WO3 [010] (1.073) remove coherent intensity residuals.

## Remaining uncertainty

The reported fractions are robust to phase-model trials, but scale, preferred orientation, displacement parameters, and size/strain are correlated; a practical systematic uncertainty is about +/-2 wt% absolute for each fraction. No amorphous fraction can be obtained from this scan alone.

PbWO4 framework symmetry and heavy-atom positions are well supported, but its oxygen coordinate is an analogue-derived powder refinement rather than a direct single-crystal determination. For the two minor phases, the detailed light-atom coordinates are not independently determined by these data and were retained from physically screened references. Monoclinic and triclinic WO3 have closely overlapping laboratory patterns; P21/c is selected by the split-line intensities and superior physically constrained fit, but subtle oxygen displacements should not be regarded as unique.
