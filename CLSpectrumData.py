import numpy as np		
from SpectrumImage import SpectrumImage
from Image import Image
import h5py

def Readh5SI(filename):
	""" Read hdf5 data file (written for CL data from Odemis)"""
	fuzzing = False
	print 'Loading...', filename
	data = h5py.File(filename, 'r')
	for kk in data.keys()[:4]:
		AcqData = data[kk]['ImageData']['Image']
		DataShape = np.shape(AcqData)
		if DataShape[0] != 1:
			SI = np.array(AcqData)
		elif DataShape[1] != 1:
			_ = AcqData # Drift image
		elif DataShape[3] == DataShape[4] == 512:
			survey = AcqData
		else:
			SEM = AcqData	
	if np.shape(SEM)[3] == 4 * np.shape(SI)[3]:
		fuzzing = True
	return SI, SEM, survey, fuzzing


class CLDataSet(object):
	""" Create CL data set, either given data set or loading from file, 
	    includes survey image, SEM image, and spectrum image"""
	def __init__(self, SI = np.array([]), SEM=np.array([]), survey=np.array([]), fuzzing=False):
		self.fuzzing = fuzzing
		self.SI = SpectrumImage(SI)
		self.SEM = Image(SEM)
		self.survey = Image(survey)

	@classmethod
	def LoadFromFile(cls, filename):
		SI, SEM, survey, fuzzing = Readh5SI(filename)
		return cls(SI=SI, SEM=SEM, survey=survey, fuzzing=fuzzing)
