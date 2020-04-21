from __future__ import division
import Spectrum
import SpectrumPlotter
import os
import matplotlib.pyplot as plt
import numpy as np
import collections
import rms
import snr
from scipy import signal
import csv
import itertools

def WriteToCSV(filename, data, heading2):
    if os.path.exists(filename):
        filename = filename[:-4] + '-1' + filename[-4:]
    print('Saving...', filename)
    ExportIterationNum = np.copy(iterations)
    Exportdata = np.copy(data)
    ExportIterationNum.resize(len(ExportIterationNum), 1)
    Exportdata.resize(len(Exportdata), 1)
    ExportData = np.append(ExportIterationNum, Exportdata, axis = 1)
    ExportHeaders = ['Iteration number', heading2]
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = u'\t')
        writer.writerow(ExportHeaders)
        writer.writerows(ExportData)

# Import test data (simulated spectrum from Bellido et al (2014)
folder = 'TestCase'
spec1name = 'SimRod_(60,0)_10meV.csv'
psfname = 'PSF_exp.csv'

# Import and plot original data
spec1 = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(folder, spec1name))
spec1plot = SpectrumPlotter.SpectrumManager(spec1, cmap=plt.get_cmap('brg'))

# Import and plot original psf
psf = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(folder, psfname))
psf.intensity = psf.intensity/np.max(psf.intensity)
psf.SpectrumRange = np.append(psf.SpectrumRange[1:], psf.SpectrumRange[-1] + psf.dispersion)
spec1plot.update_spectrum(psf, ID='PSF')

# Convolve data with PSF
conv = np.convolve(psf.intensity, spec1.intensity, 'same')
spec_conv = Spectrum.EELSSpectrum(conv/np.max(conv), ZLP=True, dispersion=0.01)
spec1plot.update_spectrum(spec_conv, ID='conv')

# Make poisson noise
noise = np.random.poisson(spec_conv.intensity/np.min(spec_conv.intensity))

# Noisy data
noised = spec_conv.intensity + noise
spec_noise = Spectrum.EELSSpectrum(noised/np.max(noised), SpectrumRange=spec_conv.SpectrumRange)
spec1plot.update_spectrum(spec_noise, ID='noisy')

iterations = np.arange(2001)
#iterations = np.array([0, 1, 10, 50, 107, 123, 293, 350, 1000, 2000])
#iterations = np.arange(100)
specRL = collections.OrderedDict()
error = []
snr_zlp = []
snr_plasmon = []
psf_sym = psf.RL_PSFsym(psf, PSF_pad=0)

# Calculate results of deconvolution for sets of different numbers of iterations and root mean square error compared to actual spectrum
for ii in iterations:
    specRL[ii] = spec_noise.RLDeconvolution(ii, psf_sym)
    specRL[ii].intensity = specRL[ii].intensity/np.max(specRL[ii].intensity)
    error.append(rms.rms(specRL[ii].eVSlice(-0.1, 4), spec1.eVSlice(-0.1, 4)))
    snr_zlp.append(snr.snr(specRL[ii].eVSlice(-0.1, 0.1), spec1.eVSlice(-0.1, 0.1)))
    snr_plasmon.append(snr.snr(specRL[ii].eVSlice(0.1, 4.0), spec1.eVSlice(0.1, 4.0)))

conv_plot = SpectrumPlotter.SpectrumManager(specRL[0], cmap=plt.get_cmap('brg'), currentID='RL'+str(0))

plotids = np.array([1, 50, 107, 123, 293, 350, 1000, 2000])
for ii in plotids:
    conv_plot.update_spectrum(specRL[ii], ID='RL'+str(ii))

lines = itertools.cycle(('-', '--', '-.', ':'))
for pp in spec1plot.axis.lines:
    plt.setp(pp, linestyle=next(lines), lw=2)
    
for pp in conv_plot.axis.lines:
    plt.setp(pp, linestyle=next(lines), lw=2)

spec1plot.add_legend()
conv_plot.add_legend()

## Plot RMS error
fig_error = plt.figure('RMS error')
ax_error = fig_error.add_subplot(111)
ax_error.plot(iterations, error)
ax_error.set_ylabel('Root mean square error')
ax_error.set_xlabel('Iteration number')

## Plot signal to noise ratio
fig_snr = plt.figure('snr')
ax_snr = fig_snr.add_subplot(111)
ax_snr.plot(iterations, snr_zlp, label='ZLP')
ax_snr.set_ylabel('Signal to noise ratio')
ax_snr.set_xlabel('Iteration number')
ax_snr.plot(iterations, snr_plasmon, label='plasmon')
ax_snr.legend()
plt.show()

rms_error_filename = 'RMS error - SimNoise exp_PSF.csv'
snr_zlp_filename = 'SNR_zlp - SimNoise exp_PSF.csv'
snr_plasmon_filename = 'SNR_plasmon - SimNoise exp_PSF.csv'
#WriteToCSV(os.path.join(folder, rms_error_filename), error, 'RMS error')
#WriteToCSV(os.path.join(folder, snr_zlp_filename), snr_zlp, 'SNR ZLP')
#WriteToCSV(os.path.join(folder, snr_plasmon_filename), snr_plasmon, 'SNR plasmon')
