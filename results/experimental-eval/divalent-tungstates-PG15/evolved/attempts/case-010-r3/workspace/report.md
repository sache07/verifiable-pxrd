# Crystalline phase analysis

## Result

The pattern is best described by monoclinic WO3 and bixbyite Mn2O3, with a small but reproducible MnWO4 contribution. Fractions are normalized over these modeled crystalline phases; no amorphous fraction can be obtained without an internal standard.

| Phase | Structural model | Weight percent |
|---|---|---:|
| WO3 | monoclinic P 21/c | 71.840 ± 0.279 |
| Mn2O3 | cubic bixbyite Ia-3 | 27.362 ± 0.270 |
| MnWO4 | monoclinic P 2/c | 0.798 ± 0.082 |

The quoted uncertainties are formal least-squares standard uncertainties, not total error estimates. The final full-range fit has Rwp = 6.9088%, Rp = 5.1260%, Rexp = 2.6624%, and goodness of fit = 2.5986 for 8,301 observations and 23 refined variables. The final replay converged to a maximum shift/e.s.d. of 0.0099.

## Evidence and model selection

The Mn/W oxide chemistry and 500 °C treatment in `metadata.json` guided the inventory but did not fix it. Fully occupied records were screened for composition, symmetry, source conditions, and coordination geometry before fitting. The selected main-phase models are COD 2311041 for WO3 and COD 1514230 for Mn2O3. Their exported geometries remain physical: W–O = 1.714–2.158 Å in WO3 and Mn–O = 1.896–2.245 Å in Mn2O3.

Multiple low-, middle-, and high-angle families support both main phases. An alternate standard-cell P21/n WO3 record gave a substantially poorer comparable fit (Rwp about 8.29%). An orthorhombic Pbca Mn2O3 model was statistically indistinguishable from cubic Ia-3 in a two-phase comparison (Rwp 6.9957% versus 6.9961%) but required extra, 98–99% correlated cell parameters. The data therefore do not reliably distinguish a very small orthorhombic distortion; the parsimonious cubic bixbyite model is submitted.

For trace MnWO4, the pressure-tagged exact record COD 1520200 was challenged against a second physical record, COD 9008131: 4.2 K hübnerite with composition Fe0.03Mn0.97WO4. Because Fe is absent from the stated chemistry and shares one fully occupied divalent site, its 0.03 Fe occupancy was replaced by Mn. This model has physical Mn–O = 2.130–2.233 Å and W–O = 1.798–2.126 Å distances. At fixed source cell it improved Rwp from 6.9478% to 6.9088%; the formal scale significance is about 9.8 sigma. Coherent diagnostic residuals near 18.69°, 30.22°, and 30.57° 2theta are strongly reduced. The pressure-tagged alternative fitted less well and gave 0.60 wt%.

Mn3O4 refined to zero scale. A final Mn3WO6 re-challenge gave only 0.22 ± 0.11 wt% (about 2.1 sigma), a negligible Rwp change, and worsened several strong predicted families; it was retained only as a rejected watch-list candidate.

## Refinement and limitations

GSAS-II used the full 9.903–100.095° range with Cu Kalpha1/Kalpha2 wavelengths 1.540598/1.544426 Å and the reported 0.5 intensity ratio. Since point uncertainties were absent, counting-statistical sigma = sqrt(counts) was used. The accepted baseline has a smooth positive eight-term Chebyshev background, one specimen-displacement correction (-517.2 micrometres), refined effective polarization, and a nonnegative common U/X profile. Unused V/W/Y/Z, roughness, transparency, size, and extra asymmetry terms were neutralized. Replay-stable isotropic strain terms were retained for the two main phases, along with very mild WO3 [010] March–Dollase texture; neither is interpreted quantitatively. Atomic coordinates and occupancies were held to the screened source structures, while the two main-phase cells were refined.

The MnWO4 cell could not be refined reliably at this concentration: free-cell trials moved toward an ambient-like volume and 1.05–1.08 wt% but oscillated on replay. Its submitted cell is therefore fixed to COD 9008131. Across the physical fixed- and free-cell alternatives, a more realistic MnWO4 estimate is roughly 0.6–1.1 wt%; its presence is supported, but the submitted 0.798 ± 0.082 wt% formal precision is not a reliable total uncertainty. Likewise, the major-phase split probably carries several tenths of a weight percent of systematic uncertainty because no calibrated instrument profile or measured point uncertainties were supplied. Residual intensity mismatch remains at some strong overlapped peaks, consistent with the goodness of fit above.
