from __future__ import division
import SpectrumImage
import Spectrum
import SpectrumImagePlotter
import SpectrumPlotter
import Image
import collections
import ImagePlotter
import os
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting, powerlaws
import numpy as np
from sklearn import datasets, linear_model

filefolder = '/home/isobel/Documents/McMaster/EELS/2017-03-31 - inverse Sierpinskis/SiN3'
filename = 'EELS Spectrum Image (dark ref corrected).dm3'

SI = SpectrumImage.EELSSpectrumImage.LoadFromDM3(os.path.join(filefolder, filename))
SI_norm = SpectrumImage.EELSSpectrumImage(SI.Normalize())

P1 = SpectrumImagePlotter.SpectrumImagePlotter(SI)
P2 = SpectrumImagePlotter.SpectrumImagePlotter(SI_norm)

FWHM = Image.Image(SI.FindFW(0.5))
IP1 = ImagePlotter.ImagePlotter(FWHM)

plt.figure()
FWHM_line = SI.FindFW(0.5).flatten()
plt.plot(FWHM_line)

plt.figure()
FWHM_fft = np.fft.fft(FWHM_line)
plt.plot(FWHM_fft)

PSF = Spectrum.EELSSpectrum(np.average(np.average(SI.data, axis=0), axis=0))
SP1 = SpectrumPlotter.SpectrumManager(PSF, cmap=plt.get_cmap('nipy_spectral'))

L = models.Lorentz1D(amplitude=np.max(PSF.intensity)/2., x_0=0, fwhm=0.005)
G = models.Gaussian1D(amplitude=np.max(PSF.intensity), mean=0., stddev=0.005)

Lrange = np.arange(-20, 20, 0.005)
Lorentzmodel = Spectrum.EELSSpectrum(L(Lrange), SpectrumRange=Lrange)
Gaussmodel = Spectrum.EELSSpectrum(G(Lrange), SpectrumRange=Lrange)
SP1.update_spectrum(Lorentzmodel, 'Lorentz_model')
SP1.update_spectrum(Gaussmodel, 'Gauss_model')

LConvolved = np.convolve(L(Lrange)[::-1], PSF.intensity, 'same')
GConvolved = np.convolve(G(Lrange)[::-1], PSF.intensity, 'same')
minE = np.min(PSF.SpectrumRange)
maxE = np.max(PSF.SpectrumRange)

LConvolved = LConvolved/np.max(LConvolved) * np.max(PSF.intensity)
GConvolved = GConvolved/np.max(GConvolved) * np.max(PSF.intensity)
PSF_Lfat = Spectrum.EELSSpectrum(LConvolved)
PSF_Gfat = Spectrum.EELSSpectrum(GConvolved)

minI = PSF_Lfat.ZLP + (minE/PSF.dispersion)
maxI = PSF_Lfat.ZLP + (maxE/PSF.dispersion)+1

SP1.update_spectrum(PSF_Lfat, 'Lorentz fat')
SP1.update_spectrum(PSF_Gfat, 'Gauss fat')

FWHM_L = PSF_Lfat.FindFW(0.5)
FWHM_G = PSF_Gfat.FindFW(0.5)

upperlim = FWHM_line[FWHM_line<0.06935]
argminL = (np.abs(FWHM.data.flatten() - FWHM_L)).argmin()
argminL_0 = int(np.floor(argminL/FWHM.data.shape[1]))
argminL_1 = (FWHM.data.shape[1] * (argminL/FWHM.data.shape[1] - argminL_0))

PSF_ex1 = Spectrum.EELSSpectrum(SI.data[48, 47, :]/np.max(SI.data[48, 47, :])*np.max(PSF.intensity))
SP1.update_spectrum(PSF_ex1, 'close experiment')

diff_L = Spectrum.EELSSpectrum(PSF_ex1.intensity-PSF_Lfat.intensity[int(minI):int(maxI)]
                            , SpectrumRange=PSF_ex1.SpectrumRange)
SP1.update_spectrum(diff_L, 'Difference Lorentz')
SP1.add_legend()


LorentzFits = {}
LorentzModel = {}
LorentzConvolved = {}
PSF_Lorentz = {}
PSF_Lorentz_FWHM = collections.OrderedDict()
SP2 = SpectrumPlotter.SpectrumManager(PSF, cmap=plt.get_cmap('nipy_spectral'))
SP3 = SpectrumPlotter.SpectrumManager(PSF, cmap=plt.get_cmap('nipy_spectral'))

for ff in np.linspace(0.002, 0.091, 10):
    LorentzFits[ff] = models.Lorentz1D(amplitude=np.max(PSF.intensity)/2., x_0=0, fwhm=ff)
    LorentzModel[ff] = Spectrum.EELSSpectrum(LorentzFits[ff](Lrange), SpectrumRange=Lrange)
    SP2.update_spectrum(LorentzModel[ff], str(ff))
    LorentzConvolved[ff] = np.convolve(LorentzFits[ff](Lrange)[::-1], PSF.intensity, 'same')
    LorentzConvolved[ff] = LorentzConvolved[ff]/np.max(LorentzConvolved[ff]) * np.max(PSF.intensity)
    PSF_Lorentz[ff] = Spectrum.EELSSpectrum(LorentzConvolved[ff], SpectrumRange=Lrange)
    PSF_Lorentz_FWHM[ff] = PSF_Lorentz[ff].FindFW(0.5)
    SP3.update_spectrum(PSF_Lorentz[ff], str(ff))
    
