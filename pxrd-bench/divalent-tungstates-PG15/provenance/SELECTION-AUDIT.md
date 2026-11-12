# Precursor Genome as an experimental evaluation pool

Audit date: 19 September 2026. These are measured evaluation cases; synthetic generation would supply the separate training/practice problems. No solver or prompt-evolution experiments were launched in this audit.

## Recommendation

The original 30-reaction spinel-precursor selection is useful but is not an established optimum. After reading the actual outcomes, the strongest shortlist is:

1. **Niobate synthesis:** the most promising broad candidate for a structural-reasoning demonstration, with a 13-reaction transition-metal core and a 30-reaction extension.
2. **Divalent-metal tungstates:** a compact 15-reaction family with several common framework types and substantial secondary phases absent from the inspected full COD.
3. **A tighter spinel/oxide family:** 15 reactions selected by precursor chemistry, with more product formation than the original 30. This is the simplest initial setting for learning prototype construction, substitution, and sensible refinement.
4. **Yttrium–transition-metal oxides:** 14 related reaction products, including reported YCrO3 and YMn2O5 phases not found in the inspected full COD.
5. **Alkali–manganese oxides:** 16 reactions, 15 with usable reference interpretations. Attractive for phase/average-structure choice but less clean for exact composition or fraction accuracy.

Niobates have greater structural breadth and evaluation ambiguity; spinels have simpler reusable transformations and many already excellent database fits. Tungstates offer a useful middle ground. These are judgments about likely learning opportunities, not measured adaptation gains.

## Data and reference availability

