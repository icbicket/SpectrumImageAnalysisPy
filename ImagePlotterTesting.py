import numpy as np
from skimage import data
import ImagePlotter
import Image
import matplotlib.pyplot as plt
import PolygonCreator
import matplotlib.artist as artst
from matplotlib.patches import Polygon

im = Image.Image(data.chelsea()[:, :, 0])

fig = plt.figure()
ax = plt.axes([0,0,1,1])
implot = ImagePlotter.ImagePlotter(im, ax)
#creator = PolygonCreator.PolygonCreator(ax)
print ax.findobj(Polygon)

plt.show()
print ax.findobj(Polygon)
#im2 = Image.Image(im.data*implot.mask)
#fig2 = plt.figure()
#ax2 = plt.axes([0,0,1,1])
#implot2 = ImagePlotter.ImagePlotter(im2, ax2)
#plt.show()
