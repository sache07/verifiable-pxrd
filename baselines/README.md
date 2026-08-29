# Comparison frameworks

Each subdirectory contains the adapter and configuration for one comparison
framework. Framework-specific target inputs are stored with the corresponding
adapter; checkpoints, upstream source checkouts, and run outputs are not included.

| Directory | Framework |
| --- | --- |
| `ab-pxrd-solver/` | Ab-PXRD-Solver |
| `crystalyze/` | Crystalyze |
| `decifer/` | deCIFer |
| `diffractgpt/` | DiffractGPT |
| `pxrdgen/` | PXRDGen |
| `realpxrd-solver/` | RealPXRD-Solver |

Each adapter provides the following commands:

1. `prepare.py` stages and verifies pinned source and model artifacts.
2. `make_targets.py` constructs the framework-native benchmark inputs.
3. `doctor.py` performs a local compatibility check.
4. `run.py` provides the common `doctor`, `preflight`, `submit`, `status`,
   and `collect` interface.

`make_targets.py` writes one self-contained directory per corpus:

```text
baselines/<framework>/targets/
├── pxrd-100/
│   ├── manifest.json
│   ├── parameters.json
│   ├── inputs*.csv
│   └── patterns*/
└── pxrd-ood/
    └── ...
```

Target builders preserve each model's required pattern representation:

| Framework | Primary generated representation |
| --- | --- |
| Crystalyze | 8,500-row `two_theta_deg,intensity_normalized` CSV (`.xy`) |
| deCIFer | 1,000-row `q_inv_angstrom,intensity_normalized` CSV (`.xy`) |
| PXRDGen | 7,500 newline-delimited intensity values (`.dat`) |
| DiffractGPT | 180-bin `.xy`, exact model vector, and rendered prompt |
| Ab-PXRD-Solver | 3,501-row noisy and clean `2theta,intensity` CSVs |
| RealPXRD-Solver | native discrete two-theta/intensity peak pairs (`.xy`) |

Every bundle also records the selected composition condition, source hashes,
framework applicability, and complete simulation parameters. Pass
`--output-root <path>` for an isolated scratch build; otherwise the directory
above is used automatically. The shared `fixedparams-v1` profiles remain under
`pxrd-bench/<corpus>/targets/` because they define the benchmark measurement,
not an individual framework's serialization.

Collection automatically creates a case-first view beside the native shard
outputs:

```text
<run-id>/
├── candidates/
│   ├── <case-id>/
│   │   ├── candidate-01.cif
│   │   └── verifier-results.json  # added by evaluation
│   └── manifest.json
└── shard-*/                       # raw worker provenance
```

For an already collected run, the CIF view can be created directly from its
input path:

```bash
uv run python -m verifiable_pxrd.baselines.candidates --input <run-directory>
```

The shared evaluator, or `crystalyze/evaluate.py` for Crystalyze, adds one
`verifier-results.json` per case after StructureMatcher evaluation. Invalid
attempts appear in that verifier record even when no valid CIF can be exposed.

`baseline.json` records the evaluated condition, and `artifacts.lock.json` records
external artifact identities. Exact structural recovery is calculated by the shared
benchmark evaluator. Each runner reads its defaults from `baseline.json`; command-line
flags can be used for diagnostic variants.
