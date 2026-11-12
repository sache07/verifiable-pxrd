# Powder diffraction phase analysis

## Result

The pattern is described by two crystalline phases: monoclinic γ-WO₃ (74.47 wt%) and cubic bixbyite α-Mn₂O₃ (25.53 wt%). Fractions are normalized only over these modeled crystalline phases. Their formal one-standard-deviation scale-factor uncertainty is about 0.27 wt%, while a more realistic model-dependent uncertainty is approximately 2 wt% absolute for either fraction.

The final Rietveld fit has Rwp = 6.813%, Rp = 4.935%, Rexp = 2.662%, and goodness of fit = 2.564. The calculated pattern, observed pattern, difference, and background are tabulated in `fit.csv`; the exact GSAS-II model is in `final.gpx`.

## Evidence

The diagnostic γ-WO₃ cluster at approximately 23.43, 23.91, and 24.68° 2θ, together with its split reflections from 33–35°, requires the monoclinic WO₃ model. Reflections near 33.27, 38.53, 49.61, 55.49, and 66.03° are accounted for independently by bixbyite Mn₂O₃. A one-phase WO₃ refinement left these peaks unexplained and gave Rwp near 11%; adding Mn₂O₃ reduced Rwp to about 8% before the final profile treatment and to 6.813% in the submitted refinement.

Candidate manganese tungstates were tested but rejected: the prominent MnWO₄ doublet near 30–31° and its low-angle line near 18.5° are absent, as are the strongest expected Mn₃WO₆ features near 20–21°. Thus the crystalline material is best interpreted as largely unreacted oxide precursors after the reported 500 °C treatment, with no detectable crystalline manganese tungstate required by the data.

## Structural refinement and uncertainty

Starting structures were COD 2311041 for γ-WO₃ (P2₁/c, No. 14) and COD 1514230 for α-Mn₂O₃ (Ia-3, No. 206). Unit-cell parameters, phase scales, specimen displacement, background, selected profile terms, effective polarization, and one isotropic microstrain term per phase were refined. Atomic coordinates were retained from the references. A common fixed Uiso = 0.005 Å² was used so unlike legacy displacement parameters in the two references could not bias the quantitative scale ratio. The unconventional but valid P2₁/c cell setting of COD 2311041 was retained in the WO₃ CIF.

The structural assignments are strong, but the exact fractions are less certain than their formal covariance errors. No calibrated instrumental profile or pointwise measurement uncertainties were supplied; Poisson counting uncertainties were used, and profile/polarization and common-ADP choices shift the WO₃ fraction by roughly 2 wt%. No microabsorption correction was possible, and any amorphous material is excluded from the normalization. A triclinic WO₃ candidate can mimic the pseudosymmetric peak set, but its freely refined cell angles moved close to 90°, favoring the room-temperature monoclinic assignment; subtle WO₃ polymorph intergrowth cannot be excluded. The refined microstrain values are empirical peak-width terms and should not be interpreted quantitatively without an instrumental standard.
