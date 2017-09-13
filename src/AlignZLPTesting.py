from __future__ import print_function
import hyperspy.api as hp
import SpectrumImage
import SpectrumImagePlotter
import Image
import ImagePlotter
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import stats

#def FindZLPArray(array3d):
#	ZLPs = np.argmax(array3d, axis=2)
#	mode = stats.mode(ZLPs, axis=None)
#	print('max', np.max(np.max(ZLPs)))
#	print('min', np.min(np.min(ZLPs)))
#	return ZLPs, mode

#def AlignZLP(array3d, ZLPs):
#	ZLPmax = np.max(np.max(ZLPs))
#	ZLPmin = np.min(np.min(ZLPs))
#	shape = np.shape(array3d)
#	index1, index2 = np.meshgrid(range(shape[0]), range(shape[1]))
#	index1 = np.expand_dims(np.transpose(index1), axis=2)
#	index2 = np.expand_dims(np.transpose(index2), axis=2)
#	index3 = np.expand_dims(np.expand_dims(range(shape[2])+ZLPmax, axis=0), axis=0)-np.expand_dims(ZLPs, axis=2)
#	new_array = np.zeros((shape[0], shape[1], shape[2] + ZLPmax - ZLPmin))
#	new_array[index1, index2, index3] = array3d
#	return new_array

folder='/home/isobel/Documents/McMaster/EELS/2017-03-16/SI-028'
filename = 'EELS Spectrum Image.dm3'
filepath = os.path.join(folder, filename)

s = hp.load(filepath)
dispersion = s.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup2.Scale

eels = SpectrumImage.EELSSpectrumImage(s.data, dispersion=dispersion)
#ZLPs, ZLPmode = FindZLPArray(eels.data)
new_eels = eels.AlignZLP()
#new_ZLP = SpectrumImage.EELSSpectrumImage(AlignZLP(eels.data, ZLPs), dispersion=dispersion)
#ZLPim = Image.Image(ZLPs)

FWHM = new_eels.FindFW(0.5)
FWHMim = Image.Image(FWHM)



p1 = SpectrumImagePlotter.SpectrumImagePlotter(eels)

ax2 = plt.figure().add_subplot(111)
p2 = ImagePlotter.ImagePlotter(FWHMim, ax2)
p3 = SpectrumImagePlotter.SpectrumImagePlotter(new_eels)
p1.ShowPlot()
