Review this completed pXRD structure-solution attempt following the judge-policy

Composition: Li3Fe2(SiO4)2
Pattern: <BENCHMARK_PATTERN>/pattern.csv
Wavelength: 1.5406 angstrom (Cu Kalpha1)
Chronological trace: <EXTERNAL_PATH>
Final response: <EXTERNAL_PATH>
Submitted CIFs:
- <EXTERNAL_PATH>
Comparable whole-pattern scores:
<EXTERNAL_PATH>

Act as a inference-time verifier for exact crystal-structure recovery. Decide whether
the submitted candidate set is sufficiently established or whether another solution attempt is warranted.

Consider the diffraction fit, physical plausibility, and what the trajectory
actually instantiated and compared. Distinguish support for the cell, Z, and
average framework from support for the submitted symmetry, coordinates,
occupancies, and element ordering. A small unresolved discrete ambiguity should
not be considered resolved merely because an averaged or convenient realization
fits well.

Decide continue when the diffraction fit is dubious or a materially different, scientifically motivated structure that could plausibly improve the candidate set seems likely.

Write `decision.json`:

```json
{
  "decision": "stop|continue",
  "reason": "..."
}
```

Do not alter or generate CIFs. Pause immediately after recording the decision.
