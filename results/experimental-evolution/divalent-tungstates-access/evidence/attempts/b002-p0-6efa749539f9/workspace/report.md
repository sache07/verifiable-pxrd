# Powder XRD phase analysis

The pattern is best described by four crystalline phases. Quantitative values below are normalized over those phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| MnWO4, wolframite | P 2/c | a=4.79424, b=5.70029, c=4.96969, β=91.1074 | 0.59590 (59.59 wt%) |
| WO3, monoclinic | P 21/c | a=7.68202, b=7.53499, c=10.50784, β=136.0517 | 0.21807 (21.81 wt%) |
| Mn2WO6, orthorhombic | P 21 21 21 | a=5.03269, b=8.68976, c=9.55927 | 0.15222 (15.22 wt%) |
| MnO, rocksalt | F m -3 m | a=4.41485 | 0.03380 (3.38 wt%) |

## Evidence and refinement

A full-pattern GSAS-II Rietveld refinement used the reported Cu Kα1/Kα2 wavelengths and 0.5 doublet ratio, the complete 9.903–100.095° scan, and count-statistical weights `1/max(Iobs,1)`. The dominant sharp reflections are indexed by wolframite MnWO4, the expected principal reaction product. A second extensive set of broader reflections matches monoclinic WO3 and is consistent with residual precursor. The weak rocksalt sequence is accounted for by MnO.

The remaining broad maxima index to an orthorhombic cell and are reproduced by a P 21 21 21 Mn2WO6 model made by chemically substituting Mn into the Y2WO6 framework (COD 1541070) and refining its cell/profile. Competing Fe2WO6-type Pbnm and Cr2WO6-type P42/mnm analogues gave materially poorer full-pattern fits. Unconstrained coordinate refinement of this broad phase was rejected because it generated impossible short metal–oxygen contacts; the submitted CIF retains the physically valid analogue geometry. Tests adding Mn3O4 or Mn2O3 produced only about 0.4 wt% with negligible fit improvement, so there is no reliable evidence for a fifth crystalline phase.

Fresh forward replay of `final.gpx` gives Rwp=13.4346%, Rp=7.5810%, χ²=376923.7, and goodness-of-fit=6.738 over 8301 points. The replay has no negative-profile, negative-background, peak-width, polarization, or displacement-parameter flags.

## Remaining uncertainty

The fit is not noise-limited: broad, strongly overlapping WO3/Mn2WO6 scattering and pronounced size/strain/texture effects leave systematic residuals. Consequently, the least-squares fraction errors understate practical uncertainty; several percentage points of model-dependent uncertainty are plausible, and the 3.38 wt% MnO fraction is not reliable to substantially better than roughly one absolute percentage point. The exact Mn2WO6 atomic coordinates cannot be determined reliably from this pattern; its composition, cell, and P 21 21 21 framework are better supported than its detailed oxygen positions. No external standard was supplied, so amorphous material and total crystalline content cannot be determined; the reported fractions must not be interpreted as absolute bulk fractions.
