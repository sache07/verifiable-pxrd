# Quantitative phase analysis

## Result

The pattern is modeled as three crystalline phases. Weight fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| MnWO₄, wolframite | P 2/c | 0.70359 (70.36 wt%) | a = 4.79925, b = 5.70716, c = 4.97595, β = 91.1263 |
| WO₃, monoclinic | P 2₁/c | 0.19748 (19.75 wt%) | a = 7.69117, b = 7.55043, c = 10.51648, β = 136.0487 |
| Mn₃O₄, hausmannite | I 4₁/amd | 0.09892 (9.89 wt%) | a = b = 5.76555, c = 9.51809 |

The full-range fit (9.9034–100.0946° 2θ, 8,301 points) has Rwp = 7.3901%, Rp = 4.9038%, Rexp = 2.4903%, and goodness of fit = 2.9761 for 48 variables. The Cu Kα1/Kα2 wavelengths and reported 0.5 intensity ratio were retained. The project was replayed four times after freezing the model; no variables froze or hit a bound, and the final maximum shift/e.s.d. was 0.0015.

## Evidence and model selection

MnWO₄ accounts for the dominant peak-position and intensity families throughout the pattern. No exact MnWO₄ entry was present in the supplied index, so health-screened P 2/c wolframite records for MgWO₄, CuWO₄, and ZnWO₄ were independently adapted to MnWO₄ and used as coordinate starts. After complete refinement, all three starts converged to the same coordinates, fractions, and Rwp within numerical noise. Scheelite, triclinic, and C 2/m alternatives were inferior. The final MnWO₄ model uses neutral size, strain, and texture terms.

The second phase is exact-formula monoclinic WO₃. The retained P 2₁/c record (COD 2311041) outperformed a structurally distinct exact-formula monoclinic record (COD 1528915) and lower-symmetry competitors when each received its own neutral/isotropic/uniaxial profile loop. Its surviving terms are [001] uniaxial coherent-domain broadening and a [101] March–Dollase correction; both survived background and nuisance replays.

Residual Mn₃O₄ has a positive replay-stable scale and independent non-coincident families, including (103) near 31.75°, (321) near 58.12°, and (413) near 73.68°. Their observed FWHM values (about 0.273°, 0.453°, and 0.580°) show the angular trend reproduced by the retained isotropic microstrain term. The I 4₁/amd source ranking survived an alternate exact-formula record, broadening challenges, and low-index texture-axis challenges. A [110] March–Dollase term was retained because it repeatedly improved multiple independent Mn₃O₄ families with stable fractions. A size-plus-strain trial reached a size bound and was rejected. An exact Mn₃WO₆ trial collapsed in scale and was not retained.

The common profile uses an 11-term smooth Chebyshev background, one specimen-shift correction, nonnegative W/X instrumental width terms, and a simple surface-roughness correction. U and V are zero, SH/L is fixed at 0.002, and polarization is fixed at 0.5 because releasing polarization jointly with roughness was strongly coupled. Every retained source and each submitted CIF passed `learned/cif_health.py`; no hard contacts, invalid occupancies, or parser warnings were reported.

## Remaining uncertainty

The formal one-standard-deviation fraction e.s.d.s from the final covariance matrix are 0.47, 0.22, and 0.54 wt%-points for MnWO₄, WO₃, and Mn₃O₄, respectively. These are smaller than model uncertainty. Changing the smooth background from 11 to 10 terms moved about 0.8 wt%-point between MnWO₄ and the broad Mn₃O₄ contribution, while the accepted-source and replay tests were nearly invariant. Conservative interpretation is therefore approximately ±1 wt%-point for MnWO₄ and Mn₃O₄ and ±0.5 wt%-point for WO₃.

No precursor amounts or ratio were reported, so no material-balance constraint was available or imposed. The fractions do not quantify amorphous material or crystalline phases below the detection level. The phase identities and average structure types are reliable, but the detailed oxygen coordinates of WO₃ and the internal coordinates of weak Mn₃O₄ are not independently determined by this powder pattern: only the WO₃ W coordinates were released, and the Mn₃O₄ coordinates were held to the health-screened source model.
