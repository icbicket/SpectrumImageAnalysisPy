import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import FuncFormatter

h = 6.626070040e-34
c = 299792458
eC = 1.6021766208e-19

class SpectrumPlotter(object):
	def __init__(self, spectrum, axis, colour='red'):
		'''Line plot with span selector
		   Input: matplotlib axis object, x and y data points
			 x and y are arrays for plotting against each other
		   '''
		self.main_axis = axis
		self.line_colour = colour
		self.linked_axis = self.main_axis.twiny()
		self.spectrum = spectrum
		self.main_axis.set_ylabel(r"Intensity (a.u.)")
		self.linked_axis.format_coord = self.axis_display
		
		

		
class CLSpectrumPlotter(SpectrumPlotter):
	def __init__(self, spectrum, axis, colour='red'):
		super(CLSpectrumPlotter, self).__init__(spectrum, axis, colour)
		formatter = FuncFormatter(nmtoeV)
		self.main_axis.plot(spectrum.WavelengthRange, spectrum.intensity, self.line_colour)
		self.linked_axis.plot(spectrum.WavelengthRange, spectrum.intensity)
		self.linked_axis.clear()
		self.linked_axis.xaxis.set_major_formatter(formatter)
		self.main_axis.set_xlabel(r"Wavelength (%s)" % spectrum.units)
		self.linked_axis.set_xlabel(r"Energy (%s)" % spectrum.secondary_units)
		self.linked_axis.format_coord = self.axis_display
		plt.gcf().canvas.draw()
		
	def axis_display(self, x, y):
	    return 'Energy=%0.4g eV, Wavelength=%0.3g nm, I=%0.5g' % (x, float(nmtoeV(x)), y)
	
class EELSSpectrumPlotter(SpectrumPlotter):
	def __init__(self, spectrum, axis, colour='blue'):
		super(EELSSpectrumPlotter, self).__init__(spectrum, axis, colour)
		formatter = FuncFormatter(eVtonm)
		self.main_axis.plot(spectrum.EnergyRange, spectrum.intensity, self.line_colour)
		self.linked_axis.plot(spectrum.EnergyRange, spectrum.intensity)
		self.linked_axis.clear()
		self.linked_axis.xaxis.set_major_formatter(formatter)
		self.main_axis.set_xlabel(r"Energy (%s)" % spectrum.units)
		self.linked_axis.set_xlabel(r"Wavelength (%s)" % spectrum.secondary_units)
		plt.gcf().canvas.draw()

	def axis_display(self, x, y):
				return 'Energy=%0.3g eV, Wavelength=%0.2g nm, I=%1.5f' % (x, float(eVtonm(x)), y)

def eVtonm(eV, pos=None):
    nm = h*c/(eC*abs(eV))*1e9
    if np.isfinite(nm): nm = int(nm)
    return "%.3g" % nm

def nmtoeV(nm, pos=None):
	eV = h*c/(eC*abs(nm))*1e9
	return "%.3g" % eV

#	def Espan(self, Emin, Emax): ##Note: draws sub-pixel Espan, fix?
#		Emin = np.round(Emin/self.x_dispersion) * self.x_dispersion
#		Emax = np.round(Emax/self.x_dispersion) * self.x_dispersion
#		self.Emin_i = np.where(self.x == Emin)
#		self.Emax_i = np.where(self.x == Emax)
#		print Emin, Emax, self.Emin_i, self.Emax_i
