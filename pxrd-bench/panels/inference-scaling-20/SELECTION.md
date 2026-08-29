# Selection protocol

The candidate pool is the actual locked 100-case `pXRD-100` plus 100-case
`pXRD-ood` benchmark. A case is eligible only when the archived neutral raw-Codex
run has an externally evaluated attempt. The three infrastructure-blocked OOD
cases are therefore ineligible. Eligibility uses no outcome field.

The selected roster is formula-, CIF-hash-, source-material-, and generation-
parent-disjoint from the 50-case development-v2 training collection. A
deterministic mixed-integer selection under seed `20260817` uses only manifest
metadata.

Hard quotas preserve the main benchmark proportions exactly where divisible:

- 10 pXRD-100 and 10 OOD cases;
- 3 representative, 3 challenge, 4 polymorph, 2 substitution, 2 ordered-
  decoration, 3 Wyckoff-enumeration, and 3 crystal-search cases;
- three distinct challenge axes;
- two complete polymorph pairs: one medium and one hard family (the indivisible
  second pair is rounded toward harder cases);
- pXRD-100 site-bin counts 1, 2, 2, 2, 3 and OOD counts 2 in every bin;
- combined crystal-system counts 2 triclinic, 5 monoclinic, 3 orthorhombic,
  3 tetragonal, 3 trigonal, 2 hexagonal, and 2 cubic;
- no space group more than twice, and no OOD stream/site-bin cell more than once.

Secondary absolute-deviation terms match category-conditioned crystal systems
and site bins, total element count, and common-element incidence. A seeded SHA-
256 coefficient breaks ties. The order is category-interleaved and separates
polymorph partners. Raw outcomes are read only after `selection-freeze.json` is
written and hash-bound.
