# Powder XRD phase analysis

The reflection-geometry 10–100° Cu Kα pattern is modeled with five crystalline phases. The calculation uses Kα1 = 1.540598 Å and Kα2 = 1.544426 Å at the reported 0.5 intensity ratio. Weight fractions are normalized over those phases; an amorphous fraction was not measured.

| Phase | Space group | Weight fraction (wt%) |
|---|---:|---:|
| CaWO₄, scheelite | I 4₁/a | 67.396 ± 0.283 |
| WO₃, monoclinic | P 2₁/c | 14.475 ± 0.109 |
| Ca₃WO₆-type, monoclinic | P 2₁ | 16.203 ± 0.297 |
| CaO | Fm-3m | 1.347 ± 0.152 |
| Ca₄.₂₆W₁₀O₃₀ tetragonal tungsten bronze | P 4/mbm | 0.580 ± 0.070 |

The quoted uncertainties are formal one-standard-deviation GSAS-II values. The final fit has Rwp = 6.376%, Rp = 4.267%, Rwp,min = 2.617%, and goodness of fit = 2.445 for 8,301 points and 61 refined variables. Raw-count Poisson weights were used. In `fit.csv`, difference means observed minus calculated.

## Evidence and model selection

Scheelite CaWO₄ (COD 7219229) and monoclinic WO₃ (COD 2311041) account for the dominant line families. Removing CaWO₄ or WO₃ in the inventory tests raised Rwp to 46.7% and 15.9%, respectively. Same-composition alternatives were substantially worse after matched restarts: the best tested triclinic WO₃ source gave Rwp 11.6%, and a fergusonite CaWO₄ source gave 48.1%.

A separate coherent family requires the Ca₃WO₆-type phase. Several chemically mapped ordered-multication frameworks were carried through matched fits. The P 2₁ Ca₃UO₆ parent (COD 2310470, U mapped to W) reached Rwp 6.80% before trace-phase and coordinate refinement, versus 8.51% for the best tetragonal and 8.55% for the best cubic alternatives; tested P 2₁/n parents were about 10.8%. Its deletion raised Rwp to 10.9%. The submitted model refines the W site and cell but retains the parent Ca/O framework.

The trace assignments also survive deletion from the final cumulative inventory. Removing CaO raises Rwp from 6.376% to 6.443%; removing the bronze raises it to 6.563%. Their gains occur over multiple reflections, not a single isolated peak. The bronze requires strong [100] March–Dollase texture; its scale and texture are correlated, but two independent starts reproduced the calculated curve and gave approximately 0.55–0.63 wt% bronze.

The profile model uses a 16-term Chebyshev background, specimen displacement, surface roughness, common U/W width and axial-divergence terms, phase size broadening, and supported texture for WO₃ [011], Ca₃WO₆ [001], and the bronze [100]. Zero shift, polarization refinement, strain, and unsupported texture/size branches were rejected after restarts or physical screening.

## Structural refinement and uncertainty

Coordinates were refined only for reproducible, physically valid blocks: CaWO₄ O, WO₃ W, and Ca₃WO₆ W. Independent nuisance/profile starts reproduced those shifts. Broader WO₃/P 2₁ oxygen blocks and the P 2₁ Ca block lowered Rwp but generated implausibly short bonds, so they were rejected. Final CIF screening gives minimum W–O distances of 1.754 Å (CaWO₄), 1.666 Å (WO₃), 1.871 Å (Ca₃WO₆), and 1.882 Å (bronze), with no short O–O or Ca–O contacts. The WO₃ CIF uses a valid nonstandard P 2₁/c cell setting with β ≈ 136.04°.

The Ca₃WO₆ identification is therefore best stated as a Ca₃WO₆-type analogue rather than a de novo structure solution; its inherited oxygen/Ca coordinates are not uniquely determined by this powder pattern. CaO is a secure trace assignment but its fraction is profile-sensitive. The bronze structure and partial Ca occupancies cannot be independently refined at only ~0.58 wt%; COD 4030741 occupancies and coordinates are retained, and its fraction has additional systematic uncertainty beyond the formal error. None of the fractions includes uncertainty from amorphous material, microabsorption, or preferred-orientation model choice.

An independent replay of `final.gpx` converged with ΔRwp = 0.00018 percentage points, maximum fraction change 0.0022 wt%, and calculated-profile RMS change 0.47 counts (maximum intensity ~39,675 counts), confirming that the submitted project, CIFs, fractions, and profile are mutually consistent.
