import numpy as np

class Spectrum(object):
	def __init__(self, intensity, units):
		self.intensity = intensity
		self.units = units
		self.length = len(self.intensity)
		
class CLSpectrum(Spectrum):
	def __init__(self, intensity, WavelengthRange, units='nm'):
		super(CLSpectrum, self).__init__(intensity, units)
		self.WavelengthRange = WavelengthRange
		self.secondary_units = 'eV'
		
class EELSSpectrum(Spectrum):
	def __init__(self, intensity, dispersion=0.005, units='eV'):
		super(EELSSpectrum, self).__init__(intensity, units)
		self.dispersion = dispersion
		self.ZLP = self.FindZLP(self.intensity)
		self.EnergyRange = np.arange(0 - self.ZLP, self.length - self.ZLP) * self.dispersion
		self.secondary_units = 'nm'

	@staticmethod		
	def FindZLP(spectrum):
		ZLP = np.argmax(spectrum)
		return ZLP
