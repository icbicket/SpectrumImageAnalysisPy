import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'axes.labelcolor': 'w'})

class PolarPlot(object):
	def __init__(self, data, axis, colourbar_axis=None, binning=4, maxintensity=None, cmap='hot'):
		self.data = data
		self.axis = axis
		self.binning = binning
		self.colourbar_axis = colourbar_axis
		self.cmap = cmap
		if not maxintensity:
			self.maxintensity = np.max(np.max(self.data))
		else:
			self.maxintensity = maxintensity
		
		self.axis.figure.patch.set_facecolor('black')
		self.axis.set_axis_off()

		self.image = self.axis.imshow(self.data, cmap=self.cmap, vmax=self.maxintensity, interpolation='none')
		self.PolarLinesLabels()
		
		if self.colourbar_axis:
			self.colourbar = plt.colorbar(mappable=self.image, cax=self.colourbar_axis, format=plt.ScalarFormatter())
			self.colourbar.formatter.set_powerlimits((-3,3))
			self.colourbar.update_ticks()
			self.colourbar_axis.tick_params(colors='w')
			self.colourbar_axis.yaxis.get_offset_text().set_color('w')
			self.colourbar_axis.tick_params(direction='out')
		self.axis.invert_yaxis()
		
	def PolarLinesLabels(self):
		plrf = self.binning/2
		angle0 = np.arange(0, 2*np.pi, np.pi/1600)
		angle1 = np.arange(0, 11/6*np.pi, np.pi/6)
		
		xdata =((200 / 3) * np.sin(angle0) + 200) / plrf
		ydata =((200 / 3) * np.cos(angle0) + 200) / plrf
		xdata1=(200 * np.sin(angle0) + 200) / plrf
		ydata1=(200 * np.cos(angle0) + 200) / plrf
		xdata2=(400 / 3 * np.sin(angle0) + 200) / plrf
		ydata2=(400 / 3*np.cos(angle0) + 200) / plrf
		plr=200 / plrf
		self.axis.plot(xdata, ydata, '--w', 
		         xdata1,ydata1,'--w', 
		         xdata2,ydata2,'--w', 
		         lw = 1.5)
		xdata4 = (plr * np.sin(angle1) + plr, -plr * np.sin(angle1) + plr)
		ydata4 = (plr * np.cos(angle1) + plr, -plr * np.cos(angle1) + plr)
		self.axis.plot(xdata4, ydata4, ':w', lw = 2.5);

		# Get rid of whitespaces
		self.axis.xaxis.set_major_locator(plt.NullLocator())
		self.axis.yaxis.set_major_locator(plt.NullLocator())

		# Add axis label text
		self.axis.text(202/plrf, 246/plrf, '30', color = 'w', fontsize = 15)
		self.axis.text(217/plrf, 311/plrf, '60', color = 'w', fontsize = 15)
		self.axis.text(237/plrf, 374/plrf, '90', color = 'w', fontsize = 15)
		self.axis.text(298/plrf, 387/plrf, '30', color = 'w', fontsize = 15)
		self.axis.text(68/plrf, 387/plrf, '330', color = 'w', fontsize = 15)
		self.axis.text(296/plrf, 12/plrf, '150', color = 'w', fontsize = 15)
		self.axis.text(69/plrf, 12/plrf, '210', color = 'w', fontsize = 15)
		self.axis.text(365/plrf, 73/plrf, '120', color = 'w', fontsize = 15)
		self.axis.text(0, 73/plrf, '240', color = 'w', fontsize = 15)
		self.axis.text(373/plrf, 328/plrf, '60', color = 'w', fontsize = 15)
		self.axis.text(0, 328/plrf, '300', color = 'w', fontsize = 15)
