import Spectrum
import unittest
import collections
import numpy as np
import traceback

class EELSSpectrumTest(unittest.TestCase):
	def assertArraysEqual(self, array1, array2):
		self.assertTrue(np.array_equal(array1, array2), 'Arrays are not equal')
	
	def testPadSpectrumleft(self):
		#Pad the left side of the spectrum with 0s
		data = np.array([1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1])
		data_pad = np.array([0, 0, 0, 1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_pad = eels.PadSpectrum(3, pad_value=0, pad_side='left')
		self.assertArraysEqual(eels_pad.intensity, data_pad)
		
	def testPadSpectrumright(self):
		#Pad the right side of the spectrum with 0s
		data = np.array([1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1])
		data_pad = np.array([1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1, 0, 0, 0])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_pad = eels.PadSpectrum(3, pad_value=0, pad_side='right')
		self.assertArraysEqual(eels_pad.intensity, data_pad)
		
	def testPadSpectrumboth(self):
		#Pad both sides of the spectrum with 0s
		data = np.array([1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1])
		data_pad = np.array([0, 0, 0, 1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1, 0, 0, 0])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_pad = eels.PadSpectrum(3, pad_value=0, pad_side='both')
		self.assertArraysEqual(eels_pad.intensity, data_pad)
	
	def testSymmetrizeAroundZLPleft(self):
		#ZLP is in the left half of the spectrum
		data = np.array([1, 20, 35, 20, 1, 1, 1, 1, 1, 1, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_sym = eels.SymmetrizeAroundZLP()
		data_sym = np.array([1, 20, 35, 20, 1])
		self.assertArraysEqual(eels_sym.intensity, data_sym)
		
	def testSymmetrizeAroundZLPright(self):
		#ZLP is in the right half of the spectrum
		data = np.array([1, 1, 1, 1, 1, 1, 1, 20, 35, 20, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_sym = eels.SymmetrizeAroundZLP()
		data_sym = np.array([1, 20, 35, 20, 1])
		self.assertArraysEqual(eels_sym.intensity, data_sym)

	def testSymmetrizeAroundZLPcenter(self):
		#ZLP is exactly in the middle of the spectrum
		data = np.array([1, 1, 1, 1, 20, 35, 20, 1, 1, 1, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_sym = eels.SymmetrizeAroundZLP()
		self.assertArraysEqual(eels.intensity, eels_sym.intensity)

	def testSymmetrizeAroundZLPnegativevalues(self):
		#Spectrum contains negative values
		data = np.array([1, -1, 1, 1, 20, 35, 20, 1, -1, -1, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_sym = eels.SymmetrizeAroundZLP()
		data_positive = np.array([1, 0, 1, 1, 20, 35, 20, 1, 0, 0, 1])
		self.assertArraysEqual(data_positive, eels_sym.intensity)

	def testNormalize(self):
		#Test normalization to integrated intensity
		data = np.array([1, 20, 35, 20, 1, 1, 1, 1, 1, 1, 1])
		eels = Spectrum.EELSSpectrum(data, dispersion=0.2, ZLP=True)
		eels_norm = eels.Normalize()
		data_norm = data/83.
		self.assertArraysEqual(data_norm, eels_norm.intensity)
		
	def testeVSlice(self):
		data = np.array([35, 20, 1, 2, 3, 5, 4, 7, 6, 9, 8])
		Srange = np.arange(0, 10)
		eels = Spectrum.EELSSpectrum(data, SpectrumRange=Srange)
		sliced = eels.eVSlice(2, 5)
		self.assertArraysEqual(np.array([1, 2, 3]), sliced)
		
	def testeVSliceNoZLP(self):
		data = np.array([35, 20, 1, 28, 3, 5, 4, 7, 6, 9, 8])
		Srange = np.arange(10, 20)
		eels = Spectrum.EELSSpectrum(data, SpectrumRange=Srange)
		sliced = eels.eVSlice(11, 13)
		self.assertArraysEqual(np.array([20, 1]), sliced)
	
	def testeVSliceDispersionFloat(self):
		data = np.array([35, 20, 1, 28, 3, 5, 4, 7, 6, 9, 8, 15])
		Srange = np.linspace(10, 15, num=11)
		eels = Spectrum.EELSSpectrum(data, SpectrumRange=Srange)
		sliced = eels.eVSlice(11, 13)
		self.assertArraysEqual(np.array([1, 28, 3, 5]), sliced)
		
	def testeVSliceDispersionIrrational(self):
		data = np.array([35, 20, 1, 28, 3, 5, 4, 7, 6, 9, 8, 15])
		Srange = np.linspace(10, 15, num=10)
		eels = Spectrum.EELSSpectrum(data, SpectrumRange=Srange)
		sliced = eels.eVSlice(11, 13)
		self.assertArraysEqual(np.array([1, 28, 3]), sliced)
		
if __name__ == '__main__':
	unittest.main()	
