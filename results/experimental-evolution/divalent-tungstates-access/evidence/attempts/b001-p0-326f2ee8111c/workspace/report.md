# Powder XRD phase analysis

The pattern is explained by two crystalline precursor phases: monoclinic WO3 and wurtzite ZnO. The refined crystalline-only weight fractions are 73.90 wt% WO3 and 26.10 wt% ZnO. These fractions are normalized over the modeled crystalline material; the scan does not determine an amorphous fraction or other noncrystalline mass.

## Evidence

The 23.13/23.60/24.40 degrees 2theta triplet, together with lines at 26.61, 28.62/28.94, 33.27/33.57/34.18, 41.44/41.91, and 49.96 degrees, identifies monoclinic WO3. A P21/c model based on COD 2311041 was refined. Its reported cell is an equivalent nonstandard monoclinic setting: a = 7.29519 A, b = 7.53904 A, c = 10.51286 A, beta = 133.010 degrees.

The peaks at 31.80, 34.58, 36.32, 47.68, 56.65, 63.09, 68.08, and 69.17 degrees identify wurtzite ZnO (P63mc), refined from COD 9004178 to a = 3.24703 A and c = 5.18385 A. This phase assignment is also consistent with the ZnO + WO3 precursor inventory and the low reported treatment temperature of 200 degrees C.

The GSAS-II refinement used the complete 9.903-100.095 degrees Cu K-alpha scan, both reported wavelengths and their 0.5 intensity ratio. Since point uncertainties were not supplied, Poisson weights 1/max(counts,1) were used. The final fit has Rwp = 2.8156%, Rp = 1.9955%, Rexp = 2.7987%, and GoF = 1.006. Independent native GSAS-II replay of `final.gpx` reproduced the submitted curve and fractions with no profile-review flags.

## Uncertainty and exclusions

The formal GSAS-II fraction standard uncertainty is 0.06 percentage point for each phase, but correlations between polarization, displacement parameters, and scale make a practical uncertainty of roughly 1 wt% more realistic. Phase identities and the heavy-atom WO3 framework are reliable; individual oxygen coordinates are less tightly determined by laboratory X-ray data.

A P2/c ZnWO4 trial was not supported: its diagnostic reflections near 30.43 and 30.68 degrees are absent, and its fitted fraction was only about 0.04 wt% before the added phase became numerically unstable. ZnWO4 is therefore not reported as a phase, though a trace amount below approximately 0.5-1 wt% cannot be excluded. Preferred-orientation trials refined to ratios within 0.3% of unity, and a surface-roughness term did not improve the fit materially.
