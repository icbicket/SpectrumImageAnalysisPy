import CLSystemReferenceImport as CLSRI
import numpy as np
import matplotlib.pyplot as plt

wvlcorr = CLSRI.SystemCorrectionFactor(1250, 1100)
wvlIR = CLSRI.WavelengthCorrectionFactor(1250, 1100)


wvlVis = CLSRI.WavelengthCorrectionFactor(800, 750).wavelength
wvlcorrvis = CLSRI.SystemCorrectionFactor(800, 750, wvlVis)

wvlcorr2000 = CLSRI.SystemCorrectionFactor(2000, 1600)
wvlIR2000 = CLSRI.WavelengthCorrectionFactor(2000, 1600)

wvlcorr2000_2 = CLSRI.SystemCorrectionFactor(2000, 1500)
wvlIR2000_2 = CLSRI.WavelengthCorrectionFactor(2000, 1500)

plt.plot(wvlVis, wvlcorrvis.correction_spectrum.intensity, 'b')
plt.plot(wvlIR.wavelength, wvlcorr.correction_spectrum.intensity, 'r')
plt.plot(wvlIR2000.wavelength, wvlcorr2000.correction_spectrum.intensity, 'g')
plt.plot(wvlIR2000_2.wavelength, wvlcorr2000_2.correction_spectrum.intensity, 'k')

plt.show()
