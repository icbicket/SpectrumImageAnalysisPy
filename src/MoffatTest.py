import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling.models import Moffat1D, Lorentz1D

plt.figure()
r = np.arange(-5, 5, .01)
s1 = Moffat1D(amplitude=1, x_0 = 0, gamma = 1, alpha = 0.1)
m = s1(r[:len(r)/2])
fwhm =  np.abs(r[(np.abs(m - 0.5)).argmin()]) * 2
l1 = Lorentz1D(amplitude = 1, x_0 = 0, fwhm = fwhm)


#for factor in range(1, 4):
#	print factor
#	s1.amplitude = factor
#	s1.width = factor
#	l1.amplitude = factor
#	l1.fwhm = factor*2
plt.plot(r, s1(r),	 color=[0, 0, 0.5], lw=2)
plt.plot(r, l1(r), color=[0.5, 0, 0], ls='--', lw=2)
plt.legend(('Moffat', 'Lorentz'))
plt.axis([-5, 5, 0, 1.5])
plt.show()
