from __future__ import print_function
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

class LineDraw(object):
	epsilon = 5
	def __init__(self, axis):
		self.axis = axis
		self.canvas = self.axis.figure.canvas
		self.LineStartx = None
		self.LineStarty = None
		self.LineEndx = None
		self.LineEndy = None
		self.LineCoords = np.empty((2, 2))
		self.line = None
		self.Dragging = False
		self.vertex = 1
		self.width = 1
		self.WidthData = self.WidthDataCoords()
		
	def ConnectDraw(self):
		print('draw a line!')
		self.cidclick = self.canvas.mpl_connect('button_press_event',
			self.LineStart)
		self.cidmotion = self.canvas.mpl_connect('motion_notify_event',
			self.DrawLine)
		self.cidrelease = self.canvas.mpl_connect('button_release_event', 
			self.LineEnd)
		self.ciddraw = self.canvas.mpl_connect('draw_event', self.DrawCanvas)
		#print(self.LineStart)
			
	def DisconnectDraw(self):
		self.canvas.mpl_disconnect(self.cidclick)
		self.canvas.mpl_disconnect(self.cidrelease)
		self.canvas.mpl_disconnect(self.ciddraw)
		self.canvas.mpl_disconnect(self.cidmotion)
		
	def ConnectMove(self):
		print('move your line!')
		self.cidendpick = self.canvas.mpl_connect('button_press_event',
			self.MoveLinePress)
		self.cidenddrag = self.canvas.mpl_connect('motion_notify_event',
			self.DrawLine)
		self.cidendrelease = self.canvas.mpl_connect('button_release_event',
			self.MoveLineUpdate)
		self.cidwidth = self.canvas.mpl_connect('scroll_event', 
			self.ChangeWidth)
		self.cidenddraw = self.canvas.mpl_connect('draw_event', self.DrawCanvas)
			
	def DisconnectMove(self):
		self.canvas.mpl_disconnect(self.cidendpick)
		self.canvas.mpl_disconnect(self.cidenddrag)
		self.canvas.mpl_disconnect(self.cidendrelease)
	
	def LineStart(self, event):
		self.LineCoords[0] = [event.xdata, event.ydata]
		self.line = mlines.Line2D(self.LineCoords[:, 0], self.LineCoords[:, 0], 
			lw=self.WidthData, c='r', animated=True)
		self.axis.add_line(self.line)
		self.background = self.canvas.copy_from_bbox(self.axis.bbox)

	def LineEnd(self, event):
		self.LineCoords[1] = [event.xdata, event.ydata]
		self.CoordTransform = self.axis.transData.inverted()
		self.WidthData = self.WidthDataCoords()
		self.line = mlines.Line2D(self.LineCoords[:, 0], self.LineCoords[:, 1],
			lw=self.WidthData, c='r', marker='o', alpha=0.5, solid_capstyle='butt')
		self.axis.add_line(self.line)
		self.Dragging = True
		self.DisconnectDraw()
		self.ConnectMove()
		plt.draw()

	def DrawLine(self, event):
		if event.button != 1:
			return
		if event.inaxes is None:
			return
		if self.vertex == 0:
			x = (event.xdata, self.LineCoords[1, 0])
			y = (event.ydata, self.LineCoords[1, 1])
		elif self.vertex == 1:
			x = (self.LineCoords[0, 0], event.xdata)
			y = (self.LineCoords[0, 1], event.ydata)
		else:
			return
		self.line.set_data(x, y)
		self.canvas.restore_region(self.background)
		self.axis.draw_artist(self.line)
		self.canvas.blit(self.axis.bbox)
		self.canvas.draw()

	def DrawCanvas(self, event):
		self.background = self.canvas.copy_from_bbox(self.axis.bbox)
		if self.line is not None:
			self.axis.draw_artist(self.line)
			self.WidthData = self.WidthDataCoords()
			self.line.set_linewidth(self.WidthData)
		self.canvas.blit(self.axis.bbox)
		print('new sketch!')
		
	def MoveLinePress(self, event):
		self.vertex = self.GetPoint(event)
		#print(self.vertex)
	
	def MoveLineUpdate(self, event):
		if self.vertex is not None:
			self.LineCoords[self.vertex] = [event.xdata, event.ydata]
			self.line.set_data(self.LineCoords[:, 0], self.LineCoords[:, 1])
			self.canvas.draw()
	
	def WidthDataCoords(self):
		diff0 = self.axis.transData.inverted().transform((1,0))
		diff1 = self.axis.transData.inverted().transform((2,0))
		diff = (diff1 - diff0) * self.width
		#print(diff)
		return diff[0]
	
	def ChangeWidth(self, event):
		if event.button == 'up':
			self.width += 1
		elif event.button == 'down' and self.width > 1:
			self.width -= 1
		else:
			return
		self.WidthData = self.WidthDataCoords()
		self.line.set_linewidth(self.WidthData)
		self.canvas.draw()
	
	def GetPoint(self, event):
		delta2 = np.sum((self.LineCoords - [event.xdata, event.ydata])**2, axis = 1)
		index = np.where(delta2 == np.min(delta2))[0]
		if delta2[index] >= self.epsilon**2:
			index = None
		return index
