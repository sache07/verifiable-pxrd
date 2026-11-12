# PXRD phase analysis

The pattern is best described by four crystalline phases. Fractions below are normalized over those modeled crystalline phases; they do not quantify amorphous material.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| PbWO4, scheelite | `I 41/a`, adapted from COD 9009811 | 0.56194 (56.19 wt%) |
| WO3, monoclinic | `P 21/c`, adapted from COD 2311041 | 0.21507 (21.51 wt%) |
| Pb3O4, minium | `P 42/m b c`, adapted from COD 9012124 | 0.17586 (17.59 wt%) |
| PbO, orthorhombic massicot | `P b c m`, adapted from COD 2310433 | 0.04713 (4.71 wt%) |

The formal one-sigma fraction uncertainties from the final covariance matrix are 0.18, 0.12, 0.18, and 0.11 wt%, respectively. They are smaller than the likely systematic uncertainty; about ±1 wt% absolute is a more realistic interpretation for each fraction, particularly PbO.

## Evidence and refinement

PbWO4 accounts for the dominant families at approximately 27.81, 30.02, 33.16, 45.13, 47.37, 51.59, 55.63, 56.89, and 72.36 degrees 2theta. The WO3 assignment is required by the characteristic 23.53/24.01/24.85 degree triplet and repeated higher-angle families. Pb3O4 is supported independently near 26.81, 31.22, 32.55, 52.52, 58.54, and 66.40 degrees. PbO has a positive replay-stable scale and independent residual families near 29.56, 38.25, 45.5, 53.59, 60.73, and 63.53 degrees when omitted; removing it worsens Rwp from 4.94% to 5.93% under the same nuisance model.

The full 9.903-100.095 degree range was refined and then reopened/replayed. The final statistics are Rwp = 4.943%, Rp = 3.557%, Rexp = 2.485%, and goodness-of-fit = 1.993 (8,301 observations, 34 variables). The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio were fixed to the metadata. The retained nuisance model uses one zero correction (+0.44197 degrees), a common low-dimensional profile, one surface-roughness term, phase scales/cells, generalized tetragonal strain for PbWO4, and isotropic strain for Pb3O4 and PbO. Size was fixed at the neutral 10 micrometre value, and preferred orientation, asymmetry, transparency, sample shift, and WO3 strain were left neutral after unsupported or nonphysical trials.

For isolated PbWO4 low/middle/high-angle families, observed versus calculated peak position and FWHM are 27.811/27.811 and 0.248/0.231 degrees; 45.132/45.121 and 0.323/0.322 degrees; and 68.984/68.984 and 0.440/0.477 degrees. Their observed/calculated left-right half-widths are 0.119/0.130 versus 0.109/0.122, 0.146/0.178 versus 0.136/0.186, and 0.158/0.282 versus 0.192/0.285 degrees. Generalized PbWO4 strain was retained because it is physical and replay-stable, improves several symmetry-distinct families, and lowers Rwp from 4.988% to 4.943%; its effective strain remains positive over all measured PbWO4 reflections.

Source and polymorph challenges favor the retained records. With matched nuisance terms, the closest triclinic WO3 competitor gives Rwp = 6.37%; the closest alternate PbWO4 record remains nonconvergent at Rwp = 6.25%; the alternate PbO record develops an invalid metric and extreme broadening. Removing Pb3O4 was also strongly rejected. No same-composition coexistence was supported. Searches for balance-motivated Pb2WO5/Pb3WO6 analogues and inspection of a disordered Pb7W8O28.8 record found no additional independent residual families, so these remain unretained watch-list possibilities.

All final CIFs pass `learned/cif_health.py`: they are ordered, fully occupied, and have no invalid sites or hard contacts. Refined nearest bonds are chemically plausible (PbWO4 W-O minimum 1.777 A; WO3 W-O 1.716-2.161 A; Pb3O4 Pb-O minimum 2.131 A; PbO Pb-O minimum 2.169 A). Atomic coordinates and occupancies were inherited from the screened source records; only cells and powder/HAP parameters were refined.

## Remaining uncertainty

The strongest remaining positive residuals coincide with modeled reflections, especially the WO3 triplet and high-angle PbWO4 lines, rather than forming a coherent new phase. Some high-angle PbWO4 peaks remain calculated slightly too broad, and the goodness-of-fit remains above one. This is consistent with unresolved profile/intensity systematics and with pointwise standard uncertainties and a calibrated instrumental profile not being supplied. The metadata gives precursor identities but no amounts or ratio, so no balance constraint was imposed; the fitted crystalline assemblage implies Pb/W = 1.025, close to 1:1. Absolute phase fractions including amorphous content cannot be determined reliably without an internal standard.
