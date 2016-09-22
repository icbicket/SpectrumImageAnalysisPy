import numpy as np

class SpectrumImage(object):
	"""Class for spectrum image data set, must be 3d numpy array
	Axis0, Axis1: spatial dimensions, Axis2: spectrum dimension"""
	def __init__(self, SI):
		self.data = SI
		self.size = np.shape(SI)
		## Add calibration for x, y, E/wavelength
