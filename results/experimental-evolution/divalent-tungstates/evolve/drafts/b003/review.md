# b003 prospective transfer review

## Panel role

This transfer batch contributes two new cases. Together with the four unresolved
frozen b001 cases (c03--c06), they form the next six-case active panel. The
b001 cases remain in their original batch and are not duplicated or regenerated.
The new batch is to be frozen before any P0 or incumbent solve is launched, and
its comparison will use three fresh rollouts of each condition on each new case.

| Case | Prospective role | Reference availability | Nominal truth by weight | Counts |
|---|---|---|---|---:|
| b003-c01 | Easier Ni source-quality/analogue control, isolated from specimen nuisance | Full library; the sole exact NiWO4 record is malformed, with tier-1 MgWO4 available | NiWO4 60.000%, NiO 9.747%, WO3 30.253% | 40,000 |
| b003-c02 | New off-stoichiometric intermediate and nominal-product-decoy test | Full; exact Cu3WO6 is tier 0 | Cu3WO6 35.255%, CuO 7.664%, WO3 57.082% | 40,000 |

Both recipes have an exact divalent-cation:W balance of 1:1. The public sample
descriptions are WO3 + NiO heated at 700 C and WO3 + CuO heated at 550 C. Seeds
and measurement-session identifiers were selected before solver work and are
fixed in the manifest. The Ni case controls angular offset and all specimen
effects, retaining ordinary registered-to-sample reference mismatch and counting
noise. The Cu case retains the ordinary nuisance realization.

## Scientific rationale

The Ni control is an easier variation of the unresolved hidden-wolframite cases.
It retains substantial, easily detectable residual NiO and WO3 and removes
profile-nuisance confounding. Its question is narrow: can a solver reject an
unusable exact-composition record, adapt a sound wolframite framework, and keep
the complete three-phase inventory? This provides a clean readout of whether the
incumbent's source/analogue procedure transfers beyond Mg, Mn, and Ba.

The Cu case introduces a challenge not represented in b001 or b002. The expected
1:1 target CuWO4 is a chemically convincing library decoy but is absent from the
truth. The pattern instead contains a published cubic Cu3WO6 intermediate,
residual tenorite, and compensating WO3. The mixture is constructed as 70 mass%
of the balanced Cu3WO6 + 2 WO3 module and 30 mass% of the balanced CuO + WO3
module. A successful solve must follow unassigned peaks to the exact
off-stoichiometric reference rather than force the nominal target, then retain
the weaker residual oxide.

## Source and analogue audit

The registered pool is `pool-v1`, SHA-256
`e16b43cc4c3d89e7fe0fdd5de78f0674de8e8928383cdf9e10313b702f16bb9a`.
It contains published ordered records for monoclinic WO3 (COD 2311041), rocksalt
NiO (1010093), cubic Pa-3 Cu3WO6 (1527404), and monoclinic tenorite CuO
(1011194), plus a provenance-tracked ordered NiWO4 analogue. All five registered
models parse as ordered structures, have 8--80 sites, densities of 6.53--7.95
g/cm3, minimum separations of 1.71--2.08 A, and no registration warnings.

The NiWO4 truth retains the fractional coordinates and P2/c symmetry of ambient
MgWO4 COD 9013902, substitutes Mg by Ni, and uses the published NiWO4 lattice
a=4.600 A, b=5.665 A, c=4.912 A, beta=90.5 degrees from COD 5910277. It has a
1.763 A minimum separation and 7.953 g/cm3 density. No coordinates were fitted.
The legacy exact NiWO4 file explicitly lists symmetry-equivalent atoms as
independent rows; direct parsing reports occupancies 2--3 and fails. It was not
repaired or used as truth. The framework-neighbour audit finds eight tier-1
survivors, led by MgWO4 COD 9013902 (Mg->Ni, framework RMS 0.0000, 2.09% cell
mismatch); FeWO4, ZnWO4, and MnWO4 are additional close tier-1 routes. Thus the
case requires reference adaptation but not ab initio structure solution.

Cu3WO6 COD 1527404 is an exact tier-0 Pa-3 survivor with framework RMS and cell
mismatch both zero. The exact reference remains available. The CuWO4 records in
the normal solver library are not removed; they are decoys to be accepted or
rejected by profile evidence rather than by a case-specific rule.

## Prospective recovery checks

The final pre-freeze preview is `preview-v2`. Both cases pass strict
known-structure recovery:

| Case | Oracle Rwp | Maximum fraction error | Omission RMS in noise units, manifest order |
|---|---:|---:|---|
| b003-c01 | 1.4362% | 0.000184 | 23.110, 4.297, 15.700 |
| b003-c02 | 2.3869% | 0.000600 | 7.289, 1.424, 14.955 |

The first Cu preview used 15,000 counts. Its Cu3WO6 omission signal was 3.652
noise units, but the 7.66 wt% CuO signal was only 0.639, which would duplicate
the near-invisible-minor bottleneck already present in b001-c04. Before freezing
and without observing any solver result, c02 was raised to 40,000 counts while
retaining its preselected recipe, seed, session, and all other settings. This
makes the intended new variable intermediate/decoy reasoning rather than another
weak-phase lottery. Recovery checks establish known-structure quantitation and
detectability; they do not prove unique identification or experimental phase
stability.

## Predeclared transfer questions

1. On clean c01, does the incumbent consistently reject the malformed exact
   NiWO4 source, adapt a physical tier-1 wolframite, and recover all three phases
   more reliably than P0?
2. On c02, does it search beyond nominal CuWO4, identify exact Cu3WO6 from
   residual evidence, and retain CuO without adding a false CuWO4 phase?
3. Are source/inventory gains reproduced across all three fresh rollouts and
   converted into profile agreement, rather than appearing only as plausible
   reports or one favorable execution?
4. Which mechanisms transfer prospectively and which unresolved b001 failures
   should remain the focus of the next package version?

No answer to these questions was available when this review was written.
