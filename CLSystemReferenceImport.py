import csv
import numpy as np
import re
import Spectrum
#import matplotlib.pyplot as plt

def ReadCSVRef(filename):
	with open(filename) as csvfile:
		 reader = csv.reader(csvfile, delimiter=',')
		 headers = filter(None, reader.next())
		 data = []
		 for row in reader:
			data.append(row[:-1])
	data = np.array(data)
	data[data == ''] = np.nan
	data = data.astype(float)
	print np.shape(headers), np.shape(data)
	dataDict = {}
	i = 0
	columns_per_data = np.shape(data[0])[0]/np.shape(headers)[0]
	for hh in headers[:-1]:
		label = tuple(map(int, re.findall(r'\d+', hh)))
		dataDict[label] = data[:, i:i+columns_per_data]
		i+= 2
	return dataDict



# Add error-checking for entering a non-existent grating/wavelength pair
class SystemCorrectionFactor(object):
	def __init__(self, grating, center_wavelength, wavelengths = None):
		self.grating = grating
		self.center_wavelength = center_wavelength
		if grating >= 1000:
			self.correction_spectrum = self.ImportIR()
		elif wavelengths is not None:
			self.correction_spectrum = self.ImportVis(wavelengths)
		else:
			print 'No valid reference for system correction!'
		
	def ImportIR(self):
		filename = '/home/isobel/Documents/McMaster/CL/SystemResponseFcns/CorrectionFactorSCAlIRCamera_2015_02_26.csv'
		dataDict = ReadCSVRef(filename)
		d = dataDict[self.grating, self.center_wavelength]
		correction_spectrum = Spectrum.CLSpectrum(d[:,1], d[:,0])
		return correction_spectrum
		
	def ImportVis(self, wavelengths):
		filename = '/home/isobel/Documents/McMaster/CL/SystemResponseFcns/SystemResponseVISInterpolated_20150717.csv'
		dataDict = ReadCSVRef(filename)
		d = dataDict[(self.grating,)]
		spectrum_interp = np.interp(wavelengths, d[:, 0], d[:, 1])
		correction_spectrum = Spectrum.CLSpectrum(spectrum_interp, wavelengths)
		return correction_spectrum
		
class WavelengthCorrectionFactor(object):
	def __init__(self, grating, center_wavelength):
		self.grating = grating
		self.center_wavelength = center_wavelength
		if grating == (1250 or 1600 or 2000):
			self.wavelength = self.importIRwavelengths()
		elif grating == (500 or 800):
			self.wavelength = self.importVISwavelengths()
		else:
			print 'No valid reference for wavelength correction!'
			
	def importIRwavelengths(self):
		filename = '/home/isobel/Documents/McMaster/CL/SystemResponseFcns/WinspecCorrWavelengthsIR20150428.csv'
		dataDict = ReadCSVRef(filename)
		correction_spectrum = dataDict[self.grating, self.center_wavelength]
		return correction_spectrum
		
	def importIRwavelengths(self):
		filename = '/home/isobel/Documents/McMaster/CL/SystemResponseFcns/WinspecCorrWavelengthsVIS20150428.csv'
		dataDict = ReadCSVRef(filename)
		correction_spectrum = dataDict[self.grating, self.center_wavelength]
		return correction_spectrum

#wvls = np.linspace(400, 980)
#p = SystemCorrectionFactor(800, 750, wvls)

#print np.shape(p.correction_spectrum.SpectrumRange)
#plt.plot(p.correction_spectrum.SpectrumRange, p.correction_spectrum.intensity)
#plt.show()
