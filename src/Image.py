from __future__ import print_function
import numpy as np
import png
import os
import file_namer
import image_functions as imfun
import sys

def py2_3_string_check():
    try:
        basestring #Python 2
        print('py2')
        def isstr(s):
            return isinstance(s, basestring)
    except NameError: #Python 3
        print('py3')
        def isstr(s):
            return isinstance(s, str)
            
def isstring(string):
    return (isinstance(string, basestring) if sys.version_info[0] == 2 else
            isinstance(string, str))
           
           
class Image(object):
    def __init__(self, Img, calibration=0):
        """Function to initialize image class: Img = 2d numpy array
        Grayscale images only!"""
        self.data = Img
        self.size = np.shape(self.data)
        self.calibration = calibration # Dimension units per pixel (eg, for microscope data)
        #Extract the contrast limits for the input image (min and max intensity value)
        self.Imglim = [np.min(self.data[~np.isnan(self.data)]), np.max(self.data[~np.isnan(self.data)])]


    def PadImg(self, pad):
        #Pad image, input pad = 2x2 array/tuple ((axis0_before, axis0_after), (axis1_before, axis1_after))
        self.data = np.pad(self.data.astype(float), pad, 'constant', constant_values = (np.nan,))

    def save_img(self, filename, clim=[None, None], cmap=None, **kwargs):
        '''
        Save image
        Filename: string to name the file, include directory path if the 
        current folder is not desired, filetype is given by the ending
        clim: colour limits, if the image should be thresholded to a minimum
        and maximum value. Should be of the form [minimum, maximum]
        cmap: colourmap to apply to the saved image (eg, for grayscale images)
        '''

        if not isstring(filename):
            raise ValueError(
                'Your filename is not a string!')

        if clim[0] is not None:
            r_min = clim[0]
#            r_min = np.maximum(clim[0], np.min(self.data.flatten()))
        else:
            r_min = np.min(self.data.flatten())
            
        if clim[1] is not None:
            r_max = clim[1]
#            r_max = np.minimum(clim[1], np.max(self.data.flatten()))
        else:
            r_max = np.max(self.data.flatten())
        filename = file_namer.name_file(filename)
        
        save_im = imfun.contrast_stretch(self.data, 
            r=[r_min, r_max], 
            s=[0,255], bits=8).astype('uint8')

        if cmap is not None:
            save_im = cmap(save_im)
#            if np.ma.is_masked(self.data) and np.shape(save_im)[-1] == 4:
#                print('mask')
#                save_im[:, :, -1] = save_im[:, :, -1] * self.data.mask.astype(int)
            imfun.write_image(save_im, filename, **kwargs)
        else:
            imfun.write_image(save_im, filename, **kwargs)


    def SaveImgAsPNG(self, filename, clim, cmap=None):
#        r_min = max(clim[0], self.Imglim[0])
#        r_max = min(clim[1], self.Imglim[1])
        r_min = clim[0]
        r_max = clim[1]
        filename = file_namer.name_file(filename)
        writefile = open(filename, 'wb')
        if type(self.data)==np.ma.MaskedArray:
            writeImage = np.empty((self.size[0], self.size[1]*2))
            writeImage[:, 0::2] = np.round(255*(self.data.data.astype(float) - r_min)/float((r_max - r_min)))*np.invert(self.data.mask)
            writeImage[:, 1::2] = np.invert(self.data.mask)*255
            alph = True
        else:
            writeImage = np.round(255*(self.data.astype(float) - r_min)/float((r_max - r_min)))
            alph = False
        if cmap is not None:
            colours = (cmap(np.arange(0,256))*255).astype(int)
            colourstuple = map(tuple, colours)
            if np.all(np.equal(np.array(colours[:,0]),np.array(colours[:,1]), np.array(colours[:,2]))):
                writer = png.Writer(size = self.size[::-1], greyscale = True, alpha = alph)
                print('I am so gray...')
            else:
                writer = png.Writer(size = self.size[::-1], palette=colourstuple, bitdepth=8)

                if type(self.data) == np.ma.MaskedArray:
                    writeImage = np.round(255*(self.data.data.astype(float) - r_min)/float((r_max - r_min)))*np.invert(self.data.mask)
                else:
                    writeImage = np.round(255*(self.data.astype(float) - r_min)/float((r_max - r_min)))
                print('Well, colour me pink!')
        else:
            writer = png.Writer(size = self.size[::-1], greyscale = True, alpha = alph)
        writeImage[writeImage < 0] = 0
        writeImage[writeImage > 255] = 255
        
        writer.write(writefile, writeImage)
        writefile.close()
        
