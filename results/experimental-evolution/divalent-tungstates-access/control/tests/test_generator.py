"""Offline checks of the generator: lab settings, specimen physics and solver inputs. No GSAS, SSH or model calls."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime'))
import labspec  # noqa: E402
import solver_inputs  # noqa: E402
import specimen  # noqa: E402

LAB = ROOT / 'evolve/LAB.md'
PROTOCOL = labspec.protocol(LAB) if LAB.exists() else None
GENERIC = {'generation': {'solver_inputs': {
    'pattern_columns': ['x', 'y'], 'line_ending': 'lf',
    'sample_fields': {'reagents': {'type': 'formula_list', 'items': [1, 3]},
                      'nominal_formula': {'type': 'formula', 'nullable': True},
                      'temperature_C': {'type': 'number', 'range': [20, 300]},
                      'route': {'type': 'string', 'choices': ['solution', 'solid-state']}},
    'element_sources': {'fields': ['reagents', 'nominal_formula'], 'ambient': ['O', 'H'], 'each_source_element_present': False},
    'metadata': {'reagents': '{sample.reagents}', 'route': '{sample.route}', 'instrument': {'time_s': {'per_session': [1, 2]}}}}}}


@unittest.skipIf(PROTOCOL is None, 'run from an instantiated run folder (evolve/LAB.md)')
class LabSettings(unittest.TestCase):
    def test_lab_settings_build_a_valid_protocol(self):
        specimen.effect_settings(PROTOCOL)
        self.assertEqual(PROTOCOL['lab_sha256'], labspec.sha(LAB))
        self.assertIn('sample_fields', PROTOCOL['generation']['solver_inputs'])

    def test_sample_draws_are_seeded_bounded_and_controllable(self):
        recipe = {'seed': 7, 'phases': [{'id': 'aa'}], 'domain_size_um': PROTOCOL['generation']['domain_size_um'][0]}
        self.assertEqual(specimen.realize_sample(recipe, PROTOCOL), specimen.realize_sample(dict(recipe), PROTOCOL))
        control = specimen.realize_sample(dict(recipe, specimen_control=True), PROTOCOL)
        self.assertEqual((control['shift_um'], control['surf_rough_A'], control['surf_rough_B']), (0., 0., 0.))
        rough = PROTOCOL['generation']['specimen_effects']['surface_roughness']
        if rough['enabled']:
            for seed in range(200):
                s = specimen.realize_sample({'seed': seed, 'phases': []}, PROTOCOL)
                if s['surf_rough_B'] > 0:
                    deficit = 1 - float(specimen.suortti(s['surf_rough_A'], s['surf_rough_B'], rough['deficit_reference_2theta_deg']))
                    self.assertLessEqual(deficit, rough['max_low_angle_deficit'] + 1e-12)

    def test_every_specimen_effect_can_be_switched_off(self):
        off = json.loads(json.dumps(PROTOCOL))
        off['generation']['specimen_effects'] = {k: {'enabled': False} for k in specimen.KEYS}
        specimen.effect_settings(off)
        recipe = {'seed': 3, 'phases': [{'id': 'aa'}], 'domain_size_um': off['generation']['domain_size_um'][0]}
        row = specimen.realize_specimen(recipe, off)[0]
        self.assertEqual((row['microstrain_ppm'], row['md_ratio'], row['size_um']), (0., 1., recipe['domain_size_um']))
        self.assertEqual(specimen.realize_sample(recipe, off)['shift_um'], 0.)

    def test_microstrain_anisotropy_is_seeded_bounded_and_off_in_controls(self):
        import copy
        strain = PROTOCOL['generation']['specimen_effects']['microstrain']
        aniso = strain.get('anisotropy')
        if not aniso:
            self.skipTest('lab has no microstrain anisotropy')
        lo, hi = aniso['axial_ratio']['range']
        seen = set()
        for seed in range(300):
            recipe = {'seed': seed, 'phases': [{'id': 'aa'}], 'domain_size_um': 1.0}
            row = specimen.realize_specimen(recipe, PROTOCOL)[0]
            self.assertEqual(row, specimen.realize_specimen(dict(recipe), PROTOCOL)[0])
            ratio = row['microstrain_axial_ppm'] / row['microstrain_ppm'] if row['microstrain_ppm'] else 1.
            seen.add(ratio != 1.)
            self.assertTrue(ratio == 1. or lo <= ratio <= hi)
            self.assertIn(row['microstrain_axis'], aniso['axes'] if ratio != 1. else [[0, 0, 1]])
            control = specimen.realize_specimen(dict(recipe, specimen_control=True), PROTOCOL)[0]
            self.assertEqual((control['microstrain_ppm'], control['microstrain_axial_ppm']), (0., 0.))
            self.assertEqual('microstrain_axial_ppm' in specimen.forward_spec(row), ratio != 1.)
        self.assertEqual(seen, {True, False})
        for bad in [{'axial_ratio': {'distribution': 'log_uniform', 'range': [0., 4.]}, 'axes': [[0, 0, 1]]},
                    {'axial_ratio': {'distribution': 'uniform', 'range': [0.5, 2.]}, 'axes': [[0, 0, 0]]},
                    {'axial_ratio': {'distribution': 'uniform', 'range': [0.5, 2.]}, 'axes': [[0, 0, 1]], 'extra': 1},
                    {'axes': [[0, 0, 1]]}]:
            broken = copy.deepcopy(PROTOCOL)
            broken['generation']['specimen_effects']['microstrain']['anisotropy'] = bad
            with self.assertRaises(ValueError):
                specimen.effect_settings(broken)

    def test_case_effects_do_not_change_phase_draws(self):
        off = json.loads(json.dumps(PROTOCOL))
        for k in specimen.CASE_KEYS:
            off['generation']['specimen_effects'][k] = {'enabled': False}
        recipe = {'seed': 11, 'phases': [{'id': 'aa'}, {'id': 'bb'}], 'domain_size_um': PROTOCOL['generation']['domain_size_um'][0]}
        self.assertEqual(specimen.realize_specimen(recipe, off), specimen.realize_specimen(recipe, PROTOCOL))


    def test_reference_mismatch_is_seeded_bounded_and_kept_in_controls(self):
        spec = specimen.mismatch_settings(PROTOCOL)
        recipe = {'seed': 5, 'phases': [{'id': 'aa'}, {'id': 'bb'}]}
        draws = specimen.realize_mismatch(recipe, PROTOCOL)
        self.assertEqual(draws, specimen.realize_mismatch(dict(recipe), PROTOCOL))
        self.assertEqual(draws, specimen.realize_mismatch(dict(recipe, specimen_control=True), PROTOCOL))
        if spec['enabled']:
            for seed in range(100):
                for d in specimen.realize_mismatch({'seed': seed, 'phases': [{'id': 'aa'}]}, PROTOCOL):
                    if d is None:
                        continue
                    for name in ['cell_strain', 'position_rms_A']:
                        if spec.get(name):
                            lo, hi = spec[name]['range']
                            self.assertTrue(lo <= d[name] <= hi)
        off = json.loads(json.dumps(PROTOCOL))
        off['generation']['reference_mismatch'] = {'enabled': False}
        self.assertEqual(specimen.realize_mismatch(recipe, off), [None, None])


class Withholding(unittest.TestCase):
    def recipe(self, **extra):
        return {'id': 'w-01', 'phases': [{'id': 'a', 'weight_fraction': .7}, {'id': 'b', 'weight_fraction': .3}],
                'availability': 'full', 'peak_counts': 15000, 'domain_size_um': 1.0, 'seed': 1, 'rationale': 'x',
                'sample': {}, **extra}

    def check(self, recipe):
        import generate
        catalog = {'a': {'id': 'a', 'provenance': 'COD 1520641', 'cif_path': '/x/1/52/06/1520641.cif', 'composition_key': 'k'},
                   'b': {'id': 'b', 'provenance': 'COD 2311041', 'cif_path': '/x/2/31/10/2311041.cif', 'composition_key': 'k2'}}
        # Only the availability/withholding rules are under test; stop before the lab-dependent checks.
        with patch.object(generate, 'realize_background', side_effect=StopIteration):
            try:
                generate.recipe_check(recipe, catalog, {'generation': {'max_components': 16, 'peak_counts': [15000], 'domain_size_um': [1.0]}})
            except StopIteration:
                return 'ok'

    def test_withhold_ids_rules(self):
        self.assertEqual(self.check(self.recipe()), 'ok')
        self.assertEqual(self.check(self.recipe(availability='withhold_ids', withhold_ids=['1520641', '9999999'], principal_id='a')), 'ok')
        self.assertEqual(self.check(self.recipe(availability='withhold_ids', withhold_ids=['9999999'])), 'ok')
        for bad in [dict(availability='withhold_ids'),                                   # list required
                    dict(withhold_ids=['9999999']),                                      # availability must say so
                    dict(availability='withhold_ids', withhold_ids=[]),
                    dict(availability='withhold_ids', withhold_ids=['abc']),
                    dict(availability='withhold_ids', withhold_ids=['2311041'], principal_id='a'),  # hides phase b's entry
                    dict(availability='withhold_principal_composition')]:               # needs principal_id
            with self.assertRaises(ValueError, msg=str(bad)):
                self.check(self.recipe(**bad))


class ReferenceMismatch(unittest.TestCase):
    SOURCE = Path('<HOME>/.local/share/characterizagent/backends/dara/cod-filtered-2024/cif/1/52/06/1520641.cif')

    @unittest.skipUnless(SOURCE.exists(), 'needs the frozen COD library')
    def test_exact_magnitudes_symmetry_and_registered_format(self):
        from pymatgen.core import Structure
        from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
        from models import write_synthetic_model
        from perturb_model import mismatch_model
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / 'parent.cif'
            write_synthetic_model(Structure.from_file(self.SOURCE), parent)
            a, b = Path(tmp) / 'a.cif', Path(tmp) / 'b.cif'
            record = mismatch_model(parent, a, 0.002, 0.01, 17)
            mismatch_model(parent, b, 0.002, 0.01, 17)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertAlmostEqual(record['maximum_cell_strain'], 0.002, places=9)
            self.assertAlmostEqual(record['coordinate_rms_A'], 0.01, places=4)
            c = Path(tmp) / 'c.cif'
            per = mismatch_model(parent, c, 0.002, 0.01, 17, rms_by_element={'O': 0.04})['coordinate_rms_by_element_A']
            self.assertAlmostEqual(per['O'], 0.04, places=4)
            self.assertTrue(all(abs(v - 0.01) < 1e-4 for e, v in per.items() if e != 'O'))
            p, m = Structure.from_file(parent), Structure.from_file(a)
            self.assertEqual(SpacegroupAnalyzer(p, symprec=.001).get_space_group_number(),
                             SpacegroupAnalyzer(m, symprec=.001).get_space_group_number())
            self.assertEqual(p.composition, m.composition)
            self.assertNotAlmostEqual(p.lattice.volume, m.lattice.volume, places=3)
            self.assertIn('_atom_site_U_iso_or_equiv', a.read_text())

    def test_settings_validation(self):
        good = {'generation': {'reference_mismatch': {'enabled': True, 'probability': 1.,
                'cell_strain': {'distribution': 'log_uniform', 'range': [0.0005, 0.004]}}}}
        specimen.mismatch_settings(good)
        specimen.mismatch_settings({'generation': {'reference_mismatch': {'enabled': True,
                'position_rms_A': {'distribution': 'log_uniform', 'range': [0.005, 0.02]},
                'position_rms_A_by_element': {'O': {'distribution': 'log_uniform', 'range': [0.01, 0.05]}}}}})
        for bad in [{'cell_strain': {'distribution': 'log_uniform', 'range': [0.001, 0.01]}},
                    {'cell_strain': {'distribution': 'normal', 'range': [0.001, 0.002]}},
                    {'position_rms_A': {'distribution': 'uniform', 'range': [0.01, 0.1]}},
                    {'position_rms_A_by_element': {'O': {'distribution': 'uniform', 'range': [0.01, 0.03]}}},
                    {'position_rms_A': {'distribution': 'uniform', 'range': [0.01, 0.02]},
                     'position_rms_A_by_element': {'o': {'distribution': 'uniform', 'range': [0.01, 0.03]}}},
                    {}]:
            with self.assertRaises(ValueError):
                specimen.mismatch_settings({'generation': {'reference_mismatch': {'enabled': True, **bad}}})


class Physics(unittest.TestCase):
    def test_gsas_conventions(self):
        self.assertAlmostEqual(float(specimen.suortti(0.3, 0.2, 180.)), 1.0)
        self.assertLess(float(specimen.suortti(0.3, 0.2, 20.)), 1.0)
        self.assertAlmostEqual(float(specimen.displacement_shift_deg(100., 0.)), -0.0573, places=4)


class LabFile(unittest.TestCase):
    def lab(self, block):
        d = tempfile.mkdtemp()
        p = Path(d) / 'LAB.md'
        p.write_text('# Lab\n\nText.\n\n```json lab-settings\n' + block + '\n```\n')
        return p

    def test_requires_exactly_one_block_and_known_fields(self):
        empty = Path(tempfile.mkdtemp()) / 'LAB.md'
        empty.write_text('# Lab\n\nNo settings here.\n')
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            labspec.settings(empty)
        p = self.lab('{"schema": "pxrd-lab-settings/1", "lab_id": "x", "measurement": {}, "specimen": {}, "solver_inputs": {}, "extra": 1}')
        with self.assertRaisesRegex(ValueError, 'Unknown lab settings fields: extra'):
            labspec.settings(p)
        p = self.lab('{"schema": "pxrd-lab-settings/1", "lab_id": "x", "measurement": {}, "specimen": {}, "solver_inputs": {}}')
        with self.assertRaisesRegex(ValueError, 'Missing measurement fields'):
            labspec.settings(p)


class SampleFields(unittest.TestCase):
    rows = [{'composition': {'Pb': 1, 'I': 2}}, {'composition': {'C': 4, 'H': 12, 'N': 1, 'I': 1}}]

    def recipe(self, **kw):
        sample = {'reagents': ['PbI2', 'C4H12NI'], 'nominal_formula': None, 'temperature_C': 100, 'route': 'solution'}
        sample.update(kw)
        return {'id': 'x', 'measurement_session': 's', 'sample': sample}

    def test_generic_fields_types_and_elements(self):
        values, allowed = solver_inputs.check_sample(self.recipe(), self.rows, GENERIC)
        self.assertEqual(allowed, ['C', 'H', 'I', 'N', 'O', 'Pb'])
        self.assertEqual(values['temperature_C'], 100.0)
        for bad in [dict(route='melt'), dict(temperature_C=500), dict(reagents=[]), dict(reagents=['PbI2', 'Qq3']), dict(temperature_C=None)]:
            with self.assertRaises(ValueError):
                solver_inputs.check_sample(self.recipe(**bad), self.rows, GENERIC)
        with self.assertRaisesRegex(ValueError, 'does not supply'):
            solver_inputs.check_sample(self.recipe(), self.rows + [{'composition': {'Sn': 1, 'I': 2}}], GENERIC)

    def test_each_source_element_present_when_required(self):
        strict = json.loads(json.dumps(GENERIC))
        strict['generation']['solver_inputs']['element_sources']['each_source_element_present'] = True
        with self.assertRaisesRegex(ValueError, 'must appear'):
            solver_inputs.check_sample(self.recipe(reagents=['PbI2', 'C4H12NI', 'CsI']), self.rows, strict)

    def test_metadata_template_and_pattern_file(self):
        values, _ = solver_inputs.check_sample(self.recipe(), self.rows, GENERIC)
        with tempfile.TemporaryDirectory() as d:
            solver_inputs.write_inputs(Path(d), [10.0, 10.01], [5.0, 7.0], self.recipe(), values, GENERIC)
            meta = json.loads((Path(d) / 'metadata.json').read_text())
            self.assertEqual(meta['reagents'], ['PbI2', 'C4H12NI'])
            self.assertEqual(meta['route'], 'solution')
            self.assertIn(meta['instrument']['time_s'], [1, 2])
            self.assertEqual((Path(d) / 'pattern.csv').read_text(), 'x,y\n10.0,5.0\n10.01,7.0\n')


if __name__ == '__main__':
    unittest.main()
