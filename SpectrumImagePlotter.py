import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
import SpectrumPlotter
import ImagePlotter
import Image

class SpectrumImagePlotter(object):
	def __init__(self, SI):
		self.SI = SI
		self.fig = plt.figure(figsize = (9,9))
		self.image_ax = plt.axes([0.075, 0.475, 0.45, 0.45])
		self.extracted_ax = plt.axes([0.525, 0.475, 0.45, 0.45])
		self.spectrum_ax = plt.axes([0.075, 0.07, 0.9, 0.35])
		self.contrast_ax = plt.axes([0.075, 0.925, 0.9, 0.075])

		# Spectrum axis plotting and interactive span
		mask3D = np.ones(self.SI.size).astype(bool)
		self.SpectrumPlot = SpectrumPlotter.SpectrumPlotter(
			self.SI.ExtractSpectrum(mask3D), self.spectrum_ax)
		self.spectrum_ax = self.SpectrumPlot.linked_axis
		self.E_span = SpanSelector(self.SpectrumPlot.linked_axis, self.SpectrumSpan, 'horizontal', 
			span_stays = True)
		self.Emin_i = 0
		self.Emax_i = 1
		
		# Contrast histogram plotting and interactive span
		self.contrastbins = 256
		
		# Image axis plotting and interactive patches
		self.summedim = np.sum(self.SI.data[:, :, self.Emin_i:self.Emax_i], axis = 2)

		self.cmin = np.min(np.min(self.summedim))
		self.cmax = np.max(np.max(self.summedim))
		self.PlotImage()
		self.PlotContrastHistogram()
		self.extractedim = Image.Image(self.summedim * self.ImagePlot.mask)
		self.PlotExtractedImage()
		self.connect()
	
	def connect(self):
		self.cidkey = self.image_ax.figure.canvas.mpl_connect('key_press_event', 
			self.keyboard_press)
	
	def keyboard_press(self, event):
		if event.inaxes != self.image_ax:
			return
		if event.key == 'enter':
			self.image_ax.autoscale(tight=True)
			print 'enter!'
	
	def PlotSpectrum(self):
		SpectrumPlot = SpectrumPlotter.SpectrumPlotter(
			self.SI.data[0,0,:], self.SI.data[1,1,:], self.spectrum_ax)
		return SpectrumPlot
	
	def PlotContrastHistogram(self):
		self.summedimhist, self.summedimbins = np.histogram(self.summedim, bins = self.contrastbins)
		self.contrast_ax.cla()
		self.contrast_ax.plot(self.summedimbins[:-1], self.summedimhist, color = 'k')
		self.contrast_ax.set_axis_off()
		self.contrast_span = SpanSelector(self.contrast_ax, self.ContrastSpan, 'horizontal',
			span_stays = True, rectprops = dict(alpha = 0.5, facecolor = 'green'))
	
	def PlotImage(self):
		self.image_ax.cla()
		self.ImagePlot = ImagePlotter.ImagePlotter(Image.Image(self.summedim), self.image_ax)
		self.image_ax.imshow(self.summedim, interpolation = 'none', 
			cmap = 'gray', clim = (self.cmin, self.cmax))
		self.image_ax.set_axis_off()
	
	def ExtractPatch(self, mask):
		self.extractedim = Image.Image(self.summedim * mask)
		self.PlotExtractedImage()
		
	
	def PlotExtractedImage(self):
		self.extracted_ax.cla()
		self.extracted_ax.set_axis_off()
		self.ExtractedImagePlot = ImagePlotter.ImagePlotter(self.extractedim, self.extracted_ax)
		self.extracted_ax.imshow(self.summedim, interpolation = 'none',
			cmap = 'gray', alpha = 0.3)
		
	def SpectrumSpan(self, Emin, Emax): ##Note: draws sub-pixel Espan, fix?
		Emin = np.max((np.round(Emin/self.SI.dispersion) * self.SI.dispersion, 
			self.SI.SpectrumRange[0]))
		Emax = np.min((np.round(Emax/self.SI.dispersion) * self.SI.dispersion, 
			self.SI.SpectrumRange[-1]))
		self.Emin_i = np.where(self.SpectrumPlot.spectrum.SpectrumRange == Emin)[0]
		self.Emax_i = np.where(self.SpectrumPlot.spectrum.SpectrumRange == Emax)[0]
#		print Emin, Emax, self.SI.SpectrumRange[0], self.SI.SpectrumRange[-1], self.Emin_i, self.Emax_i
		self.summedim = np.sum(self.SI.data[:, :, self.Emin_i:self.Emax_i], axis = 2)
		self.cmin = np.min(np.min(self.summedim))
		self.cmax = np.max(np.max(self.summedim))
		self.PlotImage()
		self.PlotContrastHistogram()
		
	def ContrastSpan(self, cmin, cmax):
		self.cmin = cmin
		self.cmax = cmax
		self.PlotImage()

#class PatchWatcher(object):
#	def __init__(self, callback):
#		self._MaskOn = True
#		self.callback = callback
#		
#	@property
#	def MaskOn(self):
#		return self._MaskOn
#		
#	@MaskOn.setter
#	def MaskOn(self, value):
#		print 'maskset!'
#		self._MaskOn = value
#		if value: self.callback()
#		
#	@MaskOn.deleter
#	def MaskOn(self):
#		del self._MaskOn
