# Methods contracts

## Solve task

Each agent receives only a composition, wavelength, and `pattern.csv`. It writes
`selected.cif` and optionally a few `alternative-<n>.cif` files. Hidden references and
other attempts are outside its readable filesystem boundary.

## Exact recovery

An attempt succeeds when at least one declared CIF matches the reference with:

- `StructureMatcher(ltol=0.2, stol=0.3, angle_tol=5)`;
- `primitive_cell=True`;
- `scale=False`;
- `attempt_supercell=True`;
- `ElementComparator()`;
- `fit(reference, candidate, symmetric=True)`;
- subset matching disabled.

## Blind comparable-fit Rwp

The test-time Rwp comparator receives only the observed pattern, wavelength, and
submitted CIFs. It holds each periodic structure fixed and applies the same bounded
GSAS-II refinement of phase scale, four background coefficients, zero shift, and two
Gaussian peak-width terms. Starting widths are estimated from observed peaks, not read
from the hidden synthetic-generation recipe. With uniform weights it reports

`sqrt(sum((y_obs - y_calc)^2) / sum(y_obs^2)) * 100`.

This is a candidate-comparison baseline, not a structural-identity criterion.

## Resource contract

Primary Codex experiments used two logical CPUs, 5 GiB memory, no swap, at most 128
tasks, network disabled, and isolated writable workspaces. Condition files preserve the
model, reasoning effort, prompt, capability, environment, and time limit. Named result
bundles preserve any run-specific deviation from the canonical bounded condition.
