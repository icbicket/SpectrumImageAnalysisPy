import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
import SpectrumPlotter
import ImagePlotter
import Image
import collections

'''Things to do:
Add vertex addition and deletion after creation for patches
Why doesn't it work in multiple figures?
Save extracted patches and spectrum and image
'''

class SpectrumImagePlotter(object):
	def __init__(self, SI):
		self.SI = SI
		self.fig = plt.figure(figsize = (9,9))
		self.image_ax = plt.axes([0.075, 0.475, 0.45, 0.45])
		self.extracted_ax = plt.axes([0.525, 0.475, 0.45, 0.45])
		self.spectrum_ax = plt.axes([0.075, 0.07, 0.9, 0.35])
		self.contrast_ax = plt.axes([0.075, 0.925, 0.9, 0.075])
		self.cmap = plt.get_cmap('brg')

		# Spectrum axis plotting and interactive span
		self.extracted_mask = np.zeros(self.SI.size[:2]).astype(bool)
		mask3D = np.zeros(self.SI.size).astype(bool)
		self.extracted_spectrum = self.SI.ExtractSpectrum(mask3D)
		self.SpectrumPlot = SpectrumPlotter.SpectrumManager(
			self.extracted_spectrum, self.spectrum_ax, self.cmap)
		self.spectrum_ax = self.SpectrumPlot.SpectrumPlot.linked_axis
		self.E_span = SpanSelector(self.SpectrumPlot.SpectrumPlot.linked_axis, self.SpectrumSpan, 'horizontal', 
			span_stays = True)
		self.Emin_i = 0
		self.Emax_i = 1
		
		# Contrast histogram plotting and interactive span
		self.contrastbins = 256
		
		# Image axis plotting and interactive patches
		self.summedim = np.sum(self.SI.data[:, :, self.Emin_i:self.Emax_i], axis = 2)

		self.cmin = np.min(np.min(self.summedim))
		self.cmax = np.max(np.max(self.summedim))
		self.ImagePlot = ImagePlotter.ImagePlotter(Image.Image(self.summedim), self.image_ax)
		self.PlotImage()
		self.PlotContrastHistogram()
		self.extractedim = Image.Image(np.ma.masked_array(self.summedim, np.invert(self.extracted_mask)))
		self.ExtractedImagePlot = collections.OrderedDict()
		self.PlotExtractedImage()
		self.connect()
	
	def connect(self):
		self.cidkey = self.image_ax.figure.canvas.mpl_connect('key_press_event', 
			self.keyboard_press)
	
	def keyboard_press(self, event):
		if event.inaxes == self.image_ax:
			if event.key == 'enter':
				MaskState = self.ImagePlot.PolygonGroups.ToggleActiveMask()
				if MaskState:
					mask = self.ImagePlot.PolygonGroups.GetActiveMask(np.shape(self.summedim))
					mask3D = np.reshape(mask, 
						(self.SI.size[0], self.SI.size[1], 1)) * np.ones((
						self.SI.size[0], self.SI.size[1], self.SI.size[2])).astype(bool)
					self.extractedim = Image.Image(np.ma.masked_array(self.summedim, np.invert(mask)))
					self.AddExtractedImagePatch(self.ImagePlot.PolygonGroups.currentID)
					self.extracted_spectrum = self.SI.ExtractSpectrum(np.invert(mask3D))
					self.SpectrumPlot.update_spectrum(self.extracted_spectrum, 
						self.ImagePlot.PolygonGroups.currentID)
					self.SpectrumPlot.make_visible(self.ImagePlot.PolygonGroups.currentID)
				else:
					self.SpectrumPlot.make_invisible(self.ImagePlot.PolygonGroups.currentID)
					self.RemoveExtractedImagePatch(self.ImagePlot.PolygonGroups.currentID)
		elif event.inaxes == self.extracted_ax:
			if event.key == 'e':
				self.extractedim.SaveImgAsPNG('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/Patch'+
					str(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange[self.Emin_i])+'to'+
					str(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange[self.Emax_i])+
					self.SpectrumPlot.SpectrumPlot.spectrum.units+'.png', self.extractedim.Imglim)
		elif event.inaxes == self.spectrum_ax:
			if event.key == 'e':
				filename = raw_input('Please enter the filepath and name to save your spectrum: ')
				self.extracted_spectrum.SaveSpectrumAsCSV('/home/isobel/Documents/McMaster/PythonCodes/DataAnalysis/testSpec.csv')
#		elif event.key == 'delete':
#			
	
	def PlotSpectrum(self):
		SpectrumPlot = SpectrumPlotter.SpectrumManager(
			self.extracted_spectrum, self.spectrum_ax, self.cmap)
		return SpectrumPlot
	
	def PlotContrastHistogram(self):
		self.summedimhist, self.summedimbins = np.histogram(self.summedim, bins = self.contrastbins)
		self.contrast_ax.cla()
		self.contrast_ax.plot(self.summedimbins[:-1], self.summedimhist, color = 'k')
		self.contrast_ax.set_axis_off()
		self.contrast_span = SpanSelector(self.contrast_ax, self.ContrastSpan, 'horizontal',
			span_stays = True, rectprops = dict(alpha = 0.5, facecolor = 'green'))
	
	def PlotImage(self):
		self.ImagePlot.RemoveImage()
		self.ImagePlot.ReplotImage(Image.Image(self.summedim))
		self.ImagePlot.PlottedImage.set_clim(vmin = self.cmin, vmax = self.cmax)
		self.image_ax.set_axis_off()
	
	def PlotExtractedImage(self):
		self.extracted_ax.cla()
		self.extracted_ax.set_axis_off()
		self.extracted_ax.imshow(self.summedim, interpolation = 'none',
			cmap = 'gray', alpha = 0.1)
	
	def AddExtractedImagePatch(self, ID):
		self.ExtractedImagePlot[self.ImagePlot.PolygonGroups.currentID] = ImagePlotter.ImagePlotter(self.extractedim, self.extracted_ax)
			
	def RemoveExtractedImagePatch(self, ID):
		self.ExtractedImagePlot[ID].PlottedImage.remove()
		pass
		
	def AdjustContrastExtractedImage(self):
		for (ID, image) in self.ExtractedImagePlot.items():
			image.PlottedImage.set_clim(vmin = self.cmin, vmax = self.cmax)
	
	def SpectrumSpan(self, Emin, Emax): ##Note: draws sub-pixel Espan, fix?
		Emin = np.max((np.round(Emin/self.SI.dispersion) * self.SI.dispersion, 
			self.SI.SpectrumRange[0]))
		Emax = np.min((np.round(Emax/self.SI.dispersion) * self.SI.dispersion, 
			self.SI.SpectrumRange[-1]))
		self.Emin_i = np.where(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange == Emin)[0]
		self.Emax_i = np.where(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange == Emax)[0]
		self.Emin_i = np.searchsorted(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange, Emin)
		self.Emax_i = np.searchsorted(self.SpectrumPlot.SpectrumPlot.spectrum.SpectrumRange, Emax)
		self.summedim = np.sum(self.SI.data[:, :, self.Emin_i:self.Emax_i], axis = 2)
		self.cmin = np.min(np.min(self.summedim))
		self.cmax = np.max(np.max(self.summedim))
		self.PlotImage()
		self.PlotContrastHistogram()
		
	def ContrastSpan(self, cmin, cmax):
		self.cmin = cmin
		self.cmax = cmax
		self.PlotImage()

