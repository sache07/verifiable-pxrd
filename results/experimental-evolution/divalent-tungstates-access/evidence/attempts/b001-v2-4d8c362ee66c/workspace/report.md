# Powder XRD phase analysis

The pattern is described by four crystalline phases. Fractions are normalized over these modeled crystalline phases; amorphous material, if present, is not quantified.

| Phase | Space group | Reference used to initialize the model | Weight fraction |
|---|---:|---:|---:|
| CuWO4 | P -1 | COD 4000806 | 0.65191 (65.19 wt%) |
| WO3 | P 21/c | COD 2311041 | 0.18901 (18.90 wt%) |
| Cu3WO6 | P a -3 | COD 1527404 | 0.13397 (13.40 wt%) |
| CuO (tenorite) | C 2/c | COD 1011194 | 0.02512 (2.51 wt%) |

## Evidence

Whole-pattern searches and common-state multiphase refinements independently supported the CuWO4, WO3, and Cu3WO6 reflection families. Coherent residual peaks near 35.1, 38.3, 48.4, 58.1, and 65.3° 2theta required tenorite CuO; its scale remained stable when refined with the other three phases. Cu2O and Cu4O3 precursor alternatives collapsed in that same state.

The final atomic replay uses the complete original grid (8301 points) and gives Rwp = 2.98895%, Rp = 2.20729%, and goodness of fit = 1.85355. The replay regenerated fresh reflection lists from `final.gpx`, reported no profile-review flags, and reproduced the listed fractions. The four phase RF-squared values in the final refinement are 2.42%, 1.74%, 1.84%, and 2.48%, respectively.

Residual-directed tests included ordinary Cu/O/W candidates and six transferred CuWO4 ABO4 frameworks: P2/c, I41/a, P21/c, C2/c, C2/m, and Pnna, using both one- and two-element substitutions. Every replacement gave a fresh-replay Rwp of about 43-50%, versus 3.53% for the then-current four-phase state. Addition scales were 0-0.15 wt% in the fixed common state. P2/c CuWO4 rose only to 0.29 wt% on an ordinary refit and was strongly correlated with the dominant triclinic CuWO4, so it is retained only as an unresolved trace possibility and is not quantified as a fifth phase. One C2/m addition optimization stalled and is treated as unknown rather than negative evidence.

## Physical checks and uncertainty

All submitted CIFs pass the occupancy/contact screen with no flagged contacts. Their calculated densities are 8.05, 7.27, 6.66, and 6.53 g cm-3; shortest unlike-atom contacts are 1.79 Å (CuWO4), 1.73 Å (WO3), 1.74 Å (Cu3WO6), and 1.91 Å (CuO).

Phase identity and the four-phase inventory are secure. Formal scale-only errors are much smaller than likely systematic error; practical uncertainty is approximately 1-2 wt% absolute for the major phases and about 0.3-0.5 wt% absolute for CuO. The detailed WO3 oxygen coordinates were weakly determined and were regularized toward the reference framework; its cell, composition, symmetry, and W sublattice are more reliable than its exact oxygen displacements. The trace P2/c CuWO4 fraction cannot be determined reliably. Correlated residuals and a goodness of fit above one indicate that small profile/systematic errors remain.
