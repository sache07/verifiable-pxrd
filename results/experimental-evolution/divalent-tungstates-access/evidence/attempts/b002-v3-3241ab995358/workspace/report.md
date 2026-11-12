# Powder-XRD phase analysis

The 700 °C WO₃ + ZnO reaction is partially complete: the pattern is modeled by dominant ZnWO₄ plus residual WO₃ and ZnO. Fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Crystalline wt.% |
|---|---|---|---:|
| ZnWO₄, wolframite | P 2/c | a=4.70424, b=5.73704, c=4.93550, β=90.6387 | 82.08 |
| γ-WO₃, monoclinic | P 2₁/c | a=7.70843, b=7.52619, c=10.54231, β=136.0732 | 12.82 |
| ZnO, wurtzite | P 6₃mc | a=3.25750, c=5.18616 | 5.10 |

The final full-grid GSAS-II replay gives Rwp=3.090%, Rp=2.344%, GOF=1.169 over all 8,301 measured points. The replay regenerated reflection lists and structure factors from `final.gpx`; it used no cached calculated profile and raised no physical-profile review flags.

## Evidence

The dominant reflections and their intensity pattern require wolframite ZnWO₄. A P 2/c model with [111] preferred orientation accounts for the principal family across the complete angular range. A second coherent family, including peaks near 23.4, 27.0, 29.2, 33.6 and 34.5° 2θ, is indexed by monoclinic γ-WO₃. Alternative monoclinic WO₃ settings were close, but the submitted P 2₁/c model gave the best physically stable refinement.

Residual peaks at the wurtzite positions, especially the 31.7–36.3° region, require ZnO. Adding wurtzite ZnO reduced Rwp from about 5.35% for the ZnWO₄+WO₃ model to 3.76% before final three-phase relaxation. Its scale remained positive under cell, size, strain and texture refinement. The final fractions also give an overall crystalline Zn:W molar ratio of about 1.03, consistent with the nominal 1:1 precursor ratio. No coherent residual reflection family remains to justify another crystalline phase.

## Remaining uncertainty

The γ-WO₃ identity, cell and fraction are supported, but its oxygen coordinates are not reliably determined by this pattern: unstable oxygen-only trials were rejected, and the submitted oxygen substructure remains at the physically clean reference coordinates while the W sites were refined. Equivalent conventional monoclinic settings therefore should not be interpreted as distinct WO₃ polymorphs here. The ZnO oxygen coordinate is also less precise than the heavy-atom framework, although it remained physical and stable after texture correction.

Preferred orientation is appreciable in all three phases, so systematic fraction uncertainty from texture and overlap is larger than formal counting-statistical errors. The reported values are defensible crystalline-phase fractions, but amorphous content—and therefore absolute whole-sample phase fractions—cannot be determined from this refinement.
