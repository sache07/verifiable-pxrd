"""Diagnostic: add a physically screened PbO record to a saved project.

Called by the controller as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.  This is
case-specific, oracle-informed investigation code and is not package material.
"""

from pathlib import Path
import json
import sys

from GSASII import GSASIIscriptable as G2sc


input_gpx = Path(sys.argv[1])
output_gpx = Path(sys.argv[2])
massicot_cif = output_gpx.with_name("massicot_2310433.cif")
massicot_cif.write_text(
    """data_2310433
_chemical_formula_sum 'O Pb'
_space_group_IT_number 57
_symmetry_space_group_name_Hall '-P 2c 2b'
_symmetry_space_group_name_H-M 'P b c m'
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_formula_units_Z 4
_cell_length_a 5.876
_cell_length_b 5.476
_cell_length_c 4.743
loop_
_symmetry_equiv_pos_as_xyz
x,y,z
-x,-y,z+1/2
x,-y+1/2,-z
-x,y+1/2,-z+1/2
-x,-y,-z
x,y,-z-1/2
-x,y-1/2,z
x,-y-1/2,z-1/2
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_U_iso_or_equiv
O1 O -0.132 0.082 0.25 1 0.0
Pb1 Pb 0.231 0.014 0.25 1 0.0
"""
)

project = G2sc.G2Project(str(input_gpx), newgpx=str(output_gpx))
hist = project.histogram(0)
phase = project.add_phase(
    str(massicot_cif),
    phasename="PbO_massicot_screened_diagnostic",
    histograms=[hist],
    fmthint="CIF",
)
hap = phase.data["Histograms"][hist.name]
hap["Scale"][:] = [0.05, True]
hap["Size"][0] = "isotropic"
hap["Size"][1][0] = 1.0
hap["Size"][2][0] = False
hap["Mustrain"][0] = "isotropic"
hap["Mustrain"][1][0] = 0.0
hap["Mustrain"][2][0] = False

# Refit all phase scales after changing the inventory.  Existing saved flags
# are deliberately retained so the original model can reconverge around it.
for existing in project.phases():
    existing.data["Histograms"][hist.name]["Scale"][1] = True

pid = phase.id
hid = hist.id
project.set_Controls("cycles", 8)
project.set_Controls("parmMin", 1e-8, variable=f"{pid}:{hid}:Scale")
project.set_Controls("parmMax", 100.0, variable=f"{pid}:{hid}:Scale")
project.save()
project.refine(makeBack=False)

# Permit the screened record to adapt to the observed peak positions, then
# fit one conservative isotropic width term and reconverge once more.
phase.data["General"]["Cell"][0] = True
project.refine(makeBack=False)
phase.set_HAP_refinements(
    {"Mustrain": {"type": "isotropic", "refine": True}}, [hist]
)
project.set_Controls("parmMin", 0.0, variable=f"{pid}:{hid}:Mustrain;i")
project.set_Controls("parmMax", 30000.0, variable=f"{pid}:{hid}:Mustrain;i")
project.refine(makeBack=False)
project.save()

denominator = sum(
    p.data["Histograms"][hist.name]["Scale"][0] * p.data["General"]["Mass"]
    for p in project.phases()
)
fractions = {
    p.name: (
        p.data["Histograms"][hist.name]["Scale"][0]
        * p.data["General"]["Mass"]
        / denominator
    )
    for p in project.phases()
}
print(
    "DIAGNOSTIC",
    json.dumps(
        {
            "Rwp": hist.data["data"][0].get("wR"),
            "fractions": fractions,
            "massicot_cell": phase.get_cell(),
            "massicot_mustrain": hap["Mustrain"][1][0],
            "frozen": project.get_Frozen(),
        },
        sort_keys=True,
    ),
)
