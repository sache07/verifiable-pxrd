# Quantitative phase analysis

The crystalline pattern is modeled by three phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure any amorphous content.

| Phase | Structure | Weight fraction | Refined cell |
|---|---|---:|---|
| MgWO4 | wolframite/huanzalaite type, `P 1 2/c 1` | 0.51102 (51.10 wt%) | a = 4.69588 Å, b = 5.68286 Å, c = 4.94665 Å, β = 90.8250° |
| WO3 | monoclinic gamma-WO3, `P 1 21/c 1` | 0.41428 (41.43 wt%) | a = 7.68590 Å, b = 7.54030 Å, c = 10.51683 Å, β = 136.0520° |
| MgO | periclase, `F m -3 m` | 0.07470 (7.47 wt%) | a = 4.20986 Å |

The final full-range replay gives Rwp = 1.78936%, Rp = 1.41498%, Rexp = 1.52707%, GOF = 1.17530, and χ² = 11397.43 for 8301 observations and 50 refined parameters. The maximum final shift/esd was 0.0015.

## Evidence and model selection

MgWO4 accounts for the distinctive 15.58° and 18.88° peaks and the dominant families throughout the scan. Monoclinic WO3 accounts for the strong 23.13/23.57/24.37° family, while MgO is required by its 42.92°, 62.31°, and higher-angle rock-salt reflections. No coherent unassigned family remains after fitting.

The starting structures were COD 9013902 (MgWO4), 2311041 (WO3), and 9000499 (MgO). All three source CIFs and all final CIFs passed `learned/cif_health.py` with full occupancies, no disorder, and no hard or short O–O contacts. Final coordination is chemically sensible: MgWO4 has W–O = 1.744–2.136 Å and Mg–O = 2.113–2.136 Å; the two WO3 W sites have six O neighbors spanning 1.698–2.166 Å; MgO has six Mg–O contacts at 2.105 Å.

The WO3 assignment was challenged under the same nuisance model. Monoclinic COD 2311041 gave Rwp 8.57% before the later profile/coordinate refinements, compared with 10.71% for a triclinic record, 11.62% for an orthorhombic record, and 15.38% for a tetragonal record. A separate monoclinic record was rejected after health review because it contained a fully occupied 1.575 Å O–O contact with no peroxide chemistry; another failed with a 0.464 Å contact. These records were treated as competing descriptions, not additional phases.

MgWO4 atomic coordinates and the two X-ray-sensitive W coordinates in WO3 were refined. This structural change was replay-stable from either phase-first path and reduced Rwp from 2.306% to 1.789%. Refining all WO3 oxygen coordinates gave only a small further decrease and poorly determined oxygen shifts relative to the neutron structure, so those coordinates were not retained. Displacement-parameter trials approached bounds or correlated strongly with polarization; source values were therefore retained. The WO3 oxygen substructure and displacement parameters are consequently not independently determined by this Cu X-ray pattern.

The accepted profile uses a nonnegative common U/W/X model, one refined zero correction, refined polarization, and a 16-term smooth Chebyshev background. Inactive size terms are fixed at 10 µm, inactive strain is zero, inactive March ratios are one, roughness is zero, and SH/L is fixed at 0.002. Only replay-stable MgWO4 [010] March texture and WO3 [100] uniaxial microstrain were retained. Size, roughness, extra asymmetry, and unsupported strain terms were rejected.

Representative numerical profile checks after the final disk replay are:

| Family | Position obs/calc (°) | FWHM obs/calc (°) | Left HWHM obs/calc (°) | Right HWHM obs/calc (°) |
|---|---:|---:|---:|---:|
| MgWO4 (010) | 15.5757 / 15.5757 | 0.1296 / 0.1276 | 0.0696 / 0.0655 | 0.0600 / 0.0620 |
| MgWO4 (200) | 38.2973 / 38.2973 | 0.1770 / 0.1778 | 0.0654 / 0.0666 | 0.1116 / 0.1112 |
| MgO (200), Cu doublet | 42.9264 / 42.9156 | 0.1923 / 0.1938 | 0.0748 / 0.0629 | 0.1175 / 0.1308 |
| MgWO4 (023) | 65.3764 / 65.3764 | 0.2160 / 0.2130 | 0.1231 / 0.1261 | 0.0930 / 0.0869 |
| High-angle family | 88.3154 / 88.3262 | 0.1285 / 0.1439 | 0.0541 / 0.0692 | 0.0744 / 0.0746 |

The largest remaining correlated residual is around the intense WO3 23.5° complex; it is a modeled peak-shape/intensity residual rather than a new peak family.

## Chemical balance and uncertainty

Using Mg2+, W6+, and O2−, the precursor reaction MgO + WO3 → MgWO4 is charge balanced. The phase fractions imply an overall Mg:W molar ratio of 1.018:1 and residual MgO:WO3 of 1.037:1, consistent with an approximately 1:1 precursor mixture and partial reaction. Charge-balanced non-1:1 candidates Mg2WO5, Mg3WO6, MgW2O7, Mg2W3O11, and Mg3W2O9 were searched through exact/analogue records; none supplied an independent residual family. They remain only a weak-phase watch list below the reliable detection level of this dataset.

Formal GSAS-II fraction esds are about 0.06–0.07 wt%, but they exclude structure, texture, broadening, background, absorption, and fixed-displacement-parameter systematics. Model challenges move the reported fractions by several tenths of a weight percent, so the formal esds should not be read as absolute accuracy. The three crystalline fractions are reliable at roughly that several-tenths-wt% level; amorphous material, if present, cannot be quantified without an internal standard.
