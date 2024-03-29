import spectrum_functions
import unittest
import numpy as np

class CheckSpectrumTest(unittest.TestCase):
    
    def test2DSpecX(self):
        '''an error is raised if check_spectrum is given a 2D x input'''
        x = np.arange(10).reshape((2, 5))
        y = np.arange(10)
        with self.assertRaisesRegex(ValueError,
           'x is not a 1 dimensional array'):
           spectrum_functions.check_spectrum(x, y)

    def test2DSpecY(self):
        '''an error is raised if check_spectrum is given a 2D y input'''
        x = np.arange(10)
        y = np.arange(10).reshape((2, 5))
        with self.assertRaisesRegex(ValueError,
           'y is not a 1 dimensional array'):
           spectrum_functions.check_spectrum(x, y)

    def testXYlenDifferent(self):
        '''an error is raised if x and y are not the same length as each 
        other'''
        x = np.arange(10)
        y = np.arange(9)
        with self.assertRaisesRegex(ValueError,
           'x and y are not the same length'):
           spectrum_functions.check_spectrum(x, y)

class SliceRangeTest(unittest.TestCase):
    def testSliceRange(self):
        '''slice_range works properly in normal use case'''
        x = np.arange(10)
        y = np.arange(10)
        start_stop = [5, 8]
        self.assertTrue(np.array_equal(
                            np.array([5, 6, 7, 8]),
                            spectrum_functions.slice_range(x, start_stop, y)
                        ))

    def testSliceRangeYCal(self):
        '''slice_range works properly with y non-integer values'''
        x = np.arange(10)
        y = np.arange(10)/10.
        start_stop = [0.3, 0.7]
        self.assertTrue(np.array_equal(
                            np.array([3, 4, 5, 6, 7]),
                            spectrum_functions.slice_range(x, start_stop, y)
                        ))

    def testSliceRangeStopOutside(self):
        '''slice_range works properly when stop is greater than max(y)'''
        x = np.arange(10)
        y = np.arange(10)
        start_stop = [5, 12]
        self.assertTrue(np.array_equal(
                            np.array([5, 6, 7, 8, 9]),
                            spectrum_functions.slice_range(x, start_stop, y)
                        ))

    def testSliceRangeStartOutside(self):
        '''slice_range works properly when stop is greater than max(y)'''
        x = np.arange(10)
        y = np.arange(10)
        start_stop = [-2, 5]
        self.assertTrue(np.array_equal(
                            np.array([0, 1, 2, 3, 4, 5]),
                            spectrum_functions.slice_range(x, start_stop, y)
                        ))

    def testSliceRangeYNegative(self):
        '''slice_range works properly when y contains negative values'''
        x = np.arange(10)
        y = np.arange(10) - 5
        start_stop = [-7, 0]
        self.assertTrue(np.array_equal(
                            np.array([0, 1, 2, 3, 4, 5]),
                            spectrum_functions.slice_range(x, start_stop, y)
                        ))

    def testSliceRangeStartStopDims(self):
        '''raise error in slice_range if start_stop are not a 2 element list or
        tuple or array'''
        x = np.arange(10)
        y = np.arange(10) - 5
        start_stop = [-7, 0, 5]
        with self.assertRaisesRegex(ValueError,
           'start_stop is not a 2 element list'):
           spectrum_functions.slice_range(x, start_stop, y)

    def testSliceRangeYDecreasing(self):
        '''slice_range works when y is monotonically decreasing'''
        x = np.arange(10)
        y = np.flip(np.arange(10))
        start_stop = [5, 2]
        self.assertTrue(np.array_equal(
            np.array([4, 5, 6, 7]),
            spectrum_functions.slice_range(x, start_stop, y)
            ))

