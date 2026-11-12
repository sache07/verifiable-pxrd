# b002 prospective transfer review

## Panel role

This transfer batch contributes two genuinely new cases. Together with the four
unresolved frozen b001 cases (c03--c06), they form the next six-case active
panel. The b001 cases remain in their original batch and are not duplicated or
regenerated here. b002 is frozen before any P0 or v6 solve is launched, and the
required comparison is three fresh rollouts of each frozen package on each new
case.

The new cases deliberately test two different transfer regimes:

| Case | Prospective role | Reference availability | Nominal truth by weight | Counts |
|---|---|---|---|---:|
| b002-c01 | Easier Mg partial-reaction control: complete inventory plus phase-specific profile allocation, without a hidden reference | Full | MgWO4 50.000%, MgO 7.405%, WO3 42.595% | 40,000 |
| b002-c02 | New Ba carbonate/off-stoichiometric four-phase mixture: source-quality rejection, analogue adaptation, weak-phase persistence and profile allocation | Full; ordered BaWO4 truth is naturally absent from the database | BaWO4 63.283%, Ba3W2O9 16.343%, BaCO3 7.482%, WO3 12.892% | 15,000 |

Both recipes have an exact divalent-cation:W balance of 1:1. The public sample
descriptions are WO3 + MgO heated at 700 C and WO3 + BaCO3 heated at 750 C.
Seeds and measurement-session identifiers were selected before solver work and
are fixed in the manifest.

## Source and analogue audit

The final registered pool is `pool-v2`, SHA-256
`7ba3ea6614c11580d2431c3f50737b88ca665ec660e104d77a97a07fae0be755`.
It contains published ordered COD records for monoclinic WO3 (2311041),
ambient-pressure wolframite MgWO4 (9013902), periclase MgO (9000499),
rhombohedral Ba3W2O9 (1533878), and 298 K witherite BaCO3 (9010928).
All registered models parse as ordered structures, have chemically appropriate
compositions, and pass generation-time physical/reference-mismatch checks.

The ordered BaWO4 source is an explicitly provenance-tracked analogue model.
It retains the fractional coordinates and I41/a symmetry of ordered SrWO4 COD
1546036, substitutes Sr by Ba, and uses the published BaWO4 lattice
a=5.614 A, c=12.719 A from COD 1527204. No coordinates were fitted. The model
has minimum separation 1.964 A, density 6.382 g cm-3, and passes the physical
screen. A framework-neighbour audit finds surviving tier-1 SrWO4 COD 1546036
with framework RMS 0.0000 and 6.49% cell mismatch. Thus the intended ordered
framework is recoverable by the package's generic analogue route.

The sole exact BaWO4 database record, COD 1527204, is retained in the solver's
normal database rather than suppressed, but is not used as truth because its
split/disordered 40-site model has a 1.1665 A minimum separation. This creates
a realistic source-rejection test without a case-specific database rule.

Withholding Ba3W2O9 COD 1533878 leaves no tier-1 or tier-2 framework survivor.
Its exact published reference therefore remains available: turning this case
into an ab-initio framework problem would not test the mechanisms under study.
A candidate CoWO4 record (COD 5910316) was also excluded during curation after
the registration parser reported occupancy 4 beyond tolerance; it was neither
repaired nor used to define a case.

## Prospective recovery checks

The final pre-freeze preview is `preview-v2`. Both cases are eligible for strict
known-structure recovery under the generation oracle:

| Case | Oracle Rwp | Maximum fraction error | Omission RMS in noise units, manifest order |
|---|---:|---:|---|
| b002-c01 | 1.5131% | 0.000690 | 14.379, 1.273, 11.559 |
| b002-c02 | 3.0085% | 0.001641 | 7.770, 2.167, 0.667, 1.530 |

Every intended phase therefore has positive omission evidence, including the
weak MgO and BaCO3 components. These checks establish quantitation and
detectability for the registered structures; they do not prove unique
structure identification or exhaust competing polymorphs.

An initial pre-freeze Mg preview used 65 wt% MgWO4, 5.18 wt% MgO and 15,000
counts. Its MgO omission RMS was only 0.303 noise units. Before freezing and
without observing any solver result, c01 was changed to the stated 50/7.405/
42.595 wt% recipe and 40,000 counts, preserving the preselected seed and
measurement session. This makes c01 the intended easier control rather than an
accidental near-invisible-minor-phase test. The Ba recipe was retained
unchanged after its first preview.

## Predeclared transfer questions

1. Does v6 preserve all phases more reliably than P0 on both a conventional
   full-reference Mg mixture and a new four-phase Ba mixture?
2. Does v6 reject the physically unsuitable exact BaWO4 record and construct
   or select an ordered scheelite analogue without case-specific knowledge?
3. Does the v6 inventory/source advantage survive while profile allocation is
   challenged by distinct phase widths, texture/strain, angular nuisance and
   weak residual phases?
4. Relative to P0, are any gains consistent over three fresh rollouts per case,
   rather than depending on a single favorable execution?

No answer to these questions was available when this review was written.
