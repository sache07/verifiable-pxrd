# PXRD phase analysis

## Result

The supported crystalline model contains two phases:

| Phase | Space group | Weight fraction* | Refined cell |
|---|---:|---:|---|
| WO3 | P -1 (No. 2) | 0.7061 (70.61 wt%) | a = 7.30560, b = 7.53518, c = 7.69095 Å; alpha = 89.7478, beta = 90.8093, gamma = 90.1752 degrees |
| CoWO4 | P 2/c (No. 13) | 0.2939 (29.39 wt%) | a = 4.66838, b = 5.68261, c = 4.94881 Å; beta = 90.0002 degrees |

*Fractions are normalized over these modeled crystalline phases. They do not measure amorphous material or absolute crystallinity. The covariance-only standard uncertainty is 0.13 wt% for each fraction, but it excludes structure choice, background, roughness, texture, and specimen-systematic errors. The spread across defensible profile/source trials suggests a more realistic uncertainty of roughly 2–3 wt% absolute.

The final fit has Rwp = 4.9335%, Rp = 3.8678%, Rexp = 3.2802%, and goodness of fit = 1.5067 (8301 points, 30 refined variables). Four full-range save/reopen replays gave Rwp = 4.93346–4.93356%; the final maximum shift/esd is 0.0248.

## Evidence and structural models

The precursor chemistry (CoO + WO3, heated to 900 °C) supports formation of CoWO4 with residual WO3. The observed WO3 triplet at approximately 23.16, 23.64, and 24.40 degrees 2theta, together with its middle- and high-angle families, fixes the majority phase. CoWO4 is supported independently by low-angle lines near 15.63 and 19.04 degrees and by coherent families near 30.69, 36.3–36.5, 52.11, 61.83, and 64.9–65.4 degrees. These families remain after the background and common profile are rebuilt.

For WO3, fully occupied COD 2106293 (the 1978 triclinic P -1 model) was selected. Monoclinic COD 1528915 and 2311041 alternatives were re-fitted under matched nuisance models; the best monoclinic trial was about 0.3 Rwp percentage point worse. Thus WO3 itself is secure, but the precise small triclinic distortion is less secure than the phase identity. Atomic coordinates were retained from the source while the cell was refined.

No exact CoWO4 entry was present in the filtered inventory, so stoichiometric analogues were searched. The fully occupied CoMoO4-II structure (COD 7205001, P 2/c, single-crystal data at 296 K) gives the expected wolframite-type octahedral framework. Isovalent Mo6+ was replaced by W6+ on the same occupied site before scale and cell refinement. FeWO4 (COD 1567215) and MnWO4 (COD 1520200) parents were tested under the same profile; both fitted substantially worse and drove less physical cells. The submitted CoWO4 coordinates therefore remain prototype-derived, which is the main structural-model limitation for that phase.

Both exported models pass a geometry screen without partial occupancy or split sites. WO3 has six W–O distances of 1.715–2.217 Å. CoWO4 has octahedral W–O = 1.774–2.153 Å and Co–O = 2.032–2.162 Å. No implausibly short contact was found.

## Refinement and profile adequacy

The Cu Kalpha1/Kalpha2 wavelengths and 0.5 intensity ratio from the metadata were used. Because pointwise uncertainties were not supplied, sigma = sqrt(max(counts, 1)) was used as a Poisson counting-statistics proxy. The fit covers the complete 9.9034–100.0949 degree range.

The accepted baseline uses a smooth 12-term Chebyshev-1 background, one specimen-displacement correction (-86.50 micrometres), nonnegative common W/X profile terms, and one surface-roughness B term. The calculated background is smooth and positive (463–2501 counts). U refined to zero and was fixed; V/Y/Z were neutral. A free asymmetry term collapsed to its lower bound, so SH/L was fixed at 0.002. A free polarization trial ran to an extreme bound and was rejected in favor of the specified doublet model with polarization fixed at 0.5. Roughness A was insignificant and 99.7% correlated with B, so A was pruned.

The common-profile FWHM rises smoothly from about 0.236 degree at 15.6 degrees to 0.244 degree at 65 degrees and 0.257 degree at 96 degrees. WO3 families require one isotropic microstrain term (4099 microstrain), giving representative widths of about 0.267 degree at 23 degrees, 0.348 degree at 65 degrees, and 0.455 degree at 96 degrees. This reproduces the distinct broader WO3 families while CoWO4 uses the common profile. Isotropic size trials hit neutral/bound values and were rejected; CoWO4 strain and phase-specific anisotropic strain were unsupported. A mild WO3 [101] March–Dollase correction (0.9654) was retained because several separated families improved together; alternate axes and all CoWO4 texture trials were unsupported. Position, width, and symmetry were checked on isolated low-, middle-, and high-angle families, and no repeating asymmetry remained.

## Watch list and remaining uncertainty

CoO, Co3O4, W18O49, WO2, and W3O8 were re-challenged after the final common profile was established. CoO and Co3O4 each returned about 0.30 wt% when fitted separately or together, and W18O49 returned about 0.40 wt%; WO2 and W3O8 were still smaller. These are not accepted detections: the scale gains are driven by isolated residual regions rather than coherent families. In particular, CoO worsens its strong 42.47 and 92.74 degree families, Co3O4 contradicts its 31.32 and 36.89 degree families, and the strongest W18O49 lines near 23.53 and 48.07 degrees worsen the residual. Their structures and fractions therefore cannot be determined reliably from this pattern and are left only as a trace-phase watch list.

The fit still contains modest peak-intensity residuals, especially in crowded WO3 regions. Consequently, the phase identities are strong, the normalized two-phase fractions are useful at the few-weight-percent level, but the exact WO3 symmetry distortion, prototype-derived CoWO4 coordinates, and sub-1 wt% impurities should not be over-interpreted.
