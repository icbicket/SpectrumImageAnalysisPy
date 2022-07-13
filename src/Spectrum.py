from __future__ import print_function
from __future__ import division
import numpy as np
import csv
from scipy.ndimage.filters import gaussian_filter1d
import os
import file_namer
import spectrum_functions as specfun
import sys
from scipy import stats

def open_csv(filename, mode='r'):
    """Open a csv file in proper mode depending on Python version."""
    return(open(filename, mode=mode+'b') if sys.version_info[0] == 2 else
           open(filename, mode=mode, newline=''))

def ImportCSV(filename):
    x = np.genfromtxt(filename,
                       delimiter = '\t', dtype = None, skip_header = 1)
    return x
    
class Spectrum(object):
    def __init__(self, intensity, units, SpectrumRange=None):
        self.intensity = intensity
        self.units = units
        self.length = len(self.intensity)
        self.SpectrumRange = SpectrumRange
        
    def SaveSpectrumAsCSV(self,filename):
        filename = file_namer.name_file(filename)
        ExportSpectrumRange = np.copy(self.SpectrumRange)
        ExportIntensity = np.copy(self.intensity)
        ExportSpectrumRange.resize(len(ExportSpectrumRange), 1)
        ExportIntensity.resize(len(ExportIntensity), 1)
        ExportData = np.append(ExportSpectrumRange, ExportIntensity, axis = 1)
        ExportHeaders = [
            (self.unit_label + ' (' + self.units + ')'), 
            'Intensity']
        with open_csv(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter = '\t')
            writer.writerow(ExportHeaders)
            writer.writerows(ExportData)
        print('Saved file...', filename)

    def SmoothingFilter1D(self, sigma=2):
        kernel = np.array([1, 1, 2, 1, 1])/6.
        intensity = np.append(self.intensity[4::-1], np.append(self.intensity, self.intensity[-5::]))
        smoothed = np.convolve(intensity, kernel, mode='same')
        smoothed = gaussian_filter1d(self.intensity, sigma)
#        smoothed[self.intensity > (0.01*np.max(self.intensity))] = self.intensity[self.intensity > (0.01*np.max(self.intensity))]
        return smoothed
        
class CLSpectrum(Spectrum):
    def __init__(self, intensity, WavelengthRange, units='nm'):
        super(CLSpectrum, self).__init__(intensity, units)
        self.SpectrumRange = WavelengthRange
        self.unit_label = 'Wavelength'
        self.secondary_units = 'eV'
        self.secondary_unit_label = 'Energy'
    
    @classmethod
    def LoadFromCSV(cls, filename):
        spectrum = ImportCSV(filename)
        return cls(intensity=spectrum[:, 1], WavelengthRange=spectrum[:, 0], units='nm')


