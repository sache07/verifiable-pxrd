# Powder XRD phase analysis

The pattern is explained by three crystalline phases. The quantitative result, normalized over those modeled crystalline phases, is:

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| PbWO4, scheelite | I41/a | a = 5.46809, c = 12.0564 | 65.24% |
| monoclinic WO3 | P21/c | a = 7.29489, b = 7.53098, c = 10.5088, beta = 132.986 | 16.64% |
| PbCO3, cerussite | Pnma | a = 6.14914, b = 5.15869, c = 8.46962 | 18.11% |

The WO3 cell is written in a valid nonconventional P21/c basis; it is crystallographically equivalent to the usual monoclinic gamma-WO3 description.

## Evidence

The dominant scheelite PbWO4 model accounts for the strong line at about 27.90 degrees 2theta and its complete higher-angle series. The resolved low-angle WO3 group near 23.64, 24.12, and 24.91 degrees requires monoclinic WO3. Cerussite is independently identified by its lines near 20.66, 21.48, 25.36, and 26.05 degrees. This is chemically consistent with partial reaction of the supplied PbCO3 and WO3 precursors at 550 degrees C to form PbWO4 while retaining both precursors. Competing Pb oxide models did not account for these diagnostic lines or the full profile.

A three-phase GSAS-II Rietveld model was refined against the complete Cu Kalpha1/Kalpha2 scan. It includes background, angular calibration, lattice parameters, phase scales, isotropic displacement parameters, peak-size/strain terms, and modest March-Dollase corrections. A fresh zero-cycle forward replay of `final.gpx` gives Rwp = 3.5226%, Rp = 2.8052%, Rexp = 3.3643%, and goodness of fit = 1.0470. No systematic unassigned crystalline peaks remain at appreciable intensity.

## Remaining uncertainty

The phase identities are reliable. Scale fractions were stable within roughly 0.5 percentage point across reasonable profile variants, but overlap and correlations among scale, preferred orientation, displacement parameters, and peak broadening make a practical uncertainty of about 1-2 wt% absolute more realistic than the least-squares errors. The reported fractions do not measure amorphous material because no internal standard was present; a trace additional crystalline phase below approximately 1 wt% cannot be excluded.

Heavy Pb and W dominate the X-ray intensities, so the exact oxygen coordinates in PbWO4 and the C/O coordinates in PbCO3 cannot be determined reliably from this pattern alone. Those light-atom coordinates are reference-guided and only restrained, small shifts were accepted. Absolute lattice accuracy is also limited by covariance between specimen displacement, zero offset, and cell parameters. The CIFs are therefore suitable phase models, but their light-atom geometry should not be interpreted as a high-precision single-crystal determination.
