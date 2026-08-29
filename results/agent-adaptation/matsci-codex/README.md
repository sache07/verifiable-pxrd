# matsci-codex

`full-200-r1/` is the completed Codex baseline with general materials-science Python
and read-only local COD access, without a pXRD-specific capability layer, GSAS-II, or
DICVOL interface.

The released exact metric gives 60 selected / 61 selected-or-declared-alternative
matches on pXRD-100 and 44 / 44 on pXRD-ood: 104 / 105 out of 200 overall. Three OOD
tasks were infrastructure-blocked and remain failures in the conservative denominator.

The result uses the same normalized layout as the other agent conditions: one
canonical attempt per case, submitted CIFs, verifier records, launch metadata, final
answers, and compressed chronological Codex event traces. The original run contained
214 attempt directories because 14 infrastructure failures were retried; the canonical
attempt choice is reproduced from the run's immutable `progress.json` and is independent
of scientific outcome.
