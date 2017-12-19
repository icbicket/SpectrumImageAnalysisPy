# Import necessary libraries
import SpectrumImage
import SpectrumImagePlotter
import Spectrum
import os
import Image
import ImagePlotter
import ImageDisplay
import matplotlib.pyplot as plt

# Define folder and filename for spectrum image
folder = '/home/user/datafolder'
filebase = 'EELS Spectrum Image.dm3'

# Define folder to save the processed data in
savefolder = os.path.join(folder, 'Processed')

# Define folder and filename of the point spread function
PSFfolder = folder
PSFfilename = 'Spectrum_ZLP.csv'

# Load spectrum image from dm3 using hyperspy
eels = SpectrumImage.EELSSpectrumImage.LoadFromDM3(os.path.join(folder, filebase), spectrum_calibrated=False)

# Load point spread function spectrum as an EELSSpectrum object from csv
PSF = Spectrum.EELSSpectrum.LoadFromCSV(os.path.join(PSFfolder, PSFfilename))

# Print the FWHM of the point spread function
print PSF.FindFW(0.5)

# Threshold the spectrum image based on the zero loss peak to eliminate data with low signal and show the thresholded 
# image (threshold applies a mask) (optional)
eels.Threshold(10000)
plt.imshow(eels.data[:,:,eels.ZLP])
plt.show()

# Deconvolve data using Richardson-Lucy algorithm, define the number of iterations to use (eg, 5), the point spread 
# function and the number of multiprocessing threads to use (eg, 8)
RLiterations = 5
eels2 = eels.RLDeconvolution(RLiterations, PSF, threads=8)

# Plot the original spectrum image (p1) and the deconvolved spectrum image (p2) (interactive)
p1 = SpectrumImagePlotter.SpectrumImagePlotter(eels, filepath=os.path.join(savefolder))
p2 = SpectrumImagePlotter.SpectrumImagePlotter(eels2, filepath=os.path.join(savefolder, str(RLiterations) + 'RL'))
p1.ShowPlot()
