# PXRD phase analysis

## Result

The crystalline pattern is best described by three phases. Fractions are normalized over these modeled crystalline phases only.

| Phase | Structure | Weight fraction |
|---|---|---:|
| WO3 | triclinic, P -1 (No. 2) | 73.25 wt% |
| Mn2O3 | bixbyite, I a -3 (No. 206) | 25.15 wt% |
| MnWO4 | wolframite, P 2/c (No. 13) | 1.60 wt% |

The final fit has Rwp = 6.490%, Rp = 4.707%, Rexp = 2.662%, and GOF = 2.440 over 8301 points. The refinement converged without dropped variables; the regenerated profile agrees exactly with the profile saved in `final.gpx`.

## Evidence

Audited atomistic Mn/W/O candidates were screened against the complete Cu K-alpha doublet pattern (9.903–100.095 degrees 2-theta), then compared with identical minimal nuisance models. The selected P -1 WO3 model reproduces the resolved low-symmetry peak splitting. After adding the trace MnWO4 phase and reconverging all nuisance terms, complete-model replacements gave Rwp = 6.621% for P21/c WO3, 13.162% for Pnma WO3, and 6.635% for Pbca Mn2O3, all worse than 6.490% for the selected model.

Mn2O3 is required by multiple bixbyite reflections: its matched leave-one-out fit rises to Rwp = 10.175%. MnWO4 has a positive, repeatable scale and improves distinct residuals around 18.8, 30.3, 30.8, and 53–54 degrees 2-theta. Removing MnWO4 after reoptimizing the remaining profile, roughness, scales, and background raises Rwp to 6.537%; removing only its strain broadening gives 6.528%. Mn3WO6 refined to a boundary/unstable scale and was rejected. CIF audits found no occupancy, duplicate-site, symmetry-expansion, or short-contact flags in any submitted structure.

Cells were refined for the two major phases. Atomic-coordinate trials were unstable or strongly correlated, so reference coordinates were retained. The trace MnWO4 cell could not be refined reproducibly and is therefore the audited reference cell. The final profile uses a 12-term Chebyshev background, a refined zero offset and global Gaussian width, simple surface roughness, WO3 size plus strain broadening, Mn2O3 size broadening, and MnWO4 strain broadening. Matched removal tests materially worsened the fit for every retained optional term. The angular branch check rejected specimen displacement and the joint zero/displacement model (99.94% correlation).

## Remaining uncertainty

The MnWO4 identification is supported, but its exact fraction cannot be determined reliably to the formal scale e.s.d. Its broadening is very large, and a broadening-free branch gave only about 0.25 wt% versus 1.60 wt% in the selected stable strain branch. Thus 1.60 wt% is the best-model estimate, but MnWO4 should be regarded as a trace component of roughly order 1 wt%, with about 1 wt% absolute systematic uncertainty. The major-phase fractions are more robust, but uncertainties of roughly 1–2 wt% are more realistic than their formal e.s.d.s.

No calibrated instrument profile or pointwise standard uncertainties were supplied, so refined size/strain terms are profile nuisance parameters and should not be interpreted as quantitative microstructure. The GOF above unity and correlated residuals indicate remaining model/systematic error. No coherent additional crystalline peak family passed the atomistic full-pattern tests, but an amorphous fraction cannot be assessed without an internal standard.
