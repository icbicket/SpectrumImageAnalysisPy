import numpy as np
from skimage import data
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import Image
import PolygonMover

pic = Image.Image(data.chelsea()[:, :, 0])
polycorners = np.array([[20,20],[20,200],[100,200],[100,20]])

poly = Polygon(polycorners, color = 'red', alpha = 0.5)


fig, ax = plt.subplots()
plt.imshow(pic.data, cmap = 'Blues')
ax.add_patch(poly)
x = PolygonMover.PolygonMover(poly, ax)
plt.show()
