# Powder XRD phase analysis

The crystalline product is a three-phase mixture. The quantitative result, normalized over the modeled crystalline phases, is:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| SrWO4 (scheelite) | `I 41/a`, a = 5.38161 A, c = 11.89686 A | 0.81879 (81.88 wt%) |
| WO3 (monoclinic gamma-WO3) | `P 21/c`, a = 7.29052 A, b = 7.53018 A, c = 10.50875 A, beta = 133.0165 deg | 0.11291 (11.29 wt%) |
| SrCO3 (strontianite) | `P n m a`, a = 5.98540 A, b = 5.07012 A, c = 8.39823 A | 0.06830 (6.83 wt%) |

## Evidence

The chemical context (WO3 plus SrCO3 heated at 650 degC) supports formation of SrWO4 with unreacted starting materials. The dominant scheelite model accounts for its diagnostic reflections near 17.73, 27.47, 29.69, 32.94 and 45.10 deg 2theta. The residual cluster near 22.78, 23.27 and 24.08 deg requires monoclinic WO3, while features near 24.98 and 25.58 deg and their higher-angle partners require orthorhombic SrCO3. Alternative single- and two-phase fits left coherent Bragg residuals at these positions.

A simultaneous GSAS-II Rietveld refinement used the stated Cu Kalpha1/Kalpha2 wavelengths and intensity ratio. Cell metrics, phase scales, peak-shape/sample terms, background, and physically modest preferred orientation were refined; the SrWO4 oxygen coordinate was also refined. Minor-phase coordinates were retained from reference structures (including the neutron-derived gamma-WO3 model) because their individual positional parameters were not supported reliably by their lower intensities. The final full-grid fit has Rp = 3.1321%, Rwp = 4.0835%, and expected Rwp = 3.9814% (Rwp/expected Rwp = 1.0257). A fresh no-refinement regeneration of all reflections from `final.gpx` gives the same Rwp and no profile-review or physical-contact flags.

## Uncertainty

The three phase identities and their relative crystalline fractions are well supported by the whole pattern. A practical uncertainty of about 1 percentage point should be attached to each reported weight percentage because scale, absorption, preferred orientation, and microstructure are correlated. The detailed coordinates and displacement parameters of the two minor phases cannot be determined independently from this scan and should be regarded as reference-constrained structural models. These fractions are normalized only over the modeled crystalline material: without an internal standard, amorphous content and therefore absolute bulk phase fractions cannot be determined. No additional crystalline phase is required above the residual/noise level.
