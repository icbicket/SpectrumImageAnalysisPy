import spectrum_functions
import unittest
import numpy as np

class SpectrumFunctionsTest(unittest.TestCase):
    
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

    def testNormalize1Index(self):
        '''Normalize works as expected when a single index is given'''
        x = np.arange(10)
        ind = 2
        np.testing.assert_allclose(
            x/2., 
            spectrum_functions.normalize(x, ind)
            )

    def testNormalizeFloatIndex(self):
        '''Normalize throws an error when given a float index'''
        x = np.arange(10)
        ind = 2.4
        with self.assertRaises(ValueError):
           spectrum_functions.normalize(x, ind)

    def testNormalize1IndexTuple(self):
        '''Normalize throws an error if a single index inside a sequence
         is given'''
        x = np.arange(10)
        ind = [3]
        with self.assertRaises(ValueError):
           spectrum_functions.normalize(x, ind)

    def testNormalize2Indices(self):
        '''Normalize works as expected when two indices are given'''
        x = np.arange(10)
        ind = (2, 5)
        np.testing.assert_allclose(
            x/9., 
            spectrum_functions.normalize(x, ind)
            )
        
    def testNormalizeMoreIndices(self):
        '''Normalize raises an error if more than two indices are passed as
        input'''
        x = np.arange(10)
        ind = (2, 5, 3)
        with self.assertRaises(ValueError):
           spectrum_functions.normalize(x, ind)

if __name__ == '__main__':
    unittest.main()
