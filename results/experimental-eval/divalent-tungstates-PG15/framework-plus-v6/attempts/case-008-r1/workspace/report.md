# Powder-XRD phase analysis

The pattern is modeled with three crystalline phases. Weight fractions are normalized over those modeled crystalline phases; they do not quantify any amorphous material.

| Phase | Space group | Refined/source cell (Å, °; GSAS-II setting) | Weight fraction |
|---|---:|---|---:|
| MnWO4, wolframite | P 2/c | a=4.83159, b=5.75747, c=4.99678, β=91.2187 | 97.433 ± 0.071 wt% |
| WO3, monoclinic | P 21/c | a=7.29959, b=7.53626, c=10.52707, β=133.0980 | 1.660 ± 0.096 wt% |
| WO3, triclinic | P -1 | a=7.309, b=7.522, c=7.678, α=88.81, β=89.08, γ=89.07 | 0.907 ± 0.106 wt% |

The quoted uncertainties are formal 1σ values propagated from the GSAS-II scale covariance. The combined residual WO3 content is 2.567 ± 0.071 wt%. The two WO3 fractions are strongly anticorrelated (r = -0.761), so their individual uncertainty is materially larger than the formal values once phase/source-model uncertainty is included.

## Evidence and model selection

The MnO + WO3, 900 °C chemical context and the dominant peak positions identify wolframite MnWO4. A single-phase fit left coherent residual families and had Rwp about 7.42%. Monoclinic WO3 accounts for separated or partly separated families including its strong 022 and 220 reflections near 33.59° and 41.77° 2θ. Rechallenging the residual after the common profile was established added triclinic WO3 at about 0.9 wt% and lowered Rwp from 6.193% to 6.162% (Δχ² about 416); support occurs across distinct families, including split groups near 33.30–34.79° and 55.60–55.82°, rather than one isolated peak.

The exact MnWO4 database entry used as the starting framework (COD 1520200) was measured at 2.4 GPa. FeWO4-type analogues were also screened, but the exact-chemistry wolframite model fit best. Its cell, all independent coordinates, and one tied isotropic displacement parameter were refined; the resulting ambient-pattern cell and geometry pass the contact/occupancy screen.

For monoclinic WO3, the best X-ray intensity fingerprint was the room-temperature 1960 record COD 1528915. Its two-decimal oxygen coordinates create unphysical 1.58 Å O···O contacts. A later neutron model (COD 2311041) is geometrically sound but gives a slightly poorer fit when used wholesale (Rwp 6.16064%). The submitted physical model therefore retains the X-ray-sensitive W sublattice from COD 1528915 and uses the neutron-derived O sublattice from COD 2311041; this removes the short contacts and gives Rwp 6.15943%. The monoclinic cell was refined, but its atoms were fixed. The triclinic model is COD 2106293; because its weak scale could not support stable angle/cell refinement, its source cell and atoms were retained.

MnO, Mn2O3, Mn3O4, Mn3WO6, and additional WO3 polymorphs were challenged under the same profile. They either collapsed to zero or below about 0.13 wt%, failed to improve coherent unique families, or worsened them, and were excluded.

## Refinement quality and limitations

The independently regenerated atomic profile gives Rwp = 6.15942%, Rp = 4.32691%, Rexp = 2.75333%, GOF = 2.23708, and χ² = 41377.56 for 8301 points and 33 varied parameters. The accepted baseline uses the stated Cu Kα doublet, one specimen shift (-571.36 µm), a smooth 8-coefficient background, positive common U/W/X peak-width terms, fixed SH/L=0.03, and a weak MnWO4 [001] March-Dollase term (0.97974). Surface roughness was required, but its two coefficients were nearly collinear, so B was fixed at 0.14 and A at the established 0.06974 value; polarization was held at 0.50. Save/reopen atomic replay reproduces all three CIFs and fractions exactly and reports no profile-validity flags. All exported structures pass the broad occupancy, density, and short-contact screen.

The remaining residual is systematic around several intense low- and middle-angle MnWO4 peaks (weighted RMS is about 2.6–4.4σ over 15–35°), whereas most high-angle bins are near 1–1.4σ. Releasing SH/L, phase size, isotropic/axial strain, or extra texture axes did not give a replay-stable physical improvement. Instrument X and phase size are confounded, so crystallite size cannot be determined reliably. The [001] texture axis is only marginally preferred over [110].

Most importantly, the powder data do not reliably determine atomic coordinates for either 1–2 wt% WO3 phase, and the monoclinic/triclinic fraction split is source-model dependent. The phase identities and combined WO3 abundance are better supported than either minor-phase atomic structure or its individual fraction. The elevated GOF and structured strong-peak residual should therefore be retained as model inadequacy rather than hidden with unsupported nuisance terms.
