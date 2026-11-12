# Powder XRD phase analysis

The crystalline sample is modeled as **80.10 wt% scheelite CaWO4**, **13.83 wt% monoclinic gamma-WO3**, and **6.07 wt% calcite CaCO3**, normalized over the three modeled crystalline phases. This is consistent with partial reaction of the WO3 + CaCO3 charge during the reported 650 degrees C treatment.

## Evidence

Scheelite CaWO4 accounts for the strong reflections near 18.27, 28.43, 31.21, 33.84, 46.89, 54.16, and 57.65 degrees 2theta. The characteristic WO3 group near 22.76, 23.18, and 23.98 degrees, together with its weaker reflections, requires a second phase. A two-phase CaWO4/WO3 fit left a concentrated positive residual around 29.1 degrees, at the displaced calcite 104 reflection. Adding calcite also accounts for its weaker, partly overlapped reflections: Rwp decreases from 3.358% to 3.135%, and the weighted chi-square decreases by about 1221. Its positive scale corresponds to approximately 6 wt%, so it is not merely a trace peak fitted at zero abundance.

COD models 7219229 (CaWO4, I 41/a), 2311041 (WO3, P 21/c), and 1547347 (calcite, R -3 c) were used as starting structures and refined or profile-scanned in GSAS-II. The final cells are a = 5.24128 A and c = 11.34184 A for CaWO4; a = 7.70055 A, b = 7.56266 A, c = 10.52648 A, beta = 135.9508 degrees for WO3; and a = 4.99121 A, c = 17.06859 A for calcite. A triclinic WO3 model was the closest alternative, but the monoclinic model gave consistently better whole-pattern agreement; orthorhombic and tetragonal alternatives were substantially worse.

The final atomic-model fit has Rwp = 3.13493%, Rp = 2.41184%, and goodness of fit = 1.00191 over all 8301 raw-count points. The counting-statistical expectation is Rwp about 3.138%, indicating that no material structured residual remains. Independent no-refinement replay of `final.gpx` regenerated the reflection lists and structure factors, reproduced the reported fractions and profile, and found no negative-background, negative-width, displacement-parameter, or polarization flags.

## Uncertainty

The three-phase inventory and dominant scheelite structure are well supported. The calcite scale remains near 6 wt% across physically allowed size/profile tests, but its crystallite size, shared displacement parameter, and sole free oxygen coordinate are weakly identified because its higher-angle peaks are small and overlapped. Those calcite details in the CIF should therefore be treated as a plausible structural model rather than a precise atomic refinement; the calcite fraction is reasonably quoted to roughly +/-0.7 percentage point. Correlations among thermal factors, peak broadening, background, and surface roughness make uncertainties of about 1-2 percentage points more realistic for the major-phase fractions than formal scale-factor errors alone.

The WO3 tungsten framework and monoclinic cell are supported, but monoclinic versus a very weak triclinic distortion is not uniquely resolved for this minor phase, and its oxygen coordinates are not independently precise. The reported fractions describe only the modeled crystalline material; amorphous content cannot be quantified from this scan without an internal standard.
