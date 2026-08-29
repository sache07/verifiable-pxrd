# Evaluation

The primary benchmark outcome is exact structural recovery under
`verifiable_pxrd.matching`: `StructureMatcher` with `scale=False`, an
`ElementComparator`, no subsets, and symmetric matching. A submitted
`alternative-<n>.cif` counts exactly as a selected CIF.

The test-time Rwp verifier is implemented in `src/verifiable_pxrd/rwp_verifier.py`.
It uses only the observed pattern, wavelength, and candidate CIFs. The periodic
structure is frozen; every candidate receives the same bounded GSAS-II nuisance fit
for scale, four-term background, zero shift, and a restrained peak-width model.

```bash
uv run vpbench rwp-verifier score \
  --pattern pattern.csv \
  --wavelength 1.5406 \
  --candidate selected.cif \
  --candidate alternative-1.cif \
  --output rwp-selection
```

For a pool of normalized monkey bundles, use `rwp-verifier monkeys`; it writes a
blind Rwp ranking and a new `selected.cif` for every panel case. It deliberately
submits only the lowest-Rwp candidate; the full ranking remains in `report.json` and
`scores.csv`, so the baseline does not gain extra exact-match coverage by copying
arbitrary runners-up into alternative slots. See
`docs/REPRODUCE.md` for an example.

Rwp is diagnostic, not the exact-match success criterion; a low residual can still
belong to a wrong subcell, ordering, or coordinate realization.
