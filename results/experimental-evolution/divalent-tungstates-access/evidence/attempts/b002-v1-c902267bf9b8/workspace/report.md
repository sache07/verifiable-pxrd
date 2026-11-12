# Powder XRD phase analysis

## Result

The crystalline pattern is described by three phases. Weight fractions are normalized over these modeled crystalline phases; they do not measure any amorphous content.

| Phase | Space group | Weight fraction | Refined cell (A, degrees) | Assessment |
|---|---:|---:|---|---|
| MnWO4, wolframite | P 2/c | 0.60206(90) | a=4.79551, b=5.70166, c=4.97096, beta=91.1075 | Reliable phase identification |
| WO3, monoclinic | P 21/c | 0.21548(79) | a=7.29450, b=7.53264, c=10.50561, beta=133.0088 | Reliable phase identification |
| Mn3W2O12, analogue-derived model | P 21/c | 0.18246(92) | a=8.68547, b=8.91345, c=14.89439, beta=123.4095 | Tentative structure/composition |

Parenthesized uncertainties are the GSAS-II least-squares e.s.d.s on the final fixed phase inventory. They are only about 0.08-0.09 wt% and substantially understate uncertainty from phase choice, peak-shape assumptions, and the tentative third-phase model.

The final refined-range statistics are Rwp=6.6724%, Rp=4.4474%, GOF=3.3526, chi-square=92818.0, with 8275 observations and 17 varied parameters. A read-only atomic replay over all 8301 original points gives Rwp=6.6715%. The replay regenerated structure factors and reflection lists from `final.gpx`; it produced a positive background and peak widths and no project-review flags.

## Chemical and diffraction evidence

The metadata describes Cu K-alpha reflection data from 9.903 to 100.095 degrees 2-theta (Kalpha1=1.540598 A, Kalpha2=1.544426 A, ratio 0.5) for an 800 C product made from WO3 and Mn3O4. No product formula or phase count was assumed.

The dominant narrow peak family is indexed and intensity-matched by wolframite MnWO4 (COD-derived model 1520200). A one-phase model left a coherent second family and had Rwp about 28.5%. All nine available same-formula WO3 structures were then fitted with identical scale/background and cell stages; monoclinic COD 2311041 gave the stable positive second phase. Even after supported profile and coordinate refinement, the two-phase model retained a coherent broad residual family at Rwp about 17.3%.

For that family, direct Mn/W oxide candidates and analogue parents were screened rather than assuming a known ternary. The broad search generated 2825 one- or two-element substitutions of binary/ternary oxide prototypes; 2690 were ranked, 93 failed the initial contact screen, and 42 remained unknown because they could not be evaluated safely. A symmetry- and topology-diverse shortlist was Rietveld-tested from the same two-phase project. The P21/c Sb2(PO4)3 parent topology (COD 4030285), transformed by P->Mn and Sb->W while preserving multiplicities, gave Mn3W2O12. Its common scale/background fit was positive, and independent cell terms reduced Rwp to 11.19%, clearly ahead of Mn2WO5 (14.25%) and Mn3WO6 (14.63%) alternatives. The chemically more conventional reverse assignment Mn2(WO4)3 on the same topology was explicitly tested but remained at Rwp 17.15%, so it does not explain the residual intensities.

Only the candidate W coordinates were retained after staged testing. Refining its Mn coordinates lowered Rwp but generated a 1.22 A Mn-O contact, so that branch was rolled back. Texture and size terms were retained only where stable. A two-parameter surface-roughness branch was not retained because its parameters were 98.95% correlated.

Candidate-ledger summary:

| Branch | Final status | Outcome |
|---|---|---|
| MnWO4 exact-formula structure (1 available) | tested | COD 1520200 accepted |
| WO3 exact-formula structures (9 available) | tested / rejected / unknown | COD 2311041 accepted; a diverged trial was left unknown rather than rejected |
| Direct known Mn/W oxide third phases (34 branches) | tested / rejected / unknown | None closed the broad residual family |
| Analogue substitutions and broad oxide-parent search (2825 coarse jobs; 23 common-fit finalists) | tested / rejected / unknown | COD 4030285-derived Mn3W2O12 accepted conditionally; failed or invalid trials remain unknown |
| Reverse Mn2(WO4)3 site assignment | tested, rejected | Positive but only 1.8 wt% and Rwp 17.15% |
| Candidate Mn-coordinate refinement | tested, rejected | Rolled back for a 1.22 A Mn-O contact |
| Fourth-phase closure set (10 branches plus profile follow-up) | tested / rejected / unknown | No physically stable fourth phase accepted |

There are no pending planned branches in the submitted inventory.

## Phase closure and uncertainty

After the three-phase refinement, precursor and residual-peak closure trials included MnO polymorphs, Mn3O4, Mn2O3, MnO2, reduced tungsten oxides, a second WO3 polymorph, Mn3WO6, and related prototypes. Rocksalt MnO and several others collapsed to negligible scale. Hexagonal MnO and Mn3WO6 each acquired about 1.2 wt% and a small numerical improvement only when their crystallite size collapsed to 0.001 micrometre, far outside the 0.04-1.5 micrometre physically supported range; those branches are marked unknown rather than accepted or chemically rejected. No reliable fourth crystalline phase is therefore reported.

MnWO4 and WO3 are well supported by their peak positions, intensities, stable positive scales, and physically reasonable coordination. The third component is less secure. Its exported model has W-O distances of 1.81-2.33 A and a minimum O-O distance of 2.41 A, but it inherits four-coordinate Mn sites from a phosphate topology with unusually short Mn-O distances of 1.48-1.69 A. Thus Mn3W2O12/P21/c is the best falsifiable PXRD model found for the remaining approximately 18 wt% crystalline contribution, not a reliable claim of a known equilibrium compound. Its topology, exact composition, and fraction have material model uncertainty despite the small formal e.s.d.; complementary chemistry or higher-resolution data would be needed to establish them independently.

Detailed branch statuses are retained in `analysis/wo3_trials_v2/ledger.json`, `analysis/third_phase_trials/ledger.json`, `analysis/prototype_search/coarse_ledger.json`, `analysis/prototype_trials/ledger.json`, `analysis/prototype_trials/reverse_ledger.json`, `analysis/closure_trials/ledger.json`, and `analysis/fourth_profile_trials/ledger.json`.
