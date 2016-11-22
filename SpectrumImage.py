import numpy as np
import Spectrum
import csv

class SpectrumImage(object):
	"""Class for spectrum image data set, must be 3d numpy array
	Axis0, Axis1: spatial dimensions, Axis2: spectrum dimension,
	spectrum_units: units along the spectral axis,
	calibration = spatial calibration (m/pixel)"""
	def __init__(self, SI, spectrum_units, calibration=0):
		if len(np.shape(SI)) != 3:
			raise ValueError('That was not a 3D spectrum image!')
		self.data = np.ma.array(SI)
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
			np.sum(np.sum(
			np.ma.masked_array(self.data, mask3D), 
			axis = 0), axis = 0), self.SpectrumRange, 
			units = self.spectrum_units)
		return extractedspectrum
		
#	def SystemCorrection(self):
		
				
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
			np.sum(np.sum(
			np.ma.masked_array(self.data, mask3D), 
			axis = 0), axis = 0), 
			dispersion = self.dispersion,
			units = self.spectrum_units)
		return extractedspectrum
