# PXRD phase analysis

The modeled crystalline material is **wolframite MnWO4, 97.45 wt%**, plus **low-symmetry WO3, 2.55 wt%**, normalized over the modeled crystalline phases. The tabulated GSAS-II standard uncertainty is 0.065 wt% for either fraction, but a more realistic model-dependent uncertainty for WO3 is about +/-0.3 wt%; amorphous material was not measured.

## Evidence

MnWO4 accounts for the characteristic P 2/c wolframite families over the full 9.90-100.09 degree range, including the low-angle 010/100 pair and the split 11-1/111 group near 30 degrees. Its refined cell is a = 4.83209, b = 5.75836, c = 4.99749 A, beta = 91.2186 degrees. The starting exact-composition record (COD 1520200) was collected under pressure, so its scale and cell were not accepted uncritically: the cell and coordinates were refined, alternative wolframite records/prototypes were screened, and the final octahedra are physical (Mn-O 2.10-2.31 A; W-O 1.77-2.14 A).

Weak but coherent intensity around the WO3 triplet at approximately 23.5-24.7 degrees and supporting families near 27-29 and 33-35 degrees requires residual WO3. Monoclinic COD 2311041 (neutron structure, P 21/c) gave the best single-record fit. Its refined cell is a = 7.68454, b = 7.54141, c = 10.52397 A, beta = 136.0649 degrees (an unconventional but valid setting), with 2668(427) microstrain. The WO3 coordinates were kept at the source values because this minor phase cannot support an independent positional refinement.

Monoclinic and triclinic WO3 records fit almost equally well and give 2.4-2.5 wt% total WO3. A two-polymorph fit split the same overlapping families with strongly anticorrelated scales; it did not provide decisive unique-family evidence. Therefore the exact WO3 polymorph cannot be determined reliably from this pattern, and one monoclinic model is reported rather than an unjustified polymorph mixture.

Mn3WO6 refined to zero. MnO, Mn2O3, and Mn3O4 trials produced only residual-level sub-0.3 wt% fits: one or two windows improved while other strong predicted families were absent. In particular, the apparent Mn3O4 low-angle signal tracked an MnWO4 asymmetry shoulder. Orthorhombic, tetragonal, and hexagonal WO3 records likewise failed the common-profile re-challenge. These candidates are not quantified reliably and were omitted.

## Refinement and uncertainty

The final full-range GSAS-II refinement used the supplied Cu K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio, a smooth six-term Chebyshev background, one specimen-shift correction, positive surface roughness, and refined axial asymmetry. The common profile has nonnegative U/W/X = 64.739/0/4.768. Unsupported size, MnWO4 strain, anisotropic broadening, and preferred orientation terms were pruned after save/reopen replay tests. Final statistics are Rwp = 4.531%, Rp = 3.507%, Rexp = 2.759%, and GOF = 1.645.

No pointwise uncertainties were supplied, so Poisson count weights were used. The formal fraction errors consequently exclude source-model choice, microabsorption/roughness, and other systematic effects; the exact fractions in `result.json` are those of the submitted model, while approximately 97.5(3) wt% MnWO4 and 2.5(3) wt% WO3 better represent practical certainty.
