import numpy as np
import SpectrumImage
import csv

def ImportCSV(filename):
    x = np.genfromtxt(filename,
                       delimiter = '\t', dtype = None, skip_header = 1)
    return x
    
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
		
	@classmethod
	def LoadFromCSV(cls, filename):
		spectrum = ImportCSV(filename)
		return cls(intensity=spectrum[:, 1], WavelengthRange=spectrum[:, 0], units='nm')

		
class EELSSpectrum(Spectrum):
	def __init__(self, intensity, dispersion=0.005, units='eV'):
		super(EELSSpectrum, self).__init__(intensity, units)
		self.dispersion = dispersion
		self.ZLP = SpectrumImage.EELSSpectrumImage.FindZLP(self.intensity)
		self.SpectrumRange = np.arange(0 - self.ZLP, self.length - self.ZLP) * self.dispersion
		self.unit_label = 'Energy'
		self.secondary_units = 'nm'
		self.secondary_unit_label = 'Wavelength'
		
	@classmethod
	def LoadFromCSV(cls, filename):
		spectrum = ImportCSV(filename)
		return cls(intensity=spectrum[:, 1], dispersion=spectrum[1,0]-spectrum[0,0], units='eV')
		
	def Normalize(self):
		'''Normalize data to integral'''
		normfactor = np.sum(self.intensity, keepdims=True)
		data_norm = self.intensity/normfactor
		return EELSSpectrum(data_norm, dispersion=self.dispersion, units=self.units)
		
	def SymmetrizeAroundZLP(self):
		data_sym = np.delete(self.intensity, np.s_[2*self.ZLP:-1], axis = -1)
		data_sym[data_sym<0] = 0
		return EELSSpectrum(data_sym, dispersion=self.dispersion, units=self.units)
#	@staticmethod		
#	def FindZLP(spectrum):
#		ZLP = np.argmax(spectrum)
#		return ZLP
