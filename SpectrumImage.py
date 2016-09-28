import numpy as np

class SpectrumImage(object):
	"""Class for spectrum image data set, must be 3d numpy array
	Axis0, Axis1: spatial dimensions, Axis2: spectrum dimension"""
	def __init__(self, SI, dispersion, calibration=0):
		if len(np.shape(SI)) != 3:
			raise ValueError('That was not a 3D spectrum image!')
		self.data = SI
		self.size = np.shape(SI)
		self.calibration = calibration
		self.dispersion = dispersion
		
		## Add calibration for x, y, E/wavelength
