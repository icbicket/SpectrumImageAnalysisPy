from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

class PolygonCreator(object):
	def __init__(self, axis, callback=None):
		self.axis = axis
		self.canvas = self.axis.figure.canvas
		self.vertices = []
		self.connect()
		self.polygon = []
		self.callback = callback
		print 'hi'

	def connect(self):
		self.cidbutton = self.canvas.mpl_connect('button_press_event', 
			self.mouse_click)

	def disconnect(self):
		self.canvas.mpl_disconnect(self.cidbutton)
		
	def abort(self):
		print "WE'RE GOING DOWN!!!"
		self.disconnect()
		if self.polygon:
			self.polygon.remove()
		plt.draw()


	def mouse_click(self, event):
		if event.inaxes != self.axis:
			return
		if event.button == 3:
			self.disconnect()
			if self.callback:
				self.callback(self.polygon)
			return
		if self.polygon:
			self.polygon.remove()
		self.vertices.append((event.xdata, event.ydata))
		self.polygon = Polygon(self.vertices, closed = True, alpha = 0.5, color='k')
		self.axis.add_patch(self.polygon)
		
		plt.draw()

# Handle clicking to add vertices and return finished polygon
