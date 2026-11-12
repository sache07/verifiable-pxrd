# PXRD phase analysis

## Result

The submitted model contains five crystalline components. Weight fractions are normalized to the modeled crystalline material; no amorphous fraction can be obtained from these data without an internal standard.

| Phase | Space group | Refined cell (Å, °) | Weight fraction | Formal GSAS-II esd | CIF | Confidence |
|---|---|---|---:|---:|---|---|
| Scheelite PbWO4 | I 41/a | a = 5.465908, c = 12.057690 | 58.504 wt% | 0.125 wt% | [PbWO4_scheelite.cif](phases/PbWO4_scheelite.cif) | High |
| Monoclinic WO3 | P 21/c | a = 7.690633, b = 7.535630, c = 10.521110, beta = 136.1902 | 17.730 wt% | 0.127 wt% | [WO3_monoclinic.cif](phases/WO3_monoclinic.cif) | High |
| Red lead Pb3O4 | P 42/m b c | a = 8.800589, c = 6.560801 | 17.027 wt% | 0.112 wt% | [Pb3O4_red_lead.cif](phases/Pb3O4_red_lead.cif) | High |
| Massicot PbO | P b c m | a = 5.877408, b = 5.490191, c = 4.749568 | 4.163 wt% | 0.073 wt% | [PbO_massicot.cif](phases/PbO_massicot.cif) | Moderate |
| Triclinic WO3 | P -1 | a = 7.295728, b = 7.525551, c = 7.699616; alpha = 88.4986, beta = 91.5692, gamma = 90.6903 | 2.576 wt% | 0.121 wt% | [WO3_triclinic.cif](phases/WO3_triclinic.cif) | Tentative |

The combined WO3 fraction is 20.306 wt%. The formal esds above describe the covariance model only and are smaller than the credible systematic uncertainty. Reasonable absolute systematic uncertainties are roughly 1 wt% for each major fraction and 0.8 wt% for massicot. The monoclinic/triclinic WO3 split is less reliable than their sum: the triclinic component overlaps the monoclinic pattern strongly and may partly represent WO3 structural or microstructural heterogeneity. Its exact 2.576 wt% fraction should therefore not be interpreted to 0.121 wt% precision.

The full-range fit has Rwp = 3.0263%, Rp = 2.3292%, Rexp = 2.4853%, and goodness of fit = 1.2209 (8301 points, 44 refined variables). The final saved replay converged with maximum shift/esd = 0.034 and no frozen variables.

## Evidence and model selection

The metadata identify a 500 °C product made from WO3 and Pb3O4, measured in reflection geometry with a PIXcel1D-Medipix3 detector and Cu K-alpha radiation. The refinement used the stated K-alpha1/K-alpha2 wavelengths and 0.5 intensity ratio. Because no calibrated instrumental profile or pointwise uncertainties were supplied, the positive-count Poisson weighting and refined profile are effective models; this limits the absolute precision of both cells and fractions.

The principal phase is identified by the scheelite PbWO4 families at approximately 27.81, 30.02, 33.16, 45.13, 47.37, 51.59, 55.63, and 72.36°. Monoclinic WO3 accounts for the 23.53/24.00/24.83° triplet and families near 33.66, 34.61, and 42.29°. Pb3O4 accounts for lines near 26.80, 31.2, 32.5, 50.4, 52.5, and 58.5°. Coherent residuals at about 29.54, 30.8, 33.0, 38.2, 45.6, and 49.7° required orthorhombic massicot PbO; adding it at the inventory-recovery stage lowered Rwp from about 4.57% to 3.74% and gave a highly significant scale.

The retained source structures are COD 9009811 (synthetic scheelite PbWO4), 2311041 (Loopstra monoclinic WO3), 9012124 (293 K Pb3O4), 2310433 (average massicot PbO), and 2106293 (triclinic WO3). Under the same restrained nuisance model, monoclinic PbWO4 was decisively poor, and alternative WO3 replacements were worse than the Loopstra monoclinic record. A large-cell modulated massicot source gave Rwp about 3.90% versus about 3.15% for the average structure at that comparison stage and was rejected. The weak triclinic WO3 component survived scale-only and refined-cell replays: refining its cell lowered Rwp from about 3.110% for the four-phase model to about 3.033%, produced a moderate monoclinic/triclinic scale correlation of -0.65, and did not bind a parameter. Adding size or strain to it inflated its fraction and correlations and was rejected.

The final nuisance/profile model uses a smooth 12-term Chebyshev background over 90.19°, nonnegative common U/W/X = 51.01/7.08/4.11, and V/Y/Z = 0. Only specimen displacement was refined as an angular correction (shift = -873.5 micrometres for a 240 mm Bragg-Brentano radius); zero and transparency were fixed. This relatively large effective shift is stable but, without a calibrant, is another source of systematic cell uncertainty. Polarization was fixed at 1.0 after challenge; surface roughness was rejected as singular and nearly 100% correlated. SH/L = 0.002 was fixed because repeated asymmetry was not supported.

Size broadening was preferred to strain for PbWO4 and Pb3O4. The final coherent-size terms are approximately 60.7/57.1 nm for PbWO4 with a [001] uniaxial axis, 27.7/38.9 nm for Pb3O4 with a [110] axis, and 53.9 nm isotropic for massicot. Anisotropic strain trials became bound or singular. A replay-stable [111] March-Dollase term was retained for massicot (MD = 0.722); axial massicot texture challenges did not reproduce its improvement. Texture for the other phases and extra massicot anisotropy were pruned.

Atomic coordinates and occupancies were retained from the literature records; phase scales and cells were refined. Thus the CIFs are refined-cell structural models, not independent atomic-coordinate determinations from this powder pattern.

