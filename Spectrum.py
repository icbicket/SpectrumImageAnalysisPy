import numpy as np
import SpectrumImage
import csv

class Spectrum(object):
	def __init__(self, intensity, units):
		self.intensity = intensity
		self.units = units
		self.length = len(self.intensity)
		
	def SaveSpectrumAsCSV(self,filename):
		print 'Saving...', filename
		ExportSpectrumRange = np.copy(self.SpectrumRange)
		ExportIntensity = np.copy(self.intensity)
		ExportSpectrumRange.resize(len(ExportSpectrumRange), 1)
		ExportIntensity.resize(len(ExportIntensity), 1)
		ExportData = np.append(ExportSpectrumRange, ExportIntensity, axis = 1)
		ExportHeaders = [self.unit_label + ' (' + self.units + ')', 'Intensity']
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = '	')
			writer.writerow(ExportHeaders)
			writer.writerows(ExportData)
		
class CLSpectrum(Spectrum):
	def __init__(self, intensity, WavelengthRange, units='nm'):
		super(CLSpectrum, self).__init__(intensity, units)
		self.SpectrumRange = WavelengthRange
		self.unit_label = 'Wavelength'
		self.secondary_units = 'eV'
		self.secondary_unit_label = 'Energy'
		
#	def SpikeRemoval(self, threshold):
#		median = np.median(self.intensity)
#		d = np.abs(self.intensity - median)
#		median_d = np.median(d)
#		s = d/median_d if median_d else 0.
#		print s
		
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
