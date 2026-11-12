# Powder XRD phase analysis

The full-grid four-phase refinement gives Rwp = 10.65%, Rp = 6.62%, Rexp = 1.77%, and GOF = 6.01 over all 8,301 measured points (9.9034–100.0946° 2θ). Weight fractions are normalized over the modeled crystalline phases; no amorphous fraction was determined.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P2/c, COD 1520200 | a=4.79622, b=5.71111, c=4.97918, β=91.1166 | 70.19(15)% |
| γ-WO3 | P21/n, COD 1528915 | a=7.30174, b=7.54319, c=7.68943, β=91.0418 | 14.76(10)% |
| MnWO4, indexed dense polymorph | P2/c, indexed/analogue-derived | a=4.33210, b=4.44548, c=6.20568, β=92.2673 | 10.86(11)% |
| MnO, wurtzite | P63mc, COD 4117966 | a=3.37060, c=5.37697 | 4.19(15)% |

## Evidence

Wolframite MnWO4 and monoclinic γ-WO3 account for the dominant peak families and refine close to their reference metrics. A coherent residual family at approximately 20.32, 20.88, 29.14, 32.26, 35.32/35.62, 46.20/47.02, 54.89/55.85, 64.88, 66.96, 70.64, 74.87, and 79.36° indexes as a primitive monoclinic cell with M20 ≈ 197. A P2/c Le Bail check reproduced that family, and the submitted bond-valence-screened model retains Mn2+/W6+ coordination after bounded heavy-atom refinement. Same-composition and transferred-topology alternatives were compared in the same multiphase state; lower numerical minima with bad contacts or incorrect bond valences were rejected.

After adding that indexed phase, wurtzite MnO gives a stable nonzero scale and lowers Rwp from 11.37% to 10.83% before final coordinate/profile refinement. Tetragonal and orthorhombic Mn3O4 and two Mn2O3 topologies collapse to zero scale; rocksalt MnO refines to only about 0.29 wt%. The final phase inventory gives Mn:W = 0.986 on a molar basis, independently agreeing with the nominal 1:1 precursor ratio. The Cu Kα doublet and Bragg–Brentano geometry were fixed from metadata; the refined specimen displacement is about −654 µm.

## Remaining uncertainty

The first MnWO4, γ-WO3, and their combined majority fraction are secure. The 10.86 wt% P2/c MnWO4 phase is lower confidence: its reflection lattice is secure, but its compact cell and atom arrangement have no exact reference match in the frozen index. Its coordinates are a physically screened structural solution, not a unique ab initio determination, and several indexed-family intensities remain imperfect. Across acceptable profile choices its fraction is approximately 10–11 wt%; the formal GSAS-II uncertainty does not include this model uncertainty.

Wurtzite MnO is supported by the residual profile and whole-inventory balance, but it is a metastable topology and contributes only 18 reflections. Its atom coordinates were therefore held at the reference values while its cell and scale were refined. Its fraction is correlated with the indexed MnWO4 phase and is better regarded as roughly 4–5 wt% than as known to the formal 0.15 wt% standard uncertainty. The high GOF and correlated residuals show that counting-statistical uncertainties alone understate the remaining systematic/model error.

The submitted `final.gpx` is the best full-grid physical checkpoint. A candidate-only isotropic microstrain term was retained; light-atom moves that produced short O–O contacts and MnO broadening that collapsed to a 1 nm size were rolled back.
