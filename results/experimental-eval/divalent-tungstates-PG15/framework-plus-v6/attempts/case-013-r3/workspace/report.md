# Powder XRD phase analysis

The 500 °C PbO + WO3 reaction product is modeled with four crystalline phases. Fractions are normalized over these modeled crystalline phases only; no amorphous fraction can be obtained without an internal standard.

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| PbWO4, scheelite | I41/a, COD 9009811 | a = 5.46159, c = 12.0535 | 0.6063 (60.63 wt%) |
| PbO, massicot | Pbcm, COD 2310433 | a = 5.89577, b = 5.48767, c = 4.75548 | 0.0653 (6.53 wt%) |
| WO3, monoclinic | P21/c, COD 2311041 | a = 7.69992, b = 7.53881, c = 10.5740, beta = 136.345 | 0.1068 (10.68 wt%) |
| Pb2WO5 intermediate | C2/m Pb2MoO5 prototype, COD 7220560, with Mo6+ replaced by W6+ | a = 14.2340, b = 5.80773, c = 7.36435, beta = 113.969 | 0.2216 (22.16 wt%) |

## Evidence

Scheelite PbWO4 accounts for the dominant families near 27.7, 45.0, 55.5 and 72.3° 2theta. Massicot, rather than litharge, reproduces its distinct 29.3, 30.6, 32.9 and 38.1° families. Residual WO3 families are consistent with the room-temperature monoclinic phase. The phase inventory also gives an overall Pb:W molar ratio of about 1.07, close to the 1:1 precursor ratio.

A three-phase PbWO4 + PbO + WO3 model left coherent unmatched families near 25.9, 26.8, 31.0, 43.4, 47.3, 52.0 and 54.0°. These are reproduced by a Pb2WO5 model obtained from the isovalent Pb2MoO5 C2/m prototype. The substituted model passes contact/occupancy screening and gives tetrahedral W–O distances near 1.77 Å. Adding Pb2WO5 reduced Rwp from about 16.9% to 13.8% before its supported profile terms were introduced. Pb7W8O28.8 and a second triclinic WO3 phase both refined to zero scale when re-challenged under the final profile.

The final model uses a smooth seven-coefficient background, one specimen-height shift, nonnegative common U/W/X broadening, polarization, and fixed SH/L = 0.01897. Roughness and unsupported phase size/strain/texture terms were pruned. Pb2WO5 alone requires broad isotropic size broadening (0.04328 µm) and [100] March–Dollase texture (1.328); alternate texture axes and uniaxial strain did not replay better without bounds or scale coupling. The verified no-refinement replay gives Rwp = 13.1182%, Rp = 8.9840%, Rexp = 3.4954%, and GOF = 3.7530.

## Remaining uncertainty

The Pb2WO5 assignment is a chemically justified cross-chemistry prototype, not an exact Pb2WO5 database record. Its broad peaks make its scale, crystallite size and detailed atom arrangement correlated; therefore 22.16 wt% should be treated as semi-quantitative with a systematic uncertainty of several weight percent, substantially larger than the covariance e.s.d. in `result.json`. Its detailed structure is not determined as reliably as those of PbWO4 and PbO.

Monoclinic and triclinic WO3 records fit almost equally at this abundance (baseline delta-Rwp about 0.02 percentage point). Monoclinic WO3 was retained because it is the physically expected room-temperature polymorph after a 500 °C firing; the exact WO3 distortion is not uniquely resolved. Structured residual intensity remains strongest from about 25–55° and likely reflects the approximate Pb2WO5 prototype and unresolved profile/coordinate disorder. Consequently, the reported fractions should not be interpreted at the sub-percent precision implied by statistical e.s.d.s.
