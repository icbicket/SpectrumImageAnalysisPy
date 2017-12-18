from __future__ import division
import Spectrum
import SpectrumPlotter
import os
import matplotlib.pyplot as plt
import numpy as np
import collections
import rms

folder = 'TestCase'

spec1name = 'SimRod_(60,0).csv'
spec1 = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(folder, spec1name))
spec1plot = SpectrumPlotter.SpectrumManager(spec1)

blankPSF = np.zeros(np.size(spec1.intensity))
blankPSF[int(len(blankPSF)/2)] = 1
blankPSF = Spectrum.EELSSpectrum(blankPSF, ZLP=True, dispersion=spec1.dispersion)

iterations = np.array([0, 1, 5, 10, 50, 100, 500, 1000, 5000])
spec1RL = collections.OrderedDict()
error = []
for ii in iterations:
	spec1RL[ii] = spec1.RLDeconvolution(ii, blankPSF)
	spec1plot.update_spectrum(spec1RL[ii], ID='RL' + str(ii))
	error.append(rms.rms(spec1RL[ii].intensity, spec1.intensity))
spec1plot.add_legend()

fig_error = plt.figure('RMS error')
plt.plot(iterations, error)
plt.show()
