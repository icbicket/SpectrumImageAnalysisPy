import image_functions
import unittest
import numpy as np

# if im is not 2d
# quad sum if im is even/odd # pixels

class ImageFunctionsTest(unittest.TestCase):

    def test3DIm(self):
        '''an error is raised given a 3d input'''
        im = np.arange(8).reshape(2, 2, 2)
        with self.assertRaisesRegex(ValueError, 
            'Your image is not 2D! Please check the number of dimensions '
            'in the input!'):
            image_functions.check_image(im)
            
    def testQuadSumSquare(self):
        '''test quadrant sum for a square image with an even number of pixels 
        on both sides'''
        im = np.arange(16).reshape(4, 4)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[10, 18], [42, 50]])))
        
    def testQuadSumOdd(self):
        '''test quadrant sum for a non-square image with an odd number of pixels 
        on both sides'''
        im = np.arange(15).reshape(3, 5)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[21, 24], [33, 27]])))

    def testQuadSumNotSquare(self):
        '''test quadrant sum for a non-square image with an odd number of pixels 
        on one side and an even number on the other side'''
        im = np.arange(20).reshape(5, 4)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[27, 39], [58, 66]])))

    def testQuadSumLine(self):
        '''test quadrant sum for a non-square image in which one dimension is 1 
        pixel (eg, a line, n by 1 image)'''
        im = np.arange(5).reshape(5, 1)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[3, 0], [7, 0]])))

if __name__ == '__main__':
    unittest.main()
