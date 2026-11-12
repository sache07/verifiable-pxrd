# Quantitative phase analysis

The pattern is modeled with two crystalline phases: triclinic tungsten(VI) oxide, WO3, and wolframite cobalt(II) tungstate, CoWO4. This is chemically consistent with incomplete reaction of the reported CoO + WO3 precursor mixture at 900 °C. Both final models are stoichiometric, charge balanced, and fully occupied; no occupational disorder was required.

| Phase | Space group and refined cell | Crystalline weight fraction | Phase R(F²) |
|---|---|---:|---:|
| WO3 | P -1; a = 7.30617, b = 7.53617, c = 7.69190 Å; α = 89.7451°, β = 90.8017°, γ = 90.1759° | 69.821 ± 0.115 wt% | 7.368% |
| CoWO4 | P 2/c; a = 4.66880, b = 5.68341, c = 4.94940 Å; β = 89.9271° | 30.179 ± 0.115 wt% | 10.851% |

Fractions and quoted e.s.d.s are normalized over the two modeled crystalline phases. The final full-range fit (9.9034–100.0949° 2θ, 8,301 points) has Rp = 4.618%, Rwp = 5.727%, Rexp = 3.280%, goodness of fit = 1.747, and reduced χ² = 3.052.

## Evidence and model selection

- WO3 is identified by the resolved 23.18/23.67/24.42° triplet and repeated split families near 33–34°, 41–42°, 54–56°, and 61–62°. Under the same restrained nuisance model, the triclinic P -1 record (COD 2106293) gave Rwp = 7.806%, compared with 8.113% for the closest monoclinic P21/c record (COD 2311041); the improvement was distributed across those independent families rather than one peak.

- CoWO4 is supported by coherent contributions near 19.09°, 30.71°, 31.53°, 38.62°, and 52.15°. The available exact CoWO4 entry was not used because its atom list duplicated symmetry-equivalent metal sites. A stoichiometric-analogue search instead selected the isostructural P 2/c CoMoO4 parent (COD 7205001), followed by the chemically conservative Mo6+ → W6+ substitution. With identical nuisance refinement, this parent gave Rwp = 8.540%, better than substituted ZnWO4 (8.673%), FeWO4 (10.008%), and MnWO4 (13.831%) alternatives.

- The exported geometries are physical: triclinic WO3 has W–O distances of 1.715–2.217 Å; CoWO4 has Co–O = 2.032–2.162 Å and W–O = 1.774–2.152 Å. The shortest O–O distances are 2.562 and 2.456 Å, respectively, with no implausible close contacts.

## Refinement and residual checks

The GSAS-II model uses the reported Cu Kα1/Kα2 wavelengths and fixed 0.5 intensity ratio. Because pointwise uncertainties were not supplied, counting uncertainties were estimated as sqrt(counts). A six-term Chebyshev background, both phase scales and cells, one zero correction, a common nonnegative W/X profile, reflection-geometry surface roughness, and isotropic WO3 microstrain were retained. Unused size/strain, preferred orientation, and asymmetry terms were neutralized. Size, strain, axial/diagonal texture, polarization, and asymmetry alternatives were accepted only when replay-stable and supported across independent low-, middle-, and high-angle families; unsupported or bound terms were removed.

CoO, Co3O4, WO2, W3O8, W3O10, and larger reduced-tungsten-oxide candidates were re-challenged after rebuilding the common profile. Co3O4 collapsed to zero scale. The others refined to only about 0.1–0.6 wt%, produced less than 0.01 percentage point Rwp improvement, or lacked coherent unique families. In particular, the approximately 0.4 wt% CoO trial was contradicted by the absent strongest unique CoO line near 42.47°. These phases were therefore not retained, although an unidentified crystalline impurity below roughly 1 wt% cannot be excluded.

The saved project was reopened and replayed over the complete range with no change in calculated intensity or Rwp. The CIFs, fractions, and `fit.csv` were then exported from that exact project.

## Remaining uncertainty

The least-squares e.s.d. of 0.115 percentage point is conditional on this model and understates systematic uncertainty because no calibrated instrumental profile, polarization value, or internal standard was supplied. A more realistic uncertainty for the two-phase crystalline split is approximately ±2–3 absolute percentage points. The absolute amount of either phase relative to amorphous material cannot be determined reliably from these data.

The phase symmetries, cells, and major-phase assignments are well supported, but the powder data do not independently determine every atomic coordinate, defect, or occupancy. Atomic coordinates were therefore held to the physically screened database/prototype models; subtle defect chemistry or a closely related CoWO4 distortion cannot be resolved reliably here.
