# PXRD phase analysis

## Result

The crystalline pattern is described by three phases. Fractions are normalized over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Formal ESD |
|---|---:|---:|---:|
| Scheelite SrWO4 | I 41/a | 60.53 wt% | 0.14 wt% |
| Monoclinic WO3 | P 21/c | 24.43 wt% | 0.11 wt% |
| Orthorhombic SrCO3 (strontianite) | P n m a | 15.03 wt% | 0.14 wt% |

The full-range fit (9.9034–100.0946° 2θ, 8,301 points) has Rp = 2.712%, Rwp = 3.535%, Rexp = 2.861%, and goodness of fit = 1.237. Phase RF values are 2.08%, 4.06%, and 4.57%, respectively. No coherent residual peak family remained that justified a fourth crystalline phase.

## Identification evidence

The chemistry and the 650°C treatment are consistent with partial formation of SrWO4 from the supplied WO3 and SrCO3. The dominant scheelite family accounts for peaks at about 17.46, 27.20, 29.44, 32.64, 44.83, 47.14, 55.53, and 56.84°. The split WO3 group near 22.51–23.83° and its families near 32.9–33.6 and 40.9–41.3° require a low-symmetry WO3 phase. SrCO3 is independently supported by peaks near 24.65, 25.30, 36.08, 43.67, and 49.46°.

No exact SrWO4 entry was present in the supplied candidate inventory, so stoichiometric analogues were screened. Fully occupied scheelite CaWO4 (COD 7219229, 298 K powder refinement) was adapted by the isovalent Ca2+ to Sr2+ substitution. Fully occupied SrMoO4 and EuWO4 parents were also fitted with the same staged nuisance treatment; the CaWO4-coordinate model gave the best common-stage Rwp (3.956%, versus 4.079% and 4.175%). A BaWO4 record was rejected before fitting because of half-occupied oxygen disorder and an unphysical approximately 1.17 Å O–O contact. The final adapted SrWO4 model is fully occupied and has W–O = 1.814 Å. Its oxygen coordinate was refined with four W–O restraints, so the phase topology and amount are supported more strongly than the exact oxygen position.

For WO3, the selected fully occupied P21/c neutron structure (COD 2311041) passed the geometry screen. Under a common profile, the alternate monoclinic and orthorhombic records were worse (Rwp about 7.09% and 7.85%, versus 6.66% for the selected record). A fully converged triclinic competitor using the same final nuisance schedule gave Rwp = 3.571%, compared with 3.535% for P21/c, while requiring more cell freedom. The monoclinic assignment is therefore preferred, although the exact low-symmetry distortion is less certain than the identification of WO3 itself. The selected SrCO3 model is the fully occupied Pnma strontianite record COD 9008198; a disordered rhombohedral record refined to zero scale and was rejected. A chemically possible high-pressure Sr3W2O9 record was also rejected because its diagnostic reflections were absent.

The refined residual WO3 and SrCO3 amounts are nearly equimolar (SrCO3/WO3 = 0.966 mol/mol), and the total modeled Sr/W ratio is 0.988. This independent precursor/product mass-balance check supports the three-phase interpretation.

## Refinement and uncertainty

The model used an eight-term Chebyshev background and a shared, nonnegative U/W/X profile. Its calculated common FWHM rises smoothly from 0.168° at 17.5° to 0.210° at 95°. Reflection-geometry angular behavior favored one specimen-displacement correction over zero shift (Rwp 3.535% versus 3.561% in the final comparison); zero and displacement were not co-refined. The approximately 1.06 mm fitted displacement is large, so the absolute lattice parameters retain some calibration uncertainty. Repeated low-angle asymmetry, surface roughness, and phase-size tests either worsened the fit, sought bounds, or were unstable and were removed. Unused size and strain terms were neutralized. Only reproducible isotropic WO3 microstrain was retained. Preferred-orientation axes were selected by comparing multiple symmetry-distinct reflection families for each phase.

The final saved project was reopened and replayed natively over the full range. It converged with maximum shift/ESD = 0.020, no frozen variables, and no singular covariance directions. The CIFs and every column of `fit.csv` were exported from that same `final.gpx` state.

The tabulated ESDs are internal covariance estimates, not external accuracy. Texture, the SrWO4 analogue construction, and correlated profile/sample terms can produce larger systematic fraction errors. With no internal standard, amorphous content and absolute whole-sample phase fractions cannot be determined reliably; only fractions normalized over the modeled crystalline material are reported. The presence of the three phases and their approximate crystalline proportions are well supported, while the restrained SrWO4 oxygen coordinate and the precise monoclinic-versus-near-triclinic WO3 distortion should not be over-interpreted.
