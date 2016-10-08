import numpy as np
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.artist import Artist

class PolygonTracker(object):
	def __init__(self, ):
		pass

class PolygonMover(object):
	''' Mostly borrowed from Matplotlib 1.5.3 example poly_editor.py
	http://matplotlib.org/examples/event_handling/poly_editor.html
	Class takes in matplotlib Polygon and axis it is plotted on and adds drag 
	handles
	'''
	showverts = True
	epsilon = 5
	def __init__(self, polygon, axis):
		self.polygon = polygon
		self.axis = axis
		canvas = self.polygon.figure.canvas
#		self.corners = polygon.xy

		self.line = Line2D(self.polygon.xy[:, 0], self.polygon.xy[:, 1], 
			marker = 'o', markerfacecolor = 'g', animated = True)
		self.axis.add_line(self.line)
		cid = self.polygon.add_callback(self.poly_changed)
		self._index = None
		
		self.ciddraw = canvas.mpl_connect('draw_event', self.draw_canvas)
		self.cidpress = canvas.mpl_connect('button_press_event', self.mouse_press)
		self.cidmotion = canvas.mpl_connect('motion_notify_event', self.mouse_move)
		self.cidrelease = canvas.mpl_connect('button_release_event', self.mouse_release)
#		canvas.mpl_connect('key_press_event', self.key_press)
		self.canvas = canvas

	def disconnect(self):
		self.canvas.mpl_disconnect(self.ciddraw)
		self.canvas.mpl_disconnect(self.cidpress)
		self.canvas.mpl_disconnect(self.cidmotion)
		self.canvas.mpl_disconnect(self.cidrelease)

		
	def poly_changed(self, poly):
		vis = self.line.get_visible()
		Artist.update_from(self.line, poly)
		self.line.set_visible(vis)
		
	def draw_canvas(self, event):
		self.background = self.canvas.copy_from_bbox(self.axis.bbox)
		self.axis.draw_artist(self.polygon)
		self.axis.draw_artist(self.line)
		self.canvas.blit(self.axis.bbox)
		
	def mouse_press(self, event):
		if not self.showverts:
			return
		if event.inaxes is None:
			return
		if event.button != 1:
			return
		self._index = self.get_point_index(event)
		
	def get_point_index(self, event):
		xy_transform = self.polygon.get_transform().transform(self.polygon.xy)
		d2 = np.sum((xy_transform - [event.x, event.y])**2, axis = 1)
#		index = np.argmin(d2)
		index = np.where(d2==np.min(d2))
		if d2[index][0] >= self.epsilon**2:
			index = None
		return index
		
	def mouse_release(self, event):
		if not self.showverts:
			return
		if event.button != 1:
			return
		self._index = None
		
	def mouse_move(self, event):
#		print self.showverts, self._index, event.inaxes, event.button
		if not self.showverts:
			return
		if self._index is None:
			return
		if event.inaxes is None:
			return
		if event.button != 1:
			return

		x, y = event.xdata, event.ydata
		self.polygon.xy[self._index] = x, y
		self.line.set_data(zip(*self.polygon.xy))
		self.canvas.restore_region(self.background)
		self.axis.draw_artist(self.polygon)
		self.axis.draw_artist(self.line)
		self.canvas.blit(self.axis.bbox)
		self.canvas.draw()
