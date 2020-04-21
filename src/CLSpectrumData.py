from __future__ import print_function
import numpy as np        
import SpectrumImage
from Image import Image
import h5py

def Readh5SI(filename):
    """ Read hdf5 data file (written for CL data from Odemis)"""
    fuzzing = False
    print('Loading...', filename)
    data = h5py.File(filename, 'r')
    SEM = np.array([])
    survey = np.array([])
    for kk in list(data)[:4]:
#    for kk in data.keys()[:4]:
        if 'Acquisition' in kk:
            AcqData = data[kk]['ImageData']['Image']
            DataShape = np.shape(AcqData)
            if DataShape[0] != 1:
                SI = np.array(AcqData)[:, 0, 0, :, :]
                Wavelengths = np.array(data[kk]['ImageData']['DimensionScaleC'])
            elif DataShape[1] != 1:
                _ = AcqData # Drift image
            elif DataShape[3] == DataShape[4] == 512:
                survey = Image(np.squeeze(AcqData), calibration=np.array(data[kk]['ImageData']['DimensionScaleX']))
            else:
                SEM = Image(np.squeeze(AcqData), calibration=np.array(data[kk]['ImageData']['DimensionScaleX']))
    if np.shape(SEM.data)[-1] == 4 * np.shape(SI)[-1]:
        fuzzing = True
    return SI, Wavelengths, SEM, survey, fuzzing


class CLDataSet(object):
    """ Create CL data set, either given data set or loading from file, 
        includes survey image, SEM image, and spectrum image"""
    def __init__(self, SI = np.array([]), Wavelengths = np.array([]), SEM=np.array([]), survey=np.array([]), fuzzing=False):
        self.fuzzing = fuzzing
        self.SI = SpectrumImage.CLSpectrumImage(SI, Wavelengths)
        self.SEM = SEM
        self.survey = survey
        if self.fuzzing:
            reshapedSEM = np.reshape(self.SEM.data, [int(self.SEM.size[0]/4), 4, int(self.SEM.size[1]/4), 4])
            self.unfuzzedSEM = Image(np.sum(np.sum(reshapedSEM, axis=1), axis=-1), calibration=self.SEM.calibration*4)
        else:
            self.unfuzzedSEM = self.SEM

    @classmethod
    def LoadFromFile(cls, filename):
        SI, Wavelengths, SEM, survey, fuzzing = Readh5SI(filename)
        print(np.shape(SI))
        # This will probably not work for all SIs...need to fix & test!
        if SI.ndim == 2:
            SI = np.expand_dims(SI, -1)
        print(np.shape(SI))
        SI = np.transpose(SI, (1, 2, 0))
        return cls(SI=SI, Wavelengths = Wavelengths*1e9, SEM=SEM, survey=survey, fuzzing=fuzzing)
