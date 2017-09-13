from __future__ import print_function
import numpy as np
import SpectrumImage as SI
import hyperspy.api as hp
import SpectrumImagePlotter as SIP
import Spectrum as S
import matplotlib.pyplot as plt
import SpectrumPlotter


###Testing SIPlotter with real data!
folder = '/home/isobel/Documents/McMaster/EELS/Stars/2015 02 11/'
filebase = 'EELS Spectrum Image (dark ref corrected)-4.dm3'
s = hp.load(folder+filebase)
eels = SI.EELSSpectrumImage(s.data, dispersion=0.01)
PSF = S.EELSSpectrum(eels.data[0,0,:], dispersion=0.01)

pad_length = int(round(1023-(np.shape(PSF.SymmetrizeAroundZLP().intensity)[0]-1)/2))
print('intest', type(pad_length))
#PSF_pad = S.EELSSpectrum(np.append(np.zeros((pad_length, 1)), PSF.intensity), dispersion=0.01).SymmetrizeAroundZLP()

PSF_pad = PSF.PadSpectrum(pad_length, pad_value=0, pad_side='left')
PSF_reverse = S.EELSSpectrum(eels.data[0,0,::-1], dispersion=0.01)

fig = plt.figure()
ax = plt.axes()
s = SpectrumPlotter.SpectrumManager(PSF, ax)
s.update_spectrum(PSF_pad, 'pad')

P1 = SIP.SpectrumImagePlotter(eels)

eels10 = eels.RLDeconvolution(1, PSF, PSF_pad=0)
eels10_pad = eels.RLDeconvolution(1, PSF_pad, PSF_pad=None)

P2 = SIP.SpectrumImagePlotter(eels10)
P3 = SIP.SpectrumImagePlotter(eels10_pad)

P1.ShowPlot()
