import numpy as np
import png

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
		
	def SaveImgAsPNG(self, filename, clim):
		r_min = max(clim[0], self.Imglim[0])
		r_max = min(clim[1], self.Imglim[1])
		writefile = open(filename, 'wb')
		if type(self.data)==np.ma.MaskedArray:
			writeImage = np.empty((self.size[0], self.size[1]*2))
			writeImage[:, 0::2] = np.round(255*(self.data.data.astype(float) - r_min)/float((r_max - r_min)))*np.invert(self.data.mask)
			writeImage[:, 1::2] = np.invert(self.data.mask)*255
			alph = True
		else:
			writeImage = np.round(255*(self.data.astype(float) - r_min)/float((r_max - r_min)))
			alph = False
		writeImage[writeImage < 0] = 0
		writeImage[writeImage > 255] = 255
		writer = png.Writer(size = self.size[::-1], greyscale = True, alpha = alph)
		writer.write(writefile, writeImage)
		writefile.close()
