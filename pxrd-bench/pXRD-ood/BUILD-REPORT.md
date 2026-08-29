# pXRD-ood v1 build report

> Provenance note: this report records the complete benchmark build. The top-level manifest,
> CIFs, fixedparams-v1 inputs, source locks, and generation/audit scripts are the authoritative
> assets included here.

Build date: 2026-07-19--20 UTC  
Dataset ID: `pXRD-ood-v1`  
Selection seed: `20260719`  
Status: **complete**

## Summary

The delivered benchmark contains 100 newly generated, ordered, full-occupancy
periodic structures. The final truth set has 25 CIFs from each of four streams:
isovalent substitution, ordered decoration, Wyckoff enumeration, and crystal
search. Every stream contains exactly five structures in each primitive-site bin
`1--4`, `5--8`, `9--12`, `13--16`, and `17--20`.

The novelty audit completed successfully with the terminal result
`OK: 100 complete-novelty pXRD-ood CIFs`. It independently reparsed the final P1
CIFs and recomputed formula, species-aware structure, and species-erased topology
certificates against a frozen 3,279,483-row exposure index. The final result is:

- 100/100 species-aware structures absent from the frozen exposure union;
- 50/50 composition-novel cases with no reduced-formula occurrence in any frozen
  source, each retaining a positive species-erased match to its recorded parent;
- 50/50 topology-novel cases with familiar formulas but no species-erased
  crystallographic match in the frozen union;
- 100 unique reduced formulas and no formula overlap with `pXRD-100`;
- 50 distinct familiar-topology parents, 100 distinct parent IDs overall, and no
  duplicate species-aware or species-erased final structures;
- all seven crystal systems represented, no crystal system above 20 cases, and no
  final space group above four cases; and
- 1--20 primitive sites, full framework support, valid CIF round trips, stable
  symmetry detection, valid periodic geometry, and at least five resolvable peaks
  under the benchmark diffraction profile.

The crystal-search stream was rerun with **MACE-MH-1**, head `omat_pbe`, on ten
Modal workers requested as `A100-40GB`. Of 156 proposals, 150 converged and 145
passed the post-relaxation geometry gates; 25 fully certified, diverse cases were
selected. The final truth set contains no result from the earlier MACE relaxation.

Native inputs are complete for the four installed frameworks: Crystalyze,
PXRDGen, deCIFer, and DiffractGPT. Each target manifest reports 100 supported and
zero unsupported cases under `require-all`. A second complete target build matched
all 615 target files byte for byte.

“Novel” in this report always means novel relative to the frozen public exposure
boundary and locked `StructureMatcher` tolerances. It is not a universal novelty,
thermodynamic-stability, dynamic-stability, or synthesizability claim.

## Final benchmark composition

| Panel | Stream | Final cases | Primitive-site quota |
|---|---|---:|---|
| Composition-novel, topology-familiar | Isovalent substitution | 25 | 5 per bin |
| Composition-novel, topology-familiar | Ordered decoration | 25 | 5 per bin |
| Topology-novel, composition-familiar | Wyckoff enumeration | 25 | 5 per bin |
| Topology-novel, composition-familiar | MACE-MH-1 crystal search | 25 | 5 per bin |

The crystal-system distribution is cubic 10, hexagonal 10, monoclinic 16,
orthorhombic 20, tetragonal 19, triclinic 8, and trigonal 17. The authoritative
case-level record is `manifest.json`; `selection-report.json` contains the quota
and diversity summaries, and `novelty-report.json` contains the top-level novelty
certificate.

Final CIFs are explicit ordered P1 files for adapter compatibility. Detected space
group and crystal system are retained in the manifest, so writing P1 does not erase
the audited symmetry metadata.

## Frozen exposure boundary

The sources were frozen before final certification. The SQLite exposure index is
11,780,169,728 bytes and contains 3,279,483 source rows. Counts are per source and
are not deduplicated across corpora, because overlapping exposure is itself part of
the audit trail.

| Locked source | Rows | Role in the exposure boundary |
|---|---:|---|
| Crystalyze released MP-20 archive | 45,052 | Exact full released split union |
| PXRDGen/CDVAE MP-20 | 45,229 | Exact train/validation/test union |
| deCIFer NOMA | 2,285,914 | Conservative full released archive |
| JARVIS-DFT 2022 | 75,993 | Official DiffractGPT/AGAPI guard |
| DiffractGPT released examples | 75,997 | Conservative released split union |
| DARA bundled COD index | 62,098 | Exact bundled public-COD retrieval index |
| Current public COD frozen union | 534,823 | Complete active snapshot plus live delta |
| Materials Project 2026.04.13 | 154,377 | Supplemental frozen natural-database guard |

