"""Make a small symmetry-preserving reference variant for parameter recovery.

This prepares a synthetic target, not a prediction of a new stable material.
Keep the original parent in the worker database when testing refinement.
"""
from pathlib import Path
import argparse
import json
import sys
import numpy as np
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.cif import CifWriter


def perturb(structure, seed, max_cell_strain=.005, position_rms_A=.02, exact=False, rms_by_element=None):
    """exact=True gives the requested maximum principal strain and coordinate RMS themselves, not bounds.
    rms_by_element overrides the coordinate RMS for named elements (for example a larger value for O)."""
    rms_by_element = dict(rms_by_element or {})
    if not 0 <= max_cell_strain <= .005 or not all(0 <= v <= .08 for v in [position_rms_A, *rms_by_element.values()]):
        raise ValueError('Use cell strain <=0.005 and coordinate RMS <=0.08 A')
    target = lambda element: rms_by_element.get(element, position_rms_A)
    analyzer = SpacegroupAnalyzer(structure, symprec=.001)
    operations = analyzer.get_symmetry_operations(cartesian=False)
    A = structure.lattice.matrix.T
    invA = np.linalg.inv(A)
    rng = np.random.default_rng(seed)
    strain = rng.normal(size=(3,3)); strain = (strain+strain.T)/2
    rotations = [A@op.rotation_matrix@invA for op in operations]
    strain = np.mean([q@strain@q.T for q in rotations], axis=0)
    length = np.max(np.abs(np.linalg.eigvalsh(strain)))
    strain *= (1. if exact else rng.uniform(.2,1))*max_cell_strain/max(length,1e-15)
    lattice = Lattice(((np.eye(3)+strain)@A).T)
    coords = structure.frac_coords.copy()
    groups = analyzer.get_symmetrized_structure().equivalent_indices
    element_of = lambda i: next(iter(structure[i].species.get_el_amt_dict()))
    for group in groups:
        i = group[0]; origin = structure.frac_coords[i]; scale = target(element_of(i))
        stabilizers = [op for op in operations if structure.lattice.get_distance_and_image(origin,op.operate(origin))[0] < .002]
        displacement = invA@rng.normal(scale=scale/np.sqrt(3),size=3)
        displacement = np.mean([op.rotation_matrix@displacement for op in stabilizers],axis=0)
        # Prevent a rare Gaussian tail from creating a large coordinate change.
        distance = np.linalg.norm(A@displacement)
        displacement *= min(1., max(.05, 2.5*scale)/max(distance,1e-15))
        for j in group:
            matches = [op for op in operations if structure.lattice.get_distance_and_image(structure.frac_coords[j],op.operate(origin))[0] < .002]
            if not matches:
                raise ValueError('Unable to preserve symmetry correspondence')
            coords[j] = (structure.frac_coords[j]+matches[0].rotation_matrix@displacement)%1
    deltas = coords-structure.frac_coords
    deltas -= np.rint(deltas)
    # Uniform rescaling within each element preserves all symmetry relations
    # (symmetry groups are single-element) while enforcing that element's
    # requested aggregate RMS as a bound, or exactly in exact mode.
    elements = np.array([element_of(i) for i in range(len(structure))])
    for element in sorted(set(elements)):
        mask = elements == element
        rms = np.sqrt(np.mean(np.sum((deltas[mask]@structure.lattice.matrix)**2,axis=1)))
        if rms > 0 and (exact or rms > target(element)):
            deltas[mask] *= target(element)/rms
    coords = (structure.frac_coords+deltas)%1
    result = Structure(lattice,structure.species,coords,site_properties=structure.site_properties)
    if SpacegroupAnalyzer(result,symprec=.001).get_space_group_number() != analyzer.get_space_group_number():
        raise ValueError('Perturbation changed detected symmetry; select another seed')
    if result.composition != structure.composition:
        raise ValueError('Perturbation changed occupied composition')
    distances = result.distance_matrix.copy();np.fill_diagonal(distances,np.inf)
    if len(result)>1 and float(distances.min()) < .8:
        raise ValueError('Perturbation creates a hard short contact')
    moved = np.array([structure.lattice.get_distance_and_image(a,b)[0] for a,b in zip(structure.frac_coords,coords)])
    return result, {'space_group_number':analyzer.get_space_group_number(),
                    'strain_tensor':strain.tolist(), 'maximum_cell_strain':float(np.max(np.abs(np.linalg.eigvalsh(strain)))),
                    'coordinate_rms_A':float(np.sqrt(np.mean(moved**2))),
                    'coordinate_rms_by_element_A':{e:float(np.sqrt(np.mean(moved[elements==e]**2))) for e in sorted(set(elements))},
                    'scope':'Synthetic parameter-recovery variant; physical screen and curator chemical review still required.'}


