from __future__ import division
import os
import hyperspy.api as hs
import Spectrum
import matplotlib.pyplot as plt
import numpy as np
import collections
import RMS
from scipy import signal
import csv


# Import test data (simulated spectrum from Bellido et al (2014)
folder = 'TestCase'
spec1name = 'SimRod_(60,0)_10meV.csv'

# Load original data
spec1 = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(folder, spec1name))

# Create point spread function (PSF)
PSF_Gauss = Spectrum.EELSSpectrum(signal.gaussian(881, std=np.sqrt(2)), 
	dispersion=0.01, ZLP=True)

# Convolve simulated data with PSF
conv = np.convolve(PSF_Gauss.intensity, spec1.intensity, 'same')
spec2 = Spectrum.EELSSpectrum(conv/np.max(conv), 
	dispersion=0.01, ZLP=True)
	
# Load convolved data into hyperspy
data = hs.signals.Signal1D(spec2.intensity)
data.set_signal_type('EELS')
psf = hs.signals.Signal1D(PSF_Gauss.intensity)
psf.set_signal_type('EELS')

deconv = data.richardson_lucy_deconvolution(psf, iterations=1)

plt.plot(deconv.data)
plt.show()
