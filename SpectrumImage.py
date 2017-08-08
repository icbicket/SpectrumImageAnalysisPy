from __future__ import print_function
import numpy as np
import Spectrum
import csv
import sys
from scipy import signal
from scipy import stats
from scipy.ndimage.filters import median_filter
import handythread
import multiprocessing
from functools import partial
import dm3_lib as DM3
import numbers

def make_dict_from_tags(iterables):
	d = {}
	for ii in iterables:
		splitted = ii.split(' = ')
		keys = list(splitted[:-1][0].split('.'))
		value = splitted[-1]
		tempD = d

		for tt in keys[:-1]:
			tempD = tempD.setdefault(tt, {})

		if keys[-1] in tempD:
			# duplicate tag
			print('You have two tags in your DM3 file which are the same! ' + keys[-1], file=sys.stderr)
		else:
			tempD[keys[-1]] = value
	return d

def import_EELS_dm3(filename):
	data = DM3.DM3(filename)
	
	tags = make_dict_from_tags(data._storedTags)
	imagedata = np.transpose(data.imagedata, axes=(1, 2, 0))
	return imagedata, tags

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
		
#	def SpatialFilter(self):
#		kernel = np.array(

		
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
#		print(i)
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
		filtermaskcorner = np.reshape(np.array([[1,1,1],[1,1,1],[1,1,1]]), (3,3,1))
		filtercopy = median_filter(np.copy(self.data), footprint=filtermask)
		corners = [(0, 0), (0, -1), (-1, -1), (-1, 0)]
		for cc in corners:
			filtercopy[cc][convolved[cc] >= 2] = median_filter(np.copy(self.data), footprint=filtermaskcorner)
			convolved[cc][convolved[cc] >= 2] = 4
		spike_free = filtercopy*(convolved >= 3) + self.data*(convolved < 3)

		spike_free = CLSpectrumImage(spike_free, self.SpectrumRange, self.spectrum_units, self.calibration)
		i = np.where(convolved > 3)

		return spike_free



class EELSSpectrumImage(SpectrumImage):
	def __init__(self, SI, SpectrumRange=None, channel_eV=None, dispersion=0.005, ZLP=True, spectrum_units='eV', calibration=0, metadata=None):
		super(EELSSpectrumImage, self).__init__(SI, spectrum_units, calibration)
		'''intensity: 3D array
		   SpectrumRange: 1D array of same length as energy axis
		   channel_eV: 2 element array [channel #, eV value]
		   dispersion: real number, width of each channel, must be provided if SpectrumRange is not, default is 5meV
		   ZLP: Boolean - True=ZLP is present
		   units: string, for plot axis
		   '''
		
		if ZLP:
			if not isinstance(dispersion, numbers.Real):
				raise ValueError('Dispersion needs to be a real number!')
			if SpectrumRange is not None:
				raise ValueError("You don't need to define a SpectrumRange and ZLP/dispersion!")
			self.ZLP = self.FindZLP(self.data)
			self.dispersion = dispersion
			self.SpectrumRange = np.arange(0 - self.ZLP, self.size[2] - self.ZLP) * self.dispersion
		elif SpectrumRange is not None:
			if len(SpectrumRange) != self.size[2]:
				raise ValueError("Your SpectrumRange is not the same size as your energy axis!")
			self.SpectrumRange = SpectrumRange
			self.dispersion = SpectrumRange[1] - SpectrumRange[0]
		elif channel_eV:
			if len(channel_eV) != 2:
				raise ValueError('channel_eV must have length 2!')
			if not isinstance(dispersion, numbers.Real):
				raise ValueError('Dispersion needs to be a real number!')
			eV0 = channel_eV[1] - channel_eV[0] * dispersion
			self.SpectrumRange = np.linspace(
						eV0, 
						eV0 + (self.size[2] - 1) * dispersion,
						self.size[2]
						)
			self.dispersion = dispersion
		else:
			raise ValueError('You need to input an energy calibration!')
		
		self.metadata = metadata
		self.unit_label = 'Energy'
		self.secondary_units = 'nm'
		self.secondary_unit_label = 'Wavelength'
		
		self.spectrum_unit_label = 'Energy'
		self.spectrum_secondary_units = 'nm'
		self.spectrum_secondary_unit_label = 'Wavelength'

	@classmethod
	def LoadFromDM3(cls, filename, spectrum_calibrated = True):
		SI, metadata = import_EELS_dm3(filename)
		dispersion = float(metadata['root']['ImageList']['1']['ImageData']['Calibrations']['Dimension']['2']['Scale'])
		drifttube = float(metadata['root']['ImageList']['1']['ImageTags']['EELS']['Acquisition']['Spectrometer']['Energy loss (eV)'])
		zero = float(metadata['root']['ImageList']['1']['ImageData']['Calibrations']['Dimension']['2']['Origin'])
		print(dispersion, drifttube, zero)
		if zero >= 0:
			ZLP = True
		else: 
			ZLP = False
		if spectrum_calibrated is True:
			channel_eV = [0, -zero * dispersion]
		else:
			channel_eV = None
		print((dispersion), channel_eV)
		return cls(SI = SI, dispersion = dispersion, ZLP = ZLP, channel_eV = channel_eV, metadata = metadata)

	@staticmethod		
	def FindZLP(data):
		ZLP = int(stats.mode(np.argmax(data, axis = -1), axis=None)[0])
		return ZLP
	
	def FindZLPArray(self):
		ZLParray = np.argmax(self.data, axis=2)
		return ZLParray
	
	def AlignZLP(self):
		aligned = self.AlignChannel(self.FindZLPArray())
		return aligned
		
	def ExtractSpectrum(self, mask3D):
		extractedspectrum = Spectrum.EELSSpectrum(
			np.mean(np.mean(
			np.ma.masked_array(self.data, mask3D), 
			axis = 0), axis = 0), 
			SpectrumRange = self.SpectrumRange,
			units = self.spectrum_units)
		return extractedspectrum
		
	def Threshold(self, threshold):
		'''To mask out pixels with very little signal'''
		thrmask = np.less(self.data.data[:, :, self.ZLP], threshold)
