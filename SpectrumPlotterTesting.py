import numpy as np
import Spectrum
import SpectrumPlotter

# Testing Spectrum and SpectrumPlotter
s = np.random.random(100)
wvl = np.arange(500, 600)
S = Spectrum.CLSpectrum(s, wvl)
fig = plt.figure()
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
s = SpectrumPlotter.SpectrumManager(S, ax)
#plt.show()
S.SaveSpectrumAsCSV('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/test.csv')
