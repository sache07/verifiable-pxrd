# Powder XRD phase analysis

The modeled crystalline assemblage is **ZnWO4 + WO3 + ZnO**. Weight fractions, normalized over these crystalline phases, are:

| Phase | Space group | Weight fraction | wt% |
|---|---:|---:|---:|
| ZnWO4 | P 2/c | 0.824118 | 82.412 |
| WO3 | P 21/n | 0.116938 | 11.694 |
| ZnO | P 63mc | 0.058943 | 5.894 |

The fresh, read-only GSAS-II replay of `final.gpx` gives Rwp = 5.3009%, Rp = 3.9310%, and GOF = 2.0061 over all 8301 points with Poisson weights, 1/max(observed counts, 1). `fit.csv` is that replayed profile.

## Evidence

ZnWO4 is supported by the dominant wolframite reflection family near 19.2, 24.1/24.8, 31.0, 36.6, and 41.5 degrees 2theta. Because the exact Zn-W-O product entry was withheld from the frozen index, two P 2/c wolframite analogues were compositionally adapted and compared at a common nuisance checkpoint. The MnReO4-derived start (COD 2100243; Mn→Zn, Re→W) reached the better physical basin; the CoMoO4-derived start was discarded. The bounded polish retained physical Zn-O, W-O, and O-O minima of 1.951, 1.804, and 2.573 A.

Monoclinic WO3 accounts for the distinct 23–29, 33–34, 50–55, and 62–65 degree families. A symmetry-equivalent, near-orthogonal adaptation of COD 2311041 was accepted. At equal profile development it improved Rwp from 7.703% to 7.320% relative to COD 1528915 and avoided that older, coarsely rounded model's 1.58 A O-O contact. The final WO3 minimum W-O and O-O distances are 1.674 and 2.539 A.

Wurtzite ZnO is independently supported at approximately 32.02, 34.89, 36.53, 47.88, and 56.69 degrees. Removing it worsened the fit across five separate reflection windows, so its positive contribution is not a single-peak artifact. After all three phases were accepted, every significant positive residual maximum mapped within 0.20 degrees of an accepted reflection; no coherent unassigned family remained.

The supplied bounded polish was run once and selected its converged heavy-light branch (no audit violations). Native forward replay regenerated the pattern without optimizing parameters, left `final.gpx` unchanged, and produced no profile-review flags.

## Remaining uncertainty

The fractions quantify only the modeled crystalline material; without an internal standard they do not measure amorphous content. Conditional GSAS-II scale ESDs are 0.083, 0.045, and 0.077 wt percentage points for ZnWO4, WO3, and ZnO, respectively, but these omit structural/profile model uncertainty. Correlations among common Lorentzian broadening, minor-phase size, polarization, and displacement parameters were observed; boundary or singular alternatives were rejected. Practical fraction uncertainty is therefore larger, especially for the two minor phases, and should be regarded as roughly a few wt percentage points rather than the formal ESDs.

Phase identity, topology, and space group are well supported. Fine oxygen coordinates—particularly in WO3—and phase-specific displacement parameters cannot be determined independently with high reliability from this overlapped laboratory pattern. A common Uiso = 0.005 A2 registration value was retained for all phases, rather than reporting unstable thermal refinements.
