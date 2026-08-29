# pXRD-100 selection protocol

## Fixed sources and eligibility

The primary population is the MP-20 data at CDVAE commit `f857f598d6f6cca5dc1ea0582d228f12dcc2c2ea`. Source
CSV hashes and row counts are locked in `SOURCE.lock.json`. A selectable MP-20 record
must have a numeric MP identifier, an ordered structure with 1--20 sites, energy
above hull at most 0.08 eV/atom, and formation energy below 2 eV/atom. Every selected
MP-20 structure is an exact member of the frozen **training split**.

Selection candidates must additionally be strict structure matches in Crystalyze's
released train split and deCIFer's public `train.h5`. They must also match the later
official DiffractGPT `train.parquet`, which is recorded as a released-split proxy
because the paper-era split is not public. Matcher tolerances are ltol 0.20, stol
0.30, angle tolerance 5 degrees, primitive-cell comparison, scaling enabled, and no
supercell search. Formulas in `pXRD-ood` are excluded.

Selection is deterministic under seed `20260720` and never uses the output of
Crystalyze, PXRDGen, deCIFer, diffractGPT, DARA, or AGAPI-XRD.

## Representative panel (30)

The target distribution is a formula-deduplicated, eligibility-filtered view of all
MP-20 splits. One lowest-energy candidate per reduced formula is available from the
training split. Formulas reserved for the polymorph panel are removed. A greedy
moment-matching selection followed by deterministic swaps minimizes disagreement in:

- crystal system;
- source-CIF site bins 1--4, 5--8, 9--12, 13--16, and 17--20;
- element-count and energy-above-hull bins;
- volume-per-atom and density quartiles; and
- incidence of the 20 most frequent elements.

This is a capped natural-distribution estimate: a prolific formula contributes only
one population unit and cannot dominate the panel.

## Challenge panel (30)

Thirty cases are selected from unused MP-20 training formulas, six from the top
decile of each predeclared score:

- `rare_symmetry`: inverse space-group frequency plus a crystal-system rarity prior;
- `site_chemical_complexity`: site count, element count, and independent-site ratio;
- `peak_congestion`: peak overlap, normalized intensity entropy, and peak count; and
- `scattering_ambiguity`: light/heavy-element contrast and nearby atomic numbers;
- `large_primitive_cell`: source-CIF site count, with primitive cells restricted to
  17--20 sites and deterministic preference for chemistry and independent-site count.

Across all five axes, space-group reuse is capped at four, anonymous-formula reuse at
two, and reduced formulas are unique.

Diffraction-based selection descriptors use ideal Cu K-alpha-1 patterns from 5 to 90
degrees two-theta, sampled every 0.05 degree with 0.12-degree Gaussian sigma.

## Polymorph panel (40)

Twenty reduced formulas contribute exactly two structures. A source family must have
at least three training records and at least three StructureMatcher-distinct clusters;
the selected pair must also be distinct. TiO2 is mandatory. Pair difficulty is based
on cosine similarity of the fixed ideal pXRD profiles, with quotas of 5 easy, 10
medium, and 5 hard pairs. The manifest records partner IDs, similarity, maximum
profile difference, and source cluster count.

## Audit and evaluation rules

`uv run python pxrd-bench/generation/build_pxrd_100.py audit --corpus-root
pxrd-bench/pXRD-100` works offline and checks all CIF hashes,
ordered structures, panel/axis quotas, site limits, unique paths and IDs, formula
deduplication, polymorph pairing, and structural non-equivalence.

`uv run --with h5py==3.16.0 python pxrd-bench/generation/build_pxrd_100.py audit
--corpus-root pxrd-bench/pXRD-100 --deep-exposure` additionally re-hashes the 11 GB
exposure index and deCIFer
`train.h5`, resolves every recorded training row, and repeats all 400 strict
cross-framework structure comparisons.

The CIFs and selection metadata are ground truth. Evaluated methods receive only the
simulated pXRD and the composition contract declared for each benchmark condition.
Exact training-exposure evidence is recorded per case and is an eligibility rule for
this revision, not a scoring outcome.
