# Writing a LAB.md

A lab file is the only document that changes between demonstrations. The evolver reads all of it; the generator reads its settings block. Write it from what the laboratory knows before any analysis (its chemistry, synthesis protocol, instrument and the metadata it records), never from evaluation results or from how solvers performed. [divalent-tungstates/LAB.md](divalent-tungstates/LAB.md) is a complete example.

## Prose sections

1. **Application.** The sample family and how samples are made: kinds of starting materials and how many, how they are combined, the heating or crystallization conditions, and what a product can contain (residual reagents, intermediates, polymorphs, phases missing from the reference library). End with the task: crystalline phases, defensible structures and mass fractions.
2. **Measurement and solver inputs.** The instrument and scan in plain words, exactly what solvers receive, and what is unknown or uncalibrated.
3. **Learning priorities** (optional). What the lab needs from the solver, stated as capabilities in order of importance, and what is out of scope. Capabilities, not case types, and never where baseline solvers fail.

Keep generic process rules out: PROMPT.md and TOOLS.md hold them for every lab. Do not describe where baseline solvers fail.

## Settings block

Exactly one fenced block whose info string is `json lab-settings`. Unknown or missing top-level fields are refused. GSAS-II units and conventions throughout.

| Field | Meaning |
|---|---|
| `schema` | `"pxrd-lab-settings/1"` |
| `lab_id` | Short name, recorded in every case |
| **measurement** | |
| `geometry` | `"bragg_brentano"` (the only geometry implemented) |
| `goniometer_radius_mm` | The instrument's radius; sets the size of specimen-displacement shifts |
| `radiation` | `wavelength_ka1_A`, `wavelength_ka2_A` (`null` for one wavelength: monochromated or synchrotron) and `ka2_ka1_ratio` |
| `grid_deg` | `min`, `max`, `step` of the lab's scans; match the experimental inputs |
| `peak_counts` | Choices for the maximum noise-free counts; span the lab's typical scans |
| `zero_offset_deg` | Distribution and range of the angular zero error |
| `instrument_profile` | Distributions for U, W, X, SH_L and polarization, drawn once per measurement session. A standard (Si, LaB₆) measured on the same instrument is the best basis |
| `background` | `sampled_families_v1` parameters: family weights, floor and tail counts, decay lengths, power exponents |
| **specimen** | Each entry may be omitted or set to `{"enabled": false}` |
| `displacement_um` | Sample-height error: `distribution` (`uniform`), `range`, `probability` |
| `surface_roughness` | Low-angle intensity deficit (Suortti): `probability`, `A_range`, `B_range`, `B_distribution`, `max_low_angle_deficit` at `deficit_reference_2theta_deg` |
| `crystallite_size_um` | Per-phase isotropic size: `distribution`, `range` |
| `microstrain_ppm` | Per-phase isotropic microstrain: `distribution`, `range`, `probability` |
| `preferred_orientation` | March–Dollase: `model`, `distribution`, `range` of ratios, `probability`, candidate `axes` |
| `uiso_A2` | Per-phase isotropic displacement parameter: `distribution`, `range` |
| `reference_mismatch` | How far each phase's true structure lies from its library entry: `cell_strain` (maximum principal strain, at most 0.005), `position_rms_A` (coordinate RMS of each element, at most 0.08 Å), optional `position_rms_A_by_element` overrides (for example a larger value for `O`), and `probability`. Symmetry-preserving; applies in specimen-control cases too |
| `control_size_um` | Size choices for specimen-control cases |
| **solver_inputs** | |
| `pattern_columns` | Header of `pattern.csv` as in the experimental inputs |
| `line_ending` | `"lf"` or `"crlf"` |
| `sample_fields` | Solver-visible sample fields. Each has `type` (`formula`, `formula_list`, `number`, `string`) and optional `items` (count range), `range`, `choices`, `nullable` |
| `element_sources` | `fields` whose formulas supply elements, `ambient` elements that can enter or leave (air, solvent, decomposition), and whether `each_source_element_present` must appear in some phase |
| `metadata` | A template that reproduces the lab's experimental `metadata.json`. `"{sample.NAME}"` inserts a sample field; `{"per_session": [...]}` picks one value per measurement session |

Distributions are `{"distribution": "uniform" | "log_uniform", "range": [low, high]}`.

## Requirements on the evaluation data

The experimental inputs must be a `pattern.csv` and a `metadata.json` per scan, because the fixed baseline prompt (P0.md) names those files. The metadata template must give synthetic cases the same structure as the experimental metadata, so solvers see one format in training and in evaluation.

Withheld-reference cases are generic: the researcher chooses `withhold_ids` per case with `runtime/library_neighbours.py` (TOOLS.md). A lab file need not mention them.

## Before a new lab can run

Check these against the lab's actual data:
- whether the instrument fits `bragg_brentano` (transmission and capillary geometries are not implemented);
- whether its phases are covered by the frozen reference library;
- whether its specimens need effects the generator lacks: anisotropic broadening, stacking faults, microabsorption, amorphous content.

DECISIONS.md lists these as open options.
