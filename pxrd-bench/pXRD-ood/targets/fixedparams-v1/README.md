# Fixed-parameter PXRD targets

`patterns-fixedparams/` contains the seeded noisy patterns for all 100 structures
in `pXRD-ood-v1` under one explicit, framework-independent measurement
condition. These files are separate from the released Ab-PXRD-Solver-style
`patterns/` and have not replaced inputs used by earlier inference runs.

The fixed condition uses monochromatic Cu Kalpha1 radiation at
1.5406 Angstrom. The inclusive two-theta grid spans
5--90 degrees with
0.01 degree sampling
(8,501 points).

GSAS-II is configured directly with U=2,
V=-2, W=5,
X=0, Y=0, polarization
0.7, SH/L=0.002, and zero shift.
Sample broadening is explicitly isotropic: crystallite size
1 micrometer, microstrain
1000, and Lorentzian fraction 1 for both. Preferred
orientation and sample displacement are disabled, and the calculated
background is asserted to be zero.

Each clean calculation is converted to a maximum of
5,000 counts, sampled with Poisson noise, augmented with
Gaussian noise of sigma 5 counts, and
normalized to a maximum of 100. Seeds are deterministic and recorded per case.

See `parameters-fixedparams.json`, `manifest-fixedparams.json`, and
`inputs-fixedparams.csv` for the complete reproducibility record.