## Numerical peak-shape audit

The table records observed/calculated position, FWHM, and left/right half-width in degrees for low-, middle-, and high-angle reflections. “Other” is the estimated contribution from other modeled phases at the calculated apex, and SNR is calculated phase height divided by counting sigma. The observed phase profile is estimated as the isolated calculated phase profile plus the total residual; it is most trustworthy where Other is small.

| Phase; region (hkl) | Position O/C | FWHM O/C | Left/right O | Left/right C | Other | SNR |
|---|---:|---:|---:|---:|---:|---:|
| PbWO4 low (1 1 2) | 27.813/27.812 | 0.225/0.224 | 0.110/0.115 | 0.108/0.115 | 0.7% | 105.2 |
| PbWO4 middle (0 2 4) | 45.130/45.129 | 0.287/0.282 | 0.128/0.159 | 0.124/0.158 | 6.8% | 51.9 |
| PbWO4 high (4 2 4) | 86.011/86.022 | 0.482/0.477 | 0.150/0.332 | 0.170/0.307 | 10.9% | 20.5 |
| Monoclinic WO3 low (2 0 -2) | 23.536/23.532 | 0.128/0.124 | 0.058/0.070 | 0.053/0.071 | 12.5% | 39.1 |
| Monoclinic WO3 middle (2 2 -4) | 42.289/42.292 | 0.160/0.145 | 0.041/0.119 | 0.042/0.104 | 14.4% | 7.0 |
| Monoclinic WO3 high (6 1 -9) | 87.685/87.690 | 0.129/0.217 | 0.082/0.047 | 0.100/0.117 | 33.3% | 4.7 |
| Pb3O4 low (2 1 1) | 26.802/26.812 | 0.274/0.301 | 0.126/0.148 | 0.150/0.151 | 9.7% | 26.4 |
| Pb3O4 middle (3 3 2) | 52.527/52.531 | 0.385/0.377 | 0.204/0.181 | 0.178/0.200 | 10.5% | 13.3 |
| Pb3O4 high (6 1 1) | 66.486/66.456 | 0.511/0.463 | 0.258/0.253 | 0.211/0.252 | 16.0% | 7.9 |
| Massicot low (1 1 1) | 29.544/29.536 | 0.253/0.252 | 0.131/0.123 | 0.122/0.131 | 17.5% | 20.9 |
| Massicot middle (3 1 1) | 53.697/53.610 | 0.289/0.335 | 0.211/0.078 | 0.142/0.193 | 36.6% | 6.1 |
| Massicot high (3 1 3) | 79.926/80.082 | 0.101/0.461 | 0.051/0.050 | 0.181/0.280 | 50.4% | 2.7 |
| Triclinic WO3 low (2 2 0) | 34.674/34.813 | 0.090/0.155 | 0.056/0.034 | 0.098/0.057 | 68.6% | 2.0 |
| Triclinic WO3 middle (0 4 0) | 48.896/48.743 | 0.097/0.214 | 0.008/0.089 | 0.065/0.150 | 85.6% | 1.4 |
| Triclinic WO3 high (1 6 0) | 77.614/77.644 | 0.100/0.458 | 0.059/0.041 | 0.181/0.277 | 81.7% | 0.9 |

The first four phases have usable low- and middle-angle width evidence, and PbWO4 remains well constrained at high angle. The high-angle monoclinic WO3 and massicot widths are overlap-limited. No isolated middle/high-angle triclinic WO3 line exists at this abundance, so its line widths and exact phase fraction cannot be determined reliably even though its multi-line scale/cell refinement is significant. This is the main structural ambiguity in the submitted model.

## Chemistry, inventory recovery, and remaining uncertainty

All retained formulas are charge balanced: Pb(II)WO4 with W(VI), W(VI)O3, mixed-valence Pb3O4, and Pb(II)O. For one gram of modeled crystalline material, the phase inventory contains 0.002217 mol Pb and 0.002162 mol W, giving Pb/W = 1.026. This near-1:1 elemental balance is consistent with the principal reaction

`Pb3O4 + 3 WO3 -> 3 PbWO4 + 1/2 O2`,

with unreacted WO3/Pb3O4 and partial Pb3O4 conversion to PbO. Oxygen exchange with the firing atmosphere is therefore expected and does not create a charge imbalance.

Exact and analogue searches included PbWO4 polymorphs, Pb7W8O28.8, PbO polymorphs, PbO2, WO2, W18O49, and triclinic/orthorhombic/tetragonal/hexagonal WO3. Charge-balanced non-1:1 formulas Pb2WO5, Pb3WO6, PbW2O7, and Pb3W2O9 were also screened with `learned/stoichiometric_analogues.py`; no exact record produced a convincing physical fit.

On the final replay, Pb7W8O28.8, PbO2, WO2, tetragonal WO3, and hexagonal WO3 refined to zero; litharge was only 0.044(23) wt%. Orthorhombic WO3 and W18O49 each absorbed a similar sub-percent residual, 0.325(63) and 0.348(80) wt% respectively, with only small Rwp changes. Their signals are not unique, W18O49 is chemically disfavoured by the oxidizing Pb3O4/WO3 context, and neither has adequate isolated-peak evidence. They remain a watch-list indication of at most roughly 0.4 wt% unassigned crystalline material and were not included as determined phases.

The goodness of fit remains above the nominal counting expectation and small coherent residuals remain around several strong/overlapped lines. Given the absent calibrated profile and supplied uncertainties, the fit should not be used to claim sub-percent absolute fraction accuracy. The submitted model is the leanest replay-stable model that explains the phase-specific families without bound terms or a non-unique sixth phase.
