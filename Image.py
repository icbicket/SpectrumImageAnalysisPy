import numpy as np

class Image(object):
	def __init__(self, Img, calibration=0):
		"""Function to initialize image class: Img = 2d numpy array"""
		self.data = Img
		self.size = np.shape(self.data)
		self.calibration = calibration # Dimension units per pixel (eg, for microscope data)
		#Extract the contrast limits for the input image (min and max intensity value)
		self.Imglim = [np.min(self.data[~np.isnan(self.data)]), np.max(self.data[~np.isnan(self.data)])]

	def PadImg(self, pad):
		#Pad image, input pad = 2x2 array/tuple ((axis0_before, axis0_after), (axis1_before, axis1_after))
		self.data = np.pad(self.data.astype(float), pad, 'constant', constant_values = (np.nan,))