class NormalizeTest(unittest.TestCase):
    '''
    value is None and index is None
    value is None and index is a single integer
    value is None and index is a pair of integers
    value is None and index is a float
    value is None and index has more than two values inside
    value is a single integer and index is None
    value is a single float and index is None
    value has two numbers inside and index is None
    value is not a float or integer and index is None
    value is a number and index is a number
    '''
    def testNormalize1Index(self):
        '''Normalize works as expected when a single index is given'''
        x = np.arange(10)*0.2
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        ind = 2
        np.testing.assert_allclose(
            y/2., 
            spectrum_functions.normalize(x, y, value=None, index=ind),
            atol=1e-7
            )

    def testNormalizeFloatIndex(self):
        '''Normalize throws an error when given a float index'''
        x = np.arange(10)*0.2
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        ind = 2.4
        with self.assertRaisesRegex(ValueError, 'index must be an integer, a pair of integers, or None'):
           spectrum_functions.normalize(x, y, value=None, index=ind)

    def testNormalize1IndexTuple(self):
        '''
        Normalize throws an error if a single index inside a sequence
        is given
         '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        ind = (3,)
        with self.assertRaisesRegex(ValueError, 'index must be an integer, a pair of integers, or None'):
           spectrum_functions.normalize(x, y, value=None, index=ind)

    def testNormalize2Indices(self):
        '''Normalize works as expected when two indices are given'''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        ind = (2, 6)
        np.testing.assert_allclose(
            y/66., 
            spectrum_functions.normalize(x, y, value=None, index=ind)
            )
        
    def testNormalizeMoreIndices(self):
        '''Normalize raises an error if more than two indices are passed as
        input'''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1, 1])
        ind = (2, 5, 3)
        with self.assertRaises(ValueError):
           spectrum_functions.normalize(x, y, value=None, index=ind)

    def testNoIndexNoValue(self):
        '''
        Uses the integral of the whole spectrum as the normalization factor
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        expected = y/82
        calculated = spectrum_functions.normalize(x, y, value=None, index=None)
        np.testing.assert_allclose(calculated, expected)

    def test1IntValueNoIndex(self):
        '''
        Feed in a single value to normalize to
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        expected = np.array([0.5, 0.5, 1, 10, 17.5, 10, 0.5, 0.5, 0.5, 0.5])
        calculated = spectrum_functions.normalize(x, y, value=2, index=None)
        np.testing.assert_allclose(calculated, expected)

    def test1FloatValueNoIndex(self):
        '''
        Feed in a single floating point value to normalize to
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        expected = np.array([0.4, 0.4, 0.8, 8.0, 14.0, 8.0, 0.4, 0.4, 0.4, 0.4])
        calculated = spectrum_functions.normalize(x, y, value=2.5, index=None)
        np.testing.assert_allclose(calculated, expected)

    def testBadValueNoIndex(self):
        '''
        value is a string - should throw an error
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        expected = np.array([0.5, 0.5, 1, 10, 17.5, 10, 0.5, 0.5, 0.5, 0.5])
        with self.assertRaisesRegex(ValueError, 'value must be a single number'):
            calculated = spectrum_functions.normalize(x, y, value='12', index=None)

    def test2ValuesNoIndex(self):
        '''
        value has two numbers - should throw an error
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        with self.assertRaisesRegex(ValueError, 'value must be a single number'):
            calculated = spectrum_functions.normalize(x, y, value=[2, 3], index=None)

    def testValueAndIndex(self):
        '''
        both value and index are defined - should throw an error
        '''
        x = np.arange(10)
        y = np.array([1, 1, 2, 20, 35, 20, 1, 1, 1, 1])
        with self.assertRaisesRegex(ValueError, 'value and index are mutually exclusive'):
            calculated = spectrum_functions.normalize(x, y, value=1.5, index=2)


