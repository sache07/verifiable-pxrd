# Powder XRD phase analysis

The pattern is modeled as two crystalline phases:

| Phase | Structure | Weight fraction* |
|---|---|---:|
| NiWO4 | wolframite, monoclinic `P 1 2/c 1` | 0.7540 (75.40 wt%) |
| WO3 | monoclinic `P 1 21/c 1` | 0.2460 (24.60 wt%) |

\*Normalized over the modeled crystalline phases. The formal covariance-matrix
standard uncertainty is 0.00145 for each fraction, but a more realistic uncertainty
is approximately ±0.01 because the instrument profile was not calibrated and scale,
surface roughness, displacement parameters, and weak-site coordinates are correlated.
No amorphous fraction can be determined from this measurement.

## Evidence

The dominant reflections at approximately 19.20, 23.90, 24.85, 30.87, 36.53,
41.62, and 54.58 degrees 2theta index to monoclinic wolframite NiWO4. The distinct
23.05/23.54/24.29 degree triplet and the 33–34.5 degree group require monoclinic
WO3. A rocksalt NiO model was tested and rejected: in particular, its strongest
diagnostic reflection near 43.38 degrees is absent, and the other NiO positions do
not form a coherent positive residual pattern. No additional crystalline phase is
supported by the final difference curve.

The starting models were COD 5910277 for NiWO4 (reduced to its valid asymmetric
unit because that old CIF lists symmetry-equivalent atoms explicitly) and COD
2311041 for WO3. A metrically near-triclinic WO3 candidate fitted almost
indistinguishably, but did not improve the screening fit despite its extra metric
degrees of freedom; the room-temperature monoclinic `P21/c` model was therefore
retained. The WO3 polymorph distinction is not completely unique at this peak
breadth.

## Refinement and uncertainty

The GSAS-II refinement used the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5
intensity ratio, Poisson counting weights, a smooth 15-term background, refined
cells/scales, bounded instrumental and specimen-profile terms, surface roughness,
one common isotropic displacement parameter per phase, and modest Ni/W coordinate
adjustments. NiWO4 oxygen coordinates were allowed to move only within about 0.05
angstrom per cell direction from the reference; two z components reached that
limit and should be regarded as restrained estimates. WO3 oxygen-coordinate
refinement was not retained because most components reached their bounds for a
negligible profile improvement, so those sites remain reference-based and cannot
be determined reliably from this pattern alone.

The final agreement is `Rwp = 4.176%`, `Rp = 3.216%`, `Rexp = 3.479%`, and
goodness-of-fit `Rwp/Rexp = 1.200`. The submitted CIFs, fractions, and `fit.csv`
were exported directly from `final.gpx`.
