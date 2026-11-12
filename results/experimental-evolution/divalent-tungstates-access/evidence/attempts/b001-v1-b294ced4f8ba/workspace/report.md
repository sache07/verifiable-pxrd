# Powder XRD phase analysis

The modeled crystalline inventory is:

| Phase | Space group | Weight fraction* | Refined cell |
|---|---:|---:|---|
| MnWO4 (wolframite) | P 2/c (13) | 69.53 wt% | a = 4.80351, b = 5.71923, c = 4.98615 A; beta = 91.1264 deg |
| WO3 | P 21/c (14) | 15.00 wt% | a = 7.70491, b = 7.55201, c = 10.54155 A; beta = 136.0816 deg |
| Mn3WO6 | R -3 (148) | 15.47 wt% | a = 8.90628, c = 10.47626 A |

*Fractions are normalized over the three modeled crystalline phases. No external standard was supplied, so amorphous material and an absolute crystalline fraction cannot be quantified.

## Evidence

MnWO4 COD 1520200 accounts for the dominant wolframite family. All nine available same-formula WO3 structures were screened with common scale/background/cell settings; monoclinic COD 2311041 gave the best profile-screen result among the topology shortlist and remained a stable 15 wt% contribution.

The two-phase model left a coherent family near 20.3, 29.1, 32.3, 35.6, 46.2, 54.9-55.8 and 67.0 deg 2theta. A target-composition Mn3WO6 model made from the isovalent Mn3TeO6 structure (COD 2211528, Te6+ -> W6+, topology and multiplicities retained) reproduced that family. Under identical nuisance settings its addition lowered Rwp from 18.225% to 6.689%, with a positive scale and modest cell relaxation. Pa-3 and P21/c Mn3WO6 alternatives were also attempted: Pa-3 remained at 0.48 wt% and did not close the family, while the P21/c trial diverged and is therefore recorded as unknown rather than rejected. A P1 construction failed its prefit geometry screen because of a 0.68 A contact.

Final closure controls gave only 0.020 wt% for a trirutile Mn2WO6 analogue and 0.036 wt% for precursor Mn3O4; the latter worsened the fit on cell release. Both were removed. A second Mn2WO6 closure trial collapsed and then diverged, so it is marked unknown. Remaining prominent residual extrema occur as adjacent positive/negative lobes around modeled strong peaks rather than as a new coherent peak family.

The accepted refinement used phase scales and a 10-term Chebyshev background; symmetry-independent cells; limited MnWO4 and Mn3WO6 coordinates; isotropic size/strain with one supported MnWO4 [100] uniaxial strain term; one mild WO3 [010] March-Dollase term (0.978); and polarization 0.78895. A seeded surface-roughness test made its two parameters 100% correlated and was rejected. The exact saved project replays from atomic models on all 8301 points with no profile-review flags and gives Rwp = 3.604%, Rp = 2.825%, Rexp = 1.774%, GOF = 2.033 and chi-square = 34262.63.

All submitted CIFs pass a physical geometry screen. The shortest contacts are 1.812 A (MnWO4), 1.718 A (WO3) and 1.891 A (Mn3WO6); representative coordination ranges are Mn-O 2.089-2.198 A and W-O 1.812-2.170 A in MnWO4, W-O 1.718-2.163 A in WO3, and Mn-O 2.093-2.413 A / W-O 1.891-1.962 A in Mn3WO6.

## Remaining uncertainty

The R -3 Mn3WO6 phase assignment and its fraction are strongly supported by phase closure, but its structure is analogue-derived because no exact-formula reference was available. The oxygen coordinates, and likewise the detailed WO3 atomic coordinates in this overlapped 15 wt% phase, are not uniquely determined to single-crystal precision by this powder pattern. The CIFs are defensible refined models, not unique coordinate solutions.

Formal scale-only fraction uncertainties are about 0.03-0.04 wt percentage point, but they exclude structural and profile choices. Accepted physical nuisance variants changed the fractions by up to about 0.4 percentage point; a conservative interpretation is roughly +/-1-2 absolute wt percentage points. Trace crystalline phases below the closure-control level may remain undetectable.

Instrument zero and specimen displacement were highly correlated. The saved 0.42545 deg term should be read as an effective combined angular correction, not a calibrated instrumental zero; a one-term physical displacement reparameterization was less stable and fit worse. Shared instrument and phase broadening are also not uniquely separable, so crystallite-size/microstrain values should not be over-interpreted. These calibration ambiguities have a much smaller effect on the reported phase fractions than omission of the Mn3WO6 phase did.

The full falsifiable candidate history is in `candidate_ledger.csv`. Submitted artifacts are `final.gpx`, `fit.csv`, `result.json`, and one root-level CIF for each phase.