class FindFWTest(unittest.TestCase):
    def testFindFWHMInt(self):
        '''
        find_fw finds the right fw given a simple function
        '''
        y = np.array([1, 1, 2, 4, 2, 1, 1])
        x = np.arange(7)
        fwhm = 2.
        self.assertEqual(fwhm, spectrum_functions.find_fw(y, 1, 3, 0.5))
    
    def testFindFWHMDecimal(self):
        '''
        find_fw finds the right fw given a simple function, answer is a fraction of the dispersion
        '''
        y = np.array([1, 1, 2, 5, 2, 1, 1])
        x = np.arange(7)
        fwhm = 5/3.
        np.testing.assert_almost_equal(spectrum_functions.find_fw(y, 1, 3, 0.5), fwhm)
        
    def testFindFWAsymmetrical(self):
        '''
        find_fw finds the right fw given an asymmetrical function
        '''
        y = np.array([1, 1, 3, 5, 2, 1, 1])
        x = np.arange(7)
        fwhm = 2.5 / 3 + 1 + 0.25
        self.assertEqual(fwhm, spectrum_functions.find_fw(y, 1, 3, 0.5))
    
    def testFindFWAsymmetricalRight(self):
        '''
        find_fw finds the right fw given an asymmetrical function, higher on the right side
        '''
        y = np.array([1, 1, 2, 5, 3, 1, 1])
        x = np.arange(7)
        fwhm = 2.5 / 3 + 1 + 0.25
        self.assertEqual(fwhm, spectrum_functions.find_fw(y, 1, 3, 0.5))
    