Framework-level interpretations are deliberately conservative:

- Crystalyze and PXRDGen use their exact released MP-20 corpora.
- deCIFer is checked against every released NOMA tuple. The archive contained
  2,285,914 unique records, 2,568 more than the 2,283,346 count in the paper; all
  additional records were retained rather than assuming they were unexposed.
- DiffractGPT is checked against the union of the official 75,993-entry JARVIS
  snapshot and all 75,997 released examples because the exact deployed split is
  not documented.
- DARA is checked against its exact bundled public-COD index and the full frozen
  public COD union. Licensed ICSD content remains explicitly unchecked.
- AGAPI-XRD is conservatively approximated by frozen JARVIS plus the full public
  COD union because the unpublished server revision cannot be frozen exactly.
- Materials Project release 2026.04.13 was fetched as a supplemental guard. The
  API key was read from the environment and was never written to an artifact.

The COD boundary combines a 2026-07-06 active snapshot with every official
live-only CIF through 2026-07-19. It includes 1,337 live-only records and one
changed existing record. Forty nonstructural catalog records are retained under
sentinel keys rather than silently dropped. Large embedded SHELX byte payloads
were omitted from the searchable SQLite payload to keep matching tractable, while
the raw archive and inventory hashes retain provenance for those bytes.

`SOURCE.lock.json` records every source status, count, artifact or per-file hash,
and the exact/conservative/inferred/licensed-unchecked classification. All sources
have `status: complete`, `failed_count: 0`, and the lock explicitly records that no
API key was committed.

## Candidate generation

A deterministic surplus pool of 496 candidates was produced:

| Stream | Generated |
|---|---:|
| Substitution | 100 |
| Ordered decoration | 100 |
| Wyckoff enumeration | 140 |
| Crystal search | 156 |

Substitutions use full symmetry-orbit, oxidation-compatible element changes on
known parents, followed by radius-based cell rescaling. Ordered decorations split
complete parent symmetry orbits using bounded supercells while preserving an
anonymous mapping to the transformed parent. The two topology-novel streams use
seeded PyXtal symmetry/Wyckoff construction with formulas that already occur in
the learned-model corpora and in at least one retrieval catalog.

All candidates were screened for ordered full occupancy, supported elements,
finite positive cells, 1--20 primitive sites, sensible per-atom volume, periodic
overlaps, CIF round trip, stable spglib standardization, and the existing
benchmark XRD profile. Near-identical candidate patterns were excluded during
selection. No baseline output, rank, fit, or failure was used to choose a case.

## MACE-MH-1 relaxation rerun

The earlier crystal-search relaxations were superseded. The active run used:

- model: `MACE-MH-1`;
- head: `omat_pbe`;
- model SHA256:
  `a522eb7f59c7879963d41586528f4980baf33e086c94aa92e3eafdeccad3be47`;
- optimizer: ASE FIRE with `FrechetCellFilter` and `FixSymmetry`;
- stopping configuration: `fmax=0.10 eV/angstrom`, maximum 1,000 steps;
- MACE 0.3.16, torch 2.13.0+cu130, ASE 3.29.0; and
- Modal run `mace-mh-1-a100-20260720`, ten workers, requested GPU string
  `A100-40GB`.

The Modal doctor ran on an `NVIDIA A100-SXM4-40GB` and verified CUDA, the model
hash, the `omat_pbe` head, a model evaluation, and a tensor smoke test before
submission. Modal honored the requested accelerator class but scheduled nine of
the ten shards on available 80 GB A100 variants. The actual device record across
all 156 proposals was 16 A100-SXM4-40GB, 64 A100-SXM4-80GB, and 76 A100 80GB PCIe.
Requested and actual hardware are both retained in diagnostics rather than
reporting every worker as a 40 GB device.

All ten shards completed with no execution or collection failure. There were 150
optimizer-converged results and six nonconverged results. Five additional
converged structures failed post-relaxation static geometry checks, leaving 145
accepted relaxed candidates. Their site-bin counts were 35, 36, 27, 31, and 16
from the smallest to largest bin, so all final quotas remained feasible.

The final 25 crystal-search cases are all converged and pass all static and novelty
checks. Their optimizer step counts range from 23 to 602 with a median of 128.
Their recorded hardware is 1 A100-SXM4-40GB, 12 A100-SXM4-80GB, and 12 A100 80GB
PCIe, spanning nine of the ten shards.

