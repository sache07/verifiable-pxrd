# Powder XRD phase analysis

The scan is modeled by three crystalline phases. Weight fractions are normalized over these modeled crystalline phases only:

| Phase | Structural model | Weight fraction |
|---|---|---:|
| ZnWO4 | wolframite, P 2/c | 0.84110 ± 0.00146 |
| WO3 | monoclinic, P 21/c | 0.11085 ± 0.00087 |
| ZnO | wurtzite, P 63 m c | 0.04805 ± 0.00126 |

The quoted uncertainties are formal scale-factor ESDs from the final refinement. They do not include model-choice, overlap, preferred-orientation, or amorphous-content uncertainty.

## Evidence and model selection

The dominant reflection family is wolframite-type ZnWO4, consistent with reaction of the stated ZnO and WO3 precursors at 700 °C. The frozen reference index contains no exact O-W-Zn entry, so the P 2/c model was built from the isostructural CoMoO4-II wolframite framework (COD 7205001), with Co→Zn and Mo→W substitution. Its cell and the W/Zn positional degrees of freedom were refined. A [111] March-Dollase term (ratio 0.704) is strongly supported; alternative tested axes returned to unity or gave negligible improvement.

Residual families identify unreacted monoclinic WO3 and minor wurtzite ZnO. The accepted WO3 model is the physically sound neutron structure COD 2311041. A competing historical WO3 model gave only a marginal early profile improvement but an implausible 1.58 Å O-O contact, so it was rejected. ZnO uses COD 9004178 and has a stable positive scale supported by multiple reflections. No coherent unassigned reflection family remains; the largest residuals are centered on reflections of accepted phases.

The final structures pass distance checks: minimum W-O is 1.785 Å in ZnWO4, minimum W-O is 1.714 Å in WO3, and minimum Zn-O is 1.980 Å in ZnO, with no catastrophic contacts. A fresh zero-parameter GSAS-II replay of `final.gpx` over all 8301 measured points gives Rwp = 10.4759%, Rp = 5.8888%, and weighted chi-square = 130074.25. The Rwp stored for the refinement interval is 10.4848%.

## Remaining uncertainty

ZnWO4 phase identity and wolframite topology are well supported, but its oxygen coordinates could not be refined reliably: bounded oxygen branches hit limits and were rolled back, so those sites remain analogue-derived. The submitted CIF should not be interpreted as a high-precision single-crystal determination. WO3 topology is reliable, while its light-atom coordinates are primarily reference-derived. The minor, broadened ZnO fraction is more sensitive to profile overlap than its formal ESD suggests. A conservative systematic uncertainty is therefore larger than the tabulated formal errors, especially for ZnO.

The fitted angular zero is an effective correction and is highly correlated with specimen displacement; those contributions cannot be separated reliably from this scan. Possible amorphous material is not quantified, so the reported fractions must not be interpreted as absolute whole-specimen mass fractions.
