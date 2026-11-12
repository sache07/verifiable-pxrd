# Powder XRD phase analysis

The crystalline model is 74.6 wt% wolframite ZnWO4, 18.9 wt% monoclinic WO3, and 6.5 wt% wurtzite ZnO. Fractions are normalized only over these modeled crystalline phases; the data do not determine an amorphous fraction.

| Phase | Space group | Cell (A, degrees) | Crystalline wt% |
|---|---|---|---:|
| ZnWO4, wolframite | P2/c | a=4.70514, b=5.73167, c=4.94312, beta=90.5944 | 74.60 |
| WO3, monoclinic | P21/c | a=7.70012, b=7.54394, c=10.52796, beta=136.0575 | 18.91 |
| ZnO, wurtzite | P63mc | a=3.25768, c=5.22269 | 6.49 |

The Cu K-alpha1/alpha2 GSAS-II refinement gives Rwp=7.9024%, Rp=4.3751%, and GOF=3.496 over all 8,301 points. A fresh atomic replay of `final.gpx`, with no optimization and without using its cached calculated profile, reproduces these fractions and Rwp and raises no profile-validity flags. Omitting ZnWO4, WO3, or ZnO raises Rwp to 51.38%, 22.18%, or 9.28%, respectively.

## Evidence and candidate ledger

- **Retained:** P2/c wolframite ZnWO4 is the only physically sound principal topology that explains the dominant peak families. All available AWO4 entries and one/two-substitution ABO4 analogues were enumerated. Controlled replacements with triclinic CuWO4-, scheelite CaWO4-, and C2/c HgWO4-derived Zn models remained near 50-51% Rwp after cell fitting. The FeWO4-derived P2/c coordinates contain a 1.50 A contact and its cell trial did not converge, so that branch is **unknown**, not treated as a profile rejection. The retained CoMoO4-derived topology has sensible coordination after refinement (minimum contact 1.76 A). A [100] March-Dollase term is strongly supported; alternative axes fit substantially worse.
- **Retained:** monoclinic WO3 is required by several independent peak families. All usable WO3 references were tested from common nuisance settings. COD 2311041 gives the best stable model; an equivalent triclinic representation was close but worse, while the distinct monoclinic/orthorhombic alternatives were much worse or nonconvergent. Thus the monoclinic WO3 phase is secure, although its exact setting/reference representation is less unique than the phase identity.
- **Retained:** wurtzite ZnO gives a stable positive scale. Rock-salt ZnO collapses to zero, and zincblende ZnO refines below about 0.3 wt% with no stable improvement.
- **Rejected after testing:** physically screened Zn3WO6, Zn2WO5, and fractional-occupancy ZnxWO3 bronze prototypes were constructed from one- and two-substitution parents. The best Zn3WO6 trial was only 0.16 wt% at fixed cell and required a 12% volume collapse while worsening the fit when its cell was released. Zn2WO5 and fractional bronze scales fell to about 0.002 and 0.02 wt%. Trials that diverged were left **unknown**, not counted as rejected.

Refinement complexity was staged. The retained model uses refined cells and scales, a smooth 14-term background, physically bounded instrument terms, one March-Dollase term for ZnWO4 and WO3, isotropic microstrain for ZnWO4/ZnO, and one supported [001] uniaxial microstrain term for WO3. Extra size, roughness, shift, anisotropy, independent displacement, and WO3 oxygen-coordinate terms were rejected because they were correlated, unstable, or physically implausible.

## Remaining uncertainty

Formal scale-covariance uncertainties are only about 0.09-0.15 wt%-points, but they exclude model choice, overlap, background, and texture systematics; roughly 1-2 wt%-points is a more realistic fraction uncertainty. The largest residual is the overlapping split family near 41.35 degrees 2-theta, with compensating negative lobes at about 41.14 and 41.57 degrees. Its shape is consistent with residual intensity/profile mismatch rather than a coherent set of peaks from a fourth phase. No additional phase structure or fraction can therefore be determined reliably. ZnWO4 oxygen positions are also less certain than its cell and heavy-atom framework because they correlate with the strong preferred-orientation correction.
