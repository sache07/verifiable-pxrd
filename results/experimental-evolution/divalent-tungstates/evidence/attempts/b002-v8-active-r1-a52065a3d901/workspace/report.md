# PXRD phase analysis

## Result

The pattern is described by four crystalline phases. Fractions are normalized over these modeled crystalline phases; they do not measure amorphous material.

| Phase | Space group | Weight fraction | Formal GSAS-II e.s.d. |
|---|---:|---:|---:|
| BaWO4 (scheelite) | I 41/a | 0.65829 (65.829 wt%) | 0.00133 |
| WO3 (gamma-monoclinic model) | P 21/c | 0.13344 (13.344 wt%) | 0.00118 |
| Ba3W2O9 | R -3 c | 0.15695 (15.695 wt%) | 0.00099 |
| BaCO3 (witherite) | P m c n / standard Pnma setting | 0.05132 (5.132 wt%) | 0.00094 |

Full-range statistics (9.9034–100.0946 degrees 2theta, 8,301 points) are Rwp = 3.1740%, Rp = 2.4374%, Rexp = 3.0170%, GOF = 1.0521, and Durbin-Watson = 1.8127.

## Phase and structure evidence

The dominant scheelite BaWO4 family is accompanied by the characteristic WO3 low-angle triplet and its higher-angle lines. Independent residual families require Ba3W2O9 (including lines near 16.5, 17.8, 26.3, 27.8, 30.8, 37.7, 40.8, 51.8, 63–64, 70–72, and 88.6 degrees) and residual BaCO3 precursor (notably near 24.2/24.5, 28.1, 34.3/34.9, 42.3, 45.2, and 47.3 degrees). Their addition removes coherent families rather than merely lowering the global residual.

The retained starting models were an ordered scheelite analogue adapted to BaWO4 (COD 1546036), gamma-WO3 (COD 2311041), exact Ba3W2O9 (COD 1533878), and witherite BaCO3 (COD 9010928). All four submitted CIFs pass `learned/cif_health.py` with full occupancy and no hard contacts. The exact BaWO4 record COD 1527204 was reviewed because of split half-occupied oxygen sites and a 1.17 A O-O contact; the ordered model both removes that nonphysical split and fits slightly better under the same nuisance model (three-phase Rwp 6.067% versus 6.151%). Reviewed WO3 COD 1528915 and triclinic WO3 COD 2106293 fit worse than the retained passing record. Atomic coordinates were kept at the source-model values; the powder data reliably refine cells and identify structure types, but do not independently determine all internal coordinates.

Charge-balanced non-1:1 Ba-W-O products were explicitly challenged. The exact stoichiometric search selected Ba3W2O9. Ba3WO6 refined to zero scale, a small-cell WO3 replacement gave Rwp 5.456%, and Ba0.9W6O18 has strong predicted signature lines that are absent. These were not retained as simultaneous phases.

## Refinement and profile checks

The final GSAS-II project uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio, Poisson count weights because pointwise uncertainties were not supplied, an eight-term Chebyshev background, one specimen-shift correction, and common nonnegative U/W/X terms. SH/L was held at its neutral 0.002 value. Inactive size, strain, March-Dollase, H-strain, extinction, and transparency terms were genuinely neutralized before testing. Polarization was fixed at 0.5: freeing it ran to an unphysical 1.038, while polarization and roughness tests were not complementary. Surface roughness was retained after replay; no texture term was used.

The structured WO3 peak-width residual required one phase width term. Effective isotropic size gives 0.14285(54) micrometres, Rwp 3.1740%, and DW 1.813; isotropic strain gives nearly the same Rwp, 3.1759%. Thus the broadening is real, but its size-versus-strain origin cannot be determined reliably. For Ba3W2O9, strain (1,476(69) microstrain) was replay-stable and fit better than the size-only alternative. All other phase sizes remain at the neutral 10 micrometre value and all other phase strains are zero.

Numerical checks on isolated, background-subtracted families are below. Observed values used only a seven-point quadratic smoothing for the half-height crossing; calculated values are direct from the final profile.

| Family (degrees) | Position obs/calc | Left/right HWHM obs | Left/right HWHM calc | FWHM obs/calc |
|---|---:|---:|---:|---:|
| low, 26.70 | 26.7029 / 26.6920 | 0.0717 / 0.0769 | 0.0615 / 0.0862 | 0.1486 / 0.1477 |
| middle, 43.19 | 43.1872 / 43.1981 | 0.0622 / 0.1335 | 0.0703 / 0.1227 | 0.1957 / 0.1930 |
| high, 90.43 | 90.4343 / 90.4343 | 0.0688 / 0.0733 | 0.0690 / 0.0703 | 0.1421 / 0.1392 |

## Balance and remaining uncertainty

On a 100 g modeled-crystalline basis, the phase amounts are 0.17091 mol BaWO4, 0.05756 mol WO3, 0.01699 mol Ba3W2O9, and 0.02600 mol BaCO3. They contain 0.24789 mol Ba and 0.26245 mol W, or Ba/W = 0.9445. Precursor masses were not supplied, so an input balance cannot be closed uniquely. If the feed was intended to be equimolar in Ba and W, the difference indicates either Ba-rich noncrystalline material or quantitative systematics; carbon/oxygen also cannot be closed because CO2 is evolved. Every retained crystalline formula is charge balanced.

The phase identities and the presence of the approximately 5 wt% carbonate phase are reliable. The listed e.s.d.s are counting-statistical values only. A 98.5% correlation between the dominant BaWO4 scale and roughness parameter, source-model choices, peak-broadening choice, and possible microabsorption make the true fraction uncertainty larger; a practical model uncertainty is of order 1–3 wt% rather than the formal approximately 0.1 wt%. No amorphous fraction can be obtained from this dataset without an internal standard.
