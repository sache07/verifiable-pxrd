# Blind Rwp selection over eight adapted-codex Sol rollouts

This experiment asks whether a reference-blind, physics-based selector can realize the
candidate-set coverage gained from independent agent rollouts. It pools every declared
`selected.cif` and `alternative-<n>.cif` from eight GPT-5.6 Sol high
`adapted-codex` attempts on each case in the frozen `inference-scaling-20` development
panel, ranks the candidates by a common profile fit, and returns the minimum-Rwp
candidate.

## Headline result

The eight-rollout pool contained an exact structure for 18 of 20 cases. Minimum-Rwp
selection chose an exact structure in all 18 of those cases, converting the complete
oracle candidate-set gain into a reference-blind top-1 result on this panel.

| Quantity | Result |
| --- | ---: |
| Source attempts | 160 |
| Attempts producing at least one declared CIF | 157 |
| Declared candidate CIFs | 213 |
| Completed candidate fits | 213/213 |
| Oracle union across eight rollouts | 18/20 |
| Minimum-Rwp selected exact | **18/20** |
| Selection accuracy conditional on an exact candidate | **18/18** |
| Exact candidate within the first two Rwp ranks | 18/20 |

The two failures, `vh-006` (Ba3In2O6) and `vh-014` (Li3(AuO)4), contained no exact
candidate in any source rollout. They are therefore coverage failures rather than
selection errors.

## Selector protocol

The selector uses only the observed diffraction profile, wavelength, and submitted
candidate CIFs. The hidden reference structure, exact-match labels, and synthetic
profile-generation parameters are unavailable during ranking.

Every candidate is evaluated under `blind-comparable-gsas-rwp-v1`. Its lattice,
atomic coordinates, species, and occupancies remain fixed. GSAS-II fits the same small
set of nuisance/profile parameters for each candidate:

- phase scale;
- four Chebyshev background coefficients;
- zero shift bounded to +/-0.15 degrees;
- Gaussian Caglioti U and W, with V fixed at zero.

Starting peak widths are estimated from the observed profile. All other profile terms
use the same neutral fixed values, and the residual uses uniform point weights:

```text
Rwp = 100 * sqrt(sum((y_obs - y_calc)^2) / sum(y_obs^2))
```

The lowest post-fit Rwp determines the selected CIF. This is a **frozen-structure
profile selector**, not structural Rietveld refinement: no cell or atomic parameter is
optimized. Only after selection are the sealed references opened and the rankings
evaluated with the benchmark `StructureMatcher` configuration.

## Case-level results

| Case | Formula | Candidates | Selected Rwp (%) | Exact available | Selected exact |
| --- | --- | ---: | ---: | :---: | :---: |
| vh-001 | TlCNO | 19 | 5.158 | yes | yes |
| vh-002 | Li(NbS2)2 | 8 | 5.451 | yes | yes |
| vh-003 | Li2NbOF5 | 10 | 5.242 | yes | yes |
| vh-004 | Zr2TeS | 11 | 5.847 | yes | yes |
| vh-005 | TiCrAgS4 | 13 | 5.446 | yes | yes |
| vh-006 | Ba3In2O6 | 8 | 6.173 | no | no |
| vh-007 | Cr | 8 | 4.524 | yes | yes |
| vh-008 | TiNi | 8 | 5.197 | yes | yes |
| vh-009 | Tb(GaCo2)4 | 8 | 5.093 | yes | yes |
| vh-010 | Hg11I2BrClO4 | 15 | 5.212 | yes | yes |
| vh-011 | NaV2O5 | 12 | 5.132 | yes | yes |
| vh-012 | SmBi2BrO4 | 11 | 5.707 | yes | yes |
| vh-013 | TiCrAgS4 | 11 | 5.442 | yes | yes |
| vh-014 | Li3(AuO)4 | 13 | 6.063 | no | no |
| vh-015 | SrCaScTaO6 | 8 | 6.084 | yes | yes |
| vh-016 | Ca(FeSb3)4 | 8 | 5.317 | yes | yes |
| vh-017 | TaVSi4 | 8 | 5.529 | yes | yes |
| vh-018 | K4MgCu3F12 | 10 | 6.043 | yes | yes |
| vh-019 | Y5Sn3 | 12 | 7.222 | yes | yes |
| vh-020 | TiNi | 12 | 16.415 | yes | yes |

## Interpretation

This result demonstrates the distinction between candidate coverage and realized
performance. Independent sampling supplied an exact candidate in 18 cases; the
diffraction-derived verifier then identified one without access to the reference. It
does not establish an absolute Rwp threshold for correctness. In particular, the two
unsolved cases have Rwp values within the range of solved cases, so Rwp is useful here
as a within-problem discriminator rather than a cross-problem correctness certificate.

The panel is a repeatedly inspected 20-case development set. The 18/20 result should
therefore be treated as a proof of concept for verifier-enabled inference-time scaling,
not as an unbiased estimate of performance on unseen experimental data.

## Artifacts

- `summary.json`: aggregate machine-readable result.
- `protocol.json`: frozen selector and post-hoc evaluator definitions.
- `case-summary.csv`: one row per benchmark case.
- `candidate-rankings.csv`: all 213 candidates in Rwp rank order with post-hoc exact
  labels and source paths.
- `cases/<case>/report.json`: complete candidate-level fit reports, including fitted
  parameters, hashes, occurrence paths, and post-hoc evaluation.
- `selected/<case>.cif`: the minimum-Rwp output returned for each case.

## Reproduction

From the repository root, with `VPBENCH_GSAS_ENV` pointing to the locked GSAS-II
environment:

```bash
uv run vpbench rwp-verifier monkeys \
  --panel pxrd-bench/panels/inference-scaling-20 \
  --source results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8 \
  --output runs/adapted-sol-rwp-selector-reproduced \
  --gsas-python "$VPBENCH_GSAS_ENV/bin/python" \
  --parallel 12

uv run python experiments/inference-scaling/rwp-selector/build_report.py \
  --panel pxrd-bench/panels/inference-scaling-20 \
  --selector-run runs/adapted-sol-rwp-selector-reproduced \
  --source-campaign results/inference-scaling/sol-monkeys/adapted-codex-sol-high-api-reps1-8 \
  --output runs/adapted-sol-rwp-selector-report-reproduced
```
