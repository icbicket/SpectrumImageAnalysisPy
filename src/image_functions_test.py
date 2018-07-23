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
        '''test quadrant sum for a non-square image with an odd number of 
        pixels on both sides'''
        im = np.arange(15).reshape(3, 5)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[21, 24], [33, 27]])))

    def testQuadSumNotSquare(self):
        '''test quadrant sum for a non-square image with an odd number of 
        pixels on one side and an even number on the other side'''
        im = np.arange(20).reshape(5, 4)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[27, 39], [58, 66]])))

    def testQuadSumLine(self):
        '''test quadrant sum for a non-square image in which one dimension is 1 
        pixel (eg, a line, n by 1 image)'''
        im = np.arange(5).reshape(5, 1)
        self.assertTrue(np.array_equal(image_functions.quadrant_sum(im),
            np.array([[3, 0], [7, 0]])))

    def testContrastStretchFullRange(self):
        '''test contrast_stretch for full contrast stretch from 0 to 255'''
        im = np.arange(10).reshape(2,5)
        im_stretch = image_functions.contrast_stretch(im)
        self.assertTrue(np.allclose(im_stretch, 
            np.array([[0, 85/3, 170/3, 85, 340/3],
                [425/3, 170, 595/3, 680/3, 255]])))

    def testContrastStretchLowerThreshold(self):
        '''test contrast_stretch for contrast stretch from 100 to 255'''
        im = np.arange(10).reshape(2,5)
        im_stretch = image_functions.contrast_stretch(im, s=[100, 255])
        self.assertTrue(np.allclose(im_stretch, 
            np.array([[100, 1055/9, 1210/9, 455/3, 1520/9],
                [1675/9, 610/3, 1985/9, 2140/9, 255]])))

    def testContrastStretchUpperThreshold(self):
        '''test contrast_stretch for contrast stretch from 0 to 90'''
        im = np.arange(10).reshape(2,5)
        im_stretch = image_functions.contrast_stretch(im, s=[0, 90])
        self.assertTrue(np.allclose(im_stretch, 
            np.array([[0, 10, 20, 30, 40],
                [50, 60, 70, 80, 90]])))

    def testContrastStretchLowerUpperThreshold(self):
        '''test contrast_stretch for contrast stretch from 90 to 180'''
        im = np.arange(10).reshape(2,5)
        im_stretch = image_functions.contrast_stretch(im, s=[90, 180])
        self.assertTrue(np.allclose(im_stretch, 
            np.array([[90, 100, 110, 120, 130],
                [140, 150, 160, 170, 180]])))
    # Test # bits
    # Test limit value > 255
    # test s1 > s2
    # test negative values

    def testContrastStretchLimitHistogram(self):
        '''test contrast_stretch for contrast stretch of only part of image
        histogram to full contrast limits'''
        im = np.arange(10).reshape(2,5)
        im_stretch = image_functions.contrast_stretch(
                                                    im, 
                                                    s=[0, 255], 
                                                    r=[2, 8]
                                                        )
        self.assertTrue(np.allclose(im_stretch, 
            np.array([[0, 0, 0, 255/6, 2*255/6],
                [3*255/6, 4*255/6, 5*255/6, 255, 255]])))

if __name__ == '__main__':
    unittest.main()
