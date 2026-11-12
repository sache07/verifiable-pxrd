# Powder XRD phase analysis

## Result

The specimen is modeled as five crystalline phases. Weight fractions are normalized over those modeled crystalline phases only.

| Phase | Space group | Refined cell (Å, °) | Weight fraction |
|---|---:|---|---:|
| PbWO4, scheelite | I 41/a | a = 5.46548, c = 12.06222 | 59.15 wt% |
| WO3, monoclinic | P 21/c | a = 7.70250, b = 7.54661, c = 10.57287, β = 136.3101 | 9.99 wt% |
| Pb2WO5 | C 2/m | a = 14.23845, b = 5.80989, c = 7.35865, β = 113.9011 | 15.13 wt% |
| PbO, massicot | P b c m | a = 5.90969, b = 5.48830, c = 4.75448 | 8.93 wt% |
| PbO, litharge | P 4/n m m | a = 3.97753, c = 5.04353 | 6.81 wt% |

The full-grid GSAS-II fit uses all 8,282 observations from 10.0094–99.9944° 2θ. Its statistics are Rwp = 9.8899%, Rp = 6.7196%, Rexp = 3.5015%, and goodness of fit = 2.8279. Since pointwise uncertainties were not supplied, counting-statistics weights were used; the goodness of fit should therefore not be interpreted as an independently calibrated error model.

## Evidence and model choice

The dominant scheelite PbWO4 model accounts for the strong families near 27.69, 33.05, 45.02, 51.48, and 55.54° 2θ. Monoclinic WO3 accounts for the characteristic 23.38/23.86/24.64° region and its higher-angle families. A third coherent family, including reflections near 25.92, 29.3–31.1, and 43.4°, is indexed by C 2/m Pb2WO5. The remaining reproducible families require both orthorhombic massicot and tetragonal litharge PbO; both refine to stable positive scales and chemically normal cells. This inventory is also consistent with partial reaction of the stated PbO and WO3 precursors at 500 °C.

Exact-composition references were tested first. Scheelite was preferred to a raspite PbWO4 alternative whose scale collapsed and whose strong predicted lines were absent. Among close WO3 checkpoints, P 21/c gave the best physical same-composition model. No exact Pb2WO5 structure was present in the frozen reference index, so its model uses the published isostructural Pb2MoO5 topology (COD 7220560), with Mo(VI) replaced by W(VI), followed by bounded coordinate refinement. The resulting W–O geometry is physical. Independent parsing of all exported CIFs recovered their stated stoichiometries and space groups; their shortest contacts range from 1.712 Å for Pb2WO5 to 2.353 Å for litharge.

After the five-phase refinement, the remaining large difference features are chiefly derivative-shaped around intense, overlapping assigned reflections, especially the 27–31° region. They do not form a separate coherent reflection family, so phase/prototype searching was stopped. The calculated profile includes background and the supplied Cu Kα1/Kα2 doublet.

## Uncertainty

The fractions reported in `result.json` have small least-squares scale-factor standard uncertainties, but these do not include model choice, peak overlap, preferred orientation, microstructure, or background systematics. The Pb2WO5 topology and phase presence are supported by a broad reflection family, but its light-atom coordinates and its 15.13 wt% fraction are less secure because the starting structure is a Mo-to-W analogue. Its exact internal structure should therefore be treated as provisional.

The two PbO polymorphs are independently supported, but their individual 8.93 and 6.81 wt% values are more model-dependent than their combined 15.73 wt% abundance: litharge size/preferred-orientation and massicot strain terms reached imposed physical bounds. These boundary-limited terms, together with overlap among PbO, Pb2WO5, and WO3 peaks, mean that realistic uncertainties are larger than the formal values. No amorphous fraction or absolute crystalline content can be determined from this pattern without an internal standard; all submitted fractions are normalized only over the modeled crystalline material.

The submitted `final.gpx` is the stable, replay-consistent full-grid checkpoint. `fit.csv` and all five CIFs were exported from a reload of that exact project.
