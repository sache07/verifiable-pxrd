# Appendix profile-residual analysis

- `as-submitted/`: frozen candidate scores, coverage, group summaries, and provenance hashes.
- `figures/`: regenerated native and shared fixedparams-v1 PDF/PNG distributions, plus recomputed summary statistics.
- `verification/`: fresh simulation checks against the frozen scores, including input hashes and software versions. All ten shared-profile conditions and all nine available native-panel conditions reproduce the fixed check-case scores exactly.

Rebuild commands and metric definitions are in `experiments/appendix/profile-residuals/README.md`. No post-refinement candidates have been substituted into these distributions. The original manuscript assets and source archives remain untouched.

The check case is `pxrd100-rep-001`, first candidate (selected candidate for agents). These 19 numerical checks verify the forward-model and metric implementations on that case; they are not a fresh resimulation of the complete corpus. DiffractGPT was verified against private archived CIFs whose hashes match the public result manifest; those CIFs are not redistributed here.
