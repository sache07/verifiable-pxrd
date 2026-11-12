# Powder-XRD phase analysis

The crystalline pattern is described by four phases. Fractions are normalized
over those modeled crystalline phases.

| Phase model | Space group | Weight fraction | Formal GSAS-II e.s.d. |
|---|---:|---:|---:|
| CuWO4 | P -1 | 0.65157 (65.16 wt%) | 0.00038 |
| WO3 | P 21/c | 0.19324 (19.32 wt%) | 0.00035 |
| Cu3WO6 | P a -3 | 0.12948 (12.95 wt%) | 0.00022 |
| CuO | C 2/c | 0.02571 (2.57 wt%) | 0.00021 |

## Evidence

The precursor context (CuO + WO3, 700 °C) is chemically consistent with
dominant triclinic CuWO4 plus unreacted WO3/CuO and a Cu-rich tungstate oxide.
CuWO4 accounts for the dominant peak family. A same-formula WO3 screen favored
COD 2311041 (P 21/c; common shift-level Rwp 10.264%) over the close triclinic
alternative COD 2106293 (10.341%) and over the other valid monoclinic,
orthorhombic and tetragonal trials (about 11.2–30.9%). Cu3WO6 gives stable
intensity at the otherwise unexplained 15.20, 19.80, 32.51, 33.78, 36.24,
49.70, 57.60, 63.29 and 70.23° family. Minor CuO closes the 35.09, 38.32,
48.45, 53.04, 58.11 and 65.34° family.

Cu2O, Cu2WO4, the high-pressure CuWO4 polymorph and an additional triclinic WO3
were removed because their small apparent gains required implausible cell
changes; Cu4O3 refined to zero scale. Once the four retained phases were active,
the largest residuals were positive/negative lobes at already modeled peaks,
not a coherent new peak family. The complete branch record is in
`analysis/candidate_ledger.md`.

Refinement was staged through scale/background, specimen shift and cells,
limited coordinates, then supported isotropic profile terms. Surface roughness,
March-Dollase texture and uniaxial strain were rejected as correlated,
boundary-seeking or non-improving. All four exported structures pass the
occupancy/contact geometry screen. A fresh read-only GSAS-II reconstruction of
`final.gpx` on all 8301 observations gives Rwp = 2.59323%, Rp = 1.87593% and
GOF = 1.61058, with no replay profile warnings.

## Remaining uncertainty

The quoted e.s.d.s are covariance-only and are smaller than realistic
model-selection/profile uncertainty. In particular, the 2.57 wt% CuO component
is weak, and its conventional C2/c model is powder-equivalent here to the tested
Cc description; that subtle symmetry choice cannot be determined reliably from
this pattern. The P 21/c WO3 model is preferred consistently, but the close
triclinic alternative is the principal polymorph uncertainty. Oxygen positions
were only released where shifts remained physically supported (CuWO4); parent
coordinates were retained for the weaker phases. The common instrumental U and
X terms reached their allowed minima and were frozen, so the partition between
instrumental and sample broadening is not uniquely determined. The reported
fractions do not measure amorphous material or any unmodeled noncrystalline content and therefore
must not be interpreted as absolute bulk assay fractions.
