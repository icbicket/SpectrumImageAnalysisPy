from __future__ import division
import Spectrum
import SpectrumPlotter
import os
import matplotlib.pyplot as plt
import numpy as np
import collections
import RMS
from scipy import signal
import csv

def WriteToCSV(filename):
		if os.path.exists(filename):
			filename = filename[:-4] + '-1' + filename[-4:]
		print('Saving...', filename)
		ExportIterationNum = np.copy(iterations)
		ExportRMS = np.copy(error)
		ExportIterationNum.resize(len(ExportIterationNum), 1)
		ExportRMS.resize(len(ExportRMS), 1)
		ExportData = np.append(ExportIterationNum, ExportRMS, axis = 1)
		ExportHeaders = ['Iteration number' , 'RMS Error']
		with open(filename, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = '	')
			writer.writerow(ExportHeaders)
			writer.writerows(ExportData)

# Import test data (simulated spectrum from Bellido et al (2014)
folder = 'TestCase'
spec1name = 'SimRod_(60,0)_10meV.csv'

# Plot original data
spec1 = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(folder, spec1name))
spec1plot = SpectrumPlotter.SpectrumManager(spec1)

# Create point spread function (PSF)
PSF_Gauss = Spectrum.EELSSpectrum(signal.gaussian(801, std=np.sqrt(2)), 
	dispersion=0.01, ZLP=True)

# Convolve simulated data with PSF
conv = np.convolve(PSF_Gauss.intensity, spec1.intensity)
spec2 = Spectrum.EELSSpectrum(conv/np.max(conv), 
	dispersion=0.01, ZLP=True)

# Plot PSF and convolved (blurred) spectra
spec1plot.update_spectrum(PSF_Gauss, ID='PSF Gauss')
spec1plot.update_spectrum(spec2, ID='Convolved')
spec1plot.add_legend()

iterations = np.append(np.arange(1, 1000), np.array([2000, 2500, 3000, 3500, 4000, 4500, 5000]))
spec2RL = collections.OrderedDict()
error = []
PSF_sym = PSF_Gauss.RL_PSFsym(PSF_Gauss, PSF_pad=None)

# Calculate results of deconvolution for sets of different numbers of iterations and root mean square error compared to actual spectrum
for ii in iterations:
	spec2RL[ii] = spec2.RLDeconvolution(ii, PSF_sym)
	spec2RL[ii].intensity = spec2RL[ii].intensity/np.max(spec2RL[ii].intensity)
	error.append(RMS.RMS(spec2RL[ii].eVSlice(-0.1, 4), spec1.eVSlice(-0.1, 4)))

# Plot RMS error
fig_error = plt.figure('RMS error')
ax_error = fig_error.add_subplot(111)
ax_error.plot(iterations, error)
ax_error.set_ylabel('Root mean square error')
ax_error.set_xlabel('Iteration number')
plt.show()

RMS_error_filename = 'RMS error - SimNoNoise.csv'
WriteToCSV(os.path.join(folder, RMS_error_filename))
