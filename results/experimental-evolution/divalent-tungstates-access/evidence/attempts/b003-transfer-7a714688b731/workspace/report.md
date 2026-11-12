# Powder XRD phase analysis

The crystalline sample is modeled with three phases. Weight fractions are normalized over these modeled crystalline phases only.

| Phase | Space group | Weight fraction | Refined cell |
|---|---:|---:|---|
| MnWO4 (wolframite) | P 2/c (No. 13) | 63.173 wt% | a = 4.79106, b = 5.70100, c = 4.96906 A; beta = 91.1630 deg |
| Mn3WO6 | R -3 (No. 148) | 17.978 wt% | a = 8.87917, c = 10.47014 A |
| WO3 | P 21/c (No. 14) | 18.849 wt% | a = 7.27929, b = 7.52015, c = 10.51053 A; beta = 133.0796 deg |

## Evidence

MnWO4 accounts for the dominant families near 15.27, 18.25, 23.46, and 29.8-30.3 deg 2theta. Mn3WO6 is required by the distinct reflections near 19.67, 20.20, 28.48, 31.68, 35.02, and 46.43 deg, while WO3 accounts for the 22.9-24.2 deg and 33-34 deg multiplets. Removing any one phase leaves strong, structured residuals. All three refined scale factors are positive and stable.

The full 10-100 deg pattern was refined in GSAS-II with the supplied Cu Kalpha1/Kalpha2 doublet and Bragg-Brentano geometry. Refined terms included background, phase scales and cells, angular zero/specimen displacement, instrumental and phase peak broadening, March-Dollase texture, surface roughness/polarization, common phase Uiso values, and bounded symmetry-preserving coordinates. An independent replay of `final.gpx` gives Rwp = 2.77595%, Rp = 2.05257%, Rexp = 1.42525%, and goodness of fit = 1.94769 over 8301 points. `fit.csv` is the replayed profile, rather than a saved calculated array.

The phase fractions imply an overall crystalline Mn:W atomic ratio of 0.999, independently consistent with the stated 1:1 precursor-metal ratio. This chemical closure supports both the three-phase inventory and the quantitative result.

Several WO3 references were tested. A superficially competitive database model was rejected because its parent structure already contains 1.57 A O-O contacts. The submitted monoclinic model (COD 2311041) passes the contact screen and needs only about 0.34% strain from its reference cell. A valid triclinic P-1 alternative gives an almost indistinguishable profile only after about 1.39% cell distortion, outside the stated 0.5% reference-variation envelope, so P 21/c is preferred. The submitted CIFs have minimum interatomic separations of 1.769 A (MnWO4), 1.859 A (Mn3WO6), and 1.682 A (WO3), and all pass the geometry/occupancy screen.

## Remaining uncertainty

Local scale-covariance uncertainties are only about 0.05-0.06 absolute wt%-point, but they omit model correlations. Preferred orientation, surface roughness, Uiso, and the exact WO3 distortion are correlated; a more realistic uncertainty is about +/-1 absolute wt%-point per phase. The fractions do not quantify amorphous material.

The three chemical phases are reliable, but powder data alone do not make every oxygen coordinate or the subtle monoclinic-versus-triclinic WO3 distortion unique. Oxygen-coordinate changes were capped at 0.05 A RMS relative to the reference models, and the profile optimum reached that cap, so the submitted oxygen positions should be regarded as bounded, profile-consistent coordinates rather than a high-precision independent structure determination. The residual goodness of fit above one likewise indicates small remaining systematic profile error.
