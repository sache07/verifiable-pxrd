# pXRD-ood

This directory contains 100 newly generated, ordered periodic structures for a
composition-plus-powder-XRD out-of-distribution benchmark. The four generation
streams contain 25 cases each. `manifest.json` is authoritative and every case
contains a frozen-corpus novelty certificate.

The truth layout is:

- `composition-novel-topology-familiar/substitution/`: 25 isovalent substitutions;
- `composition-novel-topology-familiar/ordered-decoration/`: 25 ordered decorations;
- `topology-novel/wyckoff-enumeration/`: 25 PyXtal symmetry/Wyckoff candidates; and
- `topology-novel/crystal-search/`: 25 MACE-MH-1-relaxed crystal-search candidates.

Each stream has exactly five primitive structures in each site-count bin 1--4,
5--8, 9--12, 13--16, and 17--20. Formulas and familiar-topology parents are unique,
all seven crystal systems occur, no final space group occurs more than four times,
and no formula overlaps `pXRD-100`.

`SOURCE.lock.json` records the frozen exposure boundary and source/index hashes;
`GENERATION.lock.json` records software and model hashes; `novelty-report.json` and
`selection-report.json` summarize the machine-audited certificates and quotas.
`BUILD-REPORT.md` is the comprehensive execution log, including source
counts, Modal runs, rejected work, reproducibility checks, and limitations.
`FRAMEWORKS.md` records the public coding-agent input contract and result privacy
boundary.

The crystals are geometrically valid but are not claimed to be thermodynamically
stable, dynamically stable, synthesizable, or universally novel. Ground-truth CIFs
and provenance remain hidden from evaluated agents; the public runner stages only the
reduced composition and diffraction pattern.
