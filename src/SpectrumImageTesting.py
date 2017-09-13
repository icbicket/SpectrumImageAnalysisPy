from __future__ import print_function
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


#Im = Image.Image(data.chelsea()[:, :, 0], calibration=5e-9)




## Testing ImagePlotter
#Im = np.random.random((2000,2000))
#a = ImagePlotter.ImagePlotter(ax, Im)

#### Testing SIPlotter
#SIdata = np.random.random(size = (20,30,50))
#SIdata[:, :, 10] = 2
#SI = SpectrumImage.EELSSpectrumImage(SIdata, dispersion=0.01)
#plotter=SpectrumImagePlotter.SpectrumImagePlotter(SI)
#plt.show()

###Testing SIPlotter with real data!
folder = '/home/isobel/Documents/McMaster/EELS/2016-07-28/Sq2R_(1,7)/'
filebase = 'EELS Spectrum Image (dark ref corrected).dm3'
s = hp.load(folder+filebase)
eels = SpectrumImage.EELSSpectrumImage(s.data)
#PSF = Spectrum.EELSSpectrum.LoadFromCSV('/home/isobel/Documents/McMaster/EELS/2016-07-27/SI3/Processed/Spectrum_ZLP.csv')
#print(np.shape(PSF.intensity))
p1=SpectrumImagePlotter.SpectrumImagePlotter(eels, filepath=folder)
#eels2 = eels.RLDeconvolution(2, PSF)
#p2 = SpectrumImagePlotter.SpectrumImagePlotter(eels2)
p1.ShowPlot()


folderCL = '/home/isobel/Documents/McMaster/CL/T9-3_Sq1A_(1,3)/'
fileCL = 'T9-3_Sq1A_(1,3)h_Gr800at750_30keV_Ap3Spot4_2s_noQWP_noPol_full2.h5'
cl = CLSpectrumData.CLDataSet.LoadFromFile(folderCL + fileCL)

plotter = SpectrumImagePlotter.SpectrumImagePlotter(cl.SI)

plt.show()
#plotter.extractedim.SaveImgAsPNG('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/testIm.png', plotter.extractedim.Imglim)
#print(type(plotter.extractedim.data)==np.ma.MaskedArray)
