# PXRD phase analysis

## Result

The crystalline sample is modeled as two phases:

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| Scheelite CaWO4 | I 41/a | a = 5.24901, c = 11.38071 | 82.39 ± 0.15 wt% |
| Monoclinic WO3 | P 21/c | a = 7.29904, b = 7.54039, c = 10.51223, β = 133.0241 | 17.61 ± 0.15 wt% |

Fractions are normalized over the modeled crystalline phases. The quoted uncertainties are GSAS-II covariance estimates; a more realistic model-choice uncertainty is about ±0.7 wt% because the WO3 parent/coordinate and nuisance-profile choices shift the fraction more than the formal error. Amorphous content, if present, is not quantified.

The final fit has Rwp = 10.642%, Rp = 6.597%, Rexp = 2.617%, and GOF = 4.067 for 8,301 points. Because the metadata supplied no pointwise uncertainties, Poisson counting uncertainties (`sqrt(counts)`) were used; Rexp and GOF are conditional on that assumption.

## Evidence and model selection

The dominant peak family is indexed coherently by scheelite CaWO4. A second coherent lower-symmetry family, including the split features near 23.0–24.3° 2θ and matching lines across the full range, requires WO3. In final deletion tests, removing CaWO4 raises Rwp to 48.96%, while removing WO3 raises it to 17.92%.

Normalized COD parents 7219229 (CaWO4) and 2311041 (WO3) were used. Multiple monoclinic, triclinic, and orthorhombic WO3 parents were compared with matched profile, texture, restrained-coordinate, and independent-start refinements. The submitted monoclinic P 21/c parent was the simpler physically clean solution and reproducibly outperformed the other credible lineages after texture was included. CaO was rejected because its small apparent contribution required a roughly 2.4% cell collapse and did not explain a coherent residual family. A Ca-W bronze/TTB candidate required large anisotropic cell drift and unrealistically small crystallite size, and was also rejected.

The final nuisance model includes specimen shift, axial divergence, polarization/roughness, phase size and microstrain, mild CaWO4 [100] preferred orientation and size anisotropy, and stronger WO3 [001] preferred orientation. These effects and the phase fractions reproduced across independent profile starts. Both submitted CIFs pass occupancy and contact screening. CaWO4 retains the clean parent tetrahedral geometry (W–O = 1.764 Å). WO3 has two distorted, six-coordinate W sites with W–O ranges of 1.666–2.243 Å.

## Remaining uncertainty

The CaWO4 oxygen coordinates were restored to the defensible parent because unconstrained intensity-driven movement produced an overbonded 1.677 Å W–O tetrahedron. WO3 tungsten shifts were small, restrained, and reproducible, but its oxygen-site shifts were nonconvergent, larger than 0.2 Å, or branch-dependent; those oxygen coordinates therefore remain at the parent values and are not reliably determined by this powder pattern. The monoclinic WO3 assignment is preferred, but closely related lower-symmetry WO3 descriptions remain the principal structural uncertainty. No additional crystalline phase is supported reliably by the residual.

An independent reload/refinement of `final.gpx` reproduced Rwp within 0.000005 percentage point, each phase fraction within 0.0000002 absolute, and the calculated profile within 0.009 count RMS. The replay retained the same two positive phases and unchanged coordinates.