The durable Modal handle binds every submitted candidate to its input CIF hash.
The merged relaxation report contains all 156 diagnostics, including initial and
final energy, forces, step count, convergence, model hash, actual GPU, call ID,
shard, and geometry-gate result.

## Full topology certification

Anonymous structure matching was the computational bottleneck. A physical subset
of the immutable exposure index was built for the 103 anonymous formulas needed
by the candidate pool. It contains all 303,706 matching source records and is
362,741,760 bytes. This is only a layout/cache optimization: the source lock and
full exposure-index hash remain authoritative.

Exact topology checks for all 296 topology-novel candidates were sharded over ten
Modal CPU workers with four CPUs each. No GPU was requested for this CPU-bound
operation. The successful run `complete-topology-20260720-r3` completed all ten
shards with zero failures and 8,126.464539 aggregate container-seconds. Its cache
is bound to:

- the candidate-pool manifest hash;
- every candidate CIF hash;
- the derived topology-index hash;
- pymatgen 2026.5.4; and
- the complete locked `StructureMatcher` settings.

The matcher uses `ltol=0.20`, `stol=0.30`, `angle_tol=5`, primitive reduction,
scale normalization, and no attempted supercell. Strict structure checks are
species-aware. Topology checks use `fit_anonymous` over every source structure
with the same anonymized reduced formula; space group, Wyckoff, and coordination
fingerprints are not accepted as final proof.

Two launch attempts were discarded before any match result was accepted. The
first evaluated a host-only path check during remote module import. The second
loaded a dynamic dataclass module without first registering it in `sys.modules`.
Both faults were fixed in the runner, their incomplete handles remain in `.runs`
for provenance, and only the hash-bound `r3` result is consumable. As a regression
check, all 140 unchanged Wyckoff candidates reproduced their earlier per-source
results exactly, with zero mismatches.

After all gates, 403 of 496 candidates were certified: 100 substitutions, 100
ordered decorations, 105 Wyckoff-enumeration cases, and 98 relaxed crystal-search
cases. The crystal-search certified counts by site bin were 8, 29, 19, 28, and 14,
so deterministic selection did not need to weaken any quota.

## Selection, build, and independent audit

Selection chose exactly five certified cases per site bin and stream, then applied
global formula, parent, structure, space-group, crystal-system, chemistry,
coordination, and XRD-profile diversity constraints. Tie-breaking is deterministic
and never consults a framework's benchmark outcome.

The build was run with `--verify-repeat`. It first wrote and audited a staging
truth tree, rebuilt the selection a second time, and compared all 111 truth files
present at that stage byte for byte. IDs, manifests, locks, reports, and CIFs were
identical. The authoritative tree was then audited independently from the final
P1 CIF files against the frozen source index; this source-backed audit took about
1 hour 45 minutes and passed.

The independent audit recomputed rather than trusted copied metadata:

- CIF hashes, composition, reduced formula, cell, density, primitive-site count,
  detected symmetry, and diffraction descriptors;
- formula hits and strict species-aware structure matches in every source;
- all familiar-parent and topology-novel anonymous structure certificates;
- cross-case species-aware and species-erased duplicate checks;
- formula disjointness from `pXRD-100`;
- 25/25/25/25 stream counts and five-per-bin quotas; and
- parent uniqueness, space-group caps, crystal-system coverage, static geometry,
  supported-element, and diffraction-profile constraints.

## Framework targets

The target builders were generalized to accept `--corpus-root`, `--dataset-id`,
`--case-prefix`, and `--support-policy`. This removed their hard-coded
`pXRD-100` assumptions while preserving the original framework-native numerical
environments and preprocessing contracts.

| Framework | Native target result | Manifest SHA256 |
|---|---|---|
| Crystalyze | 100 `.xy` patterns; 100 supported, 0 unsupported | `33a85903ed7560957931516561ced05a33208dd189324f7b180cb1e8e1532b1a` |
| PXRDGen | 100 GSAS-II `.dat` patterns; 100 supported, 0 unsupported | `c56520dc5f5680d6092e424b98f914658b6011681081f94151280e456c6483f1` |
| deCIFer | 100 `.xy` patterns; 100 supported, 0 unsupported | `03ecea504a0d410972e8f67153f5a0dcf81224a58a19d170badc9bb83f3adc2d` |
| DiffractGPT | 100 patterns, 100 180-bin vectors, 100 prompts; 100 supported, 0 unsupported | `eda830a26988f564f8c469c24a3867681ba29ec308f91c1366022679021972f9` |
| Ab-PXRD-Solver | 100 native noisy CSV patterns plus 100 clean audit profiles; 100 supported, 0 unsupported | `99de66c36262b37248623fc89cacb9c432365bde28f7a1b80e049045e9b566f9` |

