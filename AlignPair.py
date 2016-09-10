import numpy as np
import matplotlib.pyplot as plt

# Input two 2d images to be aligned to each other, manually (visually)

class AlignPair(object):
# Class for the pair of images which need aligning to each other
	def __init__(self, Img1, Img2):
		self.Img1 = Img1
		self.Img2 = Img2
		self.size1 = np.shape(Img1)
		self.size2 = np.shape(Img2)
		self.xy = np.array([0, 0]) # Top left corners both at (0,0)
		self.pad1, self.pad2 = self.FindPad(self.size1, self.size2)
		self.Img1lim = self.FindContrastLims(self.Img1)
		self.Img2lim = self.FindContrastLims(self.Img2)

	def FindPad(self, size1, size2):
#Find the padding required to make the images the same size
		sizediff = np.subtract(self.size2, self.size1)
		pad1 = ((0, np.sort([sizediff[0], 0])[-1]), (0, np.sort([sizediff[1], 0])[-1]))
		pad2 = ((0, np.sort([-sizediff[0], 0])[-1]), (0, np.sort([-sizediff[1], 0])[-1]))
		return pad1, pad2

	def FindContrastLims(self, Img):
#Extract the contrast limits for the input image (min and max intensity value)
		Imglim = [np.min(Img[~np.isnan(Img)]), np.max(Img[~np.isnan(Img)])]
		return Imglim

	def PadImgs(self, Img, pad):
		paddedIm = np.pad(Img.astype(float), pad, 'constant', constant_values = (np.nan,))
		return paddedIm

class AlignPlot(object):
#Class to define plot for interactive aligning of images
	def __init__(self, ImgPair):
		self.fig = plt.figure()
		self.ax = plt.axes([0.05, 0.05, 0.95, 0.95])
		self.Img1 = ImgPair.PadImgs(ImgPair.Img1, ImgPair.pad1)
		self.Img2 = ImgPair.PadImgs(ImgPair.Img2, ImgPair.pad2)
		self.paddedIms = AlignPair(self.Img1, self.Img2)
		self.ShowImages(self.paddedIms, self.ax)
		self.cidkey = self.fig.canvas.mpl_connect('key_press_event', self.MoveImg)
		self.horizontal = 0
		self.vertical = 0
		plt.show()

	def ShowImages(self, ImgPair, ax):
#Refresh the axis and plot the input pair of images
		ax.cla()
		ax.imshow(ImgPair.Img1, interpolation = 'none', cmap = 'Blues')
		ax.imshow(ImgPair.Img2, interpolation = 'none', cmap = 'Reds', clim = ImgPair.Img2lim, 
			alpha = 0.5)
		ax.axis('off')
		self.fig.canvas.draw()

	def MoveImg(self, event):
#Calculations to do on pressing a button - arrow keys to move top image to overlay the bottom
			if event.key == 'right':
				self.horizontal += 1
			elif event.key == 'left':
				self.horizontal -= 1
			elif event.key == 'up':
				self.vertical -= 1
			elif event.key == 'down':
				self.vertical += 1
			elif event.key == 'enter':
				self.fig.canvas.mpl_disconnect(self.cidkey)
				plt.clf()
				moveImg2 = np.roll(np.roll(self.paddedIms.Img2, self.horizontal, axis = 1), 
					self.vertical, axis = 0)
			else:
				return
			moveImg2 = np.roll(np.roll(self.paddedIms.Img2, self.horizontal, axis = 1), 
				self.vertical, axis = 0)
			self.paddedIms.Img2 = moveImg2
			self.ShowImages(self.paddedIms, self.ax)