STATUS = ['pass', 'needs_adjudication', 'fail']


def screen_status(structure):
    """The scorer's physical-screen status, with its rules and scorer/config.json thresholds. Not imported:
    the controller imports the generator, and the scorer's module names would collide with its own."""
    limits = json.loads((Path(__file__).resolve().parents[1]/'scorer/config.json').read_text())['physical_screen']
    hard, oxygen = limits['hard_contact_A'], limits['oxide_oxygen_contact_review_A']
    status = 0
    for i, j, image, dist in zip(*structure.get_neighbor_list(max(hard, oxygen))):
        if i > j or (i == j and tuple(image) <= (0, 0, 0)):
            continue
        a, b = structure[int(i)], structure[int(j)]
        if dist < hard:
            status = max(status, 1 if a.species.num_atoms < .9999 or b.species.num_atoms < .9999 else 2)
        elif dist < oxygen and set(a.species.get_el_amt_dict()) == set(b.species.get_el_amt_dict()) == {'O'}:
            status = max(status, 1)
    if any(s.species.num_atoms > 1.0001 or any(v < 0 for v in s.species.values()) for s in structure):
        status = 2
    return STATUS[status]


def mismatch_model(source, destination, cell_strain, position_rms_A, seed, attempts=20, rms_by_element=None):
    """One case's true structure for LAB.md's reference_mismatch: the registered model with exactly this
    maximum principal cell strain and coordinate RMS (per element where given). A draw the physical
    screen rates worse than the parent is redrawn from the next seed."""
    from pymatgen.io.cif import CifParser
    from models import write_synthetic_model
    parent = CifParser(source,occupancy_tolerance=1.,site_tolerance=1e-5,frac_tolerance=0).parse_structures(primitive=False,on_error='raise')[0]
    parent.remove_oxidation_states()
    allowed = STATUS.index(screen_status(parent))
    for attempt in range(attempts):
        try:
            model, record = perturb(parent, seed+attempt, cell_strain, position_rms_A, exact=True, rms_by_element=rms_by_element)
        except ValueError:
            continue  # symmetry change or hard contact for this draw
        status = screen_status(model)
        if STATUS.index(status) <= allowed:
            write_synthetic_model(model, destination)
            return {**record, 'requested_cell_strain':cell_strain, 'requested_position_rms_A':position_rms_A,
                    'requested_position_rms_A_by_element':dict(rms_by_element or {}),
                    'seed':seed+attempt, 'attempts':attempt+1, 'physical_status':status}
    raise ValueError('No reference-mismatch draw keeps the physical screen of '+str(source))


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--seed',type=int,required=True)
    p.add_argument('--cell-strain',type=float,default=.003)
    p.add_argument('--position-rms',type=float,default=.02)
    args=p.parse_args()
    model,record=perturb(Structure.from_file(args.source,primitive=False),args.seed,args.cell_strain,args.position_rms)
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scorer/src'))
    from structure_metrics import physical_screen
    physical=physical_screen(model)
    if physical['status']!='pass':
        raise ValueError('Variant needs physical review: '+json.dumps(physical))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    CifWriter(model,symprec=.001,significant_figures=10).write_file(args.output)
    from hashlib import sha256
    record.update(source=str(args.source.resolve()),
                  source_sha256=sha256(args.source.read_bytes()).hexdigest(),
                  output_sha256=sha256(args.output.read_bytes()).hexdigest(),
                  seed=args.seed,physical=physical)
    args.output.with_suffix('.provenance.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