Every target manifest identifies `pXRD-ood-v1`, uses case prefix `pxrdood`, uses
support policy `require-all`, and records the same source-manifest SHA256:
`613d12b8def084113332c7d94184bb4456adf9f9a7caa9bc2185b6c32d42d00e`.

PXRDGen uses GSAS-II revision 5806 and keeps reduced formula as the primary model
input. Forty-two structures have a primitive/target-cell formula that differs
from the reduced formula; this is recorded as an adapter diagnostic, not an
unsupported case. DiffractGPT uses the released checkpoint's 180 values on
`[0, 90)` degrees at 0.5-degree spacing and the locked paper-era JARVIS numerical
environment. The publication mentions Gaussian broadening without specifying a
width and released no matching preprocessing implementation, so the adapter does
not invent an undocumented width; that reconciliation is recorded in its target
artifacts.

Ab-PXRD-Solver uses the released GSAS-II synthetic-input recipe: Cu K-alpha
average at 1.54184 Angstrom, 10--80 degrees two-theta inclusive at 0.02 degrees,
U=0.2, V=-0.2, W=2.0, X=0.5, Y=0.5, 20 micrometer crystallite size, no added
background, 5,000-count Poisson noise plus 0.1% Gaussian noise, and maximum
intensity 100. Its numerical target details come from released code because the
paper describes preprocessing and refinement but does not enumerate them.

DARA and AGAPI-XRD remain part of the novelty exposure boundary, but target trees
were not generated for this corpus because their OOD target/runtime contracts are
outside this build.

## Problems encountered and adjustments made

1. **The requested relaxation model changed.** Earlier MACE results were retained
   only under ignored run provenance. The crystal-search pool was rerun from its
   original inputs with MACE-MH-1, and final selection, locks, manifests, and
   targets were rebuilt from the new structures.
2. **Local relaxation was not the requested execution shape.** The work was moved
   to ten Modal workers. Submission, status, and collection use durable handles so
   an interrupted client cannot silently duplicate or lose a shard.
3. **Requested and physical GPU models differed.** Modal accepted the exact
   `A100-40GB` request, while most workers reported 80 GB A100 devices. Both facts
   are recorded at case and run level.
4. **Not every relaxation was usable.** Six proposals did not converge and five
   more failed geometry gates. The surplus pool was large enough to reject all 11
   without relaxing any benchmark constraint.
5. **A full anonymous scan was CPU-heavy.** The 11.78 GB source index was reduced
   to a hash-bound, candidate-formula physical subset without removing any
   relevant record. Exact matching was then distributed across ten CPU workers.
6. **Two topology Modal launches failed before work began.** Import-time path and
   dynamic-module registration bugs were fixed; no partial result from either
   attempt entered the cache or benchmark.
7. **Released corpus counts were not always identical to paper counts.** The NOMA
   discrepancy was handled conservatively by indexing the larger released corpus.
   DiffractGPT duplicate JIDs were retained by split/ordinal identity.
8. **COD records vary substantially in payload quality and size.** The frozen
   official inventory, raw hashes, live delta, changed records, and nonstructural
   records are all explicit rather than silently filtered.
9. **Framework builders assumed `pXRD-100`.** Shared corpus configuration and
   support checks were factored into `scripts/target_dataset.py`, then each of the
   four installed adapters was rebuilt and audited twice.

## Integrity hashes and durable evidence

Authoritative truth hashes at completion:

| Artifact | SHA256 |
|---|---|
| `manifest.json` | `613d12b8def084113332c7d94184bb4456adf9f9a7caa9bc2185b6c32d42d00e` |
| `SOURCE.lock.json` | `ff159ebb286cefe58171311cb80785b15e4e57ae323297287329328c29edbd8a` |
| `GENERATION.lock.json` | `22321812f528d8d18417a8a8d27566c5ffebf58a12210b6edc5cbfb091fddf74` |
| `selection-report.json` | `fbf5dfc055c7188a102c325078c59dfeb39712f087f7591245e3f7826e96e551` |
| `novelty-report.json` | `f4b94ae6afb958755a729f0b13cb0a1fc09324629d0a8beaa8b10a2d4eca46df` |

Large ignored evidence:

