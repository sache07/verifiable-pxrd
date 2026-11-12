# Powder XRD phase analysis

The fitted crystalline inventory is dominated by scheelite PbWO4, with unreacted WO3 and massicot PbO, a Pb2WO5 intermediate, a minor long-period PbO polymorph, and a tentative Pb2O3-like component. Fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Refined cell (A, deg) | wt.% | Assessment |
|---|---:|---|---:|---|
| PbWO4 (scheelite) | I 41/a | a = 5.46211, c = 12.05510 | 54.59 | Confident |
| WO3 (monoclinic) | P 21/n | a = 7.29922, b = 7.54196, c = 7.69271, beta = 90.4373 | 11.37 | Confident phase; local coordinates uncertain |
| PbO (massicot) | P b c m | a = 5.89619, b = 5.48704, c = 4.75713 | 11.01 | Confident |
| Pb2WO5 | C 2/m | a = 14.22481, b = 5.80616, c = 7.35430, beta = 113.8951 | 14.82 | Probable; analogue-derived structure |
| PbO long-period alpha model | P b m a | a = 5.63307, b = 44.89506, c = 5.03245 | 3.87 | Probable minor phase; overlap-sensitive |
| Pb2O3-like | P 21/c | a = 7.67138, b = 5.64642, c = 7.70841, beta = 113.9912 | 4.34 | Tentative; structure and fraction not reliable |

## Evidence and refinement

The model uses the reported Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio over the complete 10.009-99.994 deg scan. A smooth six-term Chebyshev background, one Bragg-Brentano specimen displacement (-486.2 micrometres), common nonnegative U/W/X peak profile, phase cells and scales were reconverged after every inventory change. The final saved/reopened replay converged with maximum shift/esd 0.218 and no frozen variables. Its fit statistics are Rwp = 10.525%, Rp = 7.840%, Rexp = 3.493%, and GOF = 3.013. A fresh atomic forward replay of `final.gpx` gives Rwp = 10.5253%, confirming that the result does not depend on cached calculated intensities.

PbWO4 accounts for the dominant peak families. Residual WO3 and massicot scales remain positive and stable across source/profile challenges. The Pb2WO5 model explains coherent families near 25.90, 26.76, 29.35, 30.62 and 31.05 deg that the precursor/product set misses. No exact Pb2WO5 entry was available, so COD 7220560 (MoPb2O5) was converted by isovalent Mo-to-W substitution; the final geometry passes the contact screen, with W-O distances of about 1.765-1.792 A. The long-period PbO record is favored over simple tetragonal litharge by several partly separated families and a stable positive scale. The Pb2O3-like model is supported mainly by the persistent 30.15/30.24 deg family and related weaker peaks.

Three modest March-Dollase terms were retained only after separate-axis tests and cumulative replay: WO3 [110] = 0.744, massicot [100] = 0.864 and Pb2WO5 [100] = 1.156. A Pb2O3 texture term was unstable and was removed. Polarization changed Rwp by only 0.002 percentage point; roughness parameters were essentially 100% correlated; SH/L was over 95% correlated with displacement and worsened replay. These terms were pruned. Isotropic and [001]/[100] PbWO4 strain trials either worsened the fit or collapsed to zero, so only its replay-stable size term was retained.

## Remaining uncertainty

The reported fractions are conditional Rietveld point estimates, not absolute sample mass fractions; no amorphous fraction is determined. Instrument broadening was not independently calibrated, and the common U/W/X solution lies at the broad end of the allowed physical envelope, so size and minor-phase abundance remain correlated.

The exact WO3 record has an anomalously short O-O contact (about 1.58 A). Physical alternate WO3 records fit worse when substituted, so the phase identity and approximate abundance are retained but its detailed atomic coordinates should not be interpreted. The Pb2O3-like component is less secure: its free cell differs by roughly 1-1.5% from the sole exact record, and that record contains implausibly short Pb-O/O-O contacts. Its 4.34 wt.% value is therefore model-dependent and neither its atomic structure nor fraction can be determined reliably from this pattern alone. The long-period PbO fraction is also sensitive to overlap with the other Pb-O phases. Bounded coordinate refinements were rejected because they hit limits or became highly correlated.

Alternative monoclinic PbWO4, Pb3O4, W2O7, Pb5WO8/Pb3WO6 analogues and a second scheelite record were challenged. They gave zero/unstable scales, failed physical screening, or improved the residual only by splitting existing peak shapes without unique diffraction families, and were not included.
