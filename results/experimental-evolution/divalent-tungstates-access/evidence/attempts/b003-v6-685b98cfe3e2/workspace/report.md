# Powder XRD phase analysis

## Result

Three crystalline phases are required. Weight fractions are normalized over those modeled crystalline phases; they are not absolute fractions of the whole specimen.

| Phase | Structural model | Refined cell (Å, °) | Crystalline weight fraction |
|---|---|---|---:|
| MnWO4 | wolframite, P2/c; COD 1520200 starting model | a=4.79464, b=5.70538, c=4.97316, β=91.1638 | 0.63733 (63.733 wt%) |
| WO3 | monoclinic, P21/c; COD 2311041 starting model | a=7.28471, b=7.52582, c=10.51840, β=133.078 | 0.18082 (18.082 wt%) |
| Mn3WO6 | rhombohedral, R-3; COD 2002703 starting model | a=b=8.88646, c=10.47708 | 0.18185 (18.185 wt%) |

The final GSAS-II fit has Rwp = 2.7993%, Rp = 2.0518%, Rexp = 1.4263%, and goodness of fit = 1.9656 for 8,301 points. A fresh, no-refinement replay from `final.gpx` reproduced the fractions exactly and Rwp to 0.0000002 percentage point, with no profile-review flags.

## Evidence and model selection

The dominant wolframite MnWO4 model accounts for the families near 15.27°, 18.25°, 23.46°, and 29.78–30.23° 2θ. Monoclinic WO3 is required by the 22.90–24.18° cluster and reflections near 26.41° and 33.05–33.95°. Mn3WO6 is independently required by the 19.67–20.20°, 25.25°, 28.49°, 31.68°, and 35.02° families. These assignments persist across the full pattern rather than relying on isolated peaks. After all three phases are included, the remaining intensity errors are centered on their accepted reflections; no coherent unassigned reflection family remains.

Exact-composition WO3 references were compared because one numerically attractive P21/c candidate (COD 1528915) contained an implausible approximately 1.57 Å fully occupied O–O contact. It was rejected despite its slightly better numerical fit. COD 2311041 gives the best fit among the physically acceptable tested WO3 models. In the submitted coordinates, the shortest W–O/O–O distances are 1.748/2.534 Å for WO3, 1.796/2.458 Å for MnWO4, and 1.902/2.608 Å for Mn3WO6; the independent occupancy/contact screen passed all three CIFs. The aggregate modeled composition is Mn:W ≈ 1.01:1, an additional consistency check on the partition between residual WO3 and Mn-rich Mn3WO6.

The Rietveld model used the reported Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio, a 12-term Chebyshev background, phase scales and cells, zero and specimen displacement, supported instrumental/profile terms, crystallite-size and microstrain terms, March–Dollase preferred orientation, phase-common displacement parameters, and bounded atomic-coordinate refinement. The prescribed staged polish selected the converged heavy-then-oxygen coordinate branch: Rwp improved from 3.0017% to 2.7993%, all geometry audits passed, and no phase fraction moved by more than 0.25 percentage point. MnWO4 anisotropic strain reached the allowed axial/equatorial ratio bound of 4, so that broadening parameter should be regarded as phenomenological.

## Remaining uncertainty

The phase inventory and structure types are well supported, and approximate crystalline fractions are reliable. The formal least-squares fraction uncertainties (about 0.04–0.06 wt%) are too optimistic because pointwise standard uncertainties were not supplied and scale, texture, profile, and coordinate parameters are correlated. A more realistic interpretation is roughly ±1–2 wt% absolute for each reported crystalline fraction. Oxygen coordinates, especially in WO3, are less precisely determined than the heavy-atom frameworks.

No modeled crystalline phase is structurally unresolved. However, this powder pattern cannot determine an amorphous fraction or absolute crystallinity, and trace phases below the residual/detection level cannot be excluded; their structures and fractions therefore cannot be determined reliably from this dataset.
