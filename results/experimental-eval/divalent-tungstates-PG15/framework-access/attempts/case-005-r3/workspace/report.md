# Powder X-ray diffraction analysis

The pattern is modeled as a two-phase crystalline mixture of spinel Co3O4 and monoclinic WO3. The refined crystalline weight fractions are **23.95 wt% Co3O4** and **76.05 wt% WO3**, normalized to the two modeled crystalline phases.

## Evidence

The Co3O4 assignment is fixed by its characteristic spinel sequence, including measured maxima near 19.37, 31.64, 37.20, 38.91, 45.15, 59.67, and 65.55 degrees 2theta after the common specimen-height correction. The remaining strong and split reflections, especially the clusters at 23–25 and 33–35 degrees, are accounted for by monoclinic WO3. This is chemically consistent with the stated Co3O4 + WO3 precursor mixture. Searches and trial refinements did not reveal a coherent unmatched peak set attributable to CoWO4 or another cobalt–tungsten oxide. Alternative WO3 models gave materially poorer fits or converged toward the selected monoclinic metric.

The starting atomic models were COD 9005896 for Co3O4 and COD 2311041 for WO3. Refinement gave Co3O4 in Fd-3m with a = 8.08246 A, and WO3 in the submitted P21/c setting with a = 7.69286 A, b = 7.53569 A, c = 10.54514 A, and beta = 136.159 degrees. Phase scales were converted to mass fractions using the GSAS-II unit-cell masses.

The final full-grid agreement is Rwp = 3.066%, Rp = 2.217%, and goodness of fit = 1.784 using 1/max(counts,1) weights. The calculation includes the reported Cu Kalpha1/Kalpha2 doublet, a refined common specimen displacement of about -610 micrometres, peak broadening, polarization, and a smooth background. The profile in `fit.csv` was regenerated from `final.gpx`, rather than copied from cached calculated arrays.

## Remaining uncertainty

The phase identities and unit cells are robust. The scale factors are correlated with background, polarization, and broadening; an approximate practical uncertainty of about 0.02 absolute weight fraction is more defensible than the formal last-cycle standard errors. The reported fractions describe only the modeled crystalline material: amorphous content and a trace crystalline component below the pattern's detection level cannot be quantified or excluded.

WO3 oxygen coordinates are much less strongly constrained by laboratory X-ray data than the tungsten sublattice and were kept close to the chemically valid starting geometry; individual W/O coordinates should not be interpreted as a high-precision structure determination. No separate product-phase structure or fraction can be determined reliably because no corresponding diffraction signature is resolved.
