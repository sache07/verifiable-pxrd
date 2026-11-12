# Crystalline phase analysis

The pattern is modeled by three crystalline phases: scheelite SrWO4, residual monoclinic WO3, and residual orthorhombic SrCO3. Fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell (A, degrees) | CIF |
|---|---:|---:|---|---|
| SrWO4 | I 41/a | 0.60178 (formal s.u. 0.00140) | a = 5.39312, c = 11.89988 | `phase_srwo4.cif` |
| WO3 | P 21/c | 0.24770 (formal s.u. 0.00113) | a = 7.69357, b = 7.55527, c = 10.51422, beta = 136.1174 | `phase_wo3.cif` |
| SrCO3 | Pnma | 0.15052 (formal s.u. 0.00141) | a = 6.02353, b = 5.09731, c = 8.39409 | `phase_srco3.cif` |

The WO3 cell is the nonstandard P21/c setting used by the source record. The detailed atomic coordinates were not independently determined from this three-phase laboratory pattern: source coordinates were fixed while cells, phase scales, and supported profile terms were refined.

## Evidence and chemical balance

The SrWO4 assignment accounts for the strong families at approximately 17.456, 27.203, 32.636, 47.143, and 55.531 degrees 2theta. The characteristic monoclinic-WO3 group at 22.508, 22.943, and 23.834 degrees requires WO3, while the 24.6-25.3 degree and additional weaker families require Pnma SrCO3. These are also the chemically expected product and unreacted precursors for heating SrCO3 with WO3 at 650 degrees C.

On a 100 g crystalline-product basis, the refined fractions correspond to 0.17939 mol SrWO4, 0.10684 mol WO3, and 0.10196 mol SrCO3. Reconstructing the precursor inventory gives Sr/W = 0.983 and nearly equal residual SrCO3/WO3 moles (0.954), consistent with the charge-balanced reaction SrCO3 + WO3 -> SrWO4 + CO2. The implied CO2 loss is about 7.90 g per 100 g of final crystalline material.

Charge-balanced non-1:1 products, including Sr2WO5, Sr3WO6, SrW2O7, and Sr3W2O9, were searched. The exact Sr3W2O9 record (COD 2311977) was explicitly added as a watch-list phase after the three-phase model had converged; its scale collapsed to the positive lower bound (about 1e-12), and its unique low-angle families were absent. It was therefore rejected as unsupported rather than co-retained with an alternative structure.

## Structural and profile model

The SrWO4 model was adapted from the passing, exact-W scheelite analogue EuWO4 (COD 1561850) by Eu-to-Sr substitution. Passing SrMoO4, SrCrO4, and CaMoO4-derived competitors were tested under the same restrained model. A free SrWO4 oxygen-coordinate trial reduced Rwp but produced an implausible W-O distance near 2.02 A, so it was rejected; the retained fixed-coordinate model gives four W-O distances of 1.7694 A and Sr-O distances of 2.569-2.599 A. Ambient monoclinic WO3 COD 2311041 outperformed tested triclinic, alternate monoclinic, and orthorhombic WO3 records. Pnma SrCO3 COD 9008198 was retained over a reviewed disordered carbonate alternative.

Poisson standard uncertainties, sqrt(counts), were used because pointwise uncertainties were not supplied. The Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio came from the metadata. The inactive phase broadening terms were set to 10 micrometres size and zero strain, preferred-orientation ratios to one, and roughness to zero before profile testing. The accepted common profile refines nonnegative W and X; U refined to zero and was pruned/fixed. One angular correction, the reflection-geometry sample shift (1056.7 micrometres), was retained. No extra SH/L asymmetry, transparency, roughness, extinction, or SrCO3 texture term was supported.

The SrWO4 intensity families require a fourth-order spherical-harmonic texture correction (texture index 1.175), and WO3 requires a March-Dollase term along [1 0 -1] (ratio 1.246). Two SrWO4 fourth-order coefficients are 95.66% correlated, so their individual values are not uniquely interpretable; coefficient-hold replays changed the fractions by less than 0.4 weight-percent point. Isotropic WO3 microstrain, 4440(101) ppm, was retained after a direct profile challenge: the neutral model gave Rwp = 3.967%, a WO3 size-only model gave 3.577% with about 0.15 micrometre size, and the strain model gave 3.486%. A combined size/strain test drove size back to the neutral 10 micrometres with an uncertainty of thousands of micrometres, so size was pruned. SrCO3 size and strain terms were unsupported.

The final project was saved, reopened, and replayed twice over the complete 9.9034-100.0946 degree range. It converged with Rwp = 3.4856%, Rp = 2.6863%, Rexp = 2.8612%, goodness of fit = 1.2203, and maximum shift/s.u. = 0.045. Numerical checks on isolated SrWO4 families were:

| Family | Position obs/calc (degrees) | FWHM obs/calc (degrees) | Left/right half-width obs | Left/right half-width calc |
|---|---:|---:|---:|---:|
| 112 | 27.20274 / 27.19188 | 0.19811 / 0.19868 | 0.10027 / 0.09785 | 0.08998 / 0.10870 |
| 116 | 51.39135 / 51.39135 | 0.24955 / 0.25329 | 0.09494 / 0.15460 | 0.09606 / 0.15723 |
| 240 | 78.91594 / 78.93767 | 0.22795 / 0.20255 | 0.07135 / 0.15660 | 0.09617 / 0.10639 |

The remaining high-angle width/asymmetry mismatch and residual serial correlation (Durbin-Watson 1.34) indicate modest unmodeled profile systematics. Adding less identifiable profile terms was not justified by replay stability.

## Health checks and uncertainty

`learned/cif_health.py` reports `pass` for all three final CIFs: there are no partial/mixed sites, invalid occupancies, or hard contacts. Final local geometry is chemically plausible: WO3 has distorted W-O distances of 1.718-2.163 A, and SrCO3 has C-O distances of 1.291-1.304 A.

Phase identities and cells are reliable at the stated level, but detailed coordinates and displacement parameters remain source-model dependent. The formal fraction s.u. values above reflect counting statistics only. Texture/source-model comparisons indicate more realistic uncertainties of roughly 2-4 absolute weight-percent points for the major-phase fractions; rounded practical estimates are SrWO4 60 +/- 3 wt%, WO3 25 +/- 3 wt%, and SrCO3 15 +/- 2 wt%. No amorphous fraction can be determined without an internal standard, so these values must not be interpreted as absolute bulk fractions if amorphous material is present.