#		self.thrmask = np.reshape(thrmask, (np.append(np.shape(thrmask), 1))) * np.ones(np.shape(self.data))
		self.data.mask = np.reshape(thrmask, (np.append(np.shape(thrmask), 1))) * np.ones(np.shape(self.data))
#		print(np.shape(self.data.mask))
#		print(np.shape(self.thrmask))
		
	def InvertThreshold(self):
		self.data.mask = np.invert(self.data.mask)
		
	def Normalize(self):
		'''Normalize data to integral'''
		self.normfactor = np.sum(self.data, axis=2, keepdims=True)

		data_norm = self.data/self.normfactor
		return data_norm
	
	def AlignChannel(self, indices):
		''' Input: indices=a 2D array of the same shape as the image dimensions
		containing the indices of where the desired channel is currently in the SI'''
		channelmax = np.max(np.max(indices))
		channelmin = np.min(np.min(indices))
		index1, index2 = np.meshgrid(range(self.size[0]), range(self.size[1]))
		index1 = np.expand_dims(np.transpose(index1), axis=2)
		index2 = np.expand_dims(np.transpose(index2), axis=2)
		index3 = np.expand_dims(np.expand_dims(range(self.size[2]) + channelmax, 
			axis=0), axis=0) - np.expand_dims(indices, axis=2)
		aligned_data = np.zeros((self.size[0], self.size[1], self.size[2] + channelmax - channelmin))
		aligned_data[index1, index2, index3] = self.data
		return EELSSpectrumImage(aligned_data, 
			dispersion=self.dispersion, 
			spectrum_units = self.spectrum_units, 
			calibration=self.calibration)
		
	def eVSlice(self, starteV, stopeV):
		startchannel = int(starteV / self.dispersion + self.ZLP)
		stopchannel = int(stopeV / self.dispersion + self.ZLP)
		sliced = self.data[:, :, startchannel:stopchannel]
		return sliced
	
	def RLDeconvolution(self, RLiterations, PSF, threads=multiprocessing.cpu_count(), PSF_pad=0):
		'''Input: RLiterations=number of iterations to perform
			PSF=point spread function (an EELS spectrum object)
		Optional argument: 
			threads=number of computer's CPUs to use while deconvolving, default is all of them
			PSF_pad=value to pad PSF with (or None to not pad PSF)'''
		PSF_sym = PSF.SymmetrizeAroundZLP()
		del PSF
		if PSF_pad is not None:
			data_length = np.size(self.SpectrumRange) ##replace w/ self.size[2]
			PSF_length = np.size(PSF_sym.intensity)
			pad_length = int(data_length/2 - (1 + data_length) % 2 - PSF_length//2)
			if PSF_sym.ZLP < data_length/2:
				PSF_sym = PSF.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='left').SymmetrizeAroundZLP()
			elif PSF_sym.ZLP > data_length/2:
				PSF_sym = PSF_sym.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='right')
		print('Beginning deconvolution...')
		loopyP = partial(loopy, iterations=RLiterations, PSF=PSF_sym.Normalize().intensity)
		x_deconv = np.array(handythread.parallel_map(loopyP, abs(self.Normalize()), 
			threads = threads))
