import Image
import AlignLib
from skimage import data
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'xmin, ymin, xmax, ymax')

p1 = Image.Image(data.camera())
p2 = Image.Image(data.coins())
p3 = Image.Image(data.chelsea()[:, :, 0])
p4 = Image.Image(data.astronaut()[:, :, 0])
print np.shape(p1.Img), np.shape(p2.Img), np.shape(p3.Img), np.shape(p4.Img)

offsets = AlignLib.Align((p1,p2,p3,p4))
print offsets

def MoveAlignedImages(image, offsets):
	image.Img = np.roll(np.roll(image.Img, 
			offsets[0], axis = 1), 
			offsets[1], axis = 0)
#	mask = 
	mask = np.all(np.isnan(image.Img), axis = 0)
	mask0 = np.all(np.isnan(image.Img), axis = 1)
	image.Img = image.Img[:, ~mask]
	image.Img = image.Img[~mask0, :]
	return image
	

#	Img1a = np.copy(Img1)
#	Img2a = np.copy(Img2)

#	if self.horizontal >= 0:
#		Img2a = Img2a[:, self.horizontal:]
#		Img1a = Img1a[:, self.horizontal:]
#	#			self.Img2 = self.Img2[:, self.horizontal:]
#		self.Img1 = self.Img1[:, self.horizontal:]
#	else:
#		Img2a = Img2a[:, :self.horizontal]
#		Img1a = Img1a[:, :self.horizontal]
#	#			self.Img2 = self.Img2[:, :self.horizontal]
#	#			self.Img1 = self.Img1[:, :self.horizontal]

#	if self.vertical >= 0:
#		Img2a = Img2a[self.vertical:, :]
#		Img1a = Img1a[self.vertical:, :]
#		self.Img2 = self.Img2[self.vertical:, :]
#		self.Img1 = self.Img1[self.vertical:, :]
#	else:
#		Img2a = Img2a[:self.vertical, :]
#		Img1a = Img1a[:self.vertical, :]
#		self.Img2 = self.Img2[:self.vertical, :]
#		self.Img1 = self.Img1[:self.vertical, :]
#	#		print np.where(np.isnan(Img1a))
#	self.ax2 = plt.axes([0.05, 0.05, 0.90, 0.90])
#	#		plt.imshow(Img2a)
#	self.ShowImages(self.Img1, self.Img2, self.ax2)			
#	#		plt.close()



#p2a = MoveAlignedImages(p2, offsets[:, 1])
#print p1.size, p2.size
r1 = Rectangle(offsets[0, 0], offsets[1,0], p1.size[1]+offsets[0,0], p1.size[0]+offsets[1,0])
r2 = Rectangle(offsets[0, 1], offsets[1,1], p2.size[1]+offsets[0,1], p2.size[0]+offsets[1,1])

def FindRectangleIntersectionWillsWay(r1, r2):
	if (r1.xmax<r2.xmin or r2.xmax<r1.xmin or r1.ymax<r2.ymin or r2.ymax<r1.ymin):
		raise ValueError("No intersection! Fix it!")

	h_edge = sorted((r1.xmin, r1.xmax, r2.xmin, r2.xmax))
	v_edge = sorted((r1.ymin, r1.ymax, r2.ymin, r2.ymax))
	return Rectangle(h_edge[1], v_edge[1], h_edge[2], v_edge[2])

print "Will's rectangle stuff"
#r1=Rectangle(0,0,10,10)
#r2=Rectangle(2,2,17,17)
print FindRectangleIntersectionWillsWay(r1, r2)

#print h_edge, v_edge
#r_overlap = Rectangle(v_edge[1], h_edge[1], v_edge[2], h_edge[2]) 

#p1b = p1.Img[r_overlap.xmin-offsets[0,0]:r_overlap.xmax-offsets[0,0], 
#	r_overlap.ymin-offsets[1,0]:r_overlap.ymax-offsets[1,0]]

#print r_overlap.xmin-offsets[0,1], r_overlap.xmax-offsets[0,1], r_overlap.ymin-offsets[1,1], r_overlap.ymax-offsets[1,1]
#p2b = p2.Img[r_overlap.xmin-offsets[0,1]:r_overlap.xmax-offsets[0,1], 
#	r_overlap.ymin-offsets[1,1]:r_overlap.ymax-offsets[1,1]]

print 'offsets', offsets
#print 'sizes', np.roll(np.transpose((p1.size, p2.size, p3.size, p4.size)), 1, axis = 0)

maxcorners = np.roll(np.transpose((p1.size, p2.size, p3.size, p4.size)), 1, axis = 0)
overlapcorners = (np.max(offsets, axis = 1), np.min(maxcorners+offsets, axis = 1))

print 'overlapcorners', overlapcorners

p1_aligned = p1.Img[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]
p2_aligned = np.roll(np.roll(p2.Img, 
			offsets[0][1], axis = 1), 
			offsets[1][1], axis = 0)
p2_aligned = p2_aligned[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]

p3_aligned = np.roll(np.roll(p3.Img, 
			offsets[0][2], axis = 1), 
			offsets[1][2], axis = 0)
p3_aligned = p3_aligned[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]

p4_aligned = np.roll(np.roll(p4.Img, 
			offsets[0][3], axis = 1), 
			offsets[1][3], axis = 0)
p4_aligned = p4_aligned[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]
#p3_aligned = p3.Img[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]
#p4_aligned = p4.Img[overlapcorners[0][1]:overlapcorners[1][1], overlapcorners[0][0]:overlapcorners[1][0]]

#p1.Img = np.roll(np.roll(p1.Img, offsets[0][0], axis = 1), offsets[1][0], axis = 0)
#p2.Img = np.roll(np.roll(p2.Img, offsets[0][1], axis = 1), offsets[1][1], axis = 0)

#mask = ~np.isnan(p1.Img)&~np.isnan(p2.Img)&~np.isnan(p3.Img)&~np.isnan(p4.Img)

fig = plt.figure()
ax = plt.axes([0,0,1,1])
ax.imshow(p2_aligned, interpolation = 'none', cmap = 'Reds')
ax.imshow(p3_aligned, interpolation = 'none', cmap = 'gray', alpha = 0.2)
#ax.imshow(p4_aligned, interpolation = 'none', cmap = 'hot', alpha = 0.2)
ax.imshow(p1_aligned, alpha = 0.2, cmap = 'Blues', interpolation = 'none')
#ax.imshow(mask, cmap = 'gray', alpha = 0.8)
ax.axis('off')

plt.show()
