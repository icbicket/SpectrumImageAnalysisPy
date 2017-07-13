from __future__ import print_function
import numpy as np
import SpectrumImage
import csv
from scipy.ndimage.filters import gaussian_filter1d
import os

def ImportCSV(filename):
    x = np.genfromtxt(filename,
                       delimiter = '\t', dtype = None, skip_header = 1)
    return x
    
class Spectrum(object):
	def __init__(self, intensity, units, SpectrumRange=None):
		self.intensity = intensity
		self.units = units
		self.length = len(self.intensity)
		self.SpectrumRange = SpectrumRange
		
	def SaveSpectrumAsCSV(self,filename):
		if os.path.exists(filename):
			filename = filename[:-4] + '-1' + filename[-4:]
		print('Saving...', filename)
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
			
	def SmoothingFilter1D(self, sigma=2):
		kernel = np.array([1, 1, 2, 1, 1])/6.
		intensity = np.append(self.intensity[4::-1], np.append(self.intensity, self.intensity[-5::]))
		smoothed = np.convolve(intensity, kernel, mode='same')
		smoothed = gaussian_filter1d(self.intensity, sigma)
#		smoothed[self.intensity > (0.01*np.max(self.intensity))] = self.intensity[self.intensity > (0.01*np.max(self.intensity))]
		return smoothed
		
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
#		print(s)
		
	@classmethod
	def LoadFromCSV(cls, filename):
		spectrum = ImportCSV(filename)
		return cls(intensity=spectrum[:, 1], WavelengthRange=spectrum[:, 0], units='nm')

		
class EELSSpectrum(Spectrum):
	def __init__(self, intensity, SpectrumRange=None, channel_eV = None, dispersion=0.005, ZLP=True, units='eV'):
		super(EELSSpectrum, self).__init__(intensity, units)
		'''intensity: 1D array
		   SpectrumRange: 1D array
		   channel_eV: 2 element array [channel #, eV value]
		   dispersion: float, width of each channel, must be provided if SpectrumRange is not, default is 5meV
		   ZLP: Boolean - True=ZLP is present
		   units: string, for plot axis
		   '''
		if SpectrumRange is not None:
			self.dispersion = SpectrumRange[1] - SpectrumRange[0]
		else:
			self.dispersion = dispersion
		
		if ZLP == True:
			self.ZLP = SpectrumImage.EELSSpectrumImage.FindZLP(self.intensity)
			if SpectrumRange is not None:
				self.SpectrumRange = SpectrumRange
			else:
				self.SpectrumRange = np.arange(0 - self.ZLP, self.length - self.ZLP) * self.dispersion
		else:
			self.ZLP = None
			if SpectrumRange is not None:
				self.SpectrumRange = SpectrumRange
			elif channel_eV is not None:
				if len(channel_eV) == 2:
					eV0 = channel_eV[1] - channel_eV[0] * dispersion
					self.SpectrumRange = np.linspace(
						eV0, 
						eV0 + self.length * dispersion,
						self.length
						)
				else:
					raise ValueError('You need to define the channel and the energy!')
			else:
				raise ValueError('You need to input the energy range!')
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
		data_sym = np.delete(self.intensity, np.s_[2*self.ZLP:self.length], axis = -1)
		data_sym = np.delete(data_sym, np.s_[:np.maximum(2*self.ZLP-self.length, 0)], axis = -1)
		data_sym[data_sym<0] = 0
		return EELSSpectrum(data_sym, dispersion=self.dispersion, units=self.units)
		
	def PadSpectrum(self, pad_length, pad_value=0, pad_side='left'):
		if pad_side == 'left':
			padded = np.append(np.ones((pad_length, )) * pad_value, self.intensity)
		elif pad_side == 'right':
			padded = np.append(self.intensity, np.ones((pad_length, 1)) * pad_value)
		else:
			padded = np.append(np.ones((pad_length, 1)) * pad_value, self.intensity, np.ones((pad_length, 1)))
		return EELSSpectrum(padded, dispersion=self.dispersion, units=self.units)
		
	def FindFW(self, intensityfraction):
#		intensity_norm = self.intensity.Normalize().intensity
		lefttail = self.intensity[:self.ZLP][::-1]
		diff1 = lefttail - intensityfraction*self.intensity[self.ZLP]
		left_index_1 = np.argmax(np.diff(np.sign(diff1)) != 0)
		left_index_2 = left_index_1 + 1
		left_energy = self.dispersion * np.interp(
			intensityfraction*self.intensity[self.ZLP], 
			[lefttail[left_index_2], lefttail[left_index_1]], 
			[left_index_2, left_index_1])+self.dispersion
		
		righttail = self.intensity[self.ZLP:]
		diff2 = righttail - intensityfraction*self.intensity[self.ZLP]
		right_index_1 = np.argmax(np.diff(np.sign(diff2)) != 0) 
		right_index_2 = right_index_1 + 1
		right_energy = self.dispersion * np.interp(
			intensityfraction*self.intensity[self.ZLP], 
			[righttail[right_index_2], righttail[right_index_1]], 
			[right_index_2, right_index_1])
		
		FW = left_energy + right_energy
		return FW
		
	def RLDeconvolution(self, RLiterations, PSF, PSF_pad=0):
		'''Input: RLiterations=number of iterations to perform
			PSF=point spread function (an EELS spectrum object)
		Optional argument: 
			PSF_pad=value to pad PSF with (or None to not pad PSF)'''
		PSF_sym = PSF.SymmetrizeAroundZLP()
		if PSF_pad is not None:
			data_length = np.size(self.SpectrumRange)
			PSF_length = np.size(PSF_sym.intensity)
			pad_length = data_length/2 - (1 + data_length) % 2 - (PSF_length-(PSF_length % 2))/2
			if PSF_sym.ZLP < data_length/2:
				PSF_sym = PSF.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='left').SymmetrizeAroundZLP()
			elif PSF_sym.ZLP > data_length/2:
				PSF_sym = PSF_sym.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='right')
		print('Beginning deconvolution...')
		x_deconv = RL(RLiterations, PSF_sym.Normalize().intensity, self.Normalize().intensity)
		print('Done %s iterations!' %RLiterations)
		return EELSSpectrum(x_deconv, dispersion=self.dispersion)
		
	def eVSlice(self, starteV, stopeV):
		startchannel = int(starteV / self.dispersion + self.ZLP)
		stopchannel = int(stopeV / self.dispersion + self.ZLP)
		sliced = self.data[startchannel:stopchannel]
		return sliced
		
#Richardson-Lucy algorithm
def RL(iterations, PSF_norm, Spec):
	RL4 = Spec.copy()
	for ii in range(iterations):
		RL1 = np.convolve(PSF_norm, RL4, 'same')
		RL2 = Spec/RL1
		RL3 = np.convolve(PSF_norm, RL2, 'same')
		RL4 *= RL3
	return RL4

