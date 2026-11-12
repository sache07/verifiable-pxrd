# Powder XRD phase analysis

The crystalline pattern is modeled by two phases. Fractions are normalized only over the modeled crystalline material.

| Phase | Structural model | Weight fraction |
|---|---|---:|
| CoWO4 | wolframite, P 2/c | 0.29782 (29.78 wt%) |
| WO3 | triclinic, P -1 | 0.70218 (70.22 wt%) |

The full-grid Rietveld fit (9.9034–100.0949 degrees 2theta, 8301 points, Cu Kalpha1/Kalpha2) gives Rwp = 5.0686%, Rp = 3.8951%, chi-square = 19819.83, and goodness of fit = 1.5481. A fresh atomic forward replay of `final.gpx` reproduced Rwp = 5.0686% without using its stored calculated profile and raised no physical-profile review flags.

## Evidence and model choice

The CoWO4 model accounts for a coherent wolframite family, including the strong calculated groups at about 30.70–30.72, 36.34, 38.60, 41.34, 52.12, 53.98–54.04, and 61.86 degrees 2theta. It was initialized from the isostructural ZnWO4 wolframite reference COD 1520641 by chemically supported Zn-to-Co substitution, then its cell, Co/W coordinates, and bounded oxygen coordinates were refined. The final octahedra are physical: W–O = 1.881–2.105 A and Co–O = 1.992–2.153 A.

The remaining dominant families, especially the resolved 23.18/23.67/24.42-degree triplet and groups near 33.3–34.2, 47–50, and 54.8–56.1 degrees, are explained by triclinic WO3 (COD 2106293). This physical model fit better than the tested physical monoclinic alternative. A different fitted WO3 candidate was rejected because it produced a 1.57 A O–O contact. Both submitted CIFs pass the necessary contact/occupancy screen.

Co3O4 refined to zero scale. A CoO trial gave only 0.48 wt%, a scale of 2.9 standard uncertainties, and an absolute Rwp improvement of about 0.011 percentage point without broad unique-family support. CoO presence and fraction therefore cannot be determined reliably and it is not included as a resolved phase.

## Remaining uncertainty

The scale covariance gives a formal one-standard-uncertainty of 0.13 wt% for each reported fraction, but profile, preferred-orientation, absorption, and structural-model systematics make a realistic uncertainty closer to roughly 1–2 wt%. No amorphous fraction can be measured without an external standard.

The phase identities, cells, and heavy-atom frameworks are better constrained than the detailed oxygen geometry. The WO3 oxygen coordinates were retained from the reference because refining all 36 oxygen-coordinate parameters was underdetermined; only its W coordinates were refined. CoWO4 oxygen shifts were bounded to preserve sensible coordination. Isotropic displacement parameters were fixed at 0.003 A^2 after free refinement drove them negative, so ADPs are not determined by this data. The refined zero shift is 0.08376 degrees; instrumental/profile and microstructural parameters are boundary-limited nuisance terms and should not be interpreted as a calibrated line-profile measurement.
