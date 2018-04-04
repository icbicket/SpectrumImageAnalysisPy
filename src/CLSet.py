import numpy as np
import CLSpectrumData
import AlignLib

class CLSet(object):
    """CLSet includes a sample spectrum image dataset, and the associated substrate and dark references"""
    def __init__(self, samplefile, darkfile=None, substratefile=None, correction_spectrum=None):
        self.SampleSI = CLSpectrumData.CLDataSet.LoadFromFile(samplefile)

        if darkfile is not None:
            self.darkSI = CLSpectrumData.CLDataSet.LoadFromFile(darkfile)

        if substratefile is not None:
            self.substrateSI = CLSpectrumData.CLDataSet.LoadFromFile(substratefile)
#                self.substrate_dark = CLSpectrumData.CLDataSet(
#                    SI = self.SpectrumSubtraction(self.substrateSI, self.darkSI), 
#                    Wavelengths = self.SampleSI.SI.SpectrumRange,
#                    SEM = self.SampleSI.SEM.data, 
#                    survey = self.SampleSI.survey.data)
        
        if correction_spectrum is not None:
            self.correction_spectrum = correction_spectrum
#                    self.sample_dark_substrate_sys = CLSpectrumData.CLDataSet(
#                    SI = self.SpectrumMultiplication(self.sample_dark_substrate, correction_spectrum), 
#                    Wavelengths = self.SampleSI.SI.SpectrumRange,
#                    SEM = self.SampleSI.SEM.data, 
#                    survey = self.SampleSI.survey.data)
            
    def ReferenceCorrection(self, correction):
        sample_corr = CLSpectrumData.CLDataSet(
                SI = self.SpectrumSubtraction(self.SampleSI, correction), 
                Wavelengths = self.SampleSI.SI.SpectrumRange,
                SEM = self.SampleSI.SEM.data, 
                survey = self.SampleSI.survey.data)
        return sample_corr

#    def SubstrateCorrection(self):
#        self.sample_substrate = CLSpectrumData.CLDataSet(
#            SI=self.SpectrumSubtraction(self.sampleSI, self.substrateSI), 
#                    Wavelengths = self.SampleSI.SI.SpectrumRange,
#                    SEM = self.SampleSI.SEM.data, 
#                    survey = self.SampleSI.survey.data)
                    
#            self.sample_dark_substrate = CLSpectrumData.CLDataSet(
#                    SI = self.SpectrumSubtraction(self.sample_dark, self.substrate_dark), 
#                    Wavelengths = self.SampleSI.SI.SpectrumRange,
#                    SEM = self.SampleSI.SEM.data, 
#                    survey = self.SampleSI.survey.data)
            
    def SystemCorrection(self, spectra):
        sys_corr = CLSpectrumData.CLDataSet(
            SI = self.SpectrumMultiplication(spectra, self.correction_spectrum), 
                Wavelengths = self.SampleSI.SI.SpectrumRange,
                SEM = self.SampleSI.SEM.data, 
                survey = self.SampleSI.survey.data)
        return sys_corr
            
    def SpectrumSubtraction(self, spectra, correction):
        corrected = spectra.SI.data - np.mean(np.mean(correction.SI.data.data, axis = 0, keepdims = True), axis = 1, keepdims = True)
        return corrected
        
    def SpectrumMultiplication(self, spectra, correction):
        #spectra: SpectrumImage, correction: Spectrum, for system correction factor
        corrected = spectra.SI.data * correction.intensity
        return corrected

class PolarimetrySet(object):
    """Polarimetry set takes in a set of six polarimetry data sets to calculate the Stokes parameters and degrees of polarization"""
    def __init__(self, PolSetData, SI_name='SampleSI'):
        self.QWP0Pol0 = PolSetData['QWP0_Pol0']
        self.QWP315Pol45 = PolSetData['QWP315_Pol45']
        self.QWP270Pol45 = PolSetData['QWP270_Pol45']
        self.QWP270Pol90 = PolSetData['QWP270_Pol90']
        self.QWP270Pol135 = PolSetData['QWP270_Pol135']
        self.QWP45Pol135 = PolSetData['QWP45_Pol135']

        '''Stokes parameters calculation'''
        self.S0_total = getattr(self.QWP270Pol90, SI_name).SI.data + getattr(self.QWP0Pol0, SI_name).SI.data
        self.S0_total = self.S0_total.astype(float)

        self.S1 = getattr(self.QWP270Pol90, SI_name).SI.data - getattr(self.QWP0Pol0, SI_name).SI.data
        self.S2 = getattr(self.QWP45Pol135, SI_name).SI.data - getattr(self.QWP315Pol45, SI_name).SI.data
        self.S3 = getattr(self.QWP270Pol135, SI_name).SI.data - getattr(self.QWP270Pol45, SI_name).SI.data

        self.DoP = np.sqrt(self.S1**2 + self.S2**2 + self.S3**2)/self.S0_total
        self.DoLP = np.sqrt(self.S1**2 + self.S2**2)/self.S0_total
        self.DoCP = self.S3/self.S0_total
        
        self.S0_pol = self.DoP * self.S0_total
        self.S0_unpol = (1 - self.DoP) * self.S0_total
#    def MoveAlignedImages(self):
#        

