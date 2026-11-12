# PXRD phase analysis

The pattern is modeled by three crystalline phases. Weight fractions are normalized over those phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| MgWO4, wolframite-type | P 2/c (No. 13) | 78.24 wt% |
| WO3, monoclinic | P 21/c (No. 14) | 14.53 wt% |
| MgO, periclase | F m -3 m (No. 225) | 7.23 wt% |

The least-squares standard uncertainties are 0.16, 0.09, and 0.16 wt%, respectively. These are conditional on the selected models and counting-statistical weights; they do not include microabsorption, specimen homogeneity, or instrument-profile systematics. Reporting the fractions to about 0.5–1 wt% absolute precision is more realistic than the formal uncertainties imply.

## Evidence and model selection

MgWO4 explains the dominant wolframite reflection set across the full 9.90–100.09 degree 2theta range. The remaining families include the characteristic low-angle multiplet and numerous higher-angle reflections of WO3, plus the six observable rocksalt MgO reflections. With matched nuisance parameters, leaving out MgWO4, MgO, or WO3 increased Rwp from 8.655% to 51.876%, 9.570%, or 19.386%, respectively. Thus each reported phase has independent multi-peak support rather than overlap-only credit.

The final structures derive from COD 9013902 (MgWO4), COD 2311041 (WO3), and COD 9000499 (MgO). All three final CIFs pass the supplied composition, occupancy, symmetry-expansion, duplicate-site, and close-contact audit. A malformed alternative MgWO4 entry was rejected for dummy coordinates/invalid occupancy, and a WO3 candidate was rejected for implausible O-O contacts. A physically valid triclinic WO3 alternative was carried through the same mature refinement; it gave Rwp = 8.707%, versus 8.655% for monoclinic WO3 despite two extra cell variables. The monoclinic model is therefore preferred, but the exact low-symmetry WO3 distortion is only moderately discriminated by this powder pattern; WO3 identity and approximate amount are more reliable than its monoclinic-versus-triclinic fine detail.

Cells were refined for all phases. MgWO4 atomic coordinates were also refined and retained only after the exported geometry passed audit; MgO and WO3 coordinates and all ADPs were held to their source models because independent refinement was not justified by the overlapping laboratory powder data. Occupancies were fixed at unity. No coherent residual-peak family supported a fourth atomistic phase; the largest residual extrema coincide with reflections of the three accepted phases and mainly reflect remaining intensity/peak-shape mismatch.

## Profile treatment and fit quality

The final model uses the reported Cu Kalpha1/Kalpha2 wavelengths and fixed 0.5 intensity ratio. Although the metadata says Kalpha1 was intended, a matched Kalpha1-only branch was substantially worse (Rwp = 9.899%) and drove the Lorentzian width negative, so the measured profile supports retaining the doublet. The selected compact nuisance model contains an eight-term Chebyshev background, sample displacement, global W/X profile terms, effective polarization, isotropic microstrain for MgWO4 and WO3, and one weak MgWO4 [110] March-Dollase term. Removing those optional terms one at a time raised Rwp to 10.007%, 8.692%, 8.761%, 8.794%, and 9.049%, respectively. Size broadening was rejected as correlated or unstable, and MgO microstrain was too small in benefit to retain. Joint zero/displacement, surface-roughness, and axial-divergence branches were rejected for high correlation or nonphysical parameters.

The final full-pattern statistics are Rwp = 8.655%, Rp = 6.332%, Rexp = 2.863%, and GOF = 3.030. Refinement converged with no SVD-dropped variables, maximum shift/esd = 0.0083, no parameter correlation above 0.90, and positive regenerated peak widths for every reflection. GOF above unity and structured residuals at intense peaks show that profile/intensity imperfections remain, so the fit should not be interpreted as a uniquely exact structural determination. No amorphous content was quantified.
