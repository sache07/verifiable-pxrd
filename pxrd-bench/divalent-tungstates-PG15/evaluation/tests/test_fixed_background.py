"""Run with the GSAS-II backend Python interpreter."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scoring_v5/runtime'))
from replay_worker import attach_fixed_background, InvalidProject


class FixedBackground(unittest.TestCase):
    def histogram(self):
        return {'Background': [None, {'background PWDR': ['PWDR baseline', 2., False]}],
                'Data': [np.array([10., 20., 30.]), np.ones(3)]}

    def test_full_saved_vector_loaded_without_rescaling(self):
        hist = self.histogram()
        source = {'PWDR baseline': {'Data': [hist['Data'][0], np.array([1., 2., 3.])]}}
        with patch('replay_worker.IO.GetHistograms', return_value=source):
            report = attach_fixed_background('unused.gpx', hist, 'PWDR measured')
        np.testing.assert_array_equal(hist['Background'][1]['fixback'], [1., 2., 3.])
        self.assertEqual(report['multiplier'], 2.)
        self.assertFalse(report['interpolation'])

    def test_incompatible_or_nonfinite_source_rejected(self):
        for x, y in [([10., 20.], [1., 2.]), ([10., 20., 31.], [1., 2., 3.]),
                     ([10., 20., 30.], [1., np.nan, 3.])]:
            with self.subTest(x=x, y=y), patch('replay_worker.IO.GetHistograms',
                    return_value={'PWDR baseline': {'Data': [np.array(x), np.array(y)]}}):
                with self.assertRaises(InvalidProject):
                    attach_fixed_background('unused.gpx', self.histogram(), 'PWDR measured')

    def test_no_fixed_histogram_leaves_standard_replay_unchanged(self):
        hist = self.histogram()
        hist['Background'][1]['background PWDR'] = ['', 1., False]
        self.assertIsNone(attach_fixed_background('unused.gpx', hist, 'PWDR measured'))


if __name__ == '__main__':
    unittest.main()
