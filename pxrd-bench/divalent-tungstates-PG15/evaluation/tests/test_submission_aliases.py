import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scoring_v5/src'))
from pymatgen.core import Lattice, Structure
from structure_metrics import parse_submission


class SubmissionAliases(unittest.TestCase):
    def test_equivalent_phase_fields_preserve_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            Structure(Lattice.cubic(3.9), ['Ni', 'O'], [[0, 0, 0], [.5, .5, .5]]).to(
                filename=str(Path(directory) / 'phase.cif'))
            record = {'cif_path': 'phase.cif', 'weight_fraction': 1.0}
            for field in ('phases', 'crystalline_phases', 'modeled_crystalline_phases'):
                with self.subTest(field=field), patch('structure_metrics.read_json', return_value={field: [copy.deepcopy(record)]}):
                    data, phases, _ = parse_submission(directory, ['Ni', 'O'])
                    self.assertEqual(len(phases), 1)
                    self.assertTrue(data['_submission_parsing']['quantification_complete'])
                with patch('structure_metrics.read_json', return_value={field: [dict(record, weight_fraction=-1)]}):
                    data, _, _ = parse_submission(directory, ['Ni', 'O'])
                    self.assertFalse(data['_submission_parsing']['quantification_complete'])

    def test_conflicting_fields_rejected(self):
        with patch('structure_metrics.read_json', return_value={'phases': [], 'modeled_crystalline_phases': [{}]}):
            with self.assertRaisesRegex(ValueError, 'Conflicting'):
                parse_submission('.', ['Ni', 'O'])


if __name__ == '__main__':
    unittest.main()
