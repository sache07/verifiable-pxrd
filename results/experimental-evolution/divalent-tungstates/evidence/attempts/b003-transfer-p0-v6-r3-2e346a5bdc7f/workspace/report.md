# Crystalline phase analysis

## Result

Three crystalline phases are required. Weight fractions are normalized over these modeled crystalline phases:

| Phase | Structural model | Refined cell (Å, °) | Weight fraction |
|---|---|---|---:|
| NiWO₄ | Wolframite, *P*2/*c* (No. 13) | *a*=4.59947, *b*=5.66282, *c*=4.91138, β=90.5018 | 59.68 wt% |
| WO₃ | Monoclinic γ-WO₃, *P*2₁/*c* (No. 14) | *a*=7.68230, *b*=7.54469, *c*=10.50837, β=136.0244 | 30.03 wt% |
| NiO | Rocksalt, *Fm*3̄*m* (No. 225) | *a*=4.16504 | 10.30 wt% |

The full 9.903–100.095° 2θ range gives Rwp=1.6143%, Rp=1.2602%, Rexp=1.4476%, and GOF=1.1177 using Poisson counting weights because pointwise uncertainties were not supplied.

## Evidence and model selection

The precursor context (WO₃ + NiO, 700 °C) makes Ni–W–O phases and unreacted oxides chemically plausible. A NiWO₄-only model left strong coherent residual families (Rwp about 23.6%). Adding monoclinic WO₃ reduced Rwp to about 7.33%, and adding NiO reduced the physically neutral baseline to about 4.15% before structural and intensity corrections. No coherent family remains that requires a fourth crystalline phase.

- **NiWO₄:** 137 calculated reflections account for the dominant pattern. The exact-composition COD record 5910277 had the correct wolframite chemistry/cell but an incomplete oxygen list, so it was not used uncritically. The missing site was reconstructed after screening *P*2/*c* wolframite analogues with `learned/stoichiometric_analogues.py` (including ZnWO₄ COD 1520641, FeWO₄ 1567215/9008124, MnWO₄ 1520200, and MgWO₄ 9013902). All sites are fully occupied and ordered. Refined octahedral distances are Ni–O 2.041–2.117 Å and W–O 1.783–2.102 Å.
- **WO₃:** the ambient monoclinic neutron model COD 2311041 (*P*2₁/*c*, an unconventional but equivalent β≈136° cell) consistently fit better than room-temperature COD 1528915 and triclinic COD 2106293 under the same nuisance model. Its two W sites retain physical distorted octahedra, W–O 1.710–2.164 Å. W1 coordinates and both W isotropic ADPs were supported; oxygen coordinates were retained from the neutron model.
- **NiO:** the six rocksalt families at 37.35, 43.40, 63.06, 75.65, 79.66, and 95.41° require COD 1010093-type NiO. A modest [111] March–Dollase term, 0.8466(66), improved multiple families, especially the isolated 200 and largely isolated 220 peaks. Competing cubic axes were unsupported or unstable.

## Refinement controls

The Cu Kα1/Kα2 wavelengths and 0.5 intensity ratio were fixed to the metadata. The accepted common profile uses a smooth six-term Chebyshev background, one zero correction [−0.0195(5)°], nonnegative U/W/X terms, SH/L=0.0100(7), and refined polarization 0.8820(19). Its calculated FWHM rises smoothly from about 0.165° at low angle to 0.206° at 95°. Repeated low-angle asymmetry supports SH/L despite its correlation with zero.

Roughness returned to its neutral bound after polarization was introduced. Isotropic strain collapsed to zero for all phases; NiWO₄ and NiO size went to the neutral large-size limit. A nominal WO₃ size near 6 µm changed Rwp by only 0.0005 percentage point and was pruned as practically unresolved. H-strain, extinction, Babinet terms, and texture for NiWO₄/WO₃ are neutral. The final project was saved, reopened, and replayed over the complete measured range; the last maximum shift/esd was 0.014 and repeated Rwp values were 1.61419–1.61426%.

## Remaining uncertainty

The covariance-only fraction uncertainties are about 0.03 wt%-point, but they do not include structure-source, profile, overlap, preferred-orientation, or weighting uncertainty. Model challenges moved the major-phase fractions by up to roughly 0.7 wt%-point, so about ±1 wt%-point for NiWO₄/WO₃ and ±0.5 wt%-point for NiO is a more realistic precision from the tested models. Unknown particle size prevents a defensible microabsorption correction; if the W-rich and NiO particles are coarse, that unquantified bias could be larger.

These are relative crystalline fractions. Absolute fractions including amorphous material cannot be determined without an internal standard, and trace, poorly crystalline, or nanocrystalline material cannot be excluded. The WO₃ oxygen coordinates and oxygen ADPs cannot be determined reliably from this W-dominated laboratory X-ray pattern; the coordinates come from the neutron parent and O Uiso was fixed at 0.008 Å². The NiO texture correction is supported by several families but remains based on only six reflections, making its fraction slightly more model-dependent than the counting-statistical esd suggests.
