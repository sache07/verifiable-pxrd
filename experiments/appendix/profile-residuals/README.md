# Rwp distributions

This folder rebuilds the appendix's **as-submitted** candidate distributions. Frozen numerical data and coverage tables are in `results/appendix/profile-residuals/as-submitted`. Original archives and manuscript figures have not been changed. Native-refinement reruns are a separate experiment.

```bash
python experiments/appendix/profile-residuals/plot.py --output .runs/profile-residuals
python -m pytest experiments/appendix/profile-residuals/test_metric.py
```

Plotting needs NumPy, SciPy, and Matplotlib. The command writes two PDFs, two PNGs, and a summary CSV. Tests verify the input hashes, every archived group count/mean/median, 200 zero-residual reference self-comparisons, and equality of the agent data in the native and shared panels.

## Metrics

Both analyses use `100 * sqrt(sum((reference - candidate)^2) / sum(reference^2))`, with unit weights and independent max normalization. The profiles differ:

- **Native:** Crystalyze's masked encoder profile; DiffractGPT's released 180-bin representation; deCIFer's clean Q-space pseudo-Voigt profile; PXRDGen's frozen doublet GSAS-II profile; Ab-PXRD-Solver's native noisy GSAS-II profile. The historical Ab evaluator applies the same case seed separately to the reference and candidate simulations. Native values should not be ranked across these different representations. RealPXRD's sparse peak list has no native dense-profile panel.
- **Shared fixedparams-v1:** clean GSAS-II candidate versus clean GSAS-II reference, on the same 8,501-point, 5–90 degree grid. Cu K-alpha-1 wavelength 1.5406 Å; U=2, V=-2, W=5, X=Y=0; polarization 0.7; SH/L=0.002; isotropic size 1 micrometer and microstrain 1000. No noise, background, fitted scale, alignment, or structural refinement. This is an oracle evaluation diagnostic because it uses the reference structure. Values are not bounded by 100%.

The four LLM/agent conditions use the clean shared metric in **both** figures; equality is tested. These values are not the observation-based residuals reported by agents or by the inference-time selector.

## Plotting and interpretation

Each finite submitted candidate contributes one point, including alternatives. Blue denotes an exact structural match and red a miss; each class density is normalized separately. Solid and dashed lines show the mean and median. Counts are candidates, not problems; candidates from the same problem are correlated. Failure/missing-score counts remain in the coverage tables.

Native panels use Freedman–Diaconis bin counts clipped to 14–42 bins, with 4% range padding. The `matsci-codex`, `pxrd-codex`, and `adapted-codex` x axes stop at the pooled 95th percentile. This only crops the display: tails remain in the histograms, KDEs, means, and medians. The tool-free GPT panel is not cropped. Shared panels use 40 bins and a common maximum rounded up to the next 10 percentage points. KDE bandwidth is SciPy's default Scott rule.

These plots show how profile agreement relates to structural recovery. They are not case-weighted leaderboard scores. Any post-refinement figure should use the same candidate cohort, retain failed refinements via an explicit fallback, recompute the match labels, and report coverage. Do not silently substitute only successfully refined candidates.

## Re-simulation check

`score_pair.py` reuses the benchmark's locked GSAS-II target builder and recomputes the shared clean metric for a reference/candidate pair. Use the native-refinement pinned Python environment, fetched Ab sources, and GSAS-II commit `1a0aeec6c61b54f68e6812704730a471187ac393`:

```bash
python experiments/appendix/profile-residuals/score_pair.py reference.cif candidate.cif \
  --gsas /path/to/GSAS-II/GSASII --output .runs/profile-residuals/check
```

The binary installer supports `--binaries-only --gsas-root /path/to/GSAS-II`. This pair checker uses directly importable CIFs; the archived bulk scorer also had a canonicalization fallback for backend import failures. The retained frozen CSVs are the authoritative inputs for reproducing the published distributions.

`score_native.py METHOD CORPUS CASE CANDIDATE --gsas ... --output ...` also recalculates a specialist's native residual using the current repository's target builders. It supports Crystalyze, DiffractGPT, deCIFer, PXRDGen, and Ab-PXRD-Solver. deCIFer additionally needs PyTorch; DiffractGPT needs `jarvis-tools==2024.10.30`. The five native representations stay distinct; no obsolete Q-space cross-framework comparison is included.

`verify_scores.py --gsas ... --output ...` checks one fixed case (`pxrd100-rep-001`) across all conditions against the frozen shared scores. Add `--native` to check the native scores. DiffractGPT's generated CIFs are withheld from the public baseline bundle pending license clarification, rather than missing because parsing failed. An optional `--diffractgpt-archive /private/original/run` permits local verification using hash-checked original files; it does not copy those CIFs into the repository. Without it, that condition is explicitly recorded as not checked.

The archived data were imported with obsolete absolute workspace prefixes removed from locator fields. The manifest records the original and imported hashes; metric values, exact-match labels, eligibility, and failure records are unchanged. Historical locator fields are provenance, not current runnable paths.
