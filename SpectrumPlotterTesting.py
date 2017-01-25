import numpy as np
import Spectrum
import SpectrumPlotter
import CLSpectrumData
import SpectrumImagePlotter
import matplotlib.pyplot as plt
import SpectrumImage
import os

#### Testing Spectrum and SpectrumPlotter
PSFfolder = '/home/isobel/Documents/McMaster/EELS/2016-04-18/Sq1A_(1,8)'
PSFfilename = 'Spectrum_ZLP.csv'
Spectrumfilename = 'Processed/Spectrum_1.csv'
spectrum = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(PSFfolder, Spectrumfilename))
Spectrumsmooth = Spectrum.EELSSpectrum(spectrum.SmoothingFilter1D(sigma=2))

#PSF = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(PSFfolder, PSFfilename))
#PSFsmooth = Spectrum.EELSSpectrum(PSF.SmoothingFilter1D())

s = np.random.random(100)*0.00003
wvl = np.arange(500, 600)
SCL = Spectrum.CLSpectrum(s, wvl)
fig = plt.figure()
ax = plt.axes()
s = SpectrumPlotter.SpectrumManager(spectrum, ax)
s.update_spectrum(Spectrumsmooth, 1)
s.update_spectrum(SCL, 'CL')
plt.show()
#S.SaveSpectrumAsCSV('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/test.csv')


### Spike removal testing

#folder = '/home/isobel/Documents/McMaster/CL/T9-3_Sq1A_(1,3)/'
#filebase = 'T9-3_Sq1A_(1,3)v_Gr800at750_30keV_Ap3Spot4_2s_noQWP_noPol_SiN.h5'
#cl = CLSpectrumData.CLDataSet.LoadFromFile(folder + filebase)
#S1 = SpectrumImagePlotter.SpectrumImagePlotter(cl.SI)
#g, c = cl.SI.SpikeRemoval(100)
##g = SpectrumImage.CLSpectrumImage(g.SI, cl.SI.SpectrumRange)
#S2 = SpectrumImagePlotter.SpectrumImagePlotter(g)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.imshow(c[:,:,158],interpolation='none',cmap='gray')

#plt.show()
