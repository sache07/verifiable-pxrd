# Powder XRD phase analysis

The 900 °C MgO/WO3 product is modeled as three crystalline phases. Fractions are normalized over those phases only:

| Phase | Space group | Crystalline weight fraction |
|---|---:|---:|
| MgWO4 (wolframite) | P 2/c (No. 13) | 77.12(25)% |
| monoclinic WO3 | P 21/c (No. 14) | 14.75(10)% |
| MgO (periclase) | F m -3 m (No. 225) | 8.12(28)% |

## Evidence

MgWO4 accounts for the dominant wolframite families, including the strong reflections near 19.245°, 24.229° and 30.820° 2theta. Monoclinic WO3 is required by its coherent, characteristic 20-2/020/002 triplet at 23.450°, 23.926° and 24.688°. MgO is independently supported by the 200 line at 43.219° and the 220, 311 and higher-angle cubic family at 62.579°, 74.938° and above. These families persist after fitting a common background and profile; no coherent unmatched family remains for a fourth phase.

Starting structures were COD 9013902 (MgWO4), 2311041 (WO3) and 9000499 (MgO). Several WO3 records and polymorphs were compared under the same nuisance model. COD 2311041 gave the best physically coherent monoclinic model; a nominally better triclinic fit drove its angles toward the monoclinic metric and was rejected as over-flexible. A search for Mg2WO5 cross-chemistry prototypes returned only high-substitution-cost parents (for example Ba2ReO5, K2OsO5 and Sr2MnO5), and the residual has no supporting unique family, so none was added.

The final model uses one specimen-displacement correction (-594.59 micrometres), a smooth 10-term Chebyshev background, a nonnegative common profile, and neutral preferred orientation. Replay-stable uniaxial broadening was retained for MgWO4 along [001] and WO3 along [010]. Fresh, zero-cycle atomic replay of `final.gpx` over the full scan gives Rwp = 5.7197%, Rp = 4.0995%, Rexp = 2.8626% and goodness of fit = 2.0038. The replay background is positive throughout and raises no profile-review flags.

## Remaining uncertainty

The tabulated parentheses are covariance-only one-sigma estimates; scale/surface-roughness correlation and structural-model choice are larger systematic sources. The values are not absolute bulk fractions if amorphous material is present, and a trace phase without distinct peaks cannot be excluded.

MgWO4 independent coordinates and WO3 W coordinates were supported by staged refinements. WO3 oxygen coordinates could not be determined reliably at this abundance and overlap: unconstrained refinement produced unstable, chemically excessive shifts, so the physically screened parent oxygen geometry was retained. The instrumental U term, major-phase microstrain and crystallite size are also not uniquely separable; the reported CIFs and crystalline fractions are the supported outputs, while profile-derived microstructure values should not be interpreted quantitatively.
