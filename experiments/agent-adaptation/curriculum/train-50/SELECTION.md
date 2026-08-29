# Selection protocol

The target distribution is the union of the locked 100-case `pXRD-100` and
100-case `pXRD-ood` manifests. Candidates come from their formula-, structure-,
source-, and parent-disjoint development-v2 counterparts. All source and held-out
manifests are hash-bound in `SOURCE.lock.json`.

Selection is a deterministic mixed-integer optimization under seed `20260816`.
It uses only manifest metadata: benchmark category, challenge axis, polymorph
difficulty/family, OOD generation stream, primitive-site bin, crystal system,
space group, element count, and chemistry. No agent, model, solver, refinement,
Rwp, or benchmark outcome participates.

The hard quotas are:

- 25 pXRD-100-style and 25 OOD cases;
- 7 representative, 8 challenge, and 10 polymorph structures;
- 6 substitution, 6 ordered-decoration, 6 Wyckoff-enumeration, and 7
  crystal-search structures;
- both members of each selected polymorph family are retained as complete pairs:
  one easy, two medium, and two hard families;
- challenge-axis counts of 2 large-cell, 2 peak-congestion, 2 scattering-
  ambiguity, 1 rare-symmetry, and 1 site-chemical-complexity;
- exact OOD coverage of five cases in each primitive-site bin, with every stream
  represented one or two times in every bin;
- pXRD-100-style site-bin counts of 2, 4, 6, 5, and 8 from smallest to largest;
- combined crystal-system counts of 5 cubic, 4 hexagonal, 12 monoclinic,
  8 orthorhombic, 8 tetragonal, 6 triclinic, and 7 trigonal;
- no space group represented more than four times.

Secondary absolute-deviation terms match within-category crystal-system and site
distributions, total element-count distribution, and common-element incidence.
A SHA-256 seeded coefficient provides deterministic tie-breaking.

After selection was frozen, the fixed training order was constructed only from
the same pre-run metadata. Cumulative prefixes and the eight-case bootstrap are
balanced across category, source panel, primitive-site bin/count, crystal system,
and element count; later four-case waves are balanced where feasible. Polymorph
family members are separated. No agent outcome or refinement score informed the
ordering. See `ORDERING.md` for realized prefix statistics and the independent
post-freeze materials-science-agent audit.

Cases used in two earlier 22-case training collections are annotated but not
excluded and are not classified as previously unseen. None of the 50 overlaps a
held-out benchmark case by reduced formula, CIF hash, source material ID, or OOD
generation parent.
