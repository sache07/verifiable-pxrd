# Powder XRD phase analysis

## Result

The crystalline specimen is modeled as wolframite-type NiWO4 plus unreacted monoclinic WO3.

| Phase | Space group | Refined cell | Crystalline weight fraction |
|---|---|---|---:|
| NiWO4 | P 2/c | a = 4.59966 Å, b = 5.66204 Å, c = 4.90939 Å, beta = 89.9806° | 0.75768 (75.77 wt%) |
| WO3 | P 21/c | a = 7.30154 Å, b = 7.53227 Å, c = 10.52673 Å, beta = 133.0938° | 0.24232 (24.23 wt%) |

Fractions are normalized only over the modeled crystalline phases. The full 10.0094–99.9944° 2theta grid gives Rwp = 4.1246%, Rp = 3.1834%, Rexp = 3.4788%, and goodness of fit = 1.1879 (8,282 observations, 32 refined parameters).

## Evidence and model selection

The NiWO4 model accounts for the strong families near 30.85°, 36.49°, 52.27°, and 54.54–54.58° 2theta. It was initialized from an intact P 2/c wolframite analogue (ZnWO4, COD 1520641), changed to NiWO4, and refined. The resulting octahedra are physical: Ni–O = 2.019–2.052 Å and W–O = 1.845–2.168 Å.

The split WO3 family at approximately 23.03°, 23.52°, and 24.28° and its higher-angle families require the room-temperature monoclinic P 21/c phase. A physical neutron-derived model (COD 2311041) was retained. A triclinic WO3 checkpoint fit appreciably worse, while another nominally monoclinic database model was rejected because it contained 1.58 Å O–O contacts. The accepted WO3 model has W–O = 1.744–2.163 Å and no short nonbonded contacts.

Crystalline NiO was tested explicitly. Its scale refined to the zero bound, and its strongest expected family near 43.3° is absent. Preferred-orientation screens on five axes for each accepted phase refined to essentially random orientation (March–Dollase 0.995–1.007), so texture was not retained. No coherent residual reflection family remains that warrants another crystalline phase.

## Remaining uncertainty

The formal GSAS-II fraction uncertainty is about 0.09 wt%, but it excludes model choice and profile correlations. Acceptable physical checkpoints varied the NiWO4 fraction from roughly 75.0 to 76.2 wt%; about ±1 wt% is a more realistic uncertainty for the crystalline fractions. Amorphous material and trace phases below the pattern's detection limit are not quantified.

NiWO4 oxygen coordinates moved by at most about 0.08 Å from the analogue and remain chemically ordinary, but they are less certain than the cell and heavy-atom substructure. WO3 oxygen refinement was numerically unstable, did not improve Rwp, and produced excessive shifts; those oxygen positions therefore remain reference-based and are not independently determined by this laboratory X-ray pattern. The refined zero offset and axial-divergence term are strongly correlated (97.5%), so their individual physical interpretation is also uncertain, although the complete saved model replays the reported profile and fractions.
