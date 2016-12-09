import numpy as np

def AlignCrop(images, offsets):
	'''Crops images given a list of input Images (Image class) and corresponding offsets from each other: images should be aligned according to offsets
	offsets is a 2 by N array, with x on top row, y offsets on bottom row'''
	maxcorners = np.array([])
	for ii in images:
		maxcorners = np.append(maxcorners, ii.size[:2])
	maxcorners = np.roll(np.reshape(maxcorners, 
		(2, len(maxcorners)/2), order = 'F'), 1, axis = 0)
	overlapcorners = (np.max(offsets, axis = 1).astype(int), np.min(maxcorners + offsets, axis = 1).astype(int))
	index = 0
	for ii in images:
		ii.data = ii.data[overlapcorners[0][1] - offsets[1][index]:
			            overlapcorners[1][1] - offsets[1][index], 
			            overlapcorners[0][0] - offsets[0][index]:
			            overlapcorners[1][0] - offsets[0][index]] #Maybe fix this to make new set of aligned images
		ii.size = np.shape(ii.data)
		index += 1
