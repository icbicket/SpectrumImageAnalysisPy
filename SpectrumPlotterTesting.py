import numpy as np
import Spectrum
import SpectrumPlotter
import CLSpectrumData
import SpectrumImagePlotter
import matplotlib.pyplot as plt
import SpectrumImage

#### Testing Spectrum and SpectrumPlotter
#s = np.random.random(100)
#wvl = np.arange(500, 600)
#S = Spectrum.CLSpectrum(s, wvl)
#fig = plt.figure()
#ax = plt.axes([0.1, 0.1, 0.8, 0.8])
#s = SpectrumPlotter.SpectrumManager(S, ax)
##plt.show()
#S.SaveSpectrumAsCSV('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/test.csv')

### Spike removal testing

folder = '/home/isobel/Documents/McMaster/CL/T9-3_Sq1A_(1,3)/'
filebase = 'T9-3_Sq1A_(1,3)v_Gr800at750_30keV_Ap3Spot4_2s_noQWP_noPol_SiN.h5'
cl = CLSpectrumData.CLDataSet.LoadFromFile(folder + filebase)
S1 = SpectrumImagePlotter.SpectrumImagePlotter(cl.SI)
g, c = cl.SI.SpikeRemoval(100)
#g = SpectrumImage.CLSpectrumImage(g.SI, cl.SI.SpectrumRange)
S2 = SpectrumImagePlotter.SpectrumImagePlotter(g)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(c[:,:,158],interpolation='none',cmap='gray')

plt.show()
