from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.ticker import NullLocator
import PolygonGrouper
import PolygonCreator
from matplotlib.patches import Polygon
import PolygonMover
import os
from skimage.measure import profile_line
#import LineProfile
import LineDraw

class ImagePlotter(object):
	def __init__(self, image, axis=None, colourbar_axis = None, cmap=plt.get_cmap('gray'), filepath=os.getcwd(), polygoncallback = None):
		'''For plotting Image as an image
		Input a 2D array to plot as an image, and an axis to plot the image on
		Optional arguments: define an axis to put a colourbar in, define the filepath to save images to'''
		if axis is not None:
			self.axis = axis
		else:
			self.axis = plt.figure().add_subplot(111)

		self.cmap = cmap
		self.Image = image
		self.axis.set_axis_off()
		self.filepath = filepath
		self.PlottedImage = self.axis.imshow(self.Image.data, cmap = self.cmap, interpolation = 'none')
		if colourbar_axis is True:
			self.colourbar_axis = None
			self.cbar = self.AddColourbar()
			self.colourbar_axis = plt.gcf().axes[-1]
		elif colourbar_axis is not None:
			self.colourbar_axis = colourbar_axis
			self.cbar = self.AddColourbar()
			
		if image.calibration != 0:
			self.scalebar = ScaleBar(self.Image.calibration)
			self.scalebar.box_alpha = 0.5
			self.axis.add_artist(self.scalebar)
		if polygoncallback:
			self.polygoncallback = polygoncallback
		else:
			self.polygoncallback = self.keyboard_press
		self.PolygonGroups = PolygonGrouper.PolygonGroupManager(self.axis)
		self.Lines = LineDraw.LineDraw(self.axis)
		self.canvas = self.axis.figure.canvas
		self.connect()
		self.creator = None
		self.mover = None
#		self.mask = np.zeros(self.Image.size).astype(bool)
		
	def RemoveImage(self):
		self.PlottedImage.remove()
		
	def ReplotImage(self, image, clim=None):
		self.Image = image
		self.PlottedImage = self.axis.imshow(self.Image.data, cmap = self.cmap, interpolation = 'none')
		if clim is not None:
			self.PlottedImage.set_clim(vmin = clim[0], vmax = clim[1])
		if self.colourbar_axis:
			self.colourbar_axis.cla()
			self.cbar = self.AddColourbar()

	def AddColourbar(self):
		'''Check for comparison of the image contrast limits vs the image data contrast
		limits to indicate this on the colourbar as appropriate'''
		cbar_limit_test = np.equal(self.PlottedImage.get_clim(), self.Image.Imglim)
		if not np.any(cbar_limit_test):
			cbar_extend = 'both'
		elif np.all(cbar_limit_test):
			cbar_extend = 'neither'
		else:
			if cbar_limit_test[0] and self.PlottedImage.get_clim()[0] > self.Image.Imglim[0]:
				cbar_extend = 'max'
			elif cbar_limit_test[1] and self.PlottedImage.get_clim()[1] < self.Image.Imglim[0]:
				cbar_extend = 'min'
			else:
				cbar_extend = 'neither'
		'''Plot colourbar'''
		cbar = plt.colorbar(mappable=self.PlottedImage, cax=self.colourbar_axis, extend=cbar_extend)
		return cbar
	
	def connect(self):
		self.cidkey = self.canvas.mpl_connect('key_press_event', 
			self.polygoncallback)
		
	def disconnect(self):
		self.canvas.mpl_disconnect(self.cidkey)

