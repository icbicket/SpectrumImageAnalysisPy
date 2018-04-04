from __future__ import print_function
import numpy as np
import Image
import sys

class ImageAligner(object):
    """Holds list of images (Image class) which need aligning to each other"""
    def __init__(self, Images):
        self.Images = Images
        self.numIms = len(Images)
        self.offsets = np.zeros((2, self.numIms), dtype = 'int64')
        # Pad all images to the maximum image size - make all same shape
        self.xmax = max(i.size[0] for i in self.Images)
        self.ymax = max(i.size[1] for i in self.Images)
        
        for ii in self.Images:
            print(ii.size)
            sizediff = np.subtract((self.xmax, self.ymax), ii.size)
            pad = ((0, sizediff[0]), (0, sizediff[1]))
            ii.PadImg(pad)
