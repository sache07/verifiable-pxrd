"""List a structure's isostructural relatives in the frozen reference library, to choose what a withheld case hides.

python ../runtime/library_neighbours.py MODEL.cif [--withhold ID,ID,...] [--max-sites 80] [--stol 0.3] [--out neighbours.json]

Every library entry whose reduced formula has the same number of atoms and the same anion count as
the model is compared with pymatgen's StructureMatcher, lattice scaled and element identities
ignored, so relatives are found by atomic arrangement rather than by formula pattern: an ordered
double perovskite A2BB'O6 is a relative of A3BO6, and a tellurate or sulfate is a relative of the
corresponding tungstate. For each entry whose framework matches, the tool maps its sites onto the
model's and reports:
  substitutions   the distinct element changes needed on the matched sites, e.g. ["Te->W"]; a
                  cation change and an anion change each count once
  tier            0 same composition (a polymorph or another setting); 1 one substitution;
                  2 two substitutions. Relatives needing more than two are reported only as a
                  count, as are entries whose framework does not match.
  framework_rms   normalized rms site displacement after lattice scaling; loose_match marks values
                  above 0.2, near the matcher's tolerance
  cell_mismatch   largest relative difference of the lattice lengths in the model's setting, in %,
                  which is what a solver adapting the relative must refine across
With --withhold, the listed COD IDs are marked withheld and the summary names the nearest relative
that still survives and the tier the case therefore has; "none" means no relative within two
substitutions remains. Nothing here is hidden from the researcher; the solver never sees this output.
"""
from pathlib import Path
import argparse
import gzip
import json
import math
import warnings

HERE = Path(__file__).resolve().parent
INDEX = Path('<HOME>/.local/share/characterizagent/backends/dara/venv/lib/python3.11/site-packages/dara/data/cod_filtered_info_2024.json.gz')
CIFS = Path('<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif')
HALOGENS = {'F', 'Cl', 'Br', 'I'}


def cif_path(record_id):
    i = str(record_id)
    return CIFS / i[0] / i[1:3] / i[3:5] / (i + '.cif')


def load(path):
    from pymatgen.core import Structure
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        s = Structure.from_file(str(path), primitive=False)
    s.remove_oxidation_states()
    return s


def integer_counts(formula_or_composition):
    """Element -> integer count of the reduced formula, or None for fractional compositions."""
    from pymatgen.core import Composition
    c = formula_or_composition
    try:
        if isinstance(c, str):
            c = Composition(c)
        elif hasattr(c, 'composition'):
            c = c.composition
        counts = c.reduced_composition.get_el_amt_dict()
    except Exception:
        return None
    if any(abs(v - round(v)) > 1e-6 for v in counts.values()):
        return None
    return {e: int(round(v)) for e, v in counts.items()}


def anions_of(composition):
    """Elements that carry negative charge in the model, from an oxidation-state guess; oxygen and
    halogens when no guess exists. Te in a tellurate is therefore a cation, not an anion."""
    try:
        guesses = composition.oxi_state_guesses(max_sites=-1)
    except Exception:
        guesses = []
    if guesses:
        negative = {e for e, q in guesses[0].items() if q < 0}
        if negative:
            return negative
    elements = {str(e) for e in composition.elements}
    if 'O' in elements:
        return {'O'} | (elements & HALOGENS)
    if elements & HALOGENS:
        return elements & HALOGENS
    from pymatgen.core import Element
    return {max(elements, key=lambda e: Element(e).X)}


def framework_matcher(stol=0.3, primitive=True):
    """Same structure type regardless of chemistry: cells scaled to match, species ignored, and
    different settings or supercells handled by the matcher. The primitive-cell matcher decides the
    match; site alignment (get_s2_like_s1) needs a matcher without primitive reduction."""
    from pymatgen.analysis.structure_matcher import StructureMatcher, FrameworkComparator
    return StructureMatcher(ltol=0.2, stol=stol, angle_tol=5, primitive_cell=primitive, scale=True,
                            attempt_supercell=True, allow_subset=False, comparator=FrameworkComparator())


def site_substitutions(target, aligned):
    """Distinct element changes between the model and a relative already transformed into the model's
    setting: each model site is paired with the nearest aligned site. Returns the sorted list of
    changes like 'Sr->Ca', or None when the pairing is not one-to-one."""
    import numpy as np
    d = target.lattice.get_all_distances(target.frac_coords, aligned.frac_coords)
    nearest = d.argmin(axis=1)
    if len(set(nearest.tolist())) != len(target):
        return None
    def symbol(site):
        # Dominant element of the site; disordered sites report their majority occupant.
        return max(site.species.items(), key=lambda kv: kv[1])[0].symbol

    changes = set()
    for i, j in enumerate(nearest):
        a, b = symbol(aligned[j]), symbol(target[i])
        if a != b:
            changes.add(f'{a}->{b}')
    # An element the relative contains and the model lacks must change even where site disorder
    # hides it behind a majority occupant.
    target_elements = {e.symbol for e in target.composition.elements}
    for e in {e.symbol for e in aligned.composition.elements} - target_elements:
        if not any(ch.startswith(e + '->') for ch in changes):
            changes.add(f'{e}->?')
    return sorted(changes)


def cell_mismatch_percent(target, aligned):
    """Largest relative difference of the lattice lengths, the relative's cell in the model's setting."""
    a, b = target.lattice.abc, aligned.lattice.abc
    return round(100 * max(abs(x - y) / y for x, y in zip(b, a)), 2)


