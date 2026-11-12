# PXRD phase analysis

## Result

| Phase | Structural model | Weight fraction (crystalline basis) | Refined cell |
|---|---|---:|---|
| CaWO4 | scheelite, *I*41/*a* (COD 7219229) | 79.046(79) wt% | *a* = 5.242258 Å, *c* = 11.376160 Å |
| WO3 | monoclinic, *P*21/*c* (COD 2311041) | 11.525(47) wt% | *a* = 7.682512 Å, *b* = 7.531551 Å, *c* = 10.504461 Å, beta = 136.07019 degrees |
| Ca3WO6 | *P*21/*n* Ca3OsO6 prototype (COD 1562666), Os6+ replaced by W6+ | 9.429(57) wt% | *a* = 5.532778 Å, *b* = 5.780581 Å, *c* = 8.012738 Å, beta fixed at 90 degrees |

The fractions sum to 100% over the modeled crystalline phases. Parenthesized uncertainties are formal one-standard-deviation values from the GSAS-II covariance matrix, in the last quoted digits; they do not include structural or profile-model uncertainty. The final full-range fit (9.9034–100.0946 degrees 2-theta, 8301 points) has Rp = 3.0275%, Rwp = 3.9840%, Rexp = 2.2469%, and goodness of fit = 1.7764.

## Evidence and model selection

Scheelite CaWO4 accounts for the dominant peak family, including observed peaks near 18.43, 28.54, 31.27, 34.01, 39.03, 46.93, and 48.91 degrees. The selected 298 K, fully occupied COD model has sensible final geometry (W–O = 1.762 Å and nearest Ca–O = 2.469–2.472 Å). Records with malformed occupancy or incompatible high-pressure symmetry were rejected.

Monoclinic WO3 accounts for the characteristic 22.94/23.42/24.23-degree triplet and the 26.44, 33.10/33.43, and 41.31/41.76-degree groups. Its occupied composition and geometry are physical (W–O = 1.713–2.157 Å; minimum O–O = 2.536 Å). Under the same nuisance model, monoclinic COD 2311041 gave Rwp = 3.984%, versus 4.076% for a credible triclinic model and 8.470% for the tested orthorhombic model. Thus monoclinic WO3 is preferred, although the small monoclinic–triclinic separation leaves some uncertainty in the exact WO3 distortion.

No exact Ca3WO6 record was present in the supplied index, so the stoichiometric-analogue search was used. The best chemically valid parent was fully occupied, 293 K *P*21/*n* Ca3OsO6 (COD 1562666, a high-pressure-grown single crystal). Isovalent octahedral Os6+ was replaced by W6+ without transferring any case-specific refinement. Tested cubic and double-perovskite parents were rejected because their adapted Ca–O geometry or diagnostic multiplet splitting was incompatible. The selected model accounts for residual families near 19.29, 22.01, 30.71, 32.18, 36.6–37.5, 48.09, 50.75, and 55.23 degrees. Its final geometry remains physical (W–O = 1.922–1.939 Å; minimum O–O = 2.700 Å). Removing WO3 and fully reconverging worsened Rwp to 12.81%; removing Ca3WO6 worsened it to 8.65%. The unconstrained modeled inventory gives Ca/W = 0.993 and a molar WO3:Ca3WO6 ratio of about 2.11:1, consistent with the complementary Ca-rich/W-rich minor phases around CaWO4.

A residual-CaO challenge was not accepted. With a physically credible room-temperature CaO cell fixed, it refined to only 0.13(6) wt% and its strongest reflections were not supported coherently. Releasing its cell produced 0.26 wt% only by contracting *a* from 4.8174 to 4.7886 Å and fitting one shoulder. A CaO fraction therefore cannot be determined reliably from this pattern and is omitted.

## Refinement and uncertainty

The Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. Because pointwise uncertainties were absent, Poisson weights (1/count) were used. A common zero correction was selected over specimen displacement from its slightly better angular residual (0.01927 versus 0.01929 degrees RMS); the correlated alternatives were not co-refined. Background, all phase scales, zero, and cells were reconverged after every inventory or source change.

The clean common profile used nonnegative U/W/X with V and Y zero. Only CaWO4 supported an additional isotropic size term (0.0915 micrometres); size-only and strain-only challenges for both minor phases returned to no-broadening limits and were pruned, with inactive sizes held at GSAS-II's 10-micrometre neutral cap and strains at zero. A modest CaWO4 [001] March–Dollase term (0.8949) and a global polarization factor (0.8750) were retained. Atomic coordinates and occupancies were not refined. The final project was saved, reopened, and replayed with native atomic structure factors over the full range; it contains no frozen variables or Le Bail phases.

The exact Ca3WO6 atomic structure is not established reliably: its coordinates are those of the chemically justified analogue, and the metrically near-orthogonal beta angle was fixed because its departure from 90 degrees was unsupported and highly correlated. The formal fraction errors are consequently optimistic; model-branch variation suggests roughly 1–2 wt% systematic uncertainty is more realistic. Correlated residuals (Durbin–Watson = 0.626) reinforce that caution. No internal standard was supplied, so amorphous material or an undetected trace crystalline fraction cannot be quantified; reported fractions apply only to the modeled crystalline material.
