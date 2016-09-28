import numpy as np
import matplotlib.pyplot as plt
import SpectrumPlotter
import ImagePlotter
from skimage import data
import Image
import SpectrumImage
import SpectrumImagePlotter

Im = Image.Image(data.chelsea()[:, :, 0], calibration=5e-9)

#fig = plt.figure()
#ax = plt.axes([0.1, 0.1, 0.8, 0.8])

#Testing SpectrumPlotter
#x = np.transpose(np.arange(0,4))
#y = np.transpose(np.random.random(4))

###x = np.arange(50)*0.01
###y = np.random.random(50)


#s = SpectrumPlotter.SpectrumPlotter(ax, x, y, 'eV')

## Testing ImagePlotter
#Im = np.random.random((2000,2000))
#a = ImagePlotter.ImagePlotter(ax, Im)

SIdata = np.random.random(size = (20,20,50))
SI = SpectrumImage.SpectrumImage(SIdata, 0.01)
SpectrumImagePlotter.SpectrumImagePlotter(SI)

plt.show()