def volume_mismatch_percent(target, candidate):
    """Isotropic fallback when the relative cannot be aligned: linear mismatch from volume per atom."""
    ratio = (candidate.volume / len(candidate)) / (target.volume / len(target))
    return round(100 * abs(ratio ** (1 / 3) - 1), 2)


def formula_substitutions(target_counts, candidate_counts, anions):
    """Fallback when sites cannot be paired one-to-one: pair elements by multiplicity, anions apart."""
    def split(counts):
        return ({e: n for e, n in counts.items() if e not in anions}, {e: n for e, n in counts.items() if e in anions})
    cat_t, an_t = split(target_counts)
    cat_c, an_c = split(candidate_counts)
    changes = []
    for n in sorted({*cat_t.values(), *cat_c.values()}):
        xt = sorted(e for e, v in cat_t.items() if v == n and e not in cat_c)
        xc = sorted(e for e, v in cat_c.items() if v == n and e not in cat_t)
        changes += [f'{x}->{y}' for x, y in zip(xc, xt)]
        changes += [f'?->{y}' for y in xt[len(xc):]] + [f'{x}->?' for x in xc[len(xt):]]
    if set(an_t) != set(an_c):
        changes.append('/'.join(sorted(an_c)) + '->' + '/'.join(sorted(an_t)))
    return sorted(changes)


def tier_of(n_substitutions):
    return n_substitutions if n_substitutions <= 2 else None


def neighbours(model, withhold=(), max_sites=80, stol=0.3):
    matcher = framework_matcher(stol)
    aligner = framework_matcher(stol, primitive=False)
    target = load(model)
    tcounts = integer_counts(target)
    if tcounts is None:
        raise SystemExit('The model has fractional stoichiometry; list neighbours of its ordered parent instead')
    anions = anions_of(target.composition)
    n_atoms = sum(tcounts.values())
    n_anions = sum(v for e, v in tcounts.items() if e in anions)
    withhold = {str(i) for i in withhold}
    with gzip.open(INDEX, 'rt') as f:
        index = json.load(f)
    rows, distant, unmatched = [], 0, 0
    for system, entries in index.items():
        for formula, record_id, *_ in entries:
            counts = integer_counts(formula)
            if counts is None or sum(counts.values()) != n_atoms or max(counts.values()) != n_anions:
                continue
            path = cif_path(record_id)
            if not path.exists():
                continue
            try:
                candidate = load(path)
            except Exception:
                continue
            ccounts = integer_counts(candidate)
            if ccounts is None or len(candidate) > max_sites or sum(ccounts.values()) != n_atoms:
                continue
            try:
                rms = matcher.get_rms_dist(target, candidate)
            except Exception:
                rms = None
            if rms is None:
                unmatched += 1
                continue
            try:
                aligned = aligner.get_s2_like_s1(target, candidate)
                changes = site_substitutions(target, aligned) if aligned is not None else None
            except Exception:
                aligned, changes = None, None
            if changes is None:
                changes = formula_substitutions(tcounts, ccounts, anions)
            tier = tier_of(len(changes))
            if tier is None:
                distant += 1
                continue
            rows.append(dict(cod_id=str(record_id), formula=candidate.composition.reduced_formula,
                             chemical_system=system, space_group=candidate.get_space_group_info(symprec=1e-3)[0],
                             tier=tier, substitutions=changes, framework_rms=round(float(rms[0]), 4),
                             loose_match=bool(rms[0] > 0.2),
                             cell_mismatch_percent=(cell_mismatch_percent(target, aligned) if aligned is not None
                                                    else volume_mismatch_percent(target, candidate)),
                             withheld=str(record_id) in withhold))
    rows.sort(key=lambda r: (r['tier'], r['framework_rms'], r['cell_mismatch_percent'], r['formula']))
    survivors = [r for r in rows if not r['withheld']]
    return dict(model=str(Path(model).resolve()), formula=target.composition.reduced_formula,
                anions=sorted(anions), atoms_per_formula=n_atoms,
                matcher=dict(ltol=0.2, stol=stol, angle_tol=5, scale=True, comparator='framework'),
                tier_definition={'0': 'same composition (polymorph or other setting)', '1': 'isostructural, one substitution',
                                 '2': 'isostructural, two substitutions'},
                distant_relatives=distant, unmatched_entries=unmatched,
                withheld=sorted(withhold),
                surviving_tier=survivors[0]['tier'] if survivors else 'none',
                nearest_survivor=survivors[0] if survivors else None,
                neighbours=rows)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('model', type=Path)
    p.add_argument('--withhold', default='', help='comma-separated COD IDs the case will hide')
    p.add_argument('--max-sites', type=int, default=80)
    p.add_argument('--stol', type=float, default=0.3, help='site tolerance of the framework matcher (fraction of the mean site spacing)')
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    ids = [i.strip() for i in a.withhold.split(',') if i.strip()]
    result = neighbours(a.model, ids, a.max_sites, a.stol)
    if a.out:
        a.out.write_text(json.dumps(result, indent=1) + '\n')
    counts = {}
    for r in result['neighbours']:
        counts[r['tier']] = counts.get(r['tier'], 0) + 1
    print(json.dumps({'formula': result['formula'], 'anions': result['anions'], 'relatives_by_tier': counts,
                      'distant_relatives': result['distant_relatives'], 'unmatched_entries': result['unmatched_entries'],
                      'surviving_tier': result['surviving_tier'], 'nearest_survivor': result['nearest_survivor'],
                      'nearest': result['neighbours'][:8], 'written': str(a.out) if a.out else None}, indent=1))


if __name__ == '__main__':
    main()
