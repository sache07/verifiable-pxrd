# PXRD phase analysis

## Submitted crystalline model

Weight fractions are normalized over the five modeled crystalline phases.

| Phase | Space group | Weight fraction | Refined cell (Å, °) |
|---|---:|---:|---|
| stolzite (scheelite-type) (PbWO4) | I 41/a | 67.81% | a=5.46588, b=5.46588, c=12.06149; alpha=90.000, beta=90.000, gamma=90.000 |
| triclinic tungsten(VI) oxide (WO3) | P -1 | 10.62% | a=7.30403, b=7.54668, c=7.70227; alpha=90.079, beta=90.405, gamma=90.009 |
| massicot (PbO) | P b c m | 14.06% | a=5.89888, b=5.49125, c=4.76264; alpha=90.000, beta=90.000, gamma=90.000 |
| litharge (PbO) | P 4/n m m | 5.24% | a=3.97904, b=3.97904, c=5.03495; alpha=90.000, beta=90.000, gamma=90.000 |
| minium (red lead) (Pb3O4) | P 42/m b c | 2.27% | a=8.76097, b=8.76097, c=6.58310; alpha=90.000, beta=90.000, gamma=90.000 |

## Evidence

The PbO + WO3 precursor chemistry and 500 °C treatment first suggest PbWO4. The dominant 27.70, 29.91, 33.05, 45.02, 47.28, 51.48, 55.54 and 56.81° families are indexed by tetragonal stolzite. The 23.36/23.88/24.65° cluster and related split families require WO3. Broad families near 29.34, 30.61, 38.11, 49.52, 53.38, 60.55 and 63.28° require orthorhombic massicot; the narrower 32.10, 35.99, 45.92 and 48.84° features retain tetragonal litharge. Weak coherent groups near 26.8, 31, 34.4° and at higher angle support trace Pb3O4.

All submitted structures use full-occupancy COD coordinates (IDs 9009811, 2106293, 2310433, 9012700 and 1537983); the litharge coordinates were origin-transformed into GSAS-II's standard P4/nmm setting to preserve PbO stoichiometry. Atomic coordinates and displacement factors were held at their reference values while cells were refined. Raspite PbWO4 and epsilon-WO3 collapsed to zero scale. A room-temperature monoclinic WO3 record is nearly degenerate (Rwp 14.034% versus the submitted triclinic model), so the WO3 symmetry assignment is not definitive.

## Refinement and uncertainty

The replayed full-range fit gives Rwp=14.024%, Rp=9.360%, Rexp=3.502% and GOF=4.013. The baseline uses one zero correction, refined polarization, nonnegative W/X profile terms with U=V=0, fixed reported Kalpha2/Kalpha1=0.5, a smooth 10-term background, no roughness/texture, and one isotropic massicot domain-size term. SH/L, texture, strain, anisotropic size, and unsupported phase size terms were pruned.

The formal covariance errors in result.json are much smaller than the systematic uncertainty because the measurement supplied no pointwise uncertainties. Most importantly, massicot is nanocrystalline and its integrated intensity is correlated with background and domain size: the corrected common-profile/no-size model gives about 70.7% PbWO4 and 9.8% massicot, whereas the submitted physically broadened model gives 67.8% and 14.1%. Thus those two absolute fractions cannot be determined reliably from this pattern alone; the submitted values are the best-fit broadened-model values, not high-accuracy composition measurements. WO3 is moderately robust near 10–12%; litharge and Pb3O4 are tentative trace/minor quantities because of overlap.

The exact replayed project is `final.gpx`; its exported structures and calculated profile are the submitted CIFs and `fit.csv`.
