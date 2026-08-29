# pXRD-100

This directory contains 100 single-phase Materials Project structures selected for a
powder-XRD-plus-composition benchmark: 30 representative cases, 30 challenge cases,
and 20 two-member polymorph families (40 CIFs). `manifest.json` is authoritative.

## Selection basis

- All 100 cases are exact members of the frozen MP-20 training split at CDVAE commit
  `f857f598d6f6cca5dc1ea0582d228f12dcc2c2ea`.
- Every case also has an audited strict structure match in the released Crystalyze
  training split, the public deCIFer `train.h5`, and DiffractGPT's later official
  released training split. The latter is explicitly a proxy for the unavailable
  paper-era DiffractGPT split.
- The six `large_primitive_cell` challenge cases have 17--20 primitive sites and are
  in the top decile of the eligible unused MP-20 formula population by site count.
- All selection used seed `20260720` and descriptors fixed before running any
  compared framework. CIF targets were not selected using model outcomes.
- Ideal selection profiles use Cu K-alpha-1, 5--90 degrees two-theta, a 0.05-degree
  grid, and 0.12-degree Gaussian sigma, matching the frozen benchmark conventions.

## Important applicability note

Crystalyze has a published 20-site model cap, while PXRDGen was trained on MP-20
primitive cells containing at most 20 sites. Every current case, including the six
large-cell challenges, lies within those respective applicability envelopes.

## Files

- `manifest.json`: complete structure, provenance, selection, exposure, and hash data.
- `manifest.csv`: compact human-readable case index.
- `selection-report.json`: panel diagnostics and exact quota checks.
- `SELECTION.md`: the selection protocol and benchmark applicability rules.
- `SOURCE.lock.json`: source commits, file hashes, API/database versions, and seed.
- `FRAMEWORKS.md`: the public fixedparams-v1 input contract.
- `representative/`, `challenge/`, `polymorph/`: the 100 ground-truth CIFs.
- `targets/fixedparams-v1/`: the 100 hash-bound diffraction inputs and complete
  simulation record used by this release.

The CIFs are ground truth and should remain hidden from evaluated methods. Benchmark
inputs should expose only the simulated pXRD pattern and reduced composition.
