# Powder XRD phase analysis

The modeled crystalline fraction contains three phases:

| Phase | Space group | Weight fraction |
|---|---:|---:|
| MnWO4, wolframite | P 2/c | 70.04% |
| WO3 | P 21/c | 14.92% |
| Mn3WO6 | C 2/c | 15.04% |

Fractions are normalized over these modeled crystalline phases. The full-grid, zero-optimization replay of `final.gpx` gives Rwp = 7.259%, Rp = 4.013%, and GOF = 4.098. The replay reported no physical/profile review flags, and the exported structures have no short contacts (minimum distances 1.77, 1.72, and 1.90 Å, respectively).

## Evidence

The ordinary MnWO4 and WO3 references account for the dominant wolframite and monoclinic-WO3 reflection families expected from WO3 + Mn3O4 fired at 800 °C. Their subtraction left a coherent set at approximately 20.32, 20.88, 29.15, 32.26, 35.62, 46.20, 47.02, 54.91, 55.85, 57.00, 64.89, and 66.96° 2theta. A lower-symmetry C 2/c Mn3WO6 model indexes that complete family, including the diagnostic 20.32/20.88° split. It is also chemically compatible with the 1:1 precursor-metal balance: Mn3WO6 accompanied by two WO3 formula units has Mn:W = 1:1.

No exact Mn3WO6 reference was available, so its model was made by Zn→Mn and Te→W substitution in the C 2/c Zn3TeO6 topology (COD 2211529), followed by common cell and bounded coordinate adaptation. A second physical C 2/c start derived from Co3TeO6 was developed identically but remained much worse (about 14.3% versus 10.0% Rwp at the matched structural checkpoint). R-3 and Pnma alternatives could not reproduce the split residual families and required profile terms at supplied bounds. The final C 2/c model has a stable [110] March–Dollase basin (ratio about 0.73 from independent 0.8 and 1.2 starts).

Two Pbcn Mn2WO6 starts gave only 0.26–0.43 wt% trial contributions and no distinct residual family; Mn3O4 and trirutile trial scales collapsed to zero. These phases were therefore not retained. The zero-scale cell trials became numerically ill-conditioned, which was treated as unknown rather than as structural disproof; the exclusion is based on the absence of a stable positive reflection-family contribution. Surface roughness, coupled zero/shift calibration, and refined common Uiso branches were likewise rolled back when they became bound-pinned or inseparable.

## Remaining uncertainty

MnWO4 and WO3 are well identified. Mn3WO6 is well supported as a phase and C 2/c topology, but its exact atomic coordinates are less certain because the structure is analogue-derived and several reflections remain intensity-mismatched. Its approximately 15 wt% fraction is consequently more model-dependent than the ordinary-phase fractions. A sub-0.5 wt% Pbcn component cannot be established or strictly excluded from this scan. No formal fraction uncertainties are claimed because profile overlap and structural-model systematics dominate the covariance estimates.
