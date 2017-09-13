from scipy import signal
import numpy as np
from astropy.modeling import models, fitting
import matplotlib.pyplot as plt
from astropy.convolution import convolve

#dispersion = np.arange(0, 100, 1000)
dispersion = np.linspace(0, 100, num=2757)
Gaussdispersion = np.linspace(25, 75, num=2001)
L1 = models.Lorentz1D(amplitude=1, x_0=23, fwhm=6)
L2 = models.Lorentz1D(amplitude=0.8, x_0=64, fwhm=8)
L3 = models.Lorentz1D(amplitude=0.5, x_0=78, fwhm=15)
L_peaks = L1(dispersion) + L2(dispersion) + L3(dispersion)

G1 = models.Gaussian1D(amplitude=1, mean=50, stddev=10)

filtered = convolve(L_peaks, G1(Gaussdispersion), boundary='extend')
filtered2 = convolve(G1(Gaussdispersion), L_peaks, boundary='extend')

fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True)
ax_orig.plot(dispersion, L_peaks)
ax_orig.set_title('Original pulse')
ax_orig.margins(0, 0.1)
ax_win.plot(Gaussdispersion, G1(Gaussdispersion))
ax_win.set_title('Gaussian pulse')
ax_win.margins(0, 0.1)
ax_filt.plot(dispersion, filtered)
ax_filt.plot(Gaussdispersion, filtered2)
ax_filt.set_title('Filtered signal')
ax_filt.margins(0, 0.1)
fig.tight_layout()


plt.show()
