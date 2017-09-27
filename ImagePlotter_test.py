import ImagePlotter
import unittest

class cbarextensionfinder(unittest.TestCase):
	def testclimequalimglim(self):
		''' 
		What happens if the colour limits are equal to the image limits?
		'''
		clim = [0, 10]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('neither', cbar_extend)
		
	def testclimsmallbottom(self):
		'''	
		What happens if the minimum of the colour limit is smaller than the 
		minimum of the image limit, but the max of both are the same?
		'''
		clim = [5, 10]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('min', cbar_extend)

	def testclimsmalltop(self):
		'''
		If the minimum of the colour limit is the same as the minimum of the 
		image limit, but the maximums of the colour limit is smaller than the 
		maximum of the image limit.
		'''
		clim = [0, 4]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('max', cbar_extend)
		
	def testclimsmalltopbottom(self):
		'''
		If the minimum of the colour limit is greater than the minimum of the 
		image limit and the maximum of the colour limit is less than the 
		maximum of the image limit
		'''
		clim = [4, 7]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('both', cbar_extend)
		
	def testclimbigtopbottom(self):
		'''
		If the minimum of the colour limit is less than the minimum of the 
		image limit and the maximum of the colour limit is greater than the 
		maximum of the image limit.
		'''
		clim = [-1, 12]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('neither', cbar_extend)
		
	def testclimbigtop(self):
		'''
		If the minimum of the colour limit is the same as the minimum of the 
		image limit and the maximum of the colour limit is greater than the
		maximum of the image limit
		'''
		clim = [0, 12]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('neither', cbar_extend)
	
	def testclimbigbottom(self):
		'''
		If the minimum of the colour limit is less than the minimum of the 
		image limit and the maxima are the same.
		'''
		clim = [-2, 10]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('neither', cbar_extend)
		
	def testclimbigbottomsmalltop(self):
		'''
		If the minimum of the colour limit is smaller than the minimum of the
		image limit and the maximum of the colour limit is smaller than the 
		maximum of the image limit
		'''
		clim = [-2, 8]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('max', cbar_extend)
		
	def testclimsmallbottombigtop(self):
		'''
		If the minimum of the colour limit is greater than the minimum of the
		image limit and the maximum of the colour limit is greater than the 
		maximum of the image limit.
		'''
		clim = [2, 12]
		imglim = [0, 10]
		cbar_extend = ImagePlotter.cbarextensionfinder(clim, imglim)
		self.assertEqual('min', cbar_extend)
		
if __name__ == '__main__':
	unittest.main()
