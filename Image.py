import numpy as np

class Image(object):
	def __init__(self, Img):
		"""Function to initialize image class: Img = 2d numpy array"""
		self.Img = np.squeeze(Img)
		self.size = np.shape(self.Img)
		#Extract the contrast limits for the input image (min and max intensity value)
		self.Imglim = [np.min(self.Img[~np.isnan(self.Img)]), np.max(self.Img[~np.isnan(self.Img)])]

	def PadImg(self, pad):
		#Pad image, input pad = 2x2 array/tuple ((axis0_before, axis0_after), (axis1_before, axis1_after))
		self.Img = np.pad(self.Img.astype(float), pad, 'constant', constant_values = (np.nan,))
