# Powder XRD phase analysis

The accepted model contains two crystalline phases: scheelite CaWO4 and low-temperature monoclinic WO3. Their refined fractions, normalized only over these modeled crystalline phases, are 85.09(6) wt% CaWO4 and 14.91(6) wt% WO3. Parentheses give the one-sigma GSAS-II covariance uncertainty; a more realistic uncertainty allowing for model and profile choices is approximately ±1 wt% for each fraction.

| Phase | Space group | Refined cell (angstrom, degrees) | Crystalline wt% |
|---|---|---|---:|
| CaWO4 (scheelite) | I 41/a (No. 88) | a = b = 5.23764, c = 11.33362 | 85.09(6) |
| WO3 (monoclinic) | P 21/n (No. 14) | a = 7.31453, b = 7.55676, c = 7.69388, beta = 91.0562 | 14.91(6) |

## Evidence and model choice

The dominant reflections at about 18.27, 28.42, 31.22, 33.85, 46.88, and 57.65 degrees 2theta form the characteristic scheelite CaWO4 pattern. The separate 22.76/23.18/23.98 degree triplet and its higher-angle reflection family identify monoclinic WO3. This is chemically consistent with incomplete reaction of the reported WO3 and CaCO3 precursors at 650 degrees C.

The CaWO4 model was based on COD 7219229. For WO3, distinct monoclinic, triclinic, orthorhombic, tetragonal, and hexagonal topologies were checked; only the low-temperature monoclinic topology accounts for the split low-angle family and the full pattern. The final WO3 coordinates come from the physically coordinated neutron structure COD 2311041, transformed from P 21/c to the equivalent near-orthogonal P 21/n setting. Its two W sites remain six-coordinate with W-O distances of 1.719-2.164 angstrom; CaWO4 has tetrahedral W-O = 1.759 angstrom. A competing monoclinic coordinate set had poor W-O geometry and was rejected. High-pressure CaWO4, Ca3WO6, CaO, residual calcite, and the W-rich Ca-W-O reference were also inconsistent with their diagnostic reflections.

After accepting both phases, every coherent peak family indexed to one of them. The largest remaining local mismatch near 29 degrees lies in an overlap of accepted CaWO4/WO3 reflections; there is no repeatable residual family supporting a third crystalline phase. Texture tests refined to nearly random orientation, WO3 size remained unchanged at its starting instrument-limited value, and both phase microstrains collapsed to zero. Surface-roughness and unconstrained coordinate branches either hit parameter bounds or produced nonphysical geometry and were not retained.

## Refinement and uncertainty

The final GSAS-II refinement used the complete 9.903-100.095 degree grid, the metadata Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, Poisson counting weights because point uncertainties were not supplied, a 16-term smooth Chebyshev background, refined phase scales and cells, specimen displacement, instrumental profile terms, and CaWO4 isotropic crystallite size. Atomic coordinates were kept at the screened physical parent values because coordinate relaxation was not robustly supported by the X-ray data.

Final whole-profile statistics are Rwp = 3.5411%, Rp = 2.6959%, Rexp = 3.1382%, and Rwp/Rexp = 1.1284. A zero-cycle reload reproduces Rwp to 0.000001 percentage point with no frozen parameters, so `final.gpx`, the exported CIFs, and `fit.csv` describe the same checkpoint.

The phase identities and crystalline two-phase ratio are well supported. The formal fraction errors do not include reference-model, absorption, microabsorption, or background systematics. No internal standard was supplied, so amorphous material and any very weak or fully overlapped crystalline component cannot be quantified; the reported fractions must not be interpreted as absolute bulk fractions. Oxygen coordinates, especially in WO3, are reference-derived rather than independently determined by this powder pattern.
