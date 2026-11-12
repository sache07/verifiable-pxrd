# Powder-XRD phase analysis

## Result

The defensible crystalline model is single-phase wolframite **MnWO4**, space group **P 2/c** (No. 13), with a weight fraction of **1.000 (100 wt%) normalized over the modeled crystalline phases**. The refined cell is (a=4.83155), (b=5.75806), (c=4.99717) Å, β = 91.2173°, and (V=138.992) Å³. The fraction is not an assertion that the specimen contains no amorphous material or sub-detection crystalline residue.

## Evidence and model checks

The 1:1 Mn/W chemistry and 900 °C firing are consistent with MnWO4 formation. The P 2/c wolframite model accounts for independent low-, middle-, and high-angle families, including 18.60°, 23.81/24.28°, 30.05/30.53°, 36.21°, 37.46°, 40.53/41.12°, 48–53°, and multiple 63–88° reflections. No coherent unmatched family remains.

The starting topology was COD 1520200, the only exact occupied MnWO4 entry in the screened catalog. It is fully occupied and geometrically sound, but its source experiment was at 2.4 GPa; it was therefore used only as a wolframite topology, not as evidence that this sample was under pressure. Refinement against this scan gives a larger ambient-like cell and adjusted coordinates. The exported structure remains physically reasonable: W–O = 1.776–2.127 Å, Mn–O = 2.122–2.296 Å, full occupancies, and common positive (U_mathrm{iso}=0.0027) Å².

The final physical profile uses nonnegative (U=7.586), (W=33.524), and (X=1.127), SH/L = 0.02788, isotropic size = 0.111 µm, zero microstrain, and no preferred orientation. One angular correction was retained: specimen displacement = −464.9 µm; zero offset was fixed at zero. Polarization is 0.55. Surface roughness is needed for the low-angle intensity trend (A = 0.0467, B = 0.251), although those two coefficients are strongly correlated and should not be interpreted separately. The eight-term smooth background remains positive (398–2214 counts); no background peaks were used.

## Rejected watch-list phases and uncertainty

Mn3WO6, MnO, and orthorhombic Mn3O4 scales collapsed to zero; tetragonal Mn3O4 refined to only about 0.04 wt%. Mn2O3 trials gave about 0.37–0.41 wt%, but their gain came mainly from the ~55° overlap and was contradicted by stronger unique families near 33° and 66°.

Several physically valid WO3 records refined to approximately 0.28–0.50 wt% in fixed-cell scale challenges. Their small improvements were dominated by the 23–24° region while predicted unique peaks around 33–34°, 41°, 49–50°, and elsewhere worsened the fit. Allowing the triclinic WO3 cell to move produced a nonconverged solution and an implausible 1.6% volume contraction; the tetragonal alternative still relied almost entirely on one ~24.06° window. These records were therefore not accepted as phases. A WO3 or Mn oxide residue at roughly the sub-0.5-wt% level cannot be identified or quantified reliably from this pattern, so no structure or fraction is reported for it.

The independently regenerated full-grid fit has (R_{wp}=5.3091%), (R_p=4.0434%), and sqrt(reduced χ²) = 1.5364 using (1/\max(I_mathrm{obs},1)) weights. Remaining residuals are chiefly paired peak-shape/intensity lobes of MnWO4 rather than a consistent second-phase pattern. `fit.csv` was generated from a fresh atomic replay of `final.gpx`, and that replay reported no physical-profile flags.