class EELSSpectrum(Spectrum):
    def __init__(self, intensity, SpectrumRange=None, channel_eV = None, dispersion=0.005, ZLP=None, units='eV'):
        '''intensity: 1D array
           SpectrumRange: 1D array
           channel_eV: 2 element array [channel #, eV value]
           dispersion: float, width of each channel, must be provided if SpectrumRange is not, default is 5meV
           ZLP: Boolean - True=ZLP is present
           units: string, for plot axis
           '''
        super(EELSSpectrum, self).__init__(intensity, units)
        if (SpectrumRange is not None):
            if (len(intensity) != len(SpectrumRange)):
                raise ValueError('intensity and SpectrumRange are not the same length!')
            
        if SpectrumRange is not None:
            self.dispersion = SpectrumRange[1] - SpectrumRange[0]
        else:
            self.dispersion = dispersion

        if ZLP:
            self.ZLP = self.FindZLP(self.intensity)
            if SpectrumRange is not None:
                self.SpectrumRange = SpectrumRange
            else:
                self.SpectrumRange = np.arange(0 - self.ZLP, self.length - self.ZLP) * self.dispersion
        else:
            if SpectrumRange is not None:
                self.SpectrumRange = SpectrumRange
            elif channel_eV is not None:
                if len(channel_eV) == 2:
                    eV0 = channel_eV[1] - channel_eV[0] * dispersion
                    self.SpectrumRange = np.linspace(
                        eV0, 
                        eV0 + self.length * dispersion,
                        self.length
                        )
                else:
                    raise ValueError('You need to define the channel and the energy!')
            else:
                raise ValueError('You need to input the energy range!')
            self.ZLP = int(round(0 - np.min(SpectrumRange)/self.dispersion))
        self.unit_label = 'Energy'
        self.secondary_units = 'nm'
        self.secondary_unit_label = 'Wavelength'
        
    @classmethod
    def LoadFromCSV(cls, filename):
        spectrum = ImportCSV(filename)
        return cls(intensity=spectrum[:, 1], SpectrumRange=spectrum[:,0], dispersion=spectrum[1,0]-spectrum[0,0], units='eV')

    def FindZLP(self, data, method='max'):
        ZLP=specfun.find_zero_loss_peak(data, method)
        return ZLP
    
    def Normalize(self, ind=None):
        '''Normalize data to integral'''
        data_norm = specfun.normalize(self.intensity, ind)
        return EELSSpectrum(data_norm, SpectrumRange=self.SpectrumRange, dispersion=self.dispersion, ZLP=self.ZLP, units=self.units)

    def SymmetrizeAroundZLP(self):
        if self.ZLP < (self.length-1)/2.:
            data_sym = np.delete(self.intensity, np.s_[(2*self.ZLP+1):self.length], axis = -1)
            range_sym = np.delete(self.SpectrumRange, np.s_[(2*self.ZLP+1):self.length], axis = -1)
        elif self.ZLP > (self.length-1)/2.:
            data_sym = np.delete(self.intensity, np.s_[:np.maximum(2*self.ZLP+1-self.length, 0)], axis = -1)
            range_sym = np.delete(self.SpectrumRange, np.s_[:np.maximum(2*self.ZLP+1-self.length, 0)], axis = -1)
        else:
            data_sym = self.intensity
            range_sym = self.SpectrumRange
        data_sym[data_sym<0] = 0
        return EELSSpectrum(data_sym, SpectrumRange=range_sym, dispersion=self.dispersion, ZLP=self.ZLP, units=self.units)

    def PadSpectrum(self, pad_length, pad_value=0, pad_side='left'):
        if pad_side == 'left':
            padded = np.append(np.ones((pad_length, )) * pad_value, self.intensity)
            padded_range = np.append(
                np.linspace(
                    self.SpectrumRange[0] - pad_length * self.dispersion, 
                    self.SpectrumRange[0] - self.dispersion, 
                    pad_length), 
                self.SpectrumRange)
        elif pad_side == 'right':
            padded = np.append(self.intensity, np.ones((pad_length, 1)) * pad_value)
            padded_range = np.append(
                self.SpectrumRange, 
                np.linspace(
                    self.SpectrumRange[-1] + self.dispersion, 
                    self.SpectrumRange[-1] + pad_length * self.dispersion, 
                    pad_length)
                )
        else:
            padded = np.append(
                    np.append(
                        np.ones((pad_length, 1)) * pad_value, 
                        self.intensity), 
                    np.ones((pad_length, 1)) * pad_value)
            padded_range = np.append(
                np.append(
                    np.linspace(
                        self.SpectrumRange[0] - pad_length * self.dispersion, 
                        self.SpectrumRange[0] - self.dispersion, 
                        pad_length), 
                    self.SpectrumRange),
                np.linspace(
                    self.SpectrumRange[-1] + self.dispersion, 
                    self.SpectrumRange[-1] + pad_length * self.dispersion, 
                    pad_length)
                )

        return EELSSpectrum(padded, SpectrumRange=padded_range, dispersion=self.dispersion, ZLP=self.ZLP, units=self.units)

    def FindFW(self, intensityfraction):
        FW = specfun.find_fw(self.intensity, self.dispersion, self.ZLP, intensityfraction)
        return FW
    
    def RL_PSFsym(self, PSF, PSF_pad=0):
        PSF_sym = PSF.SymmetrizeAroundZLP()
        if PSF_pad is not None:
            data_length = np.size(self.SpectrumRange)
            PSF_length = np.size(PSF_sym.intensity)
            pad_length = int(data_length/2 - (1 + data_length) % 2 - (PSF_length-(PSF_length % 2))/2)
            if PSF_sym.ZLP < data_length/2:
                PSF_sym = PSF.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='left').SymmetrizeAroundZLP()
            elif PSF_sym.ZLP > data_length/2:
                PSF_sym = PSF_sym.PadSpectrum(pad_length, pad_value=PSF_pad, pad_side='right')
        return PSF_sym

    def RLDeconvolution(self, RLiterations, PSF):
        '''
        Input: RLiterations=number of iterations to perform
            PSF=point spread function (an EELS spectrum object)
        '''
        print('Beginning deconvolution...')
        x_deconv = RL(RLiterations, PSF.intensity, self.intensity)
        print('Done %s iterations!' %RLiterations)
        return EELSSpectrum(x_deconv, SpectrumRange=self.SpectrumRange, dispersion=self.dispersion, units=self.units)
    
    def eVSlice(self, starteV, stopeV):
        sliced = specfun.slice_range(
            self.intensity, 
            [starteV, stopeV],
            self.SpectrumRange)
        return sliced

    def trim_edge_spikes(self, delta_x=10, spike_condition=10):
        '''
        Trim the edge spikes off. Modifies the spectrum in place.
        '''
        self.SpectrumRange, self.intensity = specfun.trim_edge_spikes(
            self.SpectrumRange, 
            self.intensity, 
            delta_x, 
            spike_condition)
        print('Edge spikes trimmed')
        return

    def estimate_baseline(self, indices):
        '''
        Estimate a baseline (offset of intensity values above the x-axis)
        based on user-input indices
        '''
        baseline_value = specfun.find_baseline(self.intensity, indices)
        return baseline_value
    
    def subtract_baseline(self, baseline):
        '''
        Subtract a baseline value from the spectrum
        Modifies intensity in place
        '''
        self.intensity = specfun.subtract_value(self.intensity, baseline)
        return


#Richardson-Lucy algorithm
def RL(iterations, PSF, Spec):
    RL4 = Spec.copy()
    for ii in range(iterations):
        RL1 = np.convolve(PSF, RL4, 'same')
        if np.any(RL1==0):
            raise Exception('You have a zero value in the RL denominator!')
        RL2 = Spec/RL1
        RL3 = np.convolve(PSF, RL2, 'same')
        RL4 *= RL3
    return RL4

