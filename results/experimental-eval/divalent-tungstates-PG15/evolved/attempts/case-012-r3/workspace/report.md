# PXRD phase analysis

## Result

The crystalline product is modeled as two phases. Fractions are normalized over the modeled crystalline material only.

| Phase | Structural model | Weight fraction | Formal 1σ ESD |
|---|---|---:|---:|
| Nickel tungstate, NiWO₄ | wolframite, P2/c (No. 13) | 76.40 wt% | 0.09 wt% |
| Tungsten trioxide, WO₃ | monoclinic γ-WO₃, P2₁/c (No. 14) | 23.60 wt% | 0.09 wt% |

The final full-range refinement gives Rwp = 4.549%, Rp = 3.554%, Rexp = 3.479%, goodness of fit = 1.310, and reduced χ² = 1.717 for 8,282 observations and 32 refined parameters. The final maximum shift/ESD is 0.0049 after saving, reopening, and replaying the project.

## Evidence and model selection

The NiO + WO₃ precursor context and 900 °C treatment support formation of NiWO₄ with residual WO₃. The strong NiWO₄ families at approximately 19.19, 30.85, 36.52, and 54.58° 2θ and the characteristic WO₃ cluster near 23.1–24.3°, together with the WO₃ line near 26.5°, are reproduced coherently across the full pattern. No strong unexplained family remains.

Candidate structures were challenged under a common restrained profile model. A P2/c NiWO₄ source structure (COD 5910277) fit better than a physically plausible Ni-substituted ZnWO₄ analogue (COD 1520641; Rwp 5.02% versus 5.94% at the comparison stage). The selected ambient monoclinic WO₃ model (COD 2311041) gives the best final result. An almost metrically equivalent triclinic WO₃ model is close (Rwp 4.560%) but slightly worse than the selected monoclinic model (4.549%); an orthorhombic model is clearly worse (Rwp 7.93%). The unusual β ≈ 136° reported for the exported WO₃ CIF is a valid nonconventional P2₁/c cell setting.

Residual NiO was explicitly reintroduced as a watch-list phase. Its scale refined to the imposed numerical floor, did not improve the fit, and corresponds to zero modeled fraction. The covariance-based 3σ upper scale estimate is about 0.27 wt% under this model, so NiO is excluded from the submitted inventory but cannot be ruled out below roughly 0.3 wt%.

The exported structures pass chemical checks. Refined NiWO₄ has Ni–O = 1.96–2.01 Å and W–O = 1.90–2.21 Å, with bond-valence assignments Ni²⁺/W⁶⁺/O²⁻. The WO₃ model has W–O = 1.71–2.16 Å and W⁶⁺/O²⁻ assignments, with no unphysical short O–O contacts in either phase.

## Refinement and uncertainty

The original unsmoothed counts were fitted from 10.009 to 99.994° 2θ using the reported Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio. Since pointwise uncertainties were not supplied, Poisson count weights were used. The accepted baseline contains an eight-term smooth Chebyshev background, one zero correction, nonnegative common U/W/X profile terms, and a bounded effective polarization correction. Cells and phase scales were refined. Only replay-stable isotropic microstrain for WO₃ was retained; phase size terms, NiWO₄ strain, preferred orientation, additional asymmetry, roughness, transparency, and redundant displacement corrections were unsupported or unstable and were fixed at neutral values. Peak positions, widths, and asymmetry remain coherent in low-, middle-, and high-angle regions.

The tabulated 0.09 wt% ESDs are internal least-squares errors and are too optimistic as total uncertainties. Switching to the plausible triclinic WO₃ model changes the NiWO₄ fraction by about 0.65 wt%. A practical result is therefore **76.4 ± 1.0 wt% NiWO₄ and 23.6 ± 1.0 wt% WO₃** among crystalline phases. Monoclinic versus pseudosymmetric triclinic WO₃ cannot be distinguished decisively from this powder pattern alone; monoclinic γ-WO₃ is selected from the slight fit advantage and ambient-condition plausibility. NiWO₄ oxygen coordinates have appreciable powder-data uncertainty, while WO₃ atomic coordinates and displacement parameters were held to the source model and are not independently determined here. Any amorphous content, and crystalline phases below the detection limit, cannot be quantified without an internal standard.

The numerical profile, fractions, fit statistics, and both CIFs were exported directly from the final reopened `final.gpx` state and checked for exact agreement.
