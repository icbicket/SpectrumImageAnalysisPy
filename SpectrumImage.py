import numpy as np
import Spectrum
import csv
from scipy import signal
from scipy.ndimage.filters import median_filter

class SpectrumImage(object):
	"""Class for spectrum image data set, must be 3d numpy array
	Axis0, Axis1: spatial dimensions, Axis2: spectrum dimension,
	spectrum_units: units along the spectral axis,
	calibration = spatial calibration (m/pixel)"""
	def __init__(self, SI, spectrum_units, calibration=0):
		if len(np.shape(SI)) != 3:
			raise ValueError('That was not a 3D spectrum image!')
		self.data = np.ma.array(SI.astype(float))
		self.size = np.shape(SI)
		self.calibration = calibration
		self.spectrum_units = spectrum_units
		## Add calibration for x, y, E/wavelength
		

		
class CLSpectrumImage(SpectrumImage):
	def __init__(self, SI, WavelengthRange, spectrum_units='nm', calibration=0):
		super(CLSpectrumImage, self).__init__(SI, spectrum_units, calibration)
		self.SpectrumRange = WavelengthRange
		self.spectrum_unit_label = 'Wavelength'
		self.spectrum_secondary_units = 'eV'
		self.spectrum_secondary_unit_label = 'Energy'
		self.dispersion = self.SpectrumRange[1] - self.SpectrumRange[0]

	def ExtractSpectrum(self, mask3D):
		extractedspectrum = Spectrum.CLSpectrum(
			np.mean(np.mean(
			np.ma.masked_array(self.data, mask3D), 
			axis = 0), axis = 0), self.SpectrumRange, 
			units = self.spectrum_units)
		return extractedspectrum
		
	def SpikeRemoval(self, threshold):
#		median = np.median(self.data, axis=2, keepdims=True)
#		d = np.abs(self.data - median)
#		median_d = np.median(d)
#		s = d/median_d if median_d else 0.
#		i = np.where(s>20)
#		print i
#		self.data[i] = np.mean([self.data[(i[0]-1, i[1], i[2])], 
#								  self.data[(i[0]+1, i[1], i[2])], 
#								  self.data[(i[0], i[1]-1, i[2])], 
#								  self.data[(i[0], i[1]+1, i[2])]], axis=0)

		grad = np.abs(np.gradient(self.data.astype(float)))
		mask0 = np.zeros(np.shape(grad[0]))
		mask0[grad[0] > threshold] = 1.
		mask1 = np.zeros(np.shape(grad[1]))
		mask1[grad[1] > threshold] = 1.
		mask2 = np.zeros(np.shape(grad[2]))
		mask2[grad[2] > threshold] = 1.
		mask = np.logical_or(mask0, mask1).astype(float)

		convolutionmask = np.array([[[0,0,0],[0,1,0],[0,0,0]],[[0,1,0],[1,0,1],[0,1,0]],[[0,0,0],[0,1,0],[0,0,0]]])
		convolved = signal.convolve(mask, convolutionmask, mode='same')
		filtermask = np.reshape(np.array([[0,1,0],[1,0,1],[0,1,0]]), (3,3,1))
		print np.unique(convolved, return_counts=True), np.shape(convolved)
		filtercopy = median_filter(np.copy(self.data), footprint=filtermask)
#		print 'unique', np.unique(filtercopy, return_counts=True)
		spike_free = filtercopy*(convolved >= 3) + self.data*(convolved < 3)
		spike_free = CLSpectrumImage(spike_free, self.SpectrumRange, self.spectrum_units, self.calibration)
		i = np.where(convolved > 3)

		return spike_free



class EELSSpectrumImage(SpectrumImage):
	def __init__(self, SI, dispersion=0.005, spectrum_units='eV', calibration=0):
		super(EELSSpectrumImage, self).__init__(SI, spectrum_units, calibration)
		self.dispersion = dispersion
		self.ZLP = self.FindZLP(self.data)
		self.SpectrumRange = np.arange(0 - self.ZLP, self.size[-1] - self.ZLP) * self.dispersion
		self.spectrum_unit_label = 'Energy'
		self.spectrum_secondary_units = 'nm'
		self.spectrum_secondary_unit_label = 'Wavelength'

	@staticmethod		
	def FindZLP(data):
		ZLP = int(np.average(np.argmax(data, axis = -1)))
		return ZLP
		
	def ExtractSpectrum(self, mask3D):
		extractedspectrum = Spectrum.EELSSpectrum(
			np.mean(np.mean(
			np.ma.masked_array(self.data, mask3D), 
			axis = 0), axis = 0), 
			dispersion = self.dispersion,
			units = self.spectrum_units)
		return extractedspectrum
