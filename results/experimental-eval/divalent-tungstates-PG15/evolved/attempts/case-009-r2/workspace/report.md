# Crystalline-phase analysis

## Result

The defensible crystalline model contains one phase: wolframite **MnWO4**, monoclinic **P 2/c** (No. 13), at a normalized crystalline weight fraction of **1.000 (100 wt%)**. The refined cell is `a = 4.830561(81) Å`, `b = 5.756820(91) Å`, `c = 4.996097(84) Å`, `beta = 91.21738(11)°`, and `V = 138.90345(43) Å³`. The full-range fit gives `Rwp = 5.4253%`, `Rp = 4.1306%`, `Rexp = 3.4605%`, goodness-of-fit `1.5694`, and `RBragg = 2.3819%`.

The 100 wt% value is normalized over the modeled crystalline phases. It is not evidence of 100% bulk purity and does not constrain amorphous material without an external standard.

## Evidence and phase inventory

The Mn3O4 + WO3 precursor chemistry and 900 °C treatment are consistent with MnWO4 formation. The observed low-, middle-, and high-angle peak families are indexed by the wolframite cell; no second set of coherent, isolated peaks is required. The starting model was the fully occupied, disorder-free MnWO4 record COD 1520200. Although that record was measured at pressure, it outperformed Mn-substituted ambient FeWO4, ZnWO4, and MgWO4 wolframite parents under the same restrained nuisance model, and its refined cell is physically consistent with ambient wolframite.

The exported structure is geometrically sound: Mn is octahedrally coordinated with Mn–O distances of 2.111–2.265 Å, W is octahedrally coordinated with W–O distances of 1.794–2.136 Å, and the calculated density is 7.239 g cm⁻³. Atomic coordinates and displacement parameters were retained from the source model; releasing them gave only a small, non-robust improvement, particularly for the weakly scattering oxygen coordinates.

Plausible alternatives were challenged by refining scale before cell under the common profile:

| Watch-list model | Scale-test outcome | Decision |
|---|---:|---|
| Mn3O4, ambient I41/amd and high-pressure Pbcm | 0.23(19) and 0.13(23) wt% | Insignificant; excluded |
| Mn3WO6, R-3 | Scale collapsed to zero | Excluded |
| MnO and MnO2 | Insignificant or zero | Excluded |
| Monoclinic WO3 alternatives and Pnma WO3 | Positive but unstable, about 0.2–1.3 wt% depending on record/cell freedom | Not reliable: improvement came mainly from shoulders of the strong MnWO4 complex at 23.5–24.3°, while strong isolated WO3 predictions near 33–35° were absent |
| Mn2O3, Ia-3 | 0.46(12) wt% in a free scale trial | Not reliable: the strongest isolated predicted families were unsupported; excluded |

Thus no structure or fraction for a minor phase can be determined reliably from this pattern. Trace, strongly overlapped impurities remain possible.

## Refinement adequacy and reproducibility

The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. The accepted baseline uses an eight-term smooth Chebyshev background, one specimen-displacement correction (`-423.69 µm` for the GSAS-II 200 mm radius), and one reduced Suortti roughness parameter (`A = 0.10` fixed, `B = 0.3903` refined). The nonnegative common profile has `U = 0`, `W = 34.0105`, and `X = 9.0695`; removing X worsened Rwp to 6.629%. SH/L was fixed at 0.002 after its trial correlated with the angular correction.

Observed/calculated FWHM checks across the range were representative of a common profile (for example 0.213/0.199° near 15.7°, 0.217/0.240° near 45.1°, and 0.345/0.350° near 67.9°). Positive phase size broadening ran to the neutral 10 µm limit, strain refined slightly negative, and no coherent family-dependent broadening remained; both were pruned. March–Dollase trials along symmetry-distinct axes stayed within 0.982–1.015 of unity and improved Rwp by at most 0.024 percentage point, so texture was also pruned.

`final.gpx` was saved, reopened, and replayed over all 8,301 measured points. The CIF and `fit.csv` were then exported from that reopened project. Remaining oscillatory residuals and the Durbin–Watson value of 0.832 indicate some line-shape/intensity systematic error; this is the main limitation on trace-phase inference and detailed coordinate refinement.