#		x_deconv = np.array(handythread.parallel_map(loopyP, self.Normalize(), 
#			threads = threads))
		x_deconv = np.ma.array(x_deconv, mask = self.data.mask)
		print('Done %s iterations!' %RLiterations)

		return EELSSpectrumImage(x_deconv, dispersion=self.dispersion)

	def FindFW(self, intensityfraction):
		'''Finds the full width of the ZLP at the requested fraction of intensity
		(for full width at half max, intensityfraction=0.5)'''
		lefttail = self.data[:,:,:self.ZLP][:,:,::-1]
		diff1 = lefttail - intensityfraction*np.expand_dims(self.data[:,:,self.ZLP], axis=2)
		left_index_1 = np.argmax(np.diff(np.sign(diff1)) != 0, axis=2)
		left_index_2 = left_index_1 + 1
		index1, index2 = np.meshgrid(range(self.size[0]), range(self.size[1]))
		index1 = np.transpose(index1)
		index2 = np.transpose(index2)
		left_energy = self.dispersion * self.SpectrumInterpolation(
				left_index_1,
				left_index_2,
				lefttail[index1, index2, left_index_1],
				lefttail[index1, index2, left_index_2], 
				intensityfraction*self.data[:,:,self.ZLP])+self.dispersion
	
		righttail = self.data[:,:,self.ZLP:]
		diff2 = righttail - intensityfraction*np.expand_dims(self.data[:,:,self.ZLP], axis=-1)
		right_index_1 = np.argmax(np.diff(np.sign(diff2)) != 0, axis=2) 
		right_index_2 = right_index_1 + 1
		right_energy = self.dispersion * self.SpectrumInterpolation(
				right_index_1,
				right_index_2,
				righttail[index1, index2, right_index_1],
				righttail[index1, index2, right_index_2], 
				intensityfraction*self.data[:,:,self.ZLP])
				
		FW = left_energy + right_energy
		return FW
	
	def SpectrumInterpolation(self, E1, E2, I1, I2, I_interp):
		'''Linear interpolation given two data points and the mid-value'''
		interpvalue = E1 + (E2 - E1)/(I2 - I1) * (I_interp-I1)
		return interpvalue
		
		
#Richardson-Lucy algorithm
def RL(iterations, PSF_norm, Spec):
	RL4 = Spec.copy()
	for ii in range(iterations):
		RL1 = np.convolve(PSF_norm, RL4, 'same')
		RL2 = Spec/RL1
		RL3 = np.convolve(PSF_norm, RL2, 'same')
		RL4 *= RL3
	return RL4

#Looping function for deconvolution of spectrum images
def loopy(SIline, iterations, PSF):
    xloop = np.shape(SIline)[0]
    SIline_deconv = np.zeros([xloop, np.shape(SIline)[1]])
    for xx in range(xloop):
        SIline_deconv[xx,:] = RL(iterations, PSF, SIline[xx, :])
    return SIline_deconv
