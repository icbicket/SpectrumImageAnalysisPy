import numpy as np
import matplotlib.pyplot as plt
import itertools as itr

class AlignPlot(object):
	#Class to define plot for interactive aligning of images
	def __init__(self, ImgAligner):
		self.ImgAligner = ImgAligner
		self.fig = plt.figure()
		self.ax = plt.axes([0.05, 0.05, 0.95, 0.95])
		self.IndGen = itr.cycle(range(ImgAligner.numIms)[1:])
		self.Index = next(self.IndGen)
		self.ShowImages()
		self.cidkey = self.fig.canvas.mpl_connect('key_press_event', self.MoveImg)
		plt.show()

	def ShowImages(self):
		#Refresh the axis and plot a pair of images
		self.ax.cla()
		self.ax.imshow(self.ImgAligner.Images[0].data, interpolation = 'none', 
			clim = self.ImgAligner.Images[0].Imglim, cmap = 'Blues')
## Fix rollover error - rolled full cycle
		ImgOver = np.roll(np.roll(self.ImgAligner.Images[self.Index].data, 
			self.ImgAligner.offsets[0][self.Index], axis = 1), 
			self.ImgAligner.offsets[1][self.Index], axis = 0)
		self.ax.imshow(ImgOver, interpolation = 'none', 
			cmap = 'Reds', clim = self.ImgAligner.Images[self.Index].Imglim, alpha = 0.5)
		self.ax.axis('off')
		self.fig.canvas.draw()

	def MoveImg(self, event):
		#Calculations to do on pressing a button - arrow keys to move top image to overlay the bottom
		if event.key == 'right':
			self.ImgAligner.offsets[0][self.Index] += 1
		elif event.key == 'left':
			self.ImgAligner.offsets[0][self.Index] -= 1
		elif event.key == 'up':
			self.ImgAligner.offsets[1][self.Index] -= 1
		elif event.key == 'down':
			self.ImgAligner.offsets[1][self.Index] += 1
		elif event.key == 'n':
			self.Index = next(self.IndGen)
		elif event.key == 'enter':
			self.fig.canvas.mpl_disconnect(self.cidkey)
			plt.close()
		else:
			return
		self.ShowImages()
