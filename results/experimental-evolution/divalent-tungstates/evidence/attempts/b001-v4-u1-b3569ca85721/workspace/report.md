# PXRD phase analysis

## Result

The crystalline assemblage is scheelite CaWO4, monoclinic WO3, and a monoclinic Ca3WO6 double-perovskite-type phase. Fractions are normalized only over these modeled crystalline phases.

| Phase | Space group | Refined cell (Å, deg) | Weight fraction |
|---|---|---|---:|
| CaWO4 | I 41/a | a = 5.24502, c = 11.38222 | 78.39(7)% |
| WO3 | P 21/c | a = 7.68674, b = 7.53556, c = 10.51119, beta = 136.0775 (equivalent nonstandard setting) | 11.429(40)% |
| Ca3WO6 | P 21/n | a = 5.53570, b = 5.78420, c = 8.01765, beta = 90.0839 | 10.181(63)% |

The final full-range refinement uses all 8,301 measured points and gives Rwp = 3.2222%, Rp = 2.4759%, Rexp = 2.2413%, and goodness of fit = 1.4376. Because pointwise uncertainties were not supplied, Poisson uncertainties, sigma = sqrt(max(counts, 1)), were used. Parentheses in the table are formal GSAS-II covariance errors in the last digits; they do not include model-selection or texture systematics.

## Evidence and inventory

- CaWO4 matches ambient scheelite COD 7219229, a 298 K Cu X-ray Rietveld record. Its strong low-, middle-, and high-angle families are present throughout the pattern. The full-occupancy model refines to four equal W-O distances of 1.818 Å and eight Ca-O distances of 2.410-2.460 Å. The oxygen position was the only atomic-coordinate subset supported by this powder pattern.
- WO3 matches the low-temperature monoclinic neutron model COD 2311041. Its two distorted WO6 environments retain W-O distances of 1.714-2.158 Å and a minimum O-O separation of 2.538 Å. Under the same provisional schedule, triclinic COD 2106293 and orthorhombic COD 2107312 gave Rwp about 13.64% and 14.85%, respectively, versus about 13.55% for monoclinic WO3. Another monoclinic record fitted similarly but contained a nonphysical 1.575 Å O-O contact and was rejected on the physical inventory.
- No exact Ca3WO6 database entry was available. A stoichiometric-analogue search selected full-occupancy P 21/n Ca3OsO6 (COD 1562666); this parent is a 293 K Mo K-alpha single-crystal model from a high-pressure growth study. The chemically justified isovalent substitution Os6+ -> W6+ gives a Ca3WO6 model whose unique reflections account for the residual family near 18.7-19.3, 22.0, 30.7, 32.2, 36.6-37.5, 45.2, and 57.0 degrees 2theta. Its refined cell differs only modestly from the parent, with regular 1.924-1.940 Å WO6 octahedra and minimum O-O = 2.700 Å. An adapted Ca3UO6 parent gave provisional Rwp about 12.40%, versus 10.59% for the selected Ca3OsO6-derived model.
- CaO was tested with a physically fixed cell after Ca3WO6 was introduced; its nonnegative scale collapsed to zero. High-pressure fergusonite CaWO4 and chemically poorer/disordered analogue records failed their unique reflections or geometry. They were excluded rather than represented by zero-scale phases.
- The refined phase mixture gives an overall Ca/W molar ratio of about 1.005, consistent with the CaO + WO3 precursor balance. No retained model has partial occupancy or a short interatomic contact.

## Final profile model and checks

The final pass was restarted from neutral HAP settings after the phase inventory stabilized. It retains one angular correction (408.4 micrometre specimen displacement; zero fixed), a common nonnegative W/X profile with U fixed at zero after pruning, and isotropic size broadening only for CaWO4 (about 87 nm) and Ca3WO6 (about 305 nm). All strain-only trials and WO3 size broadening returned to a neutral/bound limit and were rejected. A bounded axial-divergence trial was strongly correlated with displacement and was pruned.

The effective polarization refined to 0.8065, inside its physical 0-1 interval. CaWO4 required a reproducible [110] March-Dollase correction (1.2448); [001], [100], [101], [111], and [112] alternatives fitted worse. WO3 texture collapsed to unity. A small apparent Ca3WO6 texture gain worsened its isolated 020 diagnostic reflection and was driven by overlaps, so it was rejected. Eighteen Chebyshev background terms were retained as the first penalized-fit minimum; higher orders introduced progressively wavier baseline structure.

The saved project was reopened and replayed over the complete measured range after the accepted changes. It has no frozen variables or bound-seeking refined terms; the largest parameter correlation is below 0.87. The submitted CIFs, fractions, and profile were exported directly from that exact project.

## Remaining uncertainty

The CaWO4 and WO3 phase assignments are high confidence. The Ca3WO6 reflection topology, cell, and roughly 10 wt% abundance are supported, but its atomic coordinates are inherited from the substituted Ca3OsO6 prototype and are not independently determined by this pattern; detailed Ca3WO6 distortions therefore cannot be claimed reliably. Its fraction, and the other fractions coupled to it, should not be interpreted at the sub-percent accuracy suggested by formal covariance errors.

There is no internal standard, so an absolute amorphous/noncrystalline fraction cannot be determined. The reported fractions exclude broad background scattering, and trace crystalline phases below the detection/resolution of this pattern may remain unmodeled.