class TrimEdgeSpikesTest(unittest.TestCase):
    '''
    Test the function for trimming edge spikes off a spectrum
    To test:
    - spectrum with no spikes on either edge
    - spectrum with spikes on positive side
    - spectrum with spikes on negative side
    - spectrum with spikes on both sides
    - spectrum with a spike not at the end, but near the end
    - spectrum with spike in the middle
    - Two Nx1 arrays
    - Two NxM arrays
    - different delta_x values vs spike width
    - spike of width 1 on etiher edge
    - spike of width 6 on either edge
    - spike condition
    - negative spike
    - spike longer than delta_x
    '''
    
    def testNoSpikes(self):
        '''
        There are no spikes on either edge
        Function should return the same spectrum
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x, calculated_x)
        np.testing.assert_equal(y, calculated_y)
    
    def testPositiveSpikeWidth1(self):
        '''
        Adding a spike that takes up one channel on the positive side
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            25.2])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[:-1], calculated_x)
        np.testing.assert_equal(y[:-1], calculated_y)
    
    def testPositiveSpikeWidth6(self):
        '''
        Adding a spike that takes up six channels at the positive edge
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            25+0.00571385, 25+0.79742504, 25+0.77946996, 25+0.13200986, 
            25+0.41926802, 25.2])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[:-6], calculated_x)
        np.testing.assert_equal(y[:-6], calculated_y)
    
    def testNegativeSpikeWidth1(self):
        '''
        A spike on the negative side, one channel wide
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([25+0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[1:], calculated_x)
        np.testing.assert_equal(y[1:], calculated_y)
        
    def testNegativeSpikeWidth6(self):
        '''
        A spike on the negative side, six channels wide
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([25+0.3391376 , 25+0.90049531, 25+0.30303949, 25+0.00884677, 
            25+0.30550112, 25+0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[6:], calculated_x)
        np.testing.assert_equal(y[6:], calculated_y)
    
    def testPositiveNegativeSpikesWidth6(self):
        '''
        Spikes on both sides, of width 6 channels
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([25+0.3391376 , 25+0.90049531, 25+0.30303949, 25+0.00884677, 
            25+0.30550112, 25+0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            25+0.00571385, 25+0.79742504, 25+0.77946996, 25+0.13200986, 
            25+0.41926802, 25.2])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[6:-6], calculated_x)
        np.testing.assert_equal(y[6:-6], calculated_y)
    
    def testDownSpike(self):
        '''
        A spike which spikes downwards instead of upwards
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([-25+0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[1:], calculated_x)
        np.testing.assert_equal(y[1:], calculated_y)
    
    def testMiddleSpike(self):
        '''
        A spike in the middle, not inside the delta_x used to look for spikes
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 25+0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x, calculated_x)
        np.testing.assert_equal(y, calculated_y)
    
    def testInnerSpike(self):
        '''
        A spike not right on the edge, but still within the delta_x used to look for spikes
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([+0.3391376 , 0.90049531, 25+0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x[3:], calculated_x)
        np.testing.assert_equal(y[3:], calculated_y)
    
    def testLongDurationSpike(self):
        '''
        A spike that has more channels than the delta_x input
        Code should not detect or remove the spike
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([25+0.3391376 , 25+0.90049531, 25+0.30303949, 25+0.00884677, 
            25+0.30550112, 24+0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 3
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x, calculated_x)
        np.testing.assert_equal(y, calculated_y)
    
    def testNby2Arrays(self):
        '''
        Input an N by 2 array for x and y
        Code should throw an error - cannot nicely remove spikes from more than one spectrum at once
        '''
        x = np.transpose(np.array([np.linspace(-10, 10, 50), np.linspace(-10, 10, 50)]))
        y = np.transpose(np.array([[25+0.3391376 , 25+0.90049531, 25+0.30303949, 25+0.00884677, 
            25+0.30550112, 24+0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816], [0.52704036, 0.34785205, 0.01248348, 0.00585664, 
            0.38531402, 0.90754936, 0.41077946, 0.16521519, 0.02543547, 
            0.39862089, 0.50918473, 0.86812735, 0.33997233, 0.63315477, 
            0.78980089, 0.15026395, 0.44836457, 0.57784553, 0.6472332 , 
            0.5200824 , 0.58102124, 0.10529875, 0.92817147, 0.06893233, 
            0.2785001 , 0.44022657, 0.41064336, 0.24470151, 0.85143201, 
            0.69318985, 0.9414429 , 0.96106755, 0.36963556, 0.70767901, 
            0.0642932 , 0.63252262, 0.85184163, 0.69795268, 0.76700572, 
            0.53899103, 0.55013708, 0.93286294, 0.9493958 , 0.94211322, 
            0.15098836, 0.38564756, 0.19447902, 0.47518195, 25+0.41088442, 
            25+0.02200037]]))
        delta_x = 10
        spike_condition = 10
        with self.assertRaisesRegex(ValueError, 'x is not a 1 dimensional array'):
            calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)

    def testNby2YArray(self):
        '''
        Input an N by 2 array for x and y
        Code should throw an error - cannot nicely remove spikes from more than one spectrum at once
        '''
        x = np.linspace(-10, 10, 50)
        y = np.transpose(np.array([[25+0.3391376 , 25+0.90049531, 25+0.30303949, 25+0.00884677, 
            25+0.30550112, 24+0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816], [0.52704036, 0.34785205, 0.01248348, 0.00585664, 
            0.38531402, 0.90754936, 0.41077946, 0.16521519, 0.02543547, 
            0.39862089, 0.50918473, 0.86812735, 0.33997233, 0.63315477, 
            0.78980089, 0.15026395, 0.44836457, 0.57784553, 0.6472332 , 
            0.5200824 , 0.58102124, 0.10529875, 0.92817147, 0.06893233, 
            0.2785001 , 0.44022657, 0.41064336, 0.24470151, 0.85143201, 
            0.69318985, 0.9414429 , 0.96106755, 0.36963556, 0.70767901, 
            0.0642932 , 0.63252262, 0.85184163, 0.69795268, 0.76700572, 
            0.53899103, 0.55013708, 0.93286294, 0.9493958 , 0.94211322, 
            0.15098836, 0.38564756, 0.19447902, 0.47518195, 25+0.41088442, 
            25+0.02200037]]))
        delta_x = 10
        spike_condition = 10
        with self.assertRaisesRegex(ValueError, 'y is not a 1 dimensional array'):
            calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)

    def testXYDifferentShapes(self):
        '''
        Input two 1D arrays of different length for x and y
        Code should throw an error  - x and y must be the same length to start
        '''
        x = np.linspace(-10, 10, 49)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        with self.assertRaisesRegex(ValueError, 'x and y are not the same length'):
            calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
    
    def testSpikeBelowCondition(self):
        '''
        There is a spike below the spike condition
        Function should return the same spectrum
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([10+0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 10
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x, calculated_x)
        np.testing.assert_equal(y, calculated_y)

    def testSpikeBelowDifferentCondition(self):
        '''
        There is a spike below the spike condition, using a different spike condition
        Function should return the same spectrum
        '''
        x = np.linspace(-10, 10, 50)
        y = np.array([25+0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        delta_x = 10
        spike_condition = 30
        calculated_x, calculated_y = spectrum_functions.trim_edge_spikes(x, y, delta_x, spike_condition)
        np.testing.assert_equal(x, calculated_x)
        np.testing.assert_equal(y, calculated_y)

class FindZLPTest(unittest.TestCase):
    '''
    max method: a spectrum with a global maximum
    max: a spectrum with two equal global maxima - should fail
    gaussian_fit method: normal
    gaussian_fit_method: spectrum with a poor fit
    lorentz fit method: normal
    lorentz_fit method: spectrum with a poor fit
    any other methods are not implemented yet
    '''
    def testFindMaximum(self):
        '''
        Identify the maximum in a spectrum
        '''
        x = np.arange(50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 5, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        calculated_zlp_location, calculated_zlp_eV = spectrum_functions.find_zero_loss_peak(x, y, method='max')
        np.testing.assert_equal(calculated_zlp_location, 16)
        np.testing.assert_equal(calculated_zlp_eV, 16)

    def testFindMaximumNot1Dispersion(self):
        '''
        Identify the maximum in a spectrum
        '''
        x = np.arange(50)*0.1
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 5, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        calculated_zlp_location, calculated_zlp_eV = spectrum_functions.find_zero_loss_peak(x, y, method='max')
        np.testing.assert_equal(calculated_zlp_location, 16)
        np.testing.assert_equal(calculated_zlp_eV, 1.6)

    def testTwoMaxima(self):
        '''
        Two equal maxima in the spectrum - pick the lowest index one, but raise a warning
        '''
        x = np.arange(50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 5, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 5, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        with self.assertRaisesRegex(Warning, 'Two possible ZLPs found'):
            calculated_zlp_location, calculated_zlp_eV = spectrum_functions.find_zero_loss_peak(x, y, method='max')
            self.assertEqual(calculated_zlp_location, 16)
            self.assertEqual(calculated_zlp_eV, 16)

    def testNotImplemented(self):
        '''
        Try a method that is not yet implemented
        '''
        x = np.arange(50)
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 5+0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        with self.assertRaises(NotImplementedError):
            calculated_zlp_location = spectrum_functions.find_zero_loss_peak(x, y, method='min')

class FindBaselineTest(unittest.TestCase):
    '''
    - indices on the left
    - indices on the right
    - single index
    - no index
    - ND data
    - 1D data
    '''
    def testLeftIndices(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        indices = np.arange(0, 5)
        expected = 0.371404058
        calculated = spectrum_functions.find_baseline(y, indices)
        self.assertAlmostEqual(expected, calculated)
    
    def testRightIndices(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        indices = np.arange(-5, 0)
        expected = 0.5030382079999999
        calculated = spectrum_functions.find_baseline(y, indices)
        self.assertAlmostEqual(expected, calculated)
        
    def testSingleIndex(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        indices = 2
        expected = 0.30303949
        calculated = spectrum_functions.find_baseline(y, indices)
        self.assertAlmostEqual(expected, calculated)

    def testNoIndex(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        indices = np.array([])
        with self.assertRaises(IndexError):
            calculated = spectrum_functions.find_baseline(y, indices)

    def test1DData(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334, 0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622, 0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949, 0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624, 0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078, 0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385, 0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816])
        indices = np.array([0, 1])
        expected = 0.619816455
        calculated = spectrum_functions.find_baseline(y, indices)
        self.assertAlmostEqual(expected, calculated)

    def testNDData(self):
        y = np.array([[0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112], [0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537], [0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048], [0.875005  , 0.76189768, 0.84585932, 0.1783356 , 
            0.80704334], [0.04382603, 0.59102601, 0.62387758, 0.51083627, 
            0.32349622], [0.92865613, 0.0199939 , 0.93996841, 0.39261883, 
            0.05113949], [0.90197447, 0.91428898, 0.35906732, 0.77910498, 
            0.47574624], [0.65789791, 0.29094445, 0.7290157 , 0.55764925, 
            0.12215078], [0.5616116 , 0.49832654, 0.65885033, 0.09776671, 
            0.00571385], [0.79742504, 0.77946996, 0.13200986, 0.41926802, 
            0.38701816]])
        indices = np.array([0, 1])
        with self.assertRaises(ValueError):
            calculated = spectrum_functions.find_baseline(y, indices)

class SubtractValueTest(unittest.TestCase):
    '''
    - Subtract a positive value
    - subtract a negative value
    - subtract a 1D array
    - subtract a single value
    - subtract NaN
    '''
    def testPositiveValue(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005])
        value = 0.1
        expected = np.array([0.2391376 , 0.80049531, 0.20303949, -0.09115323, 
            0.20550112, 0.69999341, 0.45395753, 0.82713465, 0.67807738, 
            0.06248537, 0.19886288, 0.64531467, 0.85555297, 0.88566114, 
            0.45011048, 0.775005])
        calculated = spectrum_functions.subtract_value(y, value)
        np.testing.assert_allclose(calculated, expected)
    
    def testNegativeValue(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005])
        value = -0.1
        expected = np.array([0.4391376 , 1.00049531, 0.40303949, 0.10884677, 
            0.40550112, 0.89999341, 0.65395753, 1.02713465, 0.87807738, 
            0.26248537, 0.39886288, 0.84531467, 1.05555297, 1.08566114, 
            0.65011048, 0.975005])
        calculated = spectrum_functions.subtract_value(y, value)
        np.testing.assert_allclose(calculated, expected)

    def test1DArrayValue(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005])
        value = np.array([0.1, -0.1])
        with self.assertRaises(ValueError):
            calculated = spectrum_functions.subtract_value(y, value)

    def test1DArrayValue(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005])
        value = np.nan
        with self.assertRaises(ValueError):
            calculated = spectrum_functions.subtract_value(y, value)

    def testNaNValue(self):
        y = np.array([0.3391376 , 0.90049531, 0.30303949, 0.00884677, 
            0.30550112, 0.79999341, 0.55395753, 0.92713465, 0.77807738, 
            0.16248537, 0.29886288, 0.74531467, 0.95555297, 0.98566114, 
            0.55011048, 0.875005])
        value = np.nan
        with self.assertRaisesRegex(ValueError, 'Input value should not be NaN'):
            calculated = spectrum_functions.subtract_value(y, value)

class IntegrateSpectrumTest(unittest.TestCase):
    '''
    integrate the whole spectrum
    integrate a slice of the spectrum
    same deltaX throughout spectrum
    changing deltaX at different locations
    '''
    def testWholeSpectrum(self):
        y = np.array([1, 2 ,3])
        x = np.array([4, 6, 8])
        expected = 8.0
        calculated = spectrum_functions.integrate_spectrum(x, y)
        self.assertAlmostEqual(expected, calculated)

    def testIndexWholeSpectrum(self):
        y = np.array([1, 2 ,3])
        x = np.array([4, 6, 8])
        expected = 8.0
        calculated = spectrum_functions.integrate_spectrum(x, y, indices=(0, 3))
        self.assertAlmostEqual(expected, calculated)

    def testIndexPartialSpectrum(self):
        y = np.array([1, 5, 4, 4, 6, 2])
        x = np.array([4, 6, 8, 10, 12, 14])
        expected = 17.0
        calculated = spectrum_functions.integrate_spectrum(x, y, indices=(1, 4))
        self.assertAlmostEqual(expected, calculated)

    def testIndexChangingXDiffWholeSpectrum(self):
        y = np.array([1, 5 ,4, 4, 6, 2])
        x = np.array([4, 6, 7, 9.5, 12.2, 12.5])
        expected = 35.2
        calculated = spectrum_functions.integrate_spectrum(x, y)
        self.assertAlmostEqual(expected, calculated)

    def testIndexChangingXDiffPartialSpectrum(self):
        y = np.array([1, 5 ,4, 4, 6, 2])
        x = np.array([4, 6, 7, 9.5, 12.2, 12.5])
        expected = 28
        calculated = spectrum_functions.integrate_spectrum(x, y, indices=(1,5))
        self.assertAlmostEqual(expected, calculated)

if __name__ == '__main__':
    unittest.main()