Sources: [Precursor Genome paper](https://arxiv.org/html/2607.09903v1), [ledger and schema](https://github.com/lauren-walters/precursor-genome), [experimental data deposit](https://zenodo.org/records/21285546).

The inspected ledger has 1,035 samples. Following its stored `active_scan_index` and `active_case_index`, 1,030 samples have a selected refinement with phase weights. Requiring no recorded physical failure, a valid scan, accepted human review, and quality 1 or 2 leaves **996 samples: 680 quality 1 and 316 quality 2**. These counts are calculations on the downloaded ledger, rather than quoted dataset totals.

Each selected refinement supplies phase labels with reference identifiers, weight fractions, Rwp, provenance and human quality scores. The `phase_weights` numbers are fractions: 0.7415 means 74.15 wt%. The sample-level field misleadingly named `weight_percent` uses the same fractional convention. Sums for the 996 selected references range from 0.999 to 1.0005, consistent with rounding around one. They describe the modeled crystalline components, not independently measured amorphous content.

The 591 unique selected phase labels comprise 583 ICSD-labeled entries and eight custom labels. An ICSD label does **not** establish absence from COD.

Quality scores mean excellent fit (1), good fit with minor discrepancies (2), and poor/incomplete fit (3). The final model is a reference interpretation, not an independently established exact structure/composition. Manual provenance is not a new measurement of DARA failure: this audit did not reconstruct controlled before/after refinements.

Selected exported refinement objects were also checked. Eight simple dictionary exports contain observed/calculated patterns, phase fractions and fitted cell parameters. They do not supply complete atomic coordinate models; `structs` is absent or None. Thus full atomic structure equivalence to the ICSD references was not established here. One richer manual object was retrieved but not loaded because it required executable object reconstruction. Its phase fractions are available independently in the JSON ledger.

## Family comparison

All family definitions use precursor chemistry. The measured outcomes are used to assess the definitions, not to silently remove inconvenient cases. `Mixed product` counts published partially/completely reacted labels. `Multiphase` requires at least two modeled components at >=1 wt%; this avoids counting zero-weight entries as phases.

| Family | All / usable references | Quality 1 / 2 among usable | Multiphase | Mixed product | Manual final model |
|---|---:|---:|---:|---:|---:|
| Original spinel-precursor selection | 30 / 30 | 21 / 9 | 26 | 18 | 5 |
| Tighter spinel/oxide core | 15 / 15 | 12 / 3 | 12 | 13 | 1 |
| Transition-metal niobate core | 13 / 13 | 9 / 4 | 13 | 10 | 1 |
| Broader niobate family | 30 / 30 | 18 / 12 | 30 | 17 | 6 |
| Divalent-metal tungstates | 15 / 15 | 13 / 2 | 13 | 10 | 4 |
| Yttrium–transition-metal oxides | 14 / 14 | 10 / 4 | 14 | 7 | 1 |
| Alkali–manganese oxides | 16 / 15 | 11 / 4 | 14 | 8 | 11 |

### 1. Niobate synthesis

**Scope:** Nb2O5 paired with one of a specified set of metal oxides/carbonates/hydroxides. The 13-reaction core uses MgO, ZnO, CoO, Co3O4, NiO, CuO, MnO, Mn3O4, Mn2O3, MnO2, Fe2O3, Fe3O4 or Cr2O3. The 30-reaction set extends to alkali, alkaline-earth, yttrium and other selected cation precursors; the exact list is in `families.json`.

**What the experimental tasks contain:** Nb2O5-related precursor components coexist with metal niobates, residual oxides and alternative structural descriptions. Reported products include MgNb2O6, MnNb2O6, CoNb2O6, NiNb2O6, ZnNb2O6, Mg4Nb2O9, CuNb2O6, NaNbO3, Sr5Nb4O15 and Y3NbO7. The broader family provides several substantial components whose particular models or compositions were not found in COD.

**Potential reusable procedures:** identify/reuse a common niobium-oxide component across mixtures; construct related metal-niobate candidates by substitution; compare polymorphs and cell/symmetry alternatives; attribute remaining reflections to a distinct product versus a deficient precursor model; refine fractions while testing the stability of the phase assignment. The core is chemically narrower than the extension, giving an interpretable progression in difficulty.

**Limits:** the ledger repeatedly uses a Cm Nb12O29 model. Its repeated selection does not establish exact oxygen stoichiometry or the necessity of Cm. COD contains Nb12O29 in other space groups and multiple Nb2O5 models. Broadening, compositional differences and pseudosymmetry can compete with a literal phase interpretation. Such cases are suitable for model-selection investigation, but the CIF label alone is not an unquestionable structural target.

### 2. Divalent-metal tungstates

**Scope:** WO3 paired with MgO, CaCO3, SrCO3, BaCO3, BaO2, PbO, ZnO, CuO, CoO, Co3O4, NiO, MnO, Mn3O4, Mn2O3 or MnO2. There are 15 experiments. The MoO3 analogues expand this to 30 experiments, of which 29 have accepted quality-1/2 interpretations.

**What the tasks contain:** common MWO4 compounds, residual WO3/precursors, and metal-rich tungstates. Mg/Mn/Co/Ni/Zn cases share recognizable wolframite-related structures; Sr/Ca cases include scheelite-related structures. The Sr and Pb reactions have substantial reported secondary phases not found in the searched COD systems.

**Potential procedures:** choose between a small number of framework families; adapt a related reference to a new cation/composition; examine residual peaks for a second tungstate stoichiometry; separate a WO3 polymorph/profile mismatch from a distinct product; check that a proposed phase fraction is stable to the model choice.

**Why this is a good middle ground:** the chemistry is narrow and the recurring building blocks support reusable reasoning, while some products are more demanding than textbook known-phase mixtures. The WO3-only pool has more product formation than the combined Mo/W pool because many MoO3 reactions remained at lower temperatures with substantial unreacted material.

### 3. Spinel/oxide core

**Revised scope:** {MgO, CoO, NiO, CuO, ZnO} × {Cr2O3, Fe2O3, Ga2O3}, giving 15 experiments. This removes the low-temperature Al(OH)3 branch and the less coherent MnO/Mn2O3 pairing from the original definition without selecting on solver residuals.

The original 30 comprise eight unreacted and four transformed cases. The revised 15 comprise ten completely reacted, three partially reacted, one transformed and one unreacted case according to the ledger. Retaining the original 30 as an overall evaluation and reporting the 15 as a prespecified structural subset is also reasonable.

**Potential procedures:** build spinel candidates from chemistry when an exact database composition is absent; model supported mixed cation/vacancy populations; compare cubic and distorted alternatives; avoid assigning every shifted peak to a new phase; distinguish a defective single oxide from a mixed-metal spinel. These are low-dimensional, repeated decisions and therefore a plausible setting for useful guidance to transfer.

**Limits:** many final fits are already excellent. Neighboring transition metals can have similar X-ray scattering, so precise cation partitioning/inversion may be poorly constrained. Several missing exact compositions are simply solid-solution variants of available prototypes. This motivates constructing/refining candidates, but does not by itself require solving an unfamiliar framework from scratch.

### 4. Yttrium–transition-metal oxides

**Scope:** Y2O3 paired with the transition-metal precursor list used above, plus Al(OH)3 and Ga2O3, giving 14 reactions. Seven are assigned mixed products and seven are unreacted/transformed.

Reported products include YCrO3, YFeO3, Y2Cu2O5 and Y–Mn–O phases alongside residual oxides. YCrO3 and YMn2O5 were not found at those compositions in the searched full COD systems; YFeO3 is present but with a different reference symmetry.

**Potential procedures:** account for persistent bixbyite Y2O3; construct chemically plausible ternary oxides from related prototypes; compare alternative symmetry/ordering descriptions; decide which minor products are supported by independent reflections. This is a smaller, experimentally coherent alternative to the broader niobate pool.

**Limits:** only a subset has new products, and exact polar/centrosymmetric assignments can be difficult from these scans. A model should not be rejected solely for missing the particular low-symmetry CIF label if a simpler structure explains the available evidence equally well.

### 5. Alkali–manganese oxides

**Scope:** {Li2CO3, LiOH, Na2CO3, K2CO3} × {MnO, Mn3O4, Mn2O3, MnO2}, giving 16 experiments, including one poor reference retained and flagged. Of the 15 usable references, 11 are manual.

The recurring problem is distinguishing manganese-oxide transformations, lithium-manganate products, sodium layered/hydrated components, and residual carbonate/hydroxide phases. It connects most directly to our previous average/disordered-structure discussion. The sodium examples PG_2635 and PG_2835 contain reported P63/mmc Na–Mn–O components at about 5.9 and 7.3 wt%, respectively; that family is not represented by an exact ternary entry in the inspected COD query.

**Potential procedures:** compare layered and other manganese-oxide alternatives; consider average structures and supported partial occupancy; maintain consistent treatment of hydrates/carbonates; distinguish intensity/profile errors from a missing component. This offers richer procedural choices than the wider Li/Na–transition-metal selection, which mostly retains precursors.

**Limits:** low-temperature chemistry, hydration and weak components make exact composition/fraction labels less secure. Do not expect laboratory Bragg data alone to recover exact Li/H content or local ordering. Multiple near-duplicate reference phases in some deposited fits may function as profile descriptions rather than independently established phases.

## Less promising directions in this particular deposit

- **Ammonium phosphate + transition-metal precursors:** 28 reactions, 24 usable references, but only two of those 24 are assigned mixed products. Most occur at 200 °C and describe decomposition/residual precursors. A high manual-model count does not turn this into a strong phosphate-structure evaluation set.
- **Borates:** 30 selected reactions, 29 usable, only two mixed-product outcomes. More suitable for uncertain/amorphous product handling than confident structure/fraction recovery.
- **Silicates:** 30 selected, 27 usable, five mixed-product outcomes. Again less product-rich than the family name suggests.
- **La-containing oxide families:** many runs remain at 200 °C with La(OH)3. The corresponding Y-containing branch is more useful here.
- **Vanadates:** a reasonable reserve rather than a rejection. The 60-reaction definition has 58 usable references and 29 mixed-product outcomes. A 26-reaction Mg/Zn/transition-metal subset is more coherent, but many V2O5 routes remain precursor-rich while V2O3 routes reach higher temperatures. Multiple vanadium oxidation states and related polyhedral networks could support learning; reference interpretation and reaction-condition confounding need more curation.

## COD coverage: what was actually checked

First, every parsed selected phase label was screened against the local DARA filtered COD-2024 index using chemical system, fractional composition and space-group number. Fractional-composition L1 tolerance was 0.015; this is a screening heuristic, not a definition of phase identity.

Then **51 live full-COD chemical-system queries** were cached, returning 1,781 entries. Every returned-list length agrees with the endpoint's separate count query. Searches include duplicates, entries flagged with errors, and theoretical entries. Both declared and calculated formulas were examined. Queries were performed for promising local gaps, not every possible phase in every family.

The full-COD checks matter: NiWO4, CoWO4, Mn5O8, Mn2O3 in R-3, La(OH)3 and ferrous oxalate dihydrate have suitable composition/SG entries even though the local filtered index screening missed them. They should not be advertised as absent from COD.

Three different situations must remain distinct:

1. **Composition not found in the queried chemical system:** strong evidence of a usable reference gap, subject to metadata/cross-database curation.
2. **Composition present, selected symmetry absent:** an alternative model is missing, but an available model may be sufficient after refinement.
3. **Exact solid-solution composition absent, parent prototype present:** construct/refine a related model. This is useful agent behavior but does not establish a need for an unfamiliar ab initio framework solution.

These are dated catalog checks. They are not an exhaustive comparison of atomic structures, not a proof that every missing symmetry is physically required, and not a claim that structures are unavailable in all other open resources.

## Concrete experimental cases

Fractions below are the deposited final-model fractions, multiplied by 100. They are not new refinements. Labels for approximately stoichiometric phases are simplified for readability; exact source labels are in `reference_records/`.

| Sample / precursors | Deposited crystalline model, wt% | Human quality | COD finding |
|---|---|---:|---|
| PG_1539: Ga2O3 + NiO | gamma-Ga2O3-type 74.15; NiO 18.43; beta-Ga2O3-type 7.43 | 1 | No Fd-3m Ga2O3 model in the full Ga–O query. ICSD 236276 is independently identified as the gamma model by AFLOW. |
| PG_3850: Nb2O5 + Y2O3 | Y3NbO7 (P21) 39.05; Nb12O29 (Cm) 31.65; Y2O3 29.30 | 2 | No Y3NbO7 composition in the full Y–Nb–O query. Nb12O29 exists in COD in other symmetries. |
| PG_4549: SrCO3 + WO3 | SrWO4 63.20; Sr2WO5 (Pnma) 24.78; WO3 9.64; SrCO3 2.38 | 1 | No Sr2WO5 composition in the full Sr–W–O query. |
| PG_1050: Cr2O3 + Y2O3 | YCrO3 (P21/c) 44.46; Y2O3 33.81; Cr2O3 21.73 | 1 | Full Cr–Y–O query contains YCrO4, but no YCrO3. |
| PG_2750: Mn3O4 + Y2O3 | Y2O3 38.67; YMn2O5 (Pbam) 29.73; YMnO3-type 18.96; Mn3O4 12.65 | 1 | No YMn2O5 composition in the full Y–Mn–O query. |
| PG_3538: Na2CO3 + Nb2O5 | NaNbO3 (Pm) 63.05; Nb2O5-type 36.95 | 2 | Many COD NaNbO3 structures, but no Pm entry in the query. An alternative-symmetry test, not an entirely missing compound. |
| PG_3845: Nb2O5 + SrCO3 | Sr5Nb4O15 (P2/m) 62.42; Sr2Nb2O7 37.58 | 2 | Sr5Nb4O15 exists as COD 8101224, P-3c1. Need to test structural equivalence/adequacy before calling this a relevant missing model. |
| PG_4049: PbO + WO3 | PbWO4-like (I-4) 48.28; Pb3WO6 15.35; WO3 12.79; Pb2WO5 12.53; PbO 5.51; Pb2O3 4.19; Pb3O4 1.35 | 1 | Pb3WO6 and Pb2WO5 compositions not found in full Pb–W–O query; PbWO4 has other available descriptions. |
| PG_2448: LiOH + V2O5 | LiVO3 (C2/c) 100 | 1 | No LiVO3 composition in the full Li–V–O query. Useful simpler control, rather than a multiphase centerpiece. |

Two especially important interpretation checks:

- **PG_1539:** [AFLOW](https://aflow.org/p/A11B4_cF120_227_acdf_e-001/) explicitly describes ICSD 236276 as gamma-Ga2O3 with partially occupied Ga sites. Thus this is a concrete missing-average-model example. But NiGa2O4 is available in full COD (1541403 and 5910320) and is a relevant alternative in this chemistry. The reported gamma-Ga2O3 fraction should not be treated as independently proven rather than a potentially useful structural proxy. AFLOW also means the gamma structure is openly described outside COD.
- **PG_3850:** [experimental work on Y3NbO7](https://www.sciencedirect.com/science/article/pii/S0022459623003158) distinguishes an average defect-fluorite structure from more complicated local models. A successful Bragg-data solution should be judged at the structural level actually identifiable, rather than forced to match a particular low-symmetry reference exactly.

Sr2WO5 is supported as a real material by [combined X-ray/neutron structural work](https://doi.org/10.1016/j.jallcom.2016.11.388), which used a related Ba2WO5 starting model. This is direct precedent for constructive prototype reasoning. There is also subsequent discussion of Pnma versus Pna21 descriptions in [later structural work](https://doi.org/10.1021/acs.inorgchem.4c03617). The accepted Precursor Genome label alone does not settle that distinction.

## What would establish an advantage over DARA?

The published reference analyses already used DARA with ICSD and COD. Missing COD entries demonstrate a limitation of a specified candidate library, not a categorical failure of the DARA algorithm with all structures supplied.

A useful experiment gives both systems the same starting references and measurement metadata, then tests whether an agent can construct and validate a missing model. Compare with DARA using the complete intended COD access, and with a reference-supplied DARA run to assess how much of the effect is candidate availability. A fixed cue to try structure construction and automatically evolved guidance remain informative comparisons.

If the claim is specifically ab initio structure solving, distinguish it from retrieving the target through AFLOW or a paper and from substituting into a known prototype. Each is useful for a real lab, but they support different capability claims. Missing exact composition alone does not prove that solving a new topology is necessary.

For evaluation, use complete chemistry-defined panels and report the missing-model cases as a separate diagnostic subset. Do not optimize prompts on these experimental answers. Repeated precursor routes with the same cations should be grouped when assessing transfer. Quality-2 interpretations and near-duplicate phase decompositions require sensitivity analysis or expert adjudication; phase-fraction error against the ledger is agreement with a published model, not absolute mass-fraction accuracy.

## Artifacts and reproducibility

- `audit.py`: precursor-based definitions, active-record extraction and local COD screen.
- `families.json`, `families.csv`: all inspected definitions and sample IDs. Local-gap columns are explicitly preliminary, not full-COD absence counts.
- `samples.json`, `phases.json`: complete selected ledger records and phase-level screening evidence.
- `cod_live_queries/`: all 51 cached live queries, URLs, counts and metadata.
- `live_cod_comparison.json`: phase-level full-COD comparison for the targeted systems.
- `selected_cases.csv`, `selected_phase_coverage.csv`: convenient case/fraction and phase-coverage tables for the main five families.
- `evaluation_inputs/`: 90 measured patterns converted from XRDML without intensity normalization, with source metadata and checksums. All 90 source files were found. One case has a poor/unusable reference and is retained with its flag.
- `reference_records/`: the separate author solutions and quality metadata; 89 of the 90 exported cases pass the reference-selection rule.
- `refinement_inspection/`: selected public refinement exports and safely extracted metadata; no downloaded code was executed and no unrestricted unpickling was performed.
- `provenance.json`: source ledger and local index paths, checksums and screening settings.

This is a curation/audit directory, not a blinded agent environment. Source IDs and reference interpretations are deliberately available here. A subsequent blind solver environment must expose only the permitted inputs and structure resources.
