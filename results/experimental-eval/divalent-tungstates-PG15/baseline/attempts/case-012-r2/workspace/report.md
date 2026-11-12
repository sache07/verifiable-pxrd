# PXRD phase analysis

## Result

The pattern is described by two crystalline phases, normalized over the modeled crystalline material:

| Phase | Structure | Weight fraction | Refined cell (Å, °) |
|---|---|---:|---|
| NiWO₄ | wolframite, P 2/c (No. 13) | 76.37 wt% | a=4.59940, b=5.66165, c=4.90904, β=89.9744 |
| WO₃ | room-temperature monoclinic, P 2₁/n (No. 14) | 23.63 wt% | a=7.30070, b=7.53201, c=7.68680, β=90.8146 |

For practical reporting, use NiWO₄ 76.4 ± 1.0 wt% and WO₃ 23.6 ± 1.0 wt% (absolute). The GSAS-II counting-statistical ESD is only about 0.10 wt%, but it does not include instrumental-profile, preferred-orientation, microabsorption, or model-choice uncertainty. Amorphous material, if present, cannot be quantified without an internal standard.

## Evidence and refinement

NiWO₄ accounts for the dominant reflections at approximately 15.6, 19.2, 23.9, 24.85, 30.87, 36.53, 41.62, 52.27, 54.58, and 62–66° 2θ. Monoclinic WO₃ is required by its resolved 23.05/23.54/24.29° triplet and companion peaks near 26.53, 28.83, and 33–34°. This assignment is chemically consistent with reaction of the stated NiO and WO₃ precursors at 900 °C. A three-phase trial including rocksalt NiO drove the NiO scale to zero; the characteristic non-overlapped NiO reflection near 43.3° is absent. No residual peak series supports another crystalline phase.

The starting models were COD 5910277 (NiWO₄, reduced to its asymmetric unit) and COD 1528915 (WO₃). The submitted GSAS-II refinement used the stated Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio, a smooth 12-term Chebyshev background, refined phase scales and cells, zero offset (-0.0942°), effective polarization (0.605), simple U/W instrumental broadening, phase-specific isotropic size broadening, and small March–Dollase corrections. NiWO₄ coordinates were refined; WO₃ coordinates were held at the starting literature model because minority-phase coordinate refinement was strongly correlated. The refined coherent-domain sizes (53 nm NiWO₄ and 47 nm WO₃) should be viewed as effective profile parameters because no calibrated instrumental profile was supplied.

The final fit has Rwp=4.629%, Rp=3.483%, Rexp=3.479%, GOF=1.334, and χ²=14665.5 for 8282 points and 38 refined parameters. The refinement converged without Hessian singularities. Detailed oxygen positions, the small texture corrections, and the formal cell ESDs should not be over-interpreted because the instrument profile and sample displacement were not independently calibrated.

Files: [NiWO4.cif](NiWO4.cif), [WO3.cif](WO3.cif), [fit.csv](fit.csv), [final.gpx](final.gpx), and [result.json](result.json).