| Artifact | SHA256 |
|---|---|
| Full exposure index | `34ade87e310c553cbec4a958a3375a62b4596e5a4d18c542c830a4a7f8406884` |
| Candidate topology index | `f10b29a5a926fec07f355e211de6418b59e45aad447ca1f853f3a8e566138975` |
| Candidate-pool manifest | `6098f41d29b985c42ae0580281b5c9a15464d1cfaa37c3691a4ad50bd186645e` |
| Certified-pool manifest | `5763c146b92e5c97901d680d4f187d0442446a467501fc9e80a54a8437f0b5ad` |
| Exact topology cache | `09017c300db8e11e58a35139cf6759fde23c2d54b8278350c0d1822225700896` |
| MACE Modal handle | `bb01ceed5c84246556459c210625297fbd0bb53b0bfd9d5b2ed83a1575f09081` |
| Topology Modal handle | `46405cd695b3cc887e8e9ee6079f0c0ad7a483bb2d28f5a7d30beb770764ca6a` |

Important evidence paths are:

- `.runs/pxrd-ood/indexes/exposure.sqlite3`;
- `.runs/pxrd-ood/indexes/candidate-topology.sqlite3`;
- `.runs/pxrd-ood/candidates/manifest.json`;
- `.runs/pxrd-ood/certified/manifest.json`;
- `.runs/pxrd-ood/mace-mh-1-relaxation-report.json`;
- `.runs/pxrd-ood/topology-matches/current.json`;
- `.runs/modal-handles/pxrd-ood/mace-mh-1-a100-20260720.json`; and
- `.runs/modal-handles/pxrd-ood-topology/complete-topology-20260720-r3.json`.

The source corpora, indexes, candidate pool, rejected candidates, older MACE
artifacts, and Modal handles remain under ignored `.runs/`; they are evidence and
working state, not blind benchmark inputs.

## Reproduction and audit commands

From the repository root, with the frozen `.runs/pxrd-ood` sources and indexes in
place:

```bash
sim-bench/.venv/bin/python sim-bench/scripts/build_pxrd_ood.py \
  build --replace --verify-repeat

sim-bench/.venv/bin/python sim-bench/scripts/build_pxrd_ood.py \
  audit --root sim-bench/pXRD-ood --workers 2
```

The durable Modal runs can be inspected without resubmission:

```bash
cd sim-bench
.venv/bin/python scripts/run_pxrd_ood_modal.py \
  status --run-id mace-mh-1-a100-20260720
.venv/bin/python scripts/run_pxrd_ood_topology_modal.py \
  status --run-id complete-topology-20260720-r3
```

Framework audit commands use their locked numerical environments and the common
corpus arguments. For example:

```bash
cd sim-bench
.runs/envs/crystalyze-runtime/bin/python scripts/build_crystalyze_targets.py audit \
  --corpus-root pXRD-ood --dataset-id pXRD-ood-v1 \
  --case-prefix pxrdood --support-policy require-all
.runs/envs/pxrdgen-gsas2full/bin/python scripts/build_pxrdgen_targets.py audit \
  --corpus-root pXRD-ood --dataset-id pXRD-ood-v1 \
  --case-prefix pxrdood --support-policy require-all
.venv/bin/python scripts/build_decifer_targets.py audit \
  --corpus-root pXRD-ood --dataset-id pXRD-ood-v1 \
  --case-prefix pxrdood --support-policy require-all
.runs/envs/diffractgpt-targets/bin/python scripts/build_diffractgpt_targets.py audit \
  --corpus-root pXRD-ood --dataset-id pXRD-ood-v1 \
  --case-prefix pxrdood --support-policy require-all
.runs/envs/pxrdgen-gsas2full/bin/python scripts/build_ab_pxrd_solver_targets.py audit \
  --corpus-root pXRD-ood --dataset-id pXRD-ood-v1 \
  --case-prefix pxrdood --support-policy require-all --workers 2
```

Use `build_pxrd_ood.py export-blind DESTINATION` for evaluation. The exported
tree contains only case ID, composition, radiation/grid metadata, and the pXRD
input. The truth CIFs, parent IDs, novelty evidence, and generation metadata must
not be mounted into the evaluated agent environment.

## Remaining scope limitations

- Novelty is conditional on the exact frozen sources and matcher definition.
  Private, later, or unknown corpora can contain an equivalent structure.
- DARA's licensed ICSD exposure could not be checked without a licensed snapshot.
- AGAPI-XRD's unpublished live server revision cannot be reproduced exactly; its
  reported public JARVIS/COD stores are covered conservatively instead.
- Geometry validity and a crystalline diffraction pattern do not establish a
  useful metastable basin. Formation energy, hull distance, phonons, and
  synthesizability were intentionally not selection gates.
- MACE-MH-1 relaxation is part of the crystal-search generation protocol, not an
  experimental stability certificate.
