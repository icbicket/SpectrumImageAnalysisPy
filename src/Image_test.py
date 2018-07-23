import Image
import numpy as np
import unittest

class ImageTest(unittest.TestCase):
    
    def testSaveImg(self):
        im = np.reshape(np.arange(20), (4,5))
        pass
    
if __name__ == '__main__':
    unittest.main()