#	def connect_mouse(self):
#		self.cidbutton = self.canvas.mpl_connect('button_press_event', 
#			self.LineProfileStart)
#		self.cidbuttonrelease = self.canvas.mpl_connect('button_release_event',
#			self.LineProfileEnd)
#	
#	def disconnect_mouse(self):
#		self.canvas.mpl_disconnect(self.cidbutton)
#		
	def keyboard_press(self, event):
		if event.inaxes == self.axis:
			self.image_key_commands(event.key)
		elif event.inaxes == self.colourbar_axis:
			if event.key == 'e':
				self.save_colourbar(filename=(os.path.join(self.filepath, 'Colourbar_.png')))
	
	def image_key_commands(self, key):
		if self.mover:
			self.mover.disconnect()
			self.mover = None
		if key == 'n':
			''' Start new polygon in current group and make it active polygon'''
			if self.creator:
				self.creator.abort()
			self.creator = PolygonCreator.PolygonCreator(
				self.axis, self.add_polygon_callback)
		elif key == '+':
			''' Make new polygon group and make it current active group'''
			self.PolygonGroups.NewGroup()
		elif key == 'up':
			'''Move active selection to next group'''
			self.PolygonGroups.NextGroup(step=1)
		elif key == 'down':
			'''Move active selection to previous group'''
			self.PolygonGroups.NextGroup(step=-1)
		elif key == 'right':
			'''Move active selection to next polygon'''
			self.PolygonGroups.NextPolygon(step=1)
		elif key == 'left':
			'''Move active selection to previous polygon'''
			self.PolygonGroups.NextPolygon(step=-1)
		elif key == 'm':
			'''Provide movement handles on active polygon vertices'''
			self.mover = PolygonMover.PolygonMover(
				self.PolygonGroups.GetActivePolygon(), self.axis)
		elif key == 'e':
			self.save_image(os.path.join(self.filepath, 'Image_.png'))
		elif key == 'E':
			self.save_image_scale(os.path.join(self.filepath, 'Image_scale_.png'))
		elif key == 'a':
			self.PolygonGroups.ToggleGroupActive()
		elif key == 'delete':
			self.PolygonGroups.DeleteActivePolygon()
		elif key == 'd':
#			self.connect_mouse()
			self.Lines.ConnectDraw()
		plt.draw()

	def LineProfileStart(self, event):
		self.LineStart = (event.x, event.y)
		
	def LineProfileEnd(self, event):
		self.LineEnd = (event.x, event.y)
		self.LineProfile = LineProfile.LineProfilePlot(self.Image, self.LineStart, self.LineEnd)

	def save_colourbar(self, filename):
		extent_colourbar = self.colourbar_axis.get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted())
		extent_toptick = self.colourbar_axis.yaxis.get_ticklabels()[0].get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted())
		extent_bottomtick = self.colourbar_axis.yaxis.get_ticklabels()[-1].get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted())
		new_extent = np.array([np.min((extent_colourbar.get_points()[0,:], extent_toptick.get_points()[0,:], extent_bottomtick.get_points()[0,:]), axis=0),
			np.max((extent_colourbar.get_points()[1,:], extent_toptick.get_points()[1,:], extent_bottomtick.get_points()[1,:]), axis=0)])
		extent_colourbar.set_points(new_extent)
		if os.path.exists(filename):
			filename = filename[:-4] + '-1' + filename[-4:]
		plt.gcf().savefig(filename, bbox_inches=extent_colourbar, transparent=True)
		print('Saved colourbar to...', filename)
	
	def save_image(self, filename):
		self.Image.SaveImgAsPNG(filename, self.PlottedImage.get_clim(), cmap=plt.get_cmap(self.cmap))
		print('Saved image to...', filename)
		
	def save_image_scale(self, filename):
		if self.Image.calibration==0:
			print("You gave me no scale! I can't do it!")
			return
		self.axis.yaxis.set_major_locator(NullLocator())
		self.axis.xaxis.set_major_locator(NullLocator())
		plt.savefig(filename, transparent=True, bbox_inches='tight', pad_inches=0)
		print('Saved scalebar figure to...', filename)
	
	def add_polygon_callback(self, polygon):
		self.creator = None
		self.PolygonGroups.AddPolygon(polygon)

	## Hook up key press controlling for patches
	
	
#def connect(self):
#		self.cidpress = self.figure.canvas.mpl_connect('button_press_event', self.press)
#		self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', self.release)
#		self.cidkey = self.figure.canvas.mpl_connect('key_press_event', self.key)

## Disconnect canvas from clicking and dragging events
#	def disconnect(self):
#		self.patch.figure.canvas.mpl_disconnect(self.cidpress)
#		self.patch.figure.canvas.mpl_disconnect(self.cidrelease)
#		self.patch.figure.canvas.mpl_disconnect(self.cidkey)
