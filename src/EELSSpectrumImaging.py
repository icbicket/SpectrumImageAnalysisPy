from __future__ import print_function
from hyperspy.api import load
#import hyperspy.api as hp
import numpy as np
import SpectrumImage
import SpectrumImagePlotter
import Spectrum
import os
folder = '/home/isobel/Documents/McMaster/Sierpinski/2016-07-27 - Sierpinski Ag/SI12'
filebase = 'EELS Spectrum Image (dark ref corrected).dm3'
savefolder = os.path.join(folder, 'Processed')
print(folder, filebase)
PSFfolder = folder
PSFfilename = 'Spectrum_ZLP.csv'
s = load(os.path.join(folder, filebase))
dispersion=s.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup2.Scale

eels = SpectrumImage.EELSSpectrumImage(s.data, dispersion=dispersion)

PSF = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(PSFfolder, PSFfilename))

print(PSF.FindFW(0.5))
eels.Threshold(1000)
import matplotlib.pyplot as plt
plt.imshow(eels.data[:,:,eels.ZLP])
plt.show()

RLiterations = 25
eels2 = eels.RLDeconvolution(RLiterations, PSF, threads=7)

p1=SpectrumImagePlotter.SpectrumImagePlotter(eels, filepath=os.path.join(savefolder))
p2 = SpectrumImagePlotter.SpectrumImagePlotter(eels2, filepath=os.path.join(savefolder, str(RLiterations) + 'RL'))

p2.ShowPlot()
