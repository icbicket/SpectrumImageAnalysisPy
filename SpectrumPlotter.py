import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import FuncFormatter
import collections
from matplotlib.lines import Line2D

h = 6.626070040e-34
c = 299792458
eC = 1.6021766208e-19

class SpectrumPlotter(object):
	def __init__(self, spectrum, axis, colour='red'):
		'''Line plot with span selector
		   Input: matplotlib axis object, Spectrum object to plot
		   '''
		self.main_axis = axis
		self.line_colour = colour
		self.linked_axis = self.main_axis.twiny()
		self.spectrum = spectrum
		self.label = ''
		self.main_axis.set_xlabel(r"%s (%s)" % (spectrum.unit_label, spectrum.units))
		self.main_axis.set_ylabel(r"Intensity (a.u.)")
		self.setup_linked_axis(self.spectrum.SpectrumRange, 
			r"%s (%s)" % (self.spectrum.secondary_unit_label, self.spectrum.secondary_units), nmtoeV)
#		self.plotted_spectrum = self.main_axis.plot(self.spectrum.SpectrumRange, self.spectrum.intensity, 'red')
		self.linked_axis.format_coord = self.axis_display
		plt.gcf().canvas.draw()
		
	def setup_linked_axis(self, x_range, label, FormatFunction):
		self.linked_axis.plot(x_range, self.spectrum.intensity)
		self.linked_axis.clear()
		self.linked_axis.xaxis.set_major_formatter(FuncFormatter(FormatFunction))
		self.linked_axis.set_xlabel(label)
#		plt.xticks(rotation=25)
		
	def axis_display(self, x, y):
	    return '%s = %0.4g %s, %s = %0.3g %s, I = %0.5g' % (
	    	self.spectrum.unit_label, x, self.spectrum.units, 
	    	self.spectrum.secondary_unit_label, float(nmtoeV(x)), 
	    	self.spectrum.secondary_units, y) ## Using nmtoeV! not CL friendly?

	def add_spectrum(self, spectrum, label=''):
		self.label = label
		plotted_spectrum = self.main_axis.plot(spectrum.SpectrumRange, 
				spectrum.intensity, label=self.label)
		
		return plotted_spectrum
		
	def update_spectrum(self, line, spectrum):
		line[0].remove()
		plotted_spectrum = self.main_axis.plot(spectrum.SpectrumRange, 
			spectrum.intensity, label=self.label)
		return plotted_spectrum

def eVtonm(eV, pos=None):
    nm = h*c/(eC*abs(eV))*1e9
    if np.isfinite(nm): nm = int(nm)
    return "%.0f" % nm

def nmtoeV(nm, pos=None):
	eV = h*c/(eC*abs(nm))*1e9
	return "%.0f" % eV

class SpectrumManager(object):
	def __init__(self, spectrum, axis, cmap=plt.get_cmap('cool'), currentID=0):
		self.currentID = currentID
		self.cmap = cmap
		self.axis = axis
		self.spectrumDict = collections.OrderedDict()
		self.spectrumDict[self.currentID] = spectrum
		self.lineDict = collections.OrderedDict()
		self.SpectrumPlot = SpectrumPlotter(self.spectrumDict[self.currentID], 
			self.axis, self.cmap)
		self.lineDict[self.currentID] = self.SpectrumPlot.add_spectrum(
			self.spectrumDict[self.currentID], label=str(self.currentID))
		self.colourDict = collections.OrderedDict()
		self.colourDict[self.currentID] = self.cmap(0)

	def make_colour_list(self):
		colour_callers = np.linspace(0, 1, len(self.lineDict.keys()))
		for cc, ll in zip(colour_callers, self.lineDict.keys()):
			self.colourDict[ll] = self.cmap(cc)

#	def RecolourSpectra(self):
#		colours = self.cmap(i) for i in np.linspace(0, 1, len(self.spectrumDict))
##		cmaps = []
##		for ii in self.spectrumDict.keys():
##			cmaps.append(self.cmap(i/len(self.spectrumDict)))
#		self.SpectrumPlot.colour_spectra(colours)
##		for (i, g) in self.polyDict.items():
##			g.colour_spectrum(self.cmap(i/len(self.polyDict)))
#		
		
#	def AddSpectrum(self, spectrum):
#		'''Adds spectrum to spectrum dictionary to be plotted'''
#		self.currentID = (self.currentID + step) % (max(self.spectrumDict.keys()) + 1)
#		print "I added a new spectrum for you!"
#		self.spectrumDict[self.currentID] = spectrum

	def update_spectrum(self, spectrum, ID):
		self.currentID = ID
		self.spectrumDict[ID] = spectrum
		if self.currentID in self.lineDict.keys():
			self.lineDict[self.currentID] = self.SpectrumPlot.update_spectrum(
				self.lineDict[self.currentID], self.spectrumDict[self.currentID])
			self.lineDict[self.currentID][0].set_color(self.colourDict[self.currentID])
		else:
			self.lineDict[self.currentID] = self.SpectrumPlot.add_spectrum(
				self.spectrumDict[self.currentID], label=str(self.currentID))
			self.make_colour_list()
			for ll in self.lineDict.keys():
				self.lineDict[ll][0].set_color(self.colourDict[ll])

	def make_visible(self, ID):
		self.lineDict[ID][0].set_visible(True)
#		self.lineDict[ID][0].set_color('r')
		
	def make_invisible(self, ID):
		self.lineDict[ID][0].set_visible(False)
	
	def add_legend(self):
		legend = self.axis.legend(loc='best', framealpha=0.5)
		if legend:
			legend.draggable(state=True)
