# Powder XRD phase analysis

## Result

The pattern is modeled as three crystalline phases. Fractions are normalized only over these modeled crystalline phases.

| Phase | Model | Space group | Weight % | a, b, c (Å) |
|---|---|---:|---:|---|
| ZnWO4 | wolframite | P 2/c | 72.143 ± 0.074 | 4.69768, 5.72654, 4.93584 |
| WO3 | monoclinic tungsten trioxide | P 21/c | 20.692 ± 0.070 | 7.29379, 7.53853, 10.50815 |
| ZnO | wurtzite | P 63 m c | 7.165 ± 0.042 | 3.24994, 3.24994, 5.20263 |

Fit statistics: Rwp = 2.6664%, Rp = 2.0274%, Rexp = 2.6919%, GOF = 0.9951 (8284 observations, 76 variables).

## Evidence and model selection

The metadata reports ZnO + WO3 precursors heated at 750 °C and reflection Cu Kα data (λ1 = 1.540598 Å, λ2 = 1.544426 Å, Kα2/Kα1 = 0.5). The broad dominant family indexes as wolframite ZnWO4; sharp residual families identify monoclinic WO3 and wurtzite ZnO. Clean deletion fits raise Rwp from 2.67% to 34.53% without ZnWO4, 19.85% without WO3, and 6.29% without ZnO. The WO3 deletion restores the 23.45/23.89/24.70° and related families; ZnO deletion restores 32.07/34.74/36.57/47.84/56.87/63.16° lines.

The ZnWO4 model derives from COD 9005254 after mapping its mixed Zn/Cu divalent site to Zn. Zn/Cd-, Mg-, Mn-, triclinic, doubled ordered, and scheelite parents were cell-adapted and compared. The Zn/Cu- and Zn/Cd-derived P2/c parents converge to effectively identical refined coordinates (Rwp difference <0.001%); the Zn/Cu source was retained because it is the composition-nearest parent. The low-symmetry and alternate-topology parents remained substantially worse after clean restarts.

For WO3, COD 2311041 monoclinic, COD 1528915 monoclinic, and COD 2106293 triclinic parents were compared with the cumulative inventory. After matched coordinate, heavy-W displacement, and profile refinement, the triclinic finalist gave Rwp 2.6762% with 104 variables, versus 2.6664% with 76 variables for the selected monoclinic source; monoclinic is favored by both χ² and parsimony. WO3 [001] March–Dollase texture is strongly required (ratio 1.2938); deleting it raises Rwp to 4.15%.

Coordinates were refined last by site/element blocks. The retained structures pass composition, occupancy, density, and interatomic-distance screening. The final nuisance model uses a positive 16-term Chebyshev background, specimen displacement, physical polarization, axial divergence, isotropic ZnWO4 size/strain, isotropic WO3 size/strain, WO3 texture, and stable heavy-W Uiso terms. Surface roughness, X/Y broadening, joint zero/displacement, and anisotropic post-atomic broadening were rejected because they hit bounds, were branch-dependent, or were unsupported. The largest retained parameter correlation is 0.967; independent starts reproduced the calculated curve, cells, fractions, and structure without frozen variables.

## Remaining uncertainty

The phase identities are secure, but the exact public parent for ZnWO4 is not uniquely distinguishable after coordinate refinement; the Zn/Cu- and Zn/Cd-derived P2/c models converge to the same powder solution. The reported ± values are formal covariance ESDs. Across valid nuisance/source restarts the fractions varied by roughly 0.1 weight-percentage point or less, but systematic uncertainty is larger than the formal ESDs; a practical interpretation is about ±0.2–0.4 percentage point per phase. No external standard was supplied, so amorphous material (if present) and absolute crystalline yield cannot be quantified. The final residual contains small isolated intensity/profile mismatches but no coherent unmodeled multi-line family.
