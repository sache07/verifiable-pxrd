# Quantitative crystalline phase analysis

## Result

The pattern is described by three crystalline phases, normalized over the modeled crystalline material:

| Phase | Space group | Weight percent | Refined cell (Å, °) |
|---|---:|---:|---|
| NiWO4 (wolframite) | P 2/c (13) | 60.3767 ± 0.0314 | a=4.599338, b=5.662557, c=4.911208, β=90.50116 |
| WO3 (monoclinic) | P 21/c (14) | 29.3781 ± 0.0256 | a=7.682115, b=7.544442, c=10.507964, β=136.02435 |
| NiO (rocksalt) | F m -3 m (225) | 10.2452 ± 0.0313 | a=4.164856 |

The quoted ± values are GSAS-II least-squares standard uncertainties in weight-percentage points. Rwp=1.8642%, Rp=1.4633%, Rexp=1.4476%, and GOF=1.2903 for 8,301 original observations and 32 refined variables.

## Evidence and model selection

The precursor chemistry (NiO + WO3, heated to 700 °C) supports nickel tungstate formation with residual reactants. NiWO4 is required by coherent families near 15.62, 19.27, and 30.85–31.03° 2θ; monoclinic WO3 by the 23.14/23.56/24.38° triplet; and NiO by the rocksalt 37.33, 43.43, and 63.07° peaks. After reconverging the same background/profile model, omitting NiWO4, WO3, or NiO raised Rwp from 3.588% (the pre-coordinate common-profile checkpoint) to 33.43%, 22.91%, or 7.11%, respectively.

The archived exact NiWO4 COD record 5910277 contained duplicated symmetry-equivalent sites and an unphysical NiWO6 transcription, so it was not used verbatim. A physically valid P2/c Ni-for-Mg wolframite analogue from COD 9013902, initialized with the NiWO4 cell, fit better than a corrected exact transcription and a ZnWO4 parent under the same nuisance model (Rwp 4.167%, 4.197%, and 5.035%). For WO3, the P21/c model from COD 2311041 outperformed the tested P21/n and triclinic records; NiO used COD 1010093. The required staged heavy-atom test accepted Ni and W coordinates in NiWO4 and both W coordinates in WO3, reducing Rwp from 3.5880% to 1.8642%. All accepted shifts were ≤0.060 Å; final minimum contacts are 1.786, 1.701, and 2.082 Å, with no GSAS-II short-contact flags.

## Refinement adequacy and uncertainty

The model uses the measured Cu Kα doublet on the untouched 9.90343322–100.09455322° grid, an eight-term smooth Chebyshev background, phase scales and cells, one zero correction, nonnegative W/X profile terms, and a refined polarization factor. Size/strain trials were rejected because gains were negligible, solutions hit the neutral size limit, or strain became negative. SH/L asymmetry gave only a 0.0051 percentage-point gain and was 97% correlated with zero. Symmetry-distinct texture trials gave at most a 0.0105 percentage-point gain with March ratios within 1% of unity; NiO texture trials were unstable. Size, strain, texture, roughness, extinction, and Babinet terms therefore remain neutral.

Phase identities and bulk crystalline proportions are well supported, but the formal fraction uncertainties are smaller than source/profile systematics; practical uncertainty is approximately 0.5–1 weight-percentage point. Fractions are normalized only over modeled crystalline phases, so amorphous content cannot be determined without an internal standard. Oxygen coordinates were retained from the screened parent structures and are not independently determined reliably by this laboratory pattern; the submitted CIFs should be treated as Rietveld models rather than complete single-crystal structure determinations.
