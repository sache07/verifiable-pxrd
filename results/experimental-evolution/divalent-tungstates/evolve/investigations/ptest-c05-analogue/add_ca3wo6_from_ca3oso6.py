"""Diagnostic: adapt the nearest Ca3OsO6 framework by Os -> W.

Called by the controller as SCRIPT INPUT.gpx OUTPUT.gpx INPUTS_DIR.  The
specific parent and substitution are oracle-informed investigation inputs and
must not be shipped in a reusable package.
"""

from pathlib import Path
import json
import sys

from GSASII import GSASIIscriptable as G2sc


source = Path(sys.argv[1])
destination = Path(sys.argv[2])
candidate_cif = destination.with_name("ca3wo6_from_ca3oso6.cif")
candidate_cif.write_text(
    """data_Ca3WO6_from_Ca3OsO6_diagnostic
_chemical_formula_sum 'Ca3 O6 W'
_space_group_IT_number 14
_space_group_name_Hall '-P 2yn'
_space_group_name_H-M_alt 'P 1 21/n 1'
_symmetry_space_group_name_H-M 'P 1 21/n 1'
_cell_angle_alpha 90
_cell_angle_beta 90.020
_cell_angle_gamma 90
_cell_formula_units_Z 2
_cell_length_a 5.5403
_cell_length_b 5.8049
_cell_length_c 7.9761
loop_
_symmetry_equiv_pos_as_xyz
'x, y, z'
'-x+1/2, y+1/2, -z+1/2'
'-x, -y, -z'
'x-1/2, -y-1/2, z-1/2'
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ca1 Ca 0.51316 0.5584 0.74598 0.01289 1
Ca2 Ca 0.5000 1.0000 0.5000 0.00914 1
W1 W 0.5000 0.0000 0.0000 0.00647 1
O1 O 0.2159 0.1778 0.0510 0.0167 1
O2 O 0.3304 0.7229 0.0665 0.0174 1
O3 O 0.3893 0.9491 0.7733 0.0162 1
"""
)

project = G2sc.G2Project(str(source), newgpx=str(destination))
hist = project.histogram(0)
phase = project.add_phase(
    str(candidate_cif),
    phasename="Ca3WO6_from_framework_analogue_diagnostic",
    histograms=[hist],
    fmthint="CIF",
)
hap = phase.data["Histograms"][hist.name]

# Start at a modest trial abundance relative to the saved crystalline model;
# this is only an optimizer initialization, not a submitted fraction.
existing_mass = sum(
    p.data["Histograms"][hist.name]["Scale"][0] * p.data["General"]["Mass"]
    for p in project.phases()
    if p.id != phase.id
)
hap["Scale"][:] = [0.08 / 0.92 * existing_mass / phase.data["General"]["Mass"], True]
hap["Size"][0] = "isotropic"
hap["Size"][1][0] = 1.0
hap["Size"][2][0] = False
hap["Mustrain"][0] = "isotropic"
hap["Mustrain"][1][0] = 0.0
hap["Mustrain"][2][0] = False
for existing in project.phases():
    existing.data["Histograms"][hist.name]["Scale"][1] = True

pid, hid = phase.id, hist.id
project.set_Controls("cycles", 12)
project.set_Controls("parmMin", 1e-8, variable=f"{pid}:{hid}:Scale")
project.set_Controls("parmMax", 1000.0, variable=f"{pid}:{hid}:Scale")
project.save()
project.refine(makeBack=False)

# Refine the analogue's metric before one conservative width term.
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
    p.name: p.data["Histograms"][hist.name]["Scale"][0]
    * p.data["General"]["Mass"]
    / denominator
    for p in project.phases()
}
print(
    "DIAGNOSTIC",
    json.dumps(
        {
            "Rwp": hist.data["data"][0].get("wR"),
            "fractions": fractions,
            "analogue_cell": phase.get_cell(),
            "analogue_mustrain": hap["Mustrain"][1][0],
            "frozen": project.get_Frozen(),
        },
        sort_keys=True,
    ),
)
