# Ab-PXRD-Solver targets

These 100 targets are native two-column `2theta,intensity` inputs for
Ab-PXRD-Solver, bound to dataset `pXRD-100`. `patterns/` contains the seeded
native noisy profile consumed during inference; `patterns-clean/` retains the
noise-free GSAS-II calculation for deterministic audit.

The released numerical contract is Cu Kalpha-average at 1.54184 Angstrom, an
inclusive 10--80 degree two-theta grid at 0.02 degree spacing (3,501 points),
GSAS profile overrides U=0.2, V=-0.2, W=2.0, X=0.5, Y=0.5, 20 micrometer
crystallite size, no background, Poisson noise at 5,000 maximum counts, and
Gaussian noise with relative sigma 0.001. Intensities are normalized to a
maximum of 100.

The paper documents background subtraction, smoothing, peak extraction, PXRD
similarity screening, and GSAS-II refinement, but not the numerical simulation
parameters: [Stage 1.1 and Stage 3 in the paper](https://arxiv.org/abs/2605.24594) and the
[released implementation](https://github.com/MaterSim/Ab-PXRD-Solver/tree/0d67964dfcbd2e2fa09e79bbbac2f5d020a121e9).
`parameters.json` separates paper statements from code-derived values and pins
all source/runtime hashes.

The benchmark supplies only the reduced formula and pXRD. Run each row of
`inputs.csv` independently with `--formula <formula> --infer-spg`; target space
groups are not embedded in filenames or supplied to the solver. The stock batch
CLI cannot attach a different formula override to each file, so the benchmark
Modal adapter performs one upstream invocation per case.
