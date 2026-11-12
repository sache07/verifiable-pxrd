# Powder XRD phase analysis

## Result

The pattern is a two-phase, largely unreacted precursor mixture. The modeled crystalline fractions are 75.39 wt% monoclinic WO3 and 24.61 wt% spinel Co3O4, normalized to 100% of the identified crystalline material. The GSAS-II standard uncertainty is 0.36 percentage point for either fraction; a more realistic uncertainty is about +/-1 percentage point because scale, polarization, displacement parameters, and peak-profile terms are correlated. No amorphous fraction can be obtained from this scan without an internal standard.

| Phase | Space group | Refined cell (angstrom, degrees) | Weight fraction |
|---|---|---|---:|
| WO3 | P 21/c (No. 14) | a = 7.69684, b = 7.53972, c = 10.54990, beta = 136.154 | 0.75386 |
| Co3O4 | Fd-3m (No. 227) | a = 8.08729 | 0.24614 |

## Evidence

The dominant phase reproduces the characteristic split WO3 group at approximately 23.465, 23.954, and 24.714 degrees 2theta and the extensive lower-symmetry splitting throughout the scan. Among screened WO3 references, the P 21/c model based on COD 2311041 gave the best stable starting fit and physically sensible geometry; a triclinic WO3 candidate was close in profile residual but required lower symmetry and a substantially less compatible starting metric. The average monoclinic assignment is therefore preferred, although very small lower-symmetry oxygen distortions cannot be excluded.

The minority phase is fixed by independent reflections near 19.368, 31.625, 37.200, 45.154, 59.672, and 65.550 degrees 2theta, all reproduced by spinel Co3O4 (starting model COD 9005896). Adding CoWO4 was not supported by independent peaks, and the remaining largest residuals are derivative-like mismatches at strong modeled WO3 peaks rather than a coherent set from another phase.

## Refinement and limitations

The final Rietveld model uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, a 15-term Chebyshev background, refined cells and phase scales, specimen displacement/zero correction, crystallite-size and microstrain broadening, and [010] uniaxial microstrain for WO3. Common isotropic displacement parameters refined to 0.01240(41) A2 for WO3 and 0.01692(171) A2 for Co3O4. Polarization was fixed at the documented upper physical bound of 1.0 after unconstrained joint refinement attempted to exceed it.

W coordinates and the Co3O4 oxygen coordinate were refined in isolated structural steps. Free refinement of all WO3 oxygen coordinates was unstable and produced implausible shifts, so the exported WO3 CIF retains the reference oxygen sublattice; those individual oxygen positions are not determined reliably by this powder pattern. The refined framework and cells are reliable for phase identification, but the CIF should not be interpreted as a precision determination of WO3 oxygen distortions.

The final fit statistics are Rp = 2.233%, Rwp = 3.123%, Rexp = 1.722%, and goodness-of-fit = 1.817 for 8301 observations and 32 refined parameters. Residual serial structure remains around the strongest peak clusters, so formal least-squares uncertainties are likely optimistic. `final.gpx`, the two CIFs, `fit.csv`, and `result.json` were exported from the same final project state.
