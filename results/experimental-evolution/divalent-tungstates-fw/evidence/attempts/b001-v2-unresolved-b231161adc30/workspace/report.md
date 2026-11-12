# Powder XRD phase analysis

The crystalline sample is a two-phase mixture of monoclinic WO3 and orthorhombic BaCO3 (witherite). The refined fractions, normalized over these modeled crystalline phases, are:

| Phase | Space group | Weight fraction | Refined cell |
|---|---|---:|---|
| WO3 | P 21/c | 0.535127 (formal s.u. 0.002219) | a = 7.68025 A, b = 7.53836 A, c = 10.53238 A, beta = 136.15094 degrees |
| BaCO3 | P m c n (Pnma-equivalent setting) | 0.464873 (formal s.u. 0.002219) | a = 5.34105 A, b = 8.93178 A, c = 6.42626 A |

The final full-grid fit has Rwp = 1.92991%, Rp = 1.53897%, Rexp = 1.83835%, and goodness of fit = 1.05298 for 8,301 points. A native GSAS-II replay regenerated the reflections and profile without optimization, reproduced Rwp = 1.92991%, reproduced both fractions exactly at the reported precision, and raised no project-profile review flags.

## Evidence and model selection

The dominant coherent peak families are jointly accounted for by published monoclinic WO3 (parent COD 2311041) and witherite BaCO3 (parent COD 9010928), consistent with the stated WO3 and BaCO3 precursors and low 250 degrees C treatment. Re-equilibrated phase-deletion fits increased Rwp from about 2.00% before the final coordinate pass to 7.48% without WO3 and 5.55% without BaCO3, so both phases are required.

The WO3 source was selected by matched cumulative restarts: with coordinates fixed and the same nuisance model, COD 2311041 gave Rwp = 2.0035%, compared with 2.0453% for a physically valid triclinic WO3 alternative. A superficially better early WO3 source was rejected because it contained 1.575 A O-O contacts. In the final model, W and then O coordinate blocks were refined only after the inventory and profile model had stabilized. For BaCO3, a small Ba-site shift was retained; refining the carbonate C/O block produced implausible 1.23/1.50 A C-O bonds and was rejected, so those coordinates remain at the defensible published parent values.

The profile search covered background type/order, scale and cells, zero offset versus specimen displacement and their joint branch, common width/asymmetry terms, polarization, roughness, size, strain, and plausible texture. The retained stable model uses an eight-term Chebyshev-1 background, zero offset, common instrumental width/polarization, and positive phase-specific isotropic size and strain. Displacement, roughness, and texture were not supported. Atomic displacement refinement was also rejected when it became nonphysical or destabilized polarization.

A diagnostic BaWO4 addition refined reproducibly to only 0.00130(77) weight fraction (about 1.7 standard deviations), improved Rwp by just 0.00034 percentage point, and its freed cell drifted substantially. Deleting it restored the two-phase solution, so BaWO4 is not reported as a detected phase.

## Physical checks and uncertainty

Both exported models pass composition, occupancy, density, and short-contact screens. The refined WO3 model has minimum W-O and O-O separations of 1.735 and 2.502 A; the BaCO3 model has minimum C-O and Ba-O separations of 1.281 and 2.699 A. Bond-valence assignment gives W(VI)/O(-II) and Ba(II)/C(IV)/O(-II).

The major-phase identification and their relative amounts are reliable at the level supported by this pattern. The quoted fraction uncertainties are least-squares standard uncertainties, not total systematic errors; no independent standard is available to quantify the latter. Fractions refer only to the modeled crystalline material and do not constrain amorphous content. Exact WO3 oxygen coordinates are less secure than the W sublattice because oxygen scatters weakly in Cu X-ray data, while the BaCO3 carbonate coordinates were not independently refined. A trace BaWO4 fraction or another component at a comparable sub-percent level cannot be determined reliably from these data.
