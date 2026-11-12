# PXRD phase analysis

## Result

The pattern is described by three crystalline phases. Fractions are normalized over these modeled crystalline phases only.

| Phase | Structural model | Weight fraction | CIF |
|---|---|---:|---|
| NiWO4, wolframite | P 2/c (No. 13) | 59.626 ± 0.067 wt% | `NiWO4.cif` |
| WO3, monoclinic | P 21/c (No. 14) | 30.634 ± 0.052 wt% | `WO3.cif` |
| NiO, rocksalt | F m -3 m (No. 225) | 9.740 ± 0.060 wt% | `NiO.cif` |

The uncertainties in the table are GSAS-II covariance estimates (1 sigma), not total model uncertainties. The final full-range fit has Rwp = 3.6356%, Rp = 2.2604%, Rexp = 1.4476%, Rwp/Rexp = 2.511, and reduced chi-squared = 6.307 for 8,301 points from 9.9034 to 100.0946 degrees 2theta.

## Evidence and model selection

The phase inventory is chemically consistent with reaction of the reported WO3 and NiO precursors at 700 degrees C: NiWO4 is the major product and both precursors remain. NiWO4 is supported by coherent families at approximately 15.61, 19.26, 23.94, 24.90, 30.82/31.02, and 36.54/36.58 degrees. Monoclinic WO3 gives the characteristic 23.12/23.54/24.36 degree triplet and many higher-angle families. NiO is independently supported by its 111, 200, 220, 311, 222, and 400 lines at approximately 37.34, 43.40, 63.06, 75.65, 79.66, and 95.41 degrees. A residual-led re-screen found no additional coherent family attributable to another crystalline phase; the largest remaining structured mismatch near 41.5 degrees is an overlap of modeled NiWO4 and WO3 reflections.

No exact NiWO4 entry was present in the local reference set, so the supplied stoichiometric-analogue search was used. Several P 2/c tungstates were screened. A FeWO4 parent (COD 9008124) with the chemically direct Fe-to-Ni substitution fit better than the ZnWO4 parent (COD 1520641) under the same nuisance model: Rwp 4.279% versus 4.418%. The selected geometry remains physical after refinement, with Ni-O distances of 2.049, 2.110, and 2.118 A and W-O distances of 1.763, 1.879, and 2.088 A (each pairwise in the octahedra), with no short contacts. For WO3, the room-temperature neutron model (COD 2311041) outperformed the ambient X-ray alternative (Rwp 4.279% versus 5.184% with the same NiWO4 model); a high-pressure polymorph was inconsistent with both the source conditions and the low-angle triplet. NiO was initialized from COD 1010093.

The final cells are NiWO4: a = 4.599462, b = 5.662625, c = 4.911390 A, beta = 90.50304 degrees; WO3: a = 7.682402, b = 7.544770, c = 10.508056 A, beta = 136.02226 degrees (the alternate P 21/c setting of the source model); and NiO: a = 4.164937 A. For NiWO4, the supported heavy-atom coordinates refined to Ni y = 0.66510(30) and W y = 0.17647(10).

The physically adequate baseline used a smooth six-term Chebyshev background, one zero correction, Cu Kalpha1/Kalpha2 with the reported 0.5 ratio, a common nonnegative U/W/X profile, and refined polarization. NiWO4 isotropic microstrain and weak March-Dollase corrections along NiWO4 [101] and WO3 [110] were replay-stable and supported by multiple families. Phase size, WO3/NiO strain, NiO texture, roughness, SH/L asymmetry, and extra displacement terms were neutral, boundary-seeking, or strongly correlated and were pruned. The submitted project was saved, reopened, and replayed over the full range; its final maximum shift/esd was 0.001.

## Remaining uncertainty

NiWO4 oxygen positions cannot be determined reliably from this W-dominated laboratory X-ray pattern. They were therefore retained from the physically screened FeWO4 analogue rather than accepting a lower-Rwp but weakly constrained oxygen refinement. WO3 atomic-coordinate trials were also rejected because coordinate pairs exceeded 95% correlation; its cell and scale were refined, but its coordinates remain those of the neutron source model. Thus the CIFs are suitable phase and Rietveld models, but they should not be interpreted as independent high-precision oxygen-coordinate determinations.

The reported fractions are reliable as relative fractions of the modeled crystalline material, but their formal covariance errors understate uncertainty from reference-model and preferred-orientation choices. Absolute bulk fractions, amorphous content, and a calibrated detection limit for an additional trace phase cannot be determined without an internal standard and independent uncertainty information. Since pointwise uncertainties were not supplied, raw-count Poisson weights were used; this also makes the quoted goodness-of-fit statistics conditional on that weighting model.
