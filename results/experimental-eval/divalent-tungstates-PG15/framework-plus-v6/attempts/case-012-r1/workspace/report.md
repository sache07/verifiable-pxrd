# Powder X-ray diffraction phase analysis

## Result

The crystalline sample is modeled as two phases:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| NiWO4 | wolframite, P 2/c; a = 4.59958, b = 5.66189, c = 4.90931 Å, beta = 89.9826° | 0.76113 (76.11 wt%) |
| WO3 | monoclinic, P 21/c; a = 7.30145, b = 7.53201, c = 10.52627 Å, beta = 133.0915° | 0.23887 (23.89 wt%) |

Fractions are normalized over these modeled crystalline phases; an amorphous fraction was not determined. The formal GSAS-II scale-derived standard uncertainty is about 0.0012 in absolute fraction, but model/background trials indicate a more realistic systematic uncertainty of roughly 0.01 (about one absolute wt percentage point) for each complementary fraction.

## Evidence and model selection

The precursor chemistry (NiO + WO3 heated at 900 °C) supports formation of NiWO4 with residual WO3. The wolframite assignment accounts for the coherent families at approximately 19.19, 23.91, 24.85, 30.87, 36.52, 39.10, 41.63, 44.70, 54.58 and 62.28° 2theta. Monoclinic WO3 is required by its characteristic low-angle group near 23.06, 23.53 and 24.28°, as well as families near 26.53, 28.82, 33.20–34.09, 49.87 and 55.88°.

No exact NiWO4 record was available in the screened index. Stoichiometric analogue searching identified wolframite parents; the physically sound ZnWO4 record COD 1520641 was converted by Zn-to-Ni substitution and then its cell and coordinates were refined. Under the same initial nuisance model it fit better than MnWO4- and CdWO4-derived alternatives (Rwp 6.447%, 6.467% and 7.371%, respectively). The WO3 model started from the room-temperature P21/c record COD 2311041. Other WO3 records were challenged: Pnma was clearly inferior, while a lower-symmetry P-1 model gave only a very small final profile advantage (Rwp 4.210% versus about 4.229%) at the cost of more independent structural variables and less stable geometry. P21/c was retained as the more parsimonious, physically appropriate assignment.

NiO was explicitly added as a watch-list phase after the common profile was established. Its scale collapsed to the numerical floor (modeled fraction about 1.6e-14; integrated intensity about 8.5e-9), so there is no reliable diffraction evidence for crystalline NiO. No third crystalline phase can be quantified from this pattern.

## Refinement and verification

The final full-range refinement used all 8,282 points from 10.0094 to 99.9944° 2theta and the reported Cu K-alpha doublet. It refined a smooth 12-term Chebyshev background, both phase scales and cells, one angular zero correction, common nonnegative U/W Gaussian width terms, phase-specific isotropic crystallite sizes, and supported atomic coordinates. The refined sizes are approximately 0.172 µm for NiWO4 and 0.133 µm for WO3. Isotropic displacement parameters were constrained to one value per phase (0.0053 and 0.0068 Å²). Polarization was established at 0.6202 before the displacement-parameter step and then fixed to avoid their strong common intensity correlation.

Trials of microstrain, surface roughness, preferred orientation along several symmetry-distinct axes, and an NiO scale were unsupported or acted as correlated surrogates and were pruned. X was fixed at 3.0 after its exact tradeoff with isotropic size was demonstrated; SH/L was fixed at the grid-selected 0.01. The background and total calculated intensity remain positive over the complete scan.

Fresh native GSAS-II forward replay of `final.gpx`, with no optimization and regenerated reflection lists, gives Rwp = 4.2288%, Rp = 3.2519%, Rexp = 3.4788%, and Rwp/Rexp = 1.2156. Phase RF values are 1.62% for NiWO4 and 3.16% for WO3. Replay produced no profile-validity flags, and both exported CIFs pass the occupancy/contact geometry screen.

## Remaining uncertainty

The phase identities and two-phase fractions are robust, but the detailed WO3 distortion is less certain than its identity. The two refined W-site x and z coordinate modes are 98–99% correlated, and freely refining the WO3 oxygen positions produced nonphysical short contacts; those oxygen coordinates were therefore retained from the parent model. Powder data alone do not decisively distinguish the selected P21/c description from a very small triclinic distortion. The submitted P21/c CIF should consequently be treated as a defensible average structural model, not a unique determination of every WO3 atomic coordinate.
