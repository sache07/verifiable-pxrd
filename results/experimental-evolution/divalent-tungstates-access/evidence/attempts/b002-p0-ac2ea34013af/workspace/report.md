# Powder XRD phase analysis

The crystalline pattern is described by three phases:

| Phase | Space group | Crystalline weight fraction |
|---|---:|---:|
| MnWO₄ (wolframite) | P 2/c | 60.13 wt% |
| WO₃ (triclinic) | P -1 | 20.16 wt% |
| Mn₃WO₆ (monoclinic analogue model) | C 2/c | 19.71 wt% |

These fractions are normalized over the modeled crystalline material. The zero-parameter replay of `final.gpx` gives Rwp = 9.70%, Rp = 5.93%, and Rexp = 1.99% on all 8,301 measured points.

## Evidence

The dominant reflection positions and relative intensities match wolframite MnWO₄. Triclinic WO₃ accounts for the residual precursor family and its many split reflections. A third family—especially lines near 19.85, 20.40, 35.11, 45.68–46.49, 54.46, 56.46, 59.33, 66.41, and 70.17° 2θ—requires a monoclinic C 2/c Mn₃WO₆-type phase. A Co₃TeO₆-type A₃BO₆ framework adapted to Mn/W fitted this family better than the tested Zn₃TeO₆ relative and Mn₂WO₅/MnW₂O₇ alternatives. The resulting approximately 60:20:20 mixture is also consistent with the nominal 1:1 Mn:W precursor balance.

A four-phase test initially assigned about 0.5 wt% to Mn₃O₄, but that scale refined to zero after the Mn₃WO₆ metric and intensities were improved. Mn₃O₄ is therefore not supported as a separate crystalline phase; any retained precursor is plausibly below roughly 1 wt% in this dataset.

## Uncertainty

MnWO₄ and WO₃ are confidently identified. Mn₃WO₆ is supported by its distinctive reflection family, chemistry, indexed monoclinic cell, and mass balance, but its detailed atomic arrangement cannot be determined reliably from this powder pattern alone. Its CIF is an analogue-constrained, bond-regularized Rietveld model, not a unique ab-initio structure solution. The refined Mn₃WO₆ texture reaches the allowed March–Dollase boundary, so its atomic coordinates and profile terms are model-dependent.

The phase fractions were stable near 60:20:20 across physically acceptable refinements; a practical systematic uncertainty is about ±2–3 absolute wt% per phase. The residual above counting statistics is mainly associated with the approximate Mn₃WO₆ intensity model and overlapping broadened WO₃ peaks. Amorphous content, if present, is not quantified.
