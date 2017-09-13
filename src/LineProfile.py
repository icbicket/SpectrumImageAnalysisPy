import numpy as np
from skimage.measure import profile_line
import matplotlib.pyplot as plt
from skimage import data
import Image
import ImagePlotter

#def click(event):
#	print event

#fig = plt.figure()
#ax1 = plt.axes()

#image = Image.Image(data.camera())
#imageplot = ImagePlotter.ImagePlotter(image, ax1)



#plt.show()


class LineProfilePlot(object):
	def __init__(self, image, start, end, width=1):
		self.image = image
		self.start = start
		self.end = end
		self.width = width
		self.profile = profile_line(self.image.data, start, end, linewidth=width, mode='constant', cval=0)
		
		self.fig = plt.figure()
		self.ax = plt.axes()

		self.ax.plot(self.profile)
		plt.show()

