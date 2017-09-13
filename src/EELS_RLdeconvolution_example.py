from __future__ import print_function
import hyperspy.api as hp
import SpectrumImage
import SpectrumImagePlotter
import Spectrum
import os
import matplotlib.pyplot as plt

# Define folder and filename for the spectrum image
folder = '/home/user/data'
filename = 'EELS Spectrum Image.dm3'
# Define a folder to save the processed data in
save_folder = os.path.join(folder, 'Processed')

# Define folder and filename containing point spread function for deconvolution
PSFfolder = folder
PSFfilename = 'Spectrum_ZLP.csv'

# Import spectrum image from dm3 using hyperspy
s = hp.load(os.path.join(folder, filename))
dispersion = s.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup2.Scale
eels = SpectrumImage.EELSSpectrumImage(s.data, dispersion=dispersion)

# Import point spread function from csv 
PSF = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(PSFfolder, PSFfilename))
print(PSF.FindFW(0.5)) # Print FWHM of the point spread function

# Threshold the spectrum image based on the zero loss peak to eliminate data with low signal and show the thresholded image (threshold applies a mask) (optional)
eels.Threshold(10000)
plt.imshow(eels.data[:,:,eels.ZLP])
plt.show()

# Deconvolve data using Richardson-Lucy algorithm, define the number of iterations to use, the point spread function (as an EELSSpectrum object) and the number of multiprocessing threads to use
RLiterations = 8
eels2 = eels.RLDeconvolution(RLiterations, PSF, threads=8)

# Plot the original spectrum image (p1) and the deconvolved spectrum image (p2)
p1 = SpectrumImagePlotter.SpectrumImagePlotter(eels, filepath=os.path.join(savefolder))
p2 = SpectrumImagePlotter.SpectrumImagePlotter(eels2, filepath=os.path.join(savefolder, str(RLiterations) + 'RL'))
p1.ShowPlot()
