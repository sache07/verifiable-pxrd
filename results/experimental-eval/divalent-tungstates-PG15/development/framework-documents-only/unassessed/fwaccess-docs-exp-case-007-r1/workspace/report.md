# Powder XRD phase analysis

The Cu Kα Bragg–Brentano pattern (PIXcel1D; 9.903–100.095° 2θ, 8301 points) is modeled by three crystalline phases. Fractions are normalized over those phases; no amorphous fraction can be obtained from these data.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MgWO₄, wolframite | P 2/c | a=4.69482, b=5.68024, c=4.93393, β=90.7744° | 74.92(17)% |
| WO₃, monoclinic | P 2₁/c | a=7.69820, b=7.54231, c=10.54087, β=136.0920° | 15.46(8)% |
| MgO, periclase | F m -3 m | a=4.21677 | 9.62(20)% |

The WO₃ cell is the valid nonstandard P 2₁/c setting used by the source structure. The quoted parentheses are least-squares ESDs only; specimen corrections and fixed temperature factors give an estimated additional uncertainty of roughly 1 absolute wt% per phase, most importantly for MgO.

## Evidence

Wolframite MgWO₄ accounts for the dominant peaks, including the characteristic features at approximately 19.24, 24.22, 30.81, and 31.12° 2θ. Monoclinic WO₃ is required by the resolved low-angle multiplet near 23.43–24.67° and its matching higher-angle lines. Periclase MgO has independent positive-scale reflections, especially at 43.21 and 62.54° (with its higher-angle series); omitting it leaves coherent residual peaks.

Reference parents were COD 9013902 (MgWO₄), COD 2311041 (WO₃), and COD 9000499 (MgO). At a common fixed profile the selected WO₃ parent gave Rwp 9.43%, compared with 9.76% for COD 1528915 and 12.20% for an orthorhombic candidate. A triclinic P-1 model reached 9.39% only by adding cell degrees of freedom and refined back toward monoclinic metrics, so it was rejected as over-parameterized. A three-phase Le Bail extraction assigned every strong peak family (Rwp 7.24%), with no reproducible evidence for a fourth crystalline phase.

The final constrained Rietveld fit has Rwp=7.860%, Rp=5.485%, and GOF=2.750. It includes physical size/microstrain broadening, a Suortti low-angle roughness correction, and weak [001] March–Dollase texture for MgWO₄. Final calculated and difference curves are in `fit.csv`; the exact replayable project is `final.gpx`.

## Remaining uncertainty

The angular zero and sample-height displacement are nearly perfectly correlated without an internal standard. The project therefore uses their best-fit effective angular correction; the absolute cell parameters have additional calibration uncertainty beyond their formal ESDs. MgWO₄ cation/oxygen coordinates and WO₃ W coordinates were allowed only small, symmetry-preserving adjustments. WO₃ oxygen shifts were not reliably determined by this W-dominated laboratory X-ray pattern and remain at the neutron-reference positions. MgO has only six reflections in range, so its temperature factor and scale are coupled; its 9.62 wt% fraction is secure as a phase-level estimate but not to the formal 0.20 wt% precision.
