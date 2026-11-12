# Powder XRD phase analysis

The scan is modeled as two crystalline phases: orthorhombic witherite BaCO3 and monoclinic WO3. The refined crystalline weight fractions are **52.88 wt% BaCO3** and **47.12 wt% WO3**, normalized to the modeled crystalline material.

## Evidence

The four-line 23.4–24.7 deg cluster and the 33.6–34.9 deg splitting require low-symmetry WO3 together with witherite. BaCO3 is independently supported by its 42.29, 45.17 and 47.08 deg lines. A scheelite BaWO4 model was rejected because its strong characteristic pattern (especially the ~31.9 deg line) is absent and it did not explain the observed residuals. No additional unmatched Bragg family remains at a level that justifies a third crystalline phase.

The submitted GSAS-II model includes the measured Cu Kalpha1/Kalpha2 doublet, a refined empirical background, phase-specific size/microstrain broadening, modest BaCO3 [110] March-Dollase texture, and a Suortti low-angle surface-roughness correction. Native atomic replay of `final.gpx` gives Rwp = 6.057%, Rp = 4.560% and goodness-of-fit = 1.743 with count-statistical weights. `fit.csv` is the complete observed/calculated/difference profile from that replay.

## Uncertainty

Phase identity is secure at the compound level, but the exact WO3 distortion is less unique. A triclinic P-1 alternative can lower Rwp to about 5.94%, but only by shearing its published parent metric by roughly 1 degree and using many extra positional degrees of freedom; the selected P21/c model gives 6.06% with modest 0.1–0.4% cell changes and is structurally more defensible. Oxygen coordinates are therefore only weakly constrained by this X-ray pattern; the CIF retains small, physically bounded adjustments from monoclinic COD 2311041 rather than the unstable unconstrained oxygen refinement. The BaCO3 model is based on witherite COD 9010928. The fractions varied by roughly 2–3 wt% across credible profile/polymorph alternatives, so a practical estimate is BaCO3 52.9 +/- 2.5 wt% and WO3 47.1 +/- 2.5 wt%. Amorphous material, if present, is not quantified.
