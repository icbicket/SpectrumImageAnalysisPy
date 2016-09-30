import numpy as np
import SpectrumImage

class Spectrum(object):
	def __init__(self, intensity, units):
		self.intensity = intensity
		self.units = units
		self.length = len(self.intensity)
		
class CLSpectrum(Spectrum):
	def __init__(self, intensity, WavelengthRange, units='nm'):
		super(CLSpectrum, self).__init__(intensity, units)
		self.SpectrumRange = WavelengthRange
		self.unit_label = 'Wavelength'
		self.secondary_units = 'eV'
		self.secondary_unit_label = 'Energy'
		
class EELSSpectrum(Spectrum):
	def __init__(self, intensity, dispersion=0.005, units='eV'):
		super(EELSSpectrum, self).__init__(intensity, units)
		self.dispersion = dispersion
		self.ZLP = SpectrumImage.EELSSpectrumImage.FindZLP(self.intensity)
		self.SpectrumRange = np.arange(0 - self.ZLP, self.length - self.ZLP) * self.dispersion
		self.unit_label = 'Energy'
		self.secondary_units = 'nm'
		self.secondary_unit_label = 'Wavelength'

#	@staticmethod		
#	def FindZLP(spectrum):
#		ZLP = np.argmax(spectrum)
#		return ZLP
