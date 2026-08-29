# Licensing, data provenance, and external resources

The Apache License 2.0 in [`LICENSE`](LICENSE) applies to repository-authored
software, scripts, prompts, experiment configurations, and documentation unless a
file says otherwise. It does not relicense third-party software, source structures,
models, or data. Those resources retain their original terms.

## Benchmark structures and diffraction data

### pXRD-100

The 100 reference structures were selected from the MP-20 files released with
[CDVAE](https://github.com/txie-93/cdvae) at commit
`f857f598d6f6cca5dc1ea0582d228f12dcc2c2ea`. Their Materials Project identifiers,
source-file hashes, selection procedure, and database provenance are recorded in
[`pxrd-bench/pXRD-100/SOURCE.lock.json`](pxrd-bench/pXRD-100/SOURCE.lock.json) and
the benchmark manifest. Materials Project publishes its data under CC BY 4.0;
the source structures remain subject to the applicable
[Materials Project terms](https://next-gen.materialsproject.org/about/terms) and
should be cited to the Materials Project and the originating records. The Apache
license for this repository does not grant additional rights in those source
structures.

### pXRD-ood

The 100 pXRD-ood structures were generated for this benchmark from the four frozen
procedures documented in [`pxrd-bench/pXRD-ood/README.md`](pxrd-bench/pXRD-ood/README.md).
Their source boundaries, package/model versions, hashes, and generation records are
in `SOURCE.lock.json`, `GENERATION.lock.json`, and `BUILD-REPORT.md` in that directory.
Upstream structures and models used by the generation procedures retain their
source-specific terms.

The diffraction patterns and manifests are derived research artifacts included to
reproduce the reported benchmark. Hidden reference CIFs must not be exposed to an
evaluated solver.

## Crystallography Open Database

The coding-agent conditions used a read-only local subset of the
[Crystallography Open Database (COD)](https://www.crystallography.net/cod/). COD
data are dedicated to the public domain under CC0; users should acknowledge the
original structure authors and the COD. COD data are not bundled in this repository.

The frozen experiment resource was the DARA 1.3.0 filtered COD-2024 inventory:

| Item | Frozen value |
| --- | --- |
| Metadata file | `cod_filtered_info_2024.json.gz` |
| Metadata SHA-256 | `03599f54f03f04420523dca36cc06927b74ce0070a4a80e6d859faa38a6c5aed` |
| Filtered entries / local CIFs | 62,098 |
| Mirror manifest SHA-256 | `bafdfead1ccbf97f1f7b82cc0bb6b8bcd5b64be3acfa24619d24f48e6f4d1bf2` |
| ID-list SHA-256 | `ee64e082f946be93c54eb95b3d0fccc79cb8114b39178ebfd7dd8c2c039aac9c` |
| CIF-tree aggregate SHA-256 | `ccf34bcad7da2e03d6ddce7bc90ecf0dd413d0b31d6e50bfe343bda89f7bd69b` |
| Mirror synchronization time | `2026-07-23T01:32:45.453790+00:00` |
| Upstream recorded by the mirror | `https://qiserver.ugr.es/cod` |

The CIF-tree aggregate is the SHA-256 of lexically sorted `sha256sum` output for
all relative `*.cif` paths. [DARA documents](https://cedergrouphub.github.io/dara/dara.structure_db.html)
both the packaged metadata and COD CIF acquisition. A compatible
mirror can be built from the public COD rsync service and restricted to the IDs in
the metadata. Exact byte reproduction of a named run requires the frozen resource
above; a current mirror may contain later COD revisions. Supply the metadata and CIF
tree through `VPBENCH_COD_METADATA` and `VPBENCH_COD_CIFS`.

## Scientific software

- **GSAS-II** is cloned during setup and is not vendored here. Frozen conditions use
  commit `c8f97a500d7e48fddbaf8586948c24b174d8bab3`. GSAS-II retains its
  [upstream open-source license](https://github.com/AdvancedPhotonSource/GSAS-II/blob/c8f97a500d7e48fddbaf8586948c24b174d8bab3/LICENSE).
  Cite B. H. Toby and R. B. Von Dreele, *J. Appl. Cryst.* **46**, 544–549
  (2013), <https://doi.org/10.1107/S0021889813003531>.
- **DICVOL14** is not distributed by this repository. Frozen conditions record the
  expected binary SHA-256
  `317430d2806ec8e4ed8f87b70940d9315092cab0869f84e479ec1c6e3bb5e586`
  and accept only a user-supplied, authorized binary.
- Python dependencies and their exact versions are recorded in `pyproject.toml`,
  `uv.lock`, the condition TOMLs, and the generation runtime locks. Each dependency
  retains its own license.
- External baseline implementations and model artifacts are not vendored. Their
  source commits, downloads, and redistribution decisions are recorded under
  [`baselines/`](baselines/) and [`results/baselines/`](results/baselines/).

## Result artifacts

Normalized model outputs, submitted CIFs, and traces are included as scientific
evidence. A submitted structure may reproduce or transform facts from one of the
resources above; inclusion here does not alter the underlying source terms.
