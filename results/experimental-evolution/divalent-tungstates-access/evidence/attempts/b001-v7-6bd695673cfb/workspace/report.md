# Powder XRD phase analysis

## Result

Four crystalline phases are required. Weight fractions are normalized over those modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CuWO4 | P -1 | a=4.62189, b=5.74771, c=4.85958; α=91.3246, β=91.4794, γ=84.7040 | 65.407 wt% |
| Cu3WO6 | Pa-3 | a=9.79164 | 13.127 wt% |
| WO3 | P21/c | a=7.68464, b=7.55922, c=10.50818; β=136.0058 (alternative setting) | 19.176 wt% |
| CuO | C2/c | a=4.66992, b=3.43112, c=5.12047; β=99.5566 | 2.291 wt% |

The formal GSAS-II scale-derived standard uncertainties are 0.020, 0.015, 0.015, and 0.013 wt%, respectively. These are counting/refinement uncertainties only; reference-model and profile systematics are larger, particularly for minor CuO.

## Evidence and model selection

The dominant triclinic family is CuWO4. A second distinct cubic family is indexed by Pa-3 Cu3WO6, while the remaining strong non-cupric-oxide reflections require monoclinic WO3. After these three phases were fully developed, the coherent residual family near 35.1, 38.3, 48.5, and 61.2° 2θ was indexed by tenorite CuO. Once CuO was included, no coherent residual family remained unassigned; the remaining structured residuals coincide with accepted reflections and are profile/intensity residuals rather than a fifth indexed phase.

For WO3, symmetry-diverse references were compared at equal profile checkpoints. COD 2311041 gave the best physical basin; COD 2106293 and 1528915 were worse and their size terms reached the supplied upper bound. For CuO, COD 1011194 was slightly better than COD 9016057 at equal development. The final bulk Cu/W molar ratio implied by the four fractions is 1.006, consistent with the CuO + WO3 chemical context.

CuWO4 and Cu3WO6 strain anisotropy was rejected because it either collapsed to isotropic behavior or gave start-dependent/nonterminal solutions. WO3 [001] uniaxial microstrain converged from two starts to the same interior basin and was retained. March-Dollase texture and surface roughness tests gave negligible, ambiguous, or bound-pinned contributions and were not retained.

## Fit and checks

The refinement used the metadata Cu Kα1/Kα2 wavelengths (1.540598/1.544426 Å), fixed Kα2/Kα1 ratio 0.5, and the complete measured 10–100° grid.

The independently regenerated full-grid atomic profile gives Rwp = 1.8768%, Rp = 1.4172%, goodness of fit = 1.163, and a counting-statistical Rwp floor of 1.6163% for 8,301 points. The required bounded polish selected its phasewise branch (pre-polish Rwp 2.1263%); its audit found no geometry, fraction-collapse, coordinate-bound, or convergence violations. Minimum metal–oxygen distances remain physical, and the independent replay regenerated all reflections without modifying the project or raising profile-review flags.

The submitted `final.gpx` is byte-identical to the accepted `polished.gpx` (SHA-256 `fa04ea8ea1eeeee95a77c93ec3117d21e23524956c8f1b7ee331078c602ded06`). All CIFs, fractions, and `fit.csv` were exported from that exact project/replay.

## Remaining uncertainty

- CuO is only about 2.3 wt%. Its phase identity and positive contribution are reproducible, but detailed coordinates and its crystallite size are not independently reliable; the size trial reached 1.5 µm and was fixed rather than reported as a determination.
- WO3 oxygen coordinates are less constrained by X-ray data than the W sublattice. Two oxygen-coordinate components that reached the ±0.10 Å polish window were reverted, and the WO3 common Uiso trial reached the laboratory upper bound and was rolled back to the prior interior value.
- Zero offset, specimen displacement, and axial-divergence asymmetry are partly confounded. Zero was fixed at -0.03894°, and displacement was frozen at a tested 767.49 µm checkpoint before SH/L was settled; the phase cells and fractions are replay-stable, but the individual correction terms should not be interpreted as independent metrology.
- No additional crystalline phase is justified by the residual. Trace phases below the pattern's detection capability, and any amorphous fraction, cannot be excluded or quantified from this scan alone.
