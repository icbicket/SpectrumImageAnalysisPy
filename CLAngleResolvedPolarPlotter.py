import numpy as np
import PolarPlot
import matplotlib.pyplot as plt

def Import2dCSV(filename):
	img = np.genfromtxt(filename, delimiter = ',')
	return img
	
class PolarPlotter(object):
	def __init__(self, filename, filenameout, maxintensity=None):
		self.filename = filename
		if not filenameout:
			self.filenameout = filename
		else:
			self.filenameout = filenameout
		self.data = Import2dCSV(self.filename)
		self.fig = plt.figure()
		self.ax = plt.axes([0, 0, 0.8, 1])
		self.colourbar_ax = plt.axes([0.8, 0.1, 0.075, 0.8])
		self.plot = PolarPlot.PolarPlot(self.data, self.ax, self.colourbar_ax, maxintensity=maxintensity)
		
	def SavePlot(self):
		self.fig.savefig((self.filenameout + '_PolarPlot.png'), 
		dpi = 300, bbox_inches = 'tight', 
		pad_inches = 0.05, facecolor = 'black', 
		edgecolor = 'black')
