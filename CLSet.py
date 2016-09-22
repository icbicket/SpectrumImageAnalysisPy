import numpy as np
import CLSpectrumData
import AlignLib

class CLSet(object):
	"""CLSet includes a sample spectrum image dataset, and the associated substrate and dark references"""
	def __init__(self, samplefile, darkfile, substratefile):
		self.SampleSI = CLSpectrumData.CLDataSet.LoadFromFile(samplefile)
		self.darkSI = CLSpectrumData.CLDataSet.LoadFromFile(darkfile)
		self.substrateSI = CLSpectrumData.CLDataSet.LoadFromFile(substratefile)
		"""Perform dark correction on sample and on substrate"""
		self.sample_dark = CLSpectrumData.CLDataSet(
			SI = self.SpectrumSubtraction(self.SampleSI, self.darkSI), 
			SEM = self.SampleSI.SEM.Img, 
			survey = self.SampleSI.survey.Img)
		self.substrate_dark = CLSpectrumData.CLDataSet(
			SI = self.SpectrumSubtraction(self.substrateSI, self.darkSI), 
			SEM = self.SampleSI.SEM.Img, 
			survey = self.SampleSI.survey.Img)
		"""Perform substrate correction on sample data"""
		self.sample_dark_substrate = CLSpectrumData.CLDataSet(
			SI = self.SpectrumSubtraction(self.sample_dark, self.substrate_dark), 
			SEM = self.SampleSI.SEM.Img, 
			survey = self.SampleSI.survey.Img)

	def SpectrumSubtraction(self, spectra, correction):
		corrected = spectra.SI.data - np.mean(np.mean(correction.SI.data, axis = -1, keepdims = True), axis = -2, keepdims = True)
		return corrected

class PolarimetrySet(object):
	"""Polarimetry set takes in a set of six polarimetry data sets to calculate the Stokes parameters and degrees of polarization"""
	def __init__(self, PolSetData):
		self.QWP0Pol0 = PolSetData['QWP0_Pol0']
		self.QWP315Pol45 = PolSetData['QWP315_Pol45']
		self.QWP270Pol45 = PolSetData['QWP270_Pol45']
		self.QWP270Pol90 = PolSetData['QWP270_Pol90']
		self.QWP270Pol135 = PolSetData['QWP270_Pol135']
		self.QWP45Pol135 = PolSetData['QWP45_Pol135']
		self.offsets = AlignLib.Align(PolSetData)
#		self.S0_total = self.QWP270Pol90.SI + self.QWP0Pol0.SI

#		self.S1 = self.QWP270Pol90.SI - self.QWP0Pol0.SI
#		self.S2 = self.QWP45Pol135.SI - self.QWP315Pol45.SI
#		self.S3 = self.QWP270Pol135.SI - self.QWP270Pol45.SI

#		self.DoP = np.sqrt(S1**2 + S2**2 + S3**2)/S0
#		self.S0_pol = self.DoP * self.S0_total
#		self.S0_unpol = (1 - self.DoP) * self.S0_total
#	def MoveAlignedImages(self):
#		

