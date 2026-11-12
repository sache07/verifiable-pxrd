# Crystalline phase analysis

The pattern is described by three crystalline phases: scheelite SrWO4, monoclinic WO3, and orthorhombic SrCO3. Their refined fractions, normalized only over these modeled crystalline phases, are:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| SrWO4 | I 41/a | a = 5.39308, c = 11.90002 | 60.51 ± 0.12% |
| WO3 | P 21/c | a = 7.69473, b = 7.55524, c = 10.51628, β = 136.12786 | 24.19 ± 0.10% |
| SrCO3 | P n m a | a = 6.02410, b = 5.09747, c = 8.39339 | 15.30 ± 0.12% |

Uncertainties shown are from the GSAS-II covariance matrix; they are statistical precision, not total uncertainty. The final 10–100° 2θ fit has Rwp = 3.0385%, Rp = 2.3903%, Rexp = 2.8607%, and goodness of fit = 1.0622.

## Evidence and model selection

The chemical context strongly supports the assignment: heating WO3 with SrCO3 at 650 °C should form SrWO4 with residual unreacted precursors, exactly the three-phase inventory found from the diffraction families. Removing SrCO3 or WO3 from the same neutral-profile baseline raised Rwp from 6.475% to 7.598% and 11.942%, respectively; each residual phase therefore has coherent support beyond isolated peaks.

No exact SrWO4 entry was present in the supplied index, so cross-chemistry prototype searching was used. A scheelite CaWO4 parent (COD 7219229) was converted by the chemically conservative Ca-to-Sr substitution; W, O, symmetry, occupancies, and topology were retained. It fit better under the same restrained baseline than SrMoO4- and BaWO4-derived alternatives (Rwp 6.475%, 6.640%, and 7.599%). The final geometry is physical: W–O = 1.822 Å and Sr–O = 2.549–2.565 Å. Exact-composition records supplied the selected WO3 model (COD 2311041) and SrCO3 model (COD 9008198). Alternative WO3 records in P21/c, P-1, and Pnma gave baseline Rwp values of 6.988%, 7.304%, and 7.733%; the selected P21/c model also retains plausible W–O distances of 1.718–2.163 Å. SrCO3 has C–O = 1.291–1.304 Å and Sr–O = 2.568–2.732 Å.

The physically adequate common profile used a smooth six-coefficient Chebyshev background, one specimen-height correction, and nonnegative W/X instrumental width terms. Unsupported asymmetry, polarization, crystallite-size, and extra roughness terms were pruned. WO3 alone required replay-stable anisotropic microstrain along its unique b direction. March–Dollase texture axes SrWO4 [111], WO3 [10-1], and SrCO3 [001] were each preferred over no-texture and symmetry-distinct axis trials supported by multiple reflections. The final observed/calculated profile has no remaining coherent family that warrants another phase.

Sr3W2O9 was retained on the watch list and re-tested against the exact final common profile. Its nonnegative scale refined to the zero bound with effectively zero mass fraction and no meaningful fit improvement, so neither its presence nor a fraction can be determined reliably; it is not included. A rigorous detection limit cannot be inferred from this pattern alone.

## Remaining uncertainty

Fractions are crystalline-phase-normalized. Without an internal standard they do not quantify amorphous material, and the quoted covariance errors omit systematic uncertainty from preferred orientation, source models, peak broadening, and background separation. Real fraction uncertainty is therefore larger than approximately 0.1 wt% statistical errors and may reach several tenths to a few weight percent.

Atomic coordinates were not reliably determined by this powder pattern. A trial SrWO4 oxygen-coordinate refinement gave only a small residual improvement and coupled to texture/geometry, so physically screened source coordinates were retained while cells were refined. The fitted specimen displacement is 1.057 mm; because it correlates with peak positions, absolute lattice-parameter uncertainty is also larger than the covariance precision printed by GSAS-II. These limitations affect detailed geometry more than the three phase identities.
