import numpy as np
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import PolygonGrouper
import PolygonCreator
from matplotlib.patches import Polygon
import PolygonMover


class ImagePlotter(object):
	def __init__(self, image, axis):
		'''For plotting Image as an image'''
		self.axis = axis
		self.Image = image
		self.axis.set_axis_off()
		self.axis.imshow(self.Image.data, cmap = 'gray', interpolation = 'none')
		if image.calibration != 0:
			self.scalebar = ScaleBar(self.Image.calibration)
			self.scalebar.box_alpha = 0.5
			self.axis.add_artist(self.scalebar)
		self.PolygonGroups = PolygonGrouper.PolygonGroupManager(self.axis)
		self.canvas = self.axis.figure.canvas
		self.connect()
		self.creator = None
		self.mover = None
		self.mask = np.zeros(self.Image.size).astype(bool)
		
	def connect(self):
		self.cidkey = self.canvas.mpl_connect('key_press_event', 
			self.keyboard_press)
		
	def disconnect(self):
		self.canvas.mpl_disconnect(self.cidkey)
		
	def keyboard_press(self, event):
		if event.inaxes != self.axis:
			return

		if self.mover:
			self.mover.disconnect()
			self.mover = None
		if event.key == 'n':
			''' Start new polygon in current group and make it active polygon'''
			if self.creator:
				self.creator.abort()
			self.creator = PolygonCreator.PolygonCreator(
				self.axis, self.add_polygon_callback)
		elif event.key == '+':
			''' Make new polygon group and make it current active group'''
			self.PolygonGroups.NewGroup()
		elif event.key == 'up':
			'''Move active selection to next group'''
			self.PolygonGroups.NextGroup(step=1)
		elif event.key == 'down':
			'''Move active selection to previous group'''
			self.PolygonGroups.NextGroup(step=-1)
		elif event.key == 'right':
			'''Move active selection to next polygon'''
			self.PolygonGroups.NextPolygon(step=1)
		elif event.key == 'left':
			'''Move active selection to previous polygon'''
			self.PolygonGroups.NextPolygon(step=-1)
		elif event.key == 'm':
			'''Provide movement handles on active polygon vertices'''
			self.mover = PolygonMover.PolygonMover(
				self.PolygonGroups.GetActivePolygon(), self.axis)
#		elif event.key == 'enter':
#			self.axis.autoscale(tight=True)
#			self.mask = self.PolygonGroups.GetActiveMask(self.Image.size).astype(bool)
		plt.draw()
		
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
