import hyperspy.api as hp
import numpy as np
import matplotlib.pyplot as plt
import SpectrumPlotter
import ImagePlotter
from skimage import data
import Image
import SpectrumImage
import SpectrumImagePlotter
import Spectrum
import CLSpectrumData

'''
Turn spectra on and off with enter - multiple spectra plotted at once
Copy colour scheme over from patches to spectra and extracted image
'''

## Testing Spectrum and SpectrumPlotter
#s = np.random.random(100)
#wvl = np.arange(500, 600)
#S = Spectrum.EELSSpectrum(s, dispersion=0.1)
#fig = plt.figure()
#ax = plt.axes([0.1, 0.1, 0.8, 0.8])
#s = SpectrumPlotter.SpectrumPlotter(S, ax)
#plt.show()

#Im = Image.Image(data.chelsea()[:, :, 0], calibration=5e-9)



#Testing SpectrumPlotter
#x = np.transpose(np.arange(0,4))
#y = np.transpose(np.random.random(4))

###x = np.arange(50)*0.01
###y = np.random.random(50)



## Testing ImagePlotter
#Im = np.random.random((2000,2000))
#a = ImagePlotter.ImagePlotter(ax, Im)

#### Testing SIPlotter
#SIdata = np.random.random(size = (20,20,50))
#SIdata[:, :, 10] = 2
#SI = SpectrumImage.EELSSpectrumImage(SIdata, dispersion=0.01)
#SpectrumImagePlotter.SpectrumImagePlotter(SI)
#plt.show()

####Testing SIPlotter with real data!
#folder = '/home/isobel/Documents/McMaster/EELS/2016-07-29/SI1/'
#filebase = 'EELS Spectrum Image (aligned) (aligned).dm3'
#s = hp.load(folder+filebase)
#eels = SpectrumImage.EELSSpectrumImage(s.data)
#SpectrumImagePlotter.SpectrumImagePlotter(eels)
#plt.show()

folderCL = '/home/isobel/Documents/McMaster/CL/T9-3_Sq1A_(1,3)/'
fileCL = 'T9-3_Sq1A_(1,3)h_Gr800at750_30keV_Ap3Spot4_2s_Slit12185um_QWP0_Pol0_full.h5'
cl = CLSpectrumData.CLDataSet.LoadFromFile(folderCL + fileCL)

SpectrumImagePlotter.SpectrumImagePlotter(cl.SI)
plt.show()
