from __future__ import division

import numpy as np
from matplotlib.patches import Polygon
import collections
import matplotlib.pyplot as plt
import matplotlib.path as path
#from SpectrumImagePlotter import PatchWatcher

class PolygonGroupManager(object):
	def __init__(self, axis):
		''' Dictionary containing integer key for each polygon group used 
		Pass polygons from Creator to the correct Group'''
		self.currentID = 0
		self.axis = axis
		self.polyDict = collections.OrderedDict()
		self.polyDict[self.currentID] = PolygonGroup(self.axis, 'k')
		self.RecolourGroups()
#		self.cmap = ...
#		

	def AddPolygon(self, polygon):
		print "I gots me a polygon"
		self.polyDict[self.currentID].AddPolygon(polygon)
		
		
	def NewGroup(self):
		print "makin' me a new group, boss"
		self.polyDict[self.currentID].Deselect()
		self.currentID = max(self.polyDict.keys()) + 1
		self.polyDict[self.currentID] = PolygonGroup(self.axis, 'k')
		self.RecolourGroups()
		print self.currentID
		
	def NextGroup(self, step=1):
		self.polyDict[self.currentID].Deselect()
		self.currentID = (self.currentID + step) % (max(self.polyDict.keys()) + 1)
		self.polyDict[self.currentID].SelectNext()
		print self.currentID
		
	def RecolourGroups(self):
		colours = plt.get_cmap('Paired')
		for (i, g) in self.polyDict.items():
			g.SetColour(colours(i/len(self.polyDict)))
			
	def NextPolygon(self, step=1):
		self.polyDict[self.currentID].SelectNext(step)
		
	def GetActivePolygon(self):
		return self.polyDict[self.currentID].GetActivePolygon()
		
#	def GetActiveMask(self, masksize):
#		mask = self.polyDict[self.currentID].GetMask(masksize)
#		return mask

class PolygonGroup(object):
	def __init__(self, axis, colour):
		'''A single group of polygons, containing one or more polygons to mask 
		an area of the image'''
		self.colour = colour
		self.axis = axis
		self.polygonList = []
		self.selected = None
#		self.MaskOn = PatchWatcher()
		
	def AddPolygon(self, polygon):
		self.polygonList.append(polygon)
		polygon.set_facecolor(self.colour)
		self.Select(len(self.polygonList)-1)
		
	def SetColour(self, colour):
		self.colour = colour
		for p in self.polygonList:
			p.set_facecolor(colour)
			
	def Select(self, i):
		self.Deselect()
		self.selected = i
		self.polygonList[self.selected].set_linewidth(3)
		
	def SelectNext(self, step=1):
		if not self.polygonList:
			return
		if self.selected is None:
			self.Select(0)
		else:
			self.Select((self.selected + step) % len(self.polygonList))

	def Deselect(self):
		if self.selected is not None:
			self.polygonList[self.selected].set_linewidth(1)
		self.selected = None
		
	def GetActivePolygon(self):
		if self.selected is not None:
			return self.polygonList[self.selected]
		
#	def GetMask(self, masksize):
##		PatchWatcher.MaskOn = not PatchWatcher.MaskOn
#		if PatchWatcher.MaskOn:
#			mesh = np.transpose(np.reshape(np.meshgrid(np.arange(masksize[1]), np.arange(masksize[0])),
#				(2, masksize[0] * masksize[1])))
#			testp = []
#			print 'mask!'
#			for ii in self.polygonList:
#				testp.append(np.reshape(path.Path(ii.get_xy()).contains_points(mesh), (masksize[0], masksize[1])))
#			mask = np.sum(testp, axis = 0)
#		else:
#			mask = np.zeros(masksize)
##		print PatchWatcher.MaskOn
#		return mask
