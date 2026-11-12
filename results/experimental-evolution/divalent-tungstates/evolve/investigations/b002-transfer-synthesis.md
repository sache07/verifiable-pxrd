# b002 prospective transfer synthesis

## Headline comparison

The frozen group `b002-transfer-p0-v6-r3` completed all 12 slots without
infrastructure recovery. All prospective scores, including the partial v6
submission and provisional P0 physical-review scores, remain in the means.

| Case | Condition | Scores | Mean (population SD) | 80+ | Physical pass | Full framework inventory |
|---|---|---|---:|---:|---:|---:|
| c01 Mg | P0 | 53.35, 28.32, 87.56 | 56.41 (24.28) | 1/3 | 3/3 | 3/3 |
| c01 Mg | v6 | 85.06, 11.60 partial, 83.79 | 60.15 (34.33) | 2/3 | 3/3 | 3/3 |
| c02 Ba | P0 | 87.34†, 49.64†, 46.54† | 61.17 (18.54) | 1/3 | 0/3 | 0/3 |
| c02 Ba | v6 | 84.30, 85.61, 84.29 | 84.73 (0.62) | 3/3 | 3/3 | 3/3 |

Across the six new-case rollouts, P0 averages 58.79 and v6 averages 72.44,
a +13.65-point transfer gain. v6 beats the same-case P0 mean on both cases,
has five 80+ scores versus two, and supplies physical frameworks 6/6 versus
3/6. This is positive transfer, but not a two-case strong pass: c01 remains a
high-variance execution problem and its v6 mean is below 80. c02 is a strong,
low-variance transfer success.

## Case-level sequence diagnosis

| Case | Noise-floor and observed gap | Successful sequence | Divergence from the oracle-informed route |
|---|---|---|---|
| c01 MgWO4/MgO/WO3 | Frozen floor Rwp 1.514%. P0 replay Rwp 2.470/7.284/1.646%; v6 1.662/unknown/1.686%. A schema-only researcher repair of the v6 partial exposes Rwp 2.392%, D 1.472 and score 54.74; it is diagnostic only and does not replace 11.60. | Both 80+ v6 runs retained exact physical sources and all phases, selected MgWO4 [010] texture, and combined a physical common profile with WO3 size/strain treatment. Their D values are 0.215/0.238 and fractions are within 1.3 points. P0 r3 independently reached D 0.182 with phase broadening and texture. | The generating profile has MgWO4 [010] texture, modest MgWO4 size/strain, weak MgO [111] texture/size, and WO3 size plus isotropic and [100]-axial strain. Failed v6 r2 stopped at a single 7960-ppm isotropic WO3 strain, rejected complementary size/anisotropy, and called a GOF 1.57/Rwp 2.39 model adequate. It then used `weight_fraction_normalized_crystalline` instead of required `weight_fraction`, so verified project replay was unavailable prospectively. P0 r1/r2 likewise retained complete chemistry but misallocated profile terms; r2 reached D 22.86. |
| c02 BaWO4/Ba3W2O9/BaCO3/WO3 | Frozen floor Rwp 3.011%. P0 replay Rwp 3.121/5.450/4.946%; v6 3.256/3.213/3.275%, with D 0.169/0.150/0.181. | Every v6 run rejected the split/disordered exact BaWO4 record, invoked an ordered scheelite analogue (BaMoO4, SrWO4 or EuWO4 parent), retained exact Ba3W2O9, used physical WO3/BaCO3 alternatives, and re-challenged all four phases after profile rebuilding. Fractions are all within 1 point and source/framework decisions survive three independent executions. Different supported size/strain allocations all replay near the floor. | P0 r1 reached near-floor profile D 0.079 but used a short-contact WO3 source, so the result is provisional and not full-framework correct. P0 r2 kept the disordered short-contact exact BaWO4 record; r3 omitted BaCO3 and used flagged WO3. The generating phase widths include BaWO4 size, Ba3W2O9 size plus mild axial strain, strong BaCO3 strain, and WO3 size plus mild strain/texture. v6 does not uniquely recover these nuisance values, but its physical source/inventory loop makes the profile and quantitation robust. |

## Mechanism conclusion and next package

The reusable v6 gain is confirmed prospectively: reject a bad record rather
than its chemistry, adapt an ordered framework analogue, retain a reversible
weak-phase watch list, and rebuild the profile after inventory/source changes.
The Ba case is a genuinely new chemistry/topology combination, so its 3/3
result is strong generalization evidence rather than memorization of b001.

The remaining common failure is not phase recognition alone. A solver can
declare a profile adequate without recording numerical family-wise width and
asymmetry evidence, allowing one large isotropic surrogate to replace
complementary size/strain/anisotropy. This matches the carried c03--c06
variance. The c01 submission also shows that qualitative “project/export
agreement” is insufficient: the solver validated its own nonstandard JSON
schema.

v7 should therefore replace, not append to, v6 prose. Preserve the concise
source/analogue/watch-list loop; add generic precursor-balance formulation of
missing stoichiometries for c05; require a written numerical low/mid/high-angle
peak-width/asymmetry audit before accepting profile adequacy; and require a
literal final schema check for numeric `weight_fraction`, unit sum, existing
CIFs, and project/export agreement. No new executable helper is justified
beyond the existing analogue search.
