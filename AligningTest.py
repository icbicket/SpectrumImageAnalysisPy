import Image
import AlignLib
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
import AlignCrop
import SpectrumImage

Rectangle = namedtuple('Rectangle', 'xmin, ymin, xmax, ymax')
p1shaped = np.reshape(data.camera(), (1,1,1,512,512))

p1 = Image.Image(p1shaped)
p2 = Image.Image(data.coins())
p3 = Image.Image(data.chelsea()[:, :, 0])
p4 = Image.Image(data.astronaut()[:, :, 0])
#print np.shape(p1.data), np.shape(p2.data), np.shape(p3.data), np.shape(p4.data)

offsets = AlignLib.Align((p1,p2,p3,p4))
#print offsets


################Will's thing
r1 = Rectangle(offsets[0, 0], offsets[1,0], p1.size[1]+offsets[0,0], p1.size[0]+offsets[1,0])
r2 = Rectangle(offsets[0, 1], offsets[1,1], p2.size[1]+offsets[0,1], p2.size[0]+offsets[1,1])

def FindRectangleIntersectionWillsWay(r1, r2):
	if (r1.xmax<r2.xmin or r2.xmax<r1.xmin or r1.ymax<r2.ymin or r2.ymax<r1.ymin):
		raise ValueError("No intersection! Fix it!")

	h_edge = sorted((r1.xmin, r1.xmax, r2.xmin, r2.xmax))
	v_edge = sorted((r1.ymin, r1.ymax, r2.ymin, r2.ymax))
	return Rectangle(h_edge[1], v_edge[1], h_edge[2], v_edge[2])

#print "Will's rectangle stuff"
#r1=Rectangle(0,0,10,10)
#r2=Rectangle(2,2,17,17)
#print FindRectangleIntersectionWillsWay(r1, r2)
################End of Will's thing


#maxcorners = np.roll(np.transpose((p1.size, p2.size, p3.size, p4.size)), 1, axis = 0)
#overlapcorners = (np.max(offsets, axis = 1), np.min(maxcorners+offsets, axis = 1))
#p2_alignedtest = p2.data[overlapcorners[0][1] - offsets[1][1]:overlapcorners[1][1]-offsets[1][1], overlapcorners[0][0] - offsets[0][1]:overlapcorners[1][0] - offsets[0][1]]
print (offsets)
AlignCrop.AlignCrop((p1, p2, SpectrumImage.SpectrumImage(data.chelsea()), SpectrumImage.SpectrumImage(data.astronaut())), offsets)



fig = plt.figure()
ax = plt.axes([0,0,1,1])
ax.imshow(p3.data, interpolation = 'none', cmap = 'gray')
ax.imshow(p1.data, interpolation = 'none', cmap = 'Reds', alpha = 0.2)
#ax.imshow(p4_aligned, interpolation = 'none', cmap = 'hot', alpha = 0.2)
#ax.imshow(p1_aligned, alpha = 0.2, cmap = 'Blues', interpolation = 'none')
#ax.imshow(mask, cmap = 'gray', alpha = 0.8)
ax.axis('off')

plt.show()
