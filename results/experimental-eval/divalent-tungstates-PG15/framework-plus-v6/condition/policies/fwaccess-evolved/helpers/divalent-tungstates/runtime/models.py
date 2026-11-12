"""Explicit synthetic-reference conventions; never applied to solver submissions."""
from pathlib import Path
from pymatgen.io.cif import CifWriter

def write_synthetic_model(structure,path,symprec=.001):
    structure=structure.copy()
    structure.remove_oxidation_states()
    for i,site in enumerate(structure):
        site.label=f'{site.species_string}{i}'
    writer=CifWriter(structure,symprec=symprec,significant_figures=10)
    tag='_atom_site_U_iso_or_equiv'
    for block in writer.cif_file.data.values():
        block.data[tag]=['0.0050000000']*len(block.data['_atom_site_label'])
        loop=next(loop for loop in block.loops if '_atom_site_label' in loop)
        if tag not in loop:loop.append(tag)
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(str(writer)+'\n')
