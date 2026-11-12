# Quantitative phase analysis

The pattern is modeled with three crystalline phases. Fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material or the unresolved trace signal discussed below.

| Phase | Structure used | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| CaWO₄, scheelite | *I*4₁/*a*, COD 7219229 | a = 5.24510, c = 11.38207 | 0.77709 (formal e.s.d. 0.00066) |
| WO₃, monoclinic | *P*2₁/*n*, COD 1528915 | a = 7.29226, b = 7.53558, c = 7.68671, β = 90.9233 | 0.12164 (0.00042) |
| Ca₃WO₆ | *P*2₁/*n* analogue derived from Ca₃OsO₆, COD 1562666 | a = 5.53631, b = 5.78433, c = 8.01604, β = 90.0632 | 0.10127 (0.00058) |

Thus the defensible rounded result is **77.7 wt% CaWO₄, 12.2 wt% WO₃, and 10.1 wt% Ca₃WO₆**. The covariance errors above are counting-statistical errors only; source choice, texture, overlap, and the analogue structure make rounding to about 0.1 wt% more realistic.

## Phase and chemistry evidence

The dominant 18.43°, 28.54°, 31.25°, 34.0°, 46.93°, and 57.72° families identify scheelite CaWO₄. The resolved 22.95°/23.42°/24.22° triplet and its higher-angle families select room-temperature monoclinic WO₃ over the orthorhombic alternate. Residual families at 19.29°, 22.02°, 30.72°–32.15°, 36.6°–37.5°, 45.13°, 50.8°, and 56.5°–57.0° required a Ca-rich tungstate.

The inventory included CaO, Ca(OH)₂, CaCO₃, scheelite and monoclinic CaWO₄, monoclinic and orthorhombic WO₃, and Ca₄.₂₆W₁₀O₃₀. Because the residual and precursor balance remained incomplete, charge-balanced Ca₂WO₅, Ca₃WO₆, Ca₃W₂O₉, and Ca₄W₃O₁₃ were enumerated. `learned/stoichiometric_analogues.py` found the Ca₃OsO₆ parent; replacing Os by W gives charge-balanced Ca₃WO₆ and reproduces the residual family. Its final fixed-coordinate geometry remains physical (W–O 1.924–1.940 Å; shortest Ca–O 2.251 Å).

On a one-gram modeled basis, the phase amounts give Ca = 0.003458 mol and W = 0.003477 mol, or Ca:W = 0.9947:1. The oxygen inventory exactly satisfies O = Ca + 3W for Ca²⁺/W⁶⁺, so the retained phases balance the CaO + WO₃ precursor system without an unassigned cation excess.

The final watch-list replay drove CaCO₃, Ca₄.₂₆W₁₀O₃₀, and orthorhombic WO₃ to zero; monoclinic CaWO₄ was 0.019(17) wt% and CaO 0.08(4) wt%. Ca(OH)₂ gave a formal 0.45–0.61 wt% coefficient, but its useful lines at 33.9°, 47.0°, and 54.2° coincide with much stronger retained-phase peaks, while its relatively independent 17.88° line is below 1σ. It is therefore an unresolved trace/upper-bound signal, not a reliably identified or quantified fourth phase.

## Refinement model and checks

The GSAS-II model uses the supplied Bragg–Brentano reflection geometry and both Cu Kα wavelengths (1.540598/1.544426 Å, Kα₂/Kα₁ = 0.5). An eight-term smooth Chebyshev background was retained after 6/8/10/12-term challenges. The common nonnegative profile is U = 36.622, W = 30.903, X = 0; V, Y, and Z are fixed at zero. X reached zero and was fixed before the accepted replay. Sample displacement (340.10 µm) is the sole angular correction. Polarization refined to 0.7417, and one surface-roughness coefficient refined to 0.0424; removing roughness worsened Rwp from 3.105% to 3.190% while changing phase fractions by less than 0.1 wt%.

No-texture models were compared with axial and diagonal March–Dollase axes. The supported terms are CaWO₄ [110], 1.2224(19), and WO₃ [010], 0.9638(17); alternatives [001], [100], [101], [110], [112] for scheelite and [100], [010], [001], [110], [101], [011], [111] for WO₃ were challenged. SH/L remained fixed at 0.002 because repeated low-angle asymmetry was not observed.

Size and strain were compared one phase at a time from saved baselines. CaWO₄ size broadening (0.08476 ± 0.00040 µm) decisively beat strain (Rwp 3.366% versus 4.667% at that branch point). Ca₃WO₆ size (0.239(10) µm) beat its strain branch. WO₃ size ran to the 10 µm limit and was rejected; isotropic microstrain, 1327(57) µstrain, was finite and replay-stable. The numerical width audit below shows no repeatable hkl-dependent mismatch, so anisotropic broadening was not released.

Only structurally supportable coordinates were varied: the single scheelite O site and the two strongly scattering W sites in the coarse 1960 WO₃ record. Their final geometries are physical (scheelite W–O 1.775 Å; WO₃ W–O 1.775–2.118 Å for the principal coordination). Ca₃WO₆ atomic coordinates were held to the Ca₃OsO₆ analogue; its cell and diffraction contribution are supported, but its detailed atomic structure is not independently determined by this multiphase laboratory pattern.

## Measured profile audit

Values are in degrees 2θ. “Observed phase-isolated” means the measured profile after subtracting the refined background and calculated contributions of the other phases; this preserves the residual at the audited peak. The Ca₃WO₆ high-angle cluster is only 35% phase-dominant and is consequently the least certain check.

| Phase | Range | Position obs/calc | FWHM obs/calc | Left HWHM obs/calc | Right HWHM obs/calc |
|---|---|---:|---:|---:|---:|
| CaWO₄ | low | 18.4336 / 18.4336 | 0.2086 / 0.2068 | 0.1019 / 0.1025 | 0.1067 / 0.1042 |
| CaWO₄ | middle | 46.9253 / 46.9253 | 0.2745 / 0.2751 | 0.1158 / 0.1160 | 0.1586 / 0.1592 |
| CaWO₄ | high | 79.1441 / 79.1224 | 0.4267 / 0.4324 | 0.1742 / 0.1586 | 0.2526 / 0.2739 |
| WO₃ | low | 22.9540 / 22.9540 | 0.1638 / 0.1611 | 0.0823 / 0.0809 | 0.0815 / 0.0802 |
| WO₃ | middle | 41.7746 / 41.7637 | 0.2050 / 0.2047 | 0.1028 / 0.0892 | 0.1022 / 0.1154 |
| WO₃ | high | 83.6646 / 83.6646 | 0.1816 / 0.1587 | 0.0796 / 0.0800 | 0.1020 / 0.0787 |
| Ca₃WO₆ | low | 19.2920 / 19.2920 | 0.1728 / 0.1691 | 0.0822 / 0.0813 | 0.0906 / 0.0879 |
| Ca₃WO₆ | middle | 50.8263 / 50.8046 | 0.2477 / 0.2531 | 0.1270 / 0.1084 | 0.1207 / 0.1447 |
| Ca₃WO₆ | high | 74.8845 / 74.8410 | 0.3924 / 0.3879 | 0.2467 / 0.1991 | 0.1457 / 0.1888 |

## Fit quality and limitations

The reopened full-range project gives Rwp = 3.103%, Rp = 2.245%, Rexp = 2.247%, goodness of fit Rwp/Rexp = 1.381, and reduced χ² = 1.907 for 8,301 points and 40 refined parameters. Small coherent intensity residuals remain, especially within overlapping WO₃/Ca-rich-tungstate families, and the counting-only uncertainty model does not include detector or specimen systematics. The Ca₃WO₆ formula and lattice are supported by multiple peaks and precursor balance, but its analogue-derived coordinates and any sub-percent Ca(OH)₂ content cannot be determined reliably from this pattern alone.

`final.gpx` was refined over the complete supplied range, saved, reopened, replayed, and then used directly to export all CIFs, fractions, and `fit.csv`.
