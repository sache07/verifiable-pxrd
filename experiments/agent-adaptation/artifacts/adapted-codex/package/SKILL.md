---
name: pxrd-solve
description: Determine a crystal structure from a supplied single-phase powder-XRD problem and produce valid CIF candidates.
---

# pXRD submission contract

Only `selected.cif` and `alternative-<n>.cif` are graded. Keep a parseable
`selected.cif` current once a concrete model exists; it must be the best-supported model.

A candidate is an element-specific periodic realization with explicit cell scale,
coordinates, occupancies, and ordering. A prototype, indexed cell, unmaterialized site
permutation, or averaged/disordered site is a different candidate. If a few distinct
element-to-site orderings, supercells, or periodic models genuinely survive, write each as
a separate declared CIF instead of collapsing them into mixed occupancy or leaving them in
scripts. Alternatives provide coverage; they do not replace the primary.

Round-trip every declared CIF and confirm its intended reduced formula, occupancies, cell,
and coordinates.

`dicvol14-adapter` is a neutral interface to the installed DICVOL14 binary. Its `--help`
describes explicit peak-list, input-kind, crystal-system, bound, provenance, and timeout
options; it performs no peak picking or solution ranking.