for ff in np.linspace(0.001, 0.09, 10):
    LorentzFits[ff] = models.Lorentz1D(amplitude=np.max(PSF.intensity), x_0=0, fwhm=ff)
    LorentzModel[ff] = Spectrum.EELSSpectrum(LorentzFits[ff](Lrange), SpectrumRange=Lrange)
    SP2.update_spectrum(LorentzModel[ff], str(ff))
    LorentzConvolved[ff] = np.convolve(LorentzFits[ff](Lrange)[::-1], PSF.intensity, 'same')
    LorentzConvolved[ff] = LorentzConvolved[ff]/np.max(LorentzConvolved[ff]) * np.max(PSF.intensity)
    PSF_Lorentz[ff] = Spectrum.EELSSpectrum(LorentzConvolved[ff], SpectrumRange=Lrange)
    PSF_Lorentz_FWHM[ff] = PSF_Lorentz[ff].FindFW(0.5)
    SP3.update_spectrum(PSF_Lorentz[ff], (str(ff)+'full'))
    
SP2.add_legend()
SP3.add_legend()

plt.figure()
plt.plot(PSF_Lorentz_FWHM.values(), PSF_Lorentz_FWHM.keys(), 'ro')

regr = linear_model.LinearRegression()
y = np.array(PSF_Lorentz_FWHM.keys())
x = np.array(PSF_Lorentz_FWHM.values()).reshape((20,1))

regr.fit(x, y)
valuefit = regr.predict(x)
plt.plot(x, valuefit, 'b-')

PSF_SI = SpectrumImage.EELSSpectrumImage(np.ones((SI.size)) * PSF.intensity, ZLP=True, dispersion=SI.dispersion)
PSF_SI_m = SpectrumImage.EELSSpectrumImage(np.ones((SI.size)) * PSF.intensity, ZLP=True, dispersion=SI.dispersion)

L_FWHM_line = regr.predict(FWHM_line.reshape(len(FWHM_line), 1)).reshape(FWHM.size)
L_FWHM_line[L_FWHM_line < 0] = 0

xx_yy = np.array(np.meshgrid(range(FWHM.size[0]), range(FWHM.size[1])))
x = xx_yy[0].flatten()
y = xx_yy[1].flatten()

for xx, yy in zip(x,y):
    if L_FWHM_line[xx, yy] > 0:
        LorentzFit = models.Lorentz1D(amplitude=np.max(PSF.intensity), x_0=0, fwhm=L_FWHM_line[xx, yy])
        PSF_Lorentz = np.convolve(LorentzFit(Lrange)[::-1][int(minI):int(maxI)], PSF.intensity, 'same')
        MoffatFit = models.Moffat1D(amplitude=np.max(PSF.intensity), x_0=0, gamma=L_FWHM_line[xx, yy]/2., alpha=0.95)
        PSF_Moffat = np.convolve(MoffatFit(Lrange)[::-1][int(minI):int(maxI)], PSF.intensity, 'same')
    else: 
        PSF_Lorentz = PSF.intensity
        PSF_Moffat = PSF.intensity
    PSF_SI.data[xx, yy, :] = PSF_Lorentz/np.max(PSF_Lorentz)
    PSF_SI_m.data[xx, yy, :] = PSF_Lorentz/np.max(PSF_Lorentz)

Spectest1 = Spectrum.EELSSpectrum(PSF_SI.data[46, 38, :], ZLP=True, dispersion=0.005)
Spectest2 = Spectrum.EELSSpectrum(SI.data[46, 38, :]/SI.data[38, 29, SI.ZLP], ZLP=True, dispersion=0.005)
SP4 = SpectrumPlotter.SpectrumManager(Spectest1, cmap=plt.get_cmap('nipy_spectral'))
SP4.update_spectrum(Spectest2, 'Raw data')
SP4.add_legend()

PSF_plot = SpectrumImagePlotter.SpectrumImagePlotter(PSF_SI)
RLiterations = 15
SI2 = SI.RLDeconvolution(RLiterations, PSF, threads=8)

PSF_SI2 = SI.RLDeconvolution_Adaptive(RLiterations, PSF_SI, threads=8)
#PSF_SI3 = SI.RLDeconvolution_Adaptive(RLiterations, PSF_SI_m, threads=8)

PSF_RL1 = SpectrumImagePlotter.SpectrumImagePlotter(SI2)
PSF_RL2 = SpectrumImagePlotter.SpectrumImagePlotter(PSF_SI2)
#PSF_RL3 = SpectrumImagePlotter.SpectrumImagePlotter(PSF_SI3)
PSF_RL2.ShowPlot()
