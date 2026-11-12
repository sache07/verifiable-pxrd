# Powder XRD phase analysis

## Result

The crystalline specimen is modeled as **triclinic CuWO4 (P -1), 97.22 wt%**, plus **monoclinic WO3 (P 21/c), 2.78 wt%**. Fractions are normalized to the modeled crystalline material. The GSAS-II covariance standard uncertainties are 0.06 and 0.06 wt percentage point, respectively.

The final full-range fit (9.9034-100.0949 degrees 2theta, 8,301 points, Cu Kalpha1/Kalpha2) has Rwp = 4.167%, Rp = 3.242%, Rexp = 2.433%, and goodness-of-fit = 1.718. The refined cells are:

- CuWO4: a = 4.70852, b = 5.84290, c = 4.88172 A; alpha = 88.3455, beta = 92.5335, gamma = 97.2504 degrees; V = 133.06195 A^3.
- WO3 (the reference P 21/c setting): a = 7.69053, b = 7.53907, c = 10.52491 A; beta = 136.0667 degrees; V = 423.38916 A^3.

## Evidence and model selection

The CuO + WO3 starting chemistry and 800 C treatment support CuWO4 formation. An ambient CuWO4 topology, initialized from COD 2101690 ((Cu0.9Zn0.1)WO4 with Zn replaced by Cu), indexes the dominant pattern. Refining its cell and coordinates gave a one-phase Rwp of 5.263%. Coherent residual peaks at approximately 23.45, 24.69, 33.59, and 34.49 degrees match multiple reflections of ambient monoclinic WO3 (COD 2311041); adding it lowered Rwp to 4.237% before supported profile terms and to 4.167% in the final model. A physical CuO C2/c trial refined to the imposed near-zero scale boundary (about 5e-9 normalized fraction), so CuO was not retained. No remaining coherent reflection family supports a third crystalline phase.

The submitted CuWO4 geometry is physical: Cu-O distances span 1.90-2.41 A and W-O distances 1.81-2.26 A. Two bounded coordinate restarts converged to a slightly worse solution. WO3 coordinates were retained from the ambient reference because unconstrained coordinate refinement of this approximately 3 wt% phase was unstable and produced inferior local geometry; its phase identity, cell, and amount are supported, but its detailed atomic coordinates are not independently determined by this pattern.

Instrument zero and sample-height shift were nearly perfectly correlated. The insignificant zero offset was fixed at 0, while a specimen displacement of about -596 micrometres was retained. The polarization factor was fixed at the instrument value of 0.8 because refining it was strongly correlated with the common displacement parameter and changed Rwp by only about 0.003 percentage point. A weak CuWO4 [001] March-Dollase term and [001] uniaxial microstrain were retained because each gave reproducible improvements; unsupported WO3 texture/size/strain terms were omitted.

## Uncertainty

The formal phase-fraction standard uncertainty is about 0.06 wt percentage point, but model variants place WO3 between roughly 2.5 and 2.8 wt%. A practical uncertainty of about +/-0.3 wt percentage point is therefore more realistic. Trace CuO below the powder-XRD detection limit cannot be excluded, and no amorphous fraction can be determined without an internal standard. The files `phase_CuWO4.cif`, `phase_WO3.cif`, `fit.csv`, and `final.gpx` all come from the same selected full-grid checkpoint.
