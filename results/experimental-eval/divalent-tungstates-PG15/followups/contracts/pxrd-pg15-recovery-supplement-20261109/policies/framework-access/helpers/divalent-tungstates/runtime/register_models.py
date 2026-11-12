"""Register curator-chosen CIFs without selecting chemistry or prototypes."""
from pathlib import Path
import argparse,json,re,shutil,warnings
import numpy as np
from pymatgen.io.cif import CifParser
from physics import save_json,sha
from models import write_synthetic_model

def register(manifest,out):
    data=json.loads(manifest.read_text())
    if data.get('schema_version')!=1 or not data.get('records'):
        raise ValueError('sources.json needs schema_version 1 and nonempty records')
    if out.exists():raise ValueError('Choose a new pool directory; existing pools are not overwritten')
    prepared=[];ids=set()
    for row in data['records']:
        ident=row['id']
        if not isinstance(ident,str) or not re.fullmatch('[a-z][a-z0-9_-]{0,79}',ident) or ident in ids:
            raise ValueError('invalid or duplicate model ID')
        ids.add(ident)
        if not row.get('provenance') or not row.get('lineage_group'):
            raise ValueError('provenance and lineage_group are required')
        if row.get('model_basis') not in ['published','repaired','analogue_derived','perturbed']:
            raise ValueError('model_basis must describe the actual source/construction')
        if row['model_basis']!='published' and (not row.get('parent_ids') or not row.get('transformation')):
            raise ValueError('constructed/repaired models require parent_ids and transformation')
        source=(manifest.parent/row['cif_path']).resolve()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            parser=CifParser(source,occupancy_tolerance=1.,site_tolerance=1e-5,frac_tolerance=0)
            structures=parser.parse_structures(primitive=False,on_error='raise')
        if len(structures)!=1:raise ValueError('Each selected CIF must contain one structural model')
        st=structures[0];st.remove_oxidation_states()
        if not 1<=len(st)<=2000 or not .5<float(st.density)<30:
            raise ValueError('Model outside broad size/density screen: '+ident)
        if any(site.species.num_atoms>1.0001 for site in st):raise ValueError('Overoccupied site: '+ident)
        distance=st.distance_matrix.copy();np.fill_diagonal(distance,np.inf)
        nearest=float(np.min(distance)) if len(st)>1 else min(st.lattice.abc)
        if nearest<.8:raise ValueError('Interatomic separation below 0.8 A: '+ident)
        block=next(iter(parser.as_dict().values()))
        prepared.append((row,source,st,[str(w.message) for w in caught],block,nearest))
    records=[]
    for row,source,st,notes,block,nearest in prepared:
        ident=row['id'];model=out/'models'/f'{ident}.cif';original=out/'sources'/f'{ident}.cif'
        original.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,original)
        write_synthetic_model(st,model)
        composition=st.composition.reduced_composition.get_el_amt_dict()
        key='|'.join(f'{e}:{v:.6f}' for e,v in sorted(st.composition.fractional_composition.get_el_amt_dict().items()))
        records.append({**row,'formula':st.composition.reduced_formula,'composition':composition,
            'composition_key':key,'chemical_system':'-'.join(sorted(composition)),
            'role':row.get('role','candidate'),'model_path':str(model.relative_to(out)),
            'source_path':str(original.relative_to(out)),'source_sha256':sha(original),'model_sha256':sha(model),
            'source_conditions':{k:str(v) for k,v in block.items() if k in ['_publ_section_title','_journal_paper_doi','_journal_year','_chemical_formula_sum','_diffrn_ambient_pressure','_diffrn_ambient_temperature','_cell_measurement_temperature']},
            'sites':len(st),'ordered':st.is_ordered,'density_g_cm3':float(st.density),
            'minimum_separation_A':nearest,'parsing_warnings':notes,
            'normalization':'neutral elements, symmetry tolerance 0.001 A, Uiso=0.005 A^2; occupied composition is used for synthetic truth',
            'validation_scope':'Parsing and broad geometry only; chemistry, complete-compound identity, compatibility, and feasibility require curator review. GSAS consistency checked at generation.'})
    result={'schema_version':1,'source_manifest_sha256':sha(manifest),'registration_code_sha256':sha(Path(__file__)),
            'selection_author':'curator','records':records}
    save_json(out/'catalog.json',result)
    return {'registered_models':len(records),'catalog':str(out/'catalog.json'),'catalog_sha256':sha(out/'catalog.json')}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path)
    p.add_argument('--out',type=Path,default=Path('outputs/pool'));a=p.parse_args()
    print(json.dumps(register(a.manifest.resolve(),a.out.resolve()),indent=2))

if __name__=='__main__':main()
