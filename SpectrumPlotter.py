import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import FuncFormatter

h = 6.626070040e-34
c = 299792458
eC = 1.6021766208e-19

class SpectrumPlotter(object):
	def __init__(self, axis, x, y, unit = ''):
		'''Line plot with span selector
		   Input: matplotlib axis object, x and y data points
			 x and y are arrays for plotting against each other
		   '''

		self.x = x
		self.x_dispersion = x[1] - x[0]
		self.y = y
		self.units = unit


		if 'nm' in self.units:
			self.wvl_axis = axis
			self.wvl_axis.plot(self.x, self.y)
			formatter = FuncFormatter(nmtoeV)
			self.ene_axis = self.wvl_axis.twiny()
			self.ene_axis.plot(self.x, self.y)
			self.ene_axis.clear()
			self.ene_axis.xaxis.set_major_formatter(formatter)
		else:
			self.ene_axis = axis
			self.ene_axis.plot(self.x, self.y)
			formatter = FuncFormatter(eVtonm)
			self.wvl_axis = self.ene_axis.twiny()
			self.wvl_axis.plot(self.x, self.y)
			self.wvl_axis.clear()
			self.wvl_axis.xaxis.set_major_formatter(formatter)
			
		self.ene_axis.set_xlabel(r"Energy (eV)")
		self.ene_axis.set_ylabel(r"Intensity (a.u.)")
		self.wvl_axis.set_xlabel(r"Wavelength (nm)")
		plt.gcf().canvas.draw()




#self.E_span = SpanSelector(self.axis, self.Espan, 'horizontal', 
#					span_stays = True)
#		self.Emin_i = 0
#		self.Emax_i = 1

def eVtonm(eV, pos=None):
    nm = h*c/(eC*abs(eV))*1e9
    if np.isfinite(nm): nm = int(nm)
    return "%.4g" % nm

def nmtoeV(nm, pos=None):
	eV = h*c/(eC*abs(nm))*1e9
	return "%.4g" % eV

#	def Espan(self, Emin, Emax): ##Note: draws sub-pixel Espan, fix?
#		Emin = np.round(Emin/self.x_dispersion) * self.x_dispersion
#		Emax = np.round(Emax/self.x_dispersion) * self.x_dispersion
#		self.Emin_i = np.where(self.x == Emin)
#		self.Emax_i = np.where(self.x == Emax)
#		print Emin, Emax, self.Emin_i, self.Emax_i
