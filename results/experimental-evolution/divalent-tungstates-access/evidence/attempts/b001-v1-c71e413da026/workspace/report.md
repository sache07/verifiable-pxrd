# Powder XRD phase analysis

## Result

The crystalline sample is modeled by three phases. Fractions are normalized over these modeled crystalline phases; they do not quantify amorphous material.

| Phase | Refined cell | Weight fraction |
|---|---|---:|
| CaWO4 scheelite, I41/a | a = 5.23729, c = 11.33335 Å | 0.80736 (80.74 wt%) |
| WO3 monoclinic, P21/n | a = 7.31401, b = 7.55626, c = 7.69325 Å, beta = 91.0559° | 0.13860 (13.86 wt%) |
| CaCO3 calcite, R-3c | a = 4.98846, c = 17.04823 Å | 0.05404 (5.40 wt%) |

Formal scale-covariance standard uncertainties are approximately 0.21, 0.057, and 0.24 wt%, respectively. Model-choice and profile correlations make a practical uncertainty of roughly 0.5 wt% more realistic for the minor calcite fraction.

The read-only replay of `final.gpx`, with fresh reflections and no optimization, gives Rwp = 3.2002%, Rp = 2.4708%, Rexp = 3.1320%, and goodness-of-fit = 1.0218 for 8,301 points. The replay raised no negative-background, displacement-tensor, or peak-width flags. All three exported CIFs pass the occupancy/contact geometry screen.

## Evidence and phase closure

Scheelite CaWO4 explains the broad dominant families at approximately 18.27, 28.42, 31.22, 33.85, 46.88, 54.16, 57.65, and 59.32° 2theta. The sharp split family at 22.76, 23.18, 23.98, and 26.19°, together with peaks near 28.77 and 32.88–33.12°, requires monoclinic WO3. Among a symmetry-diverse WO3 shortlist, the transformed COD 2311041 model gave the best chemically acceptable common-setting fit. The slightly lower-metric triclinic decoy required a large source-to-fit shear toward monoclinic geometry and was rejected.

After those two phases, a coherent positive residual family remained near 29.09, 35.67, 39.17, 42.81, 47–48, 57.0, and 64.39°. Calcite accounts for this family and lowers Rwp from 3.4166% to about 3.2010% with a stable positive scale. Aragonite, vaterite, CaO, Ca3WO6, Ca4.26W10O30, and fergusonite additions all collapsed to zero scale. The final residual contains signed lobes around strong modeled peaks but no remaining multi-peak family that supports another crystalline phase.

The same-formula inventories were enumerated for CaWO4, WO3, and CaCO3. Imported candidates were compared from common projects; unsuccessful or unimported branches remain explicitly unknown rather than being called rejected. Full statuses and metrics are in `candidate_ledger.md`.

## Structural model and uncertainty

The CaWO4 parent is COD 7219229. The WO3 parent is COD 2311041, expressed by the topology-preserving basis change `a'=-(a+c), b'=b, c'=a` to the equivalent small-beta P21/n setting. Calcite is the 294 K COD 1547347 model normalized to isotropic Uiso before import, matching the reference-library convention.

Only bounded, symmetry-allowed coordinate adjustments were retained: the CaWO4 oxygen displacement was capped at 0.050 Å, the aggregate WO3 tungsten displacement at 0.040 Å, and the calcite oxygen displacement at 0.050 Å. WO3 oxygen-coordinate trials required implausible 0.11–0.80 Å shifts for small gains, so those coordinates cannot be determined reliably from this pattern and remain at the parent values. The calcite common Uiso also cannot be determined reliably; its refinement crossed the allowed bound, so 0.005 Å² was retained. Calcite isotropic size and strain are strongly correlated (about 96%); they are useful for profile reproduction but should not be interpreted separately.

Surface roughness, preferred orientation, and uniaxial strain were tested and rejected as unsupported or boundary/correlation-driven. Instrument zero and specimen displacement are intrinsically correlated here; zero was constrained at -0.25°, the edge of the documented laboratory range, while displacement and phase cells were refined. This calibration correlation is an additional systematic limitation on absolute lattice parameters, but not on the phase inventory.
