# Powder XRD phase analysis

The modeled crystalline material is **97.4909 wt% triclinic CuWO4 (P -1)** and **2.5091 wt% monoclinic WO3 (P 21/c)**, normalized over those two phases. The scale-covariance statistical uncertainty is about 0.08 wt% for either fraction; a more realistic allowance for source-model/profile systematics is roughly 0.3 wt%, especially for the minor phase.

## Evidence

The dominant peak positions and intensities across 9.903–100.095 degrees 2theta are explained by triclinic wolframite-type CuWO4. The available exact-composition COD entries are high-pressure structures and fit poorly or refine to zero scale under the common profile. An analogue search identified COD 2101690, reported as Cu0.9Zn0.1WO4, whose ambient triclinic cell directly matches the pattern. Replacing its single divalent-site label by fully occupied Cu gives CuWO4 without changing the framework; subsequent cell and coordinate refinement yields the submitted physical model.

The remaining coherent, partly overlapped families are best described by room-temperature monoclinic WO3 using COD 2311041. Two alternative room-temperature WO3 records were tested under the same restrained model and gave worse fits. Re-challenges with CuO, Cu2WO4, and the high-pressure CuWO4 record refined to zero scale. Cu3WO6 repeatedly gave only about 0.15 wt% (2.7 standard uncertainties) and an estimated whole-pattern signal below reliable detectability; this is retained only as a trace-level uncertainty, not as a reported phase.

The final full-range model uses the supplied Cu Kalpha1/Kalpha2 wavelengths and ratio, a smooth positive ten-term Chebyshev background, one specimen-displacement correction (-555.6 micrometres), nonnegative U/W/X profile terms, and polarization 0.6784. Background orders 6–14 were compared; order 10 removes the low-angle baseline trend, while orders 12–14 give only marginal gains. Main-phase [010] March-Dollase texture is small but replay-stable (ratio 0.98233(14)); the weakly determined WO3 isotropic size term is 0.428(150) micrometres. Removing either term worsens Rwp. Roughness, main-phase size/strain, minor-phase texture, and variable SH/L trials were unsupported, singular, or collapsed to neutral values and were pruned.

Native replay of `final.gpx` over all 8,301 observations gives Rwp = 6.7987%, Rp = 4.9017%, and goodness of fit = 2.7989. The replay has a positive background and no negative-width, polarization, displacement-tensor, or geometry flags. The submitted CIFs have minimum interatomic distances of 1.846 A (CuWO4) and 1.772 A (WO3), with minimum O-O distances of 2.444 and 2.539 A, respectively.

## Remaining uncertainty

The CuWO4 identity, cell, and dominant fraction are secure. Its refined oxygen coordinates are supported by the intensities, but the common isotropic displacement value was fixed at 0.005 A2 because Uiso and polarization were strongly correlated. For 2.5 wt% WO3, the phase identity and fraction are supported, but its detailed oxygen coordinates, crystallite size, and thermal parameters cannot be determined precisely from this pattern; the submitted structure therefore remains mostly source-model constrained. The possible trace Cu3WO6 contribution cannot be distinguished reliably from residual profile/model error.
