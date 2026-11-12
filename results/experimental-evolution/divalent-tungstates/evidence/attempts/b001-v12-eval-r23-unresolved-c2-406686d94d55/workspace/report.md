# PXRD phase analysis

## Result

The crystalline pattern is modeled by reaction product scheelite PbWO4 plus unreacted WO3 and Pb3O4. Fractions are normalized only over these modeled crystalline phases.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| PbWO4 | scheelite, `I 41/a`, COD 9009811 | 0.6060 (60.60 wt%) |
| WO3 | monoclinic, `P 21/c`, COD 2311041 | 0.2198 (21.98 wt%) |
| Pb3O4 | tetragonal minium, `P 42/mbc`, COD 9012124 | 0.1742 (17.42 wt%) |

The full-range final fit (9.9034–100.0946° 2θ, 8301 points) has Rwp = 5.0718%, Rp = 3.3918%, and GOF = 2.0441. The submitted CIFs contain refined cells and the fixed source-record atomic coordinates; the powder data do not reliably support refining atomic coordinates.

## Evidence

The three structures account for distinct peak families. Monoclinic WO3 gives the sharp 23.53/24.02/24.84° triplet. Scheelite PbWO4 accounts for the broad families near 27.81, 33.16, 47.37, 55.6, 68.98, and 72.34°. Pb3O4 is required by positive, replay-stable intensity at independent noncoincident families near 31.22 and 32.55°, with further support around 47.9, 58.5, and 66.4°. Removing Pb3O4 raised the earlier common-profile fit from about 6.8% to 9.7% Rwp.

Isolated-family auditing found WO3 peak-position differences of about 0.005–0.007° and FWHM differences near 0.008° for the low-angle triplet. Representative PbWO4 low-, middle-, and high-angle positions agreed within 0.014°. Uniaxial size broadening was reproducible for PbWO4 and Pb3O4; a small PbWO4 [100] March–Dollase term also survived removal/replay and shared-intensity challenges. Strain trials crossed negative or collapsed, and were rejected. Refined polarization approached its physical boundary, while joint polarization/roughness became nonphysical, so the final model retains the replay-stable one-parameter roughness correction with polarization fixed at the unpolarized value.

Source competition remained decisive after cross-seeding the mature profile. The retained model reproduced Rwp = 5.078% on the search range, compared with 5.317% for Pb7W8O28.8, 5.458% for the nearest alternate monoclinic WO3 record, and 5.152% for the alternate tetragonal Pb3O4 record. Triclinic WO3 and orthorhombic Pb3O4 were substantially worse; the latter also collapsed a width and distorted its cell. Raspite PbWO4 was rejected much earlier by a very poor fit. All final CIFs pass `learned/cif_health.py` without invalid occupancies or hard contacts.

The assemblage is chemically plausible for incomplete reaction of the reported precursors. Reversing `Pb3O4 + 3 WO3 -> 3 PbWO4 + 1/2 O2` through the fitted fractions gives an approximate initial WO3:Pb3O4 molar ratio of 3.27:1. This was not imposed because no precursor amounts were supplied.

## Remaining uncertainty

The covariance-only fraction uncertainties are about 0.14–0.18 wt% absolute, but they are optimistic because pointwise uncertainties and a calibrated instrumental profile were unavailable. Source/background/intensity-correction challenges indicate a more realistic systematic uncertainty of roughly 1–2 wt% absolute, greatest for Pb3O4. High-angle PbWO4 width/asymmetry is not fully reproduced. No amorphous fraction or absolute crystalline content can be determined without an internal standard, so the reported fractions must not be interpreted as whole-sample fractions if amorphous material is present.
