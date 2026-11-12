# PXRD phase analysis

## Result

The pattern is best represented by six crystalline phases. Fractions are normalized only over those modeled crystalline phases; they do **not** measure amorphous material or any unmodeled phase.

| Phase | Space group | wt% | Estimated model uncertainty (percentage points) | Assessment |
|---|---:|---:|---:|---|
| PbWO4 (scheelite) | I 41/a | 61.84 | ±2.5 | identified |
| WO3 (monoclinic) | P 21/c | 9.94 | ±0.6 | identified; equivalent nonstandard monoclinic cell setting |
| PbO (orthorhombic) | P b c m | 7.05 | ±0.8 | identified |
| PbO (tetragonal/litharge) | P 4/n m m | 5.20 | ±3.5 | identified; fraction cannot be constrained tightly because width models are unstable |
| Pb3O4 (minium) | P 42/m b c | 1.50 | ±0.5 | weak but supported minor phase |
| Pb2WO5 (C2/m prototype) | C 2/m | 14.48 | ±2.0 | provisional prototype; oxygen coordinates and site ordering not independently determined |

The uncertainties in the table are conservative model-spread estimates. The much smaller covariance-only standard uncertainties are retained in `result.json`, but they omit phase-choice, background, overlap, and profile-model uncertainty.

## Evidence

The PbWO4 scheelite model (COD 9009811) accounts for the dominant reflection families and outperformed COD 1527935 (Rwp 12.117%); raspite did not give a physical competitive fit. Monoclinic WO3 COD 2311041 was preferred over COD 1528915 after the corrected common profile was rebuilt (Rwp 10.988% versus 11.079%). Both orthorhombic and tetragonal PbO have coherent families not represented by the other polymorph.

Pb3O4 is weak but retained: omitting it raises Rwp to 11.127%, and its partly independent families near 26.72°, 50.20°, and 66.23° improve locally. Tetragonal PbO is decisive: omitting it raises Rwp to 13.100%, and 20 of 23 tested families improve when it is restored. COD 9012700 was transformed exactly from P4/nmm origin choice 1 to GSAS-II origin choice 2 so that both Pb and O have the correct multiplicity of two. An isotropic tetragonal-PbO strain term lowered Rwp but drifted from about 15,000 to 15,700 ppm on repeated save–reopen cycles and inflated its fraction from 5.2% toward 9%; its size trial collapsed at the 0.01 µm bound and inflated the fraction further. Both were rejected. All final phase-size and phase-strain terms are therefore neutral. March-Dollase texture trials stayed close to random (ratios 0.992–1.020) and were pruned.

No exact Pb2WO5 database entry was found. A required stoichiometric-analogue search selected monoclinic MoPb2O5 (COD 7220560), followed by the valence-compatible Mo6+→W6+ substitution. This C2/m prototype explains the otherwise coherent families near 25.92°, 29.27°, 31.06°, 43.40°, and higher angles and has physical occupancies and geometry. The assignment remains **provisional**: powder data do not independently determine its oxygen coordinates or cation ordering. Its fraction is therefore less secure. Pb2WO5 size gave no useful improvement; isotropic strain changed Rwp only from 10.988% to 10.981% and shifted the fraction from 14.48% to 14.90%, while anisotropic variants were not replay-stable. These terms were rejected.

## Refinement and fit quality

The final full-range GSAS-II replay used the supplied Cu Kα1/Kα2 wavelengths and 0.5 ratio, a smooth positive 10-coefficient Chebyshev-1 background, nonnegative W/X peak width, refined SH/L asymmetry, fixed polarization 0.5, and one Bragg-Brentano specimen-displacement correction (-544.4 µm; zero fixed at 0). Surface-roughness B was refined; unused size, strain, roughness-A, texture, extinction, Babinet, and hkl-strain terms were neutralized. Isolated major families at low, middle, and high angle have calculated FWHM within roughly 0.02–0.03° of observation; the background remains positive (304–2188 counts).

Final statistics over 8270 points (10.0529–99.9075° 2θ) are Rwp = 10.988%, Rp = 7.131%, Rexp = 3.502%, and GOF = 3.145. Poisson counting weights were used because pointwise uncertainties were not supplied. GOF above unity indicates remaining counting/model systematics, so the reported model-spread uncertainties should be used rather than formal errors alone.

## Remaining uncertainty

The phase identities are well supported except for the prototype-level Pb2WO5 structural details and the weak Pb3O4 contribution. The stable neutral-profile tetragonal-PbO fraction is reported, but its drifting strain trial inflates it toward 9%; a bound-hitting size surrogate reaches 14% and is physically rejected. Its fraction therefore cannot be constrained more tightly than the stated ±3.5 percentage-point model estimate. WO3 is secure as monoclinic, but this powder pattern does not justify finer symmetry lowering. Without an internal standard, the six fractions cannot be converted into absolute sample fractions or an amorphous content.

`final.gpx`, all six CIFs, `fit.csv`, and `result.json` were exported from the same save–reopen–replayed project state.
