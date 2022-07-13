from __future__ import division
import numpy as np
from astropy.modeling import models, fitting, powerlaws

'''
This file contains functions for 1D datasets, primarily intended for use with
spectra (with 2 1D vectors, values along x and y).
'''

def check_spectrum(x, y):
    '''
    Handles raising exceptions if x and y are not 1D arrays of the same length
    '''
    if len(np.shape(x)) != 1:
        raise ValueError('x is not a 1 dimensional array')
    if len(np.shape(y)) != 1:
        raise ValueError('y is not a 1 dimensional array')
    if len(x) != len(y):
        raise ValueError('x and y are not the same length')
    return

def check_spectrum_one_axis(x):
    if len(np.shape(x)) != 1:
        raise ValueError('This is not a 1 dimensional array')
    return

def slice_range(x, start_stop, y=None):
    '''
    Slices x (1D array) from the start value to the stop value, where start
    and stop are given in terms of the values along y (a 1D array).
    If no y is given, start_stop gives the nearest indices of
    x along which to slice. If y is given, returns a calibrated slice of x
    according to the values of y.
    x and y should be 1D arrays of the same length.
    start_stop should be a 2 element list, array, or tuple, containing the 
    values at which to start and stop the slice (these should exist inside y)
    y should be monotonic for the result to make sense.
    '''
    if y is None:
        y = np.arange(len(x))
    check_spectrum(x, y)
    
    if len(start_stop) != 2:
        raise ValueError('start_stop is not a 2 element list')
    
    start_i = (np.abs(y - start_stop[0])).argmin()
    stop_i = 1 + (np.abs(y - start_stop[1])).argmin()
    return x[start_i:stop_i]

def normalize(x, y, value=None, index=None):
    '''
    Normalize data to value given in the input value or to the value of y at the given index or the integral of y over the given indices. If value is None and index is None, normalize the data to the integral of the whole spectrum
    '''
#    if isinstance(ind, int):
#        normfactor = x[ind]
#    elif ind is None:
#        normfactor = np.sum(x, keepdims=True)
#    elif np.size(ind) == 2:
#        normfactor = np.sum(x[ind[0]:ind[1]], keepdims=True)
#    else:
#        raise ValueError('ind is not right: it should be a single integer or '
#        'a list of two integers, or None')
    check_spectrum(x,y)
    if value is not None and index is not None:
        raise ValueError('value and index are mutually exclusive inputs')
    elif value is None and index is not None:
        if isinstance(index, int):
            value = y[index]
        elif np.size(index) == 2:
            value = integrate_spectrum(x, y, index)
        else:
            raise ValueError('index must be an integer, a pair of integers, or None')
    elif value is not None and index is None:
        if isinstance(value, int) or isinstance(value, float):
            pass
        else:
            raise ValueError('value must be a single number')
    else:
        value = integrate_spectrum(x, y)
    y_norm = y/value
    return y_norm

def find_fw(y, dx, x_0, fraction):
    '''
    Find the full width at the given fraction of the height of a peak
    y: the intensity
    dx: the difference between neighbouring x values (dispersion), constant over the whole spectrum (for now)
    x_0: the index of the centre of the peak
    fraction: the fraction of the peak height at which to calculate the full width
    '''
    lefttail = y[:x_0+1][::-1]
    diff1 = lefttail - fraction * y[x_0]
    left_index_1 = np.argmax(np.diff(np.sign(diff1)) != 0)
    left_index_2 = left_index_1 + 1
    left_energy = dx * np.interp(
        fraction * y[x_0], 
        [lefttail[left_index_2], lefttail[left_index_1]], 
        [left_index_2, left_index_1])
    righttail = y[x_0:]
    diff2 = righttail - fraction * y[x_0]
    right_index_1 = np.argmax(np.diff(np.sign(diff2)) != 0) 
    right_index_2 = right_index_1 + 1
    right_energy = dx * np.interp(
        fraction * y[x_0], 
        [righttail[right_index_2], righttail[right_index_1]], 
        [right_index_2, right_index_1])
    FW = left_energy + right_energy
    return FW

def trim_edge_spikes(x, y, delta_x=10, spike_condition=10):
    '''
    Trim any large spikes that appear on the edges of a spectrum, 
    typically due to distortions on the camera/pile-up of counts at the edges
    Input
    x: the x-values of the spectrum (range), 1D array
    y: the y-values of the spectrum (intensity), 1D array
    delta_x: how many channels to look for a spike in on either side of the edge
    spike_condition: the value of the magnitude of the slope of the spike in order to be considered a spike to trim
    Output
    The x and y values of the spectrum, trimmed to remove any spikes in the data
    '''
    check_spectrum(x,y)
    spectrum_diff = np.diff(y)
    condition = np.abs(spectrum_diff) > spike_condition
    trimmed_x = np.copy(x)
    trimmed_y = np.copy(y)
    if np.any(condition[:delta_x]):
        trim_index_min = np.argwhere(condition[:delta_x])
        trimmed_x = trimmed_x[np.max(trim_index_min+1):]
        trimmed_y = trimmed_y[np.max(trim_index_min+1):]
    if np.any(condition[-delta_x:]):
        trim_index_max = np.argwhere(condition[-delta_x:])
        trimmed_x = trimmed_x[:-(delta_x-np.min(trim_index_max))]
        trimmed_y = trimmed_y[:-(delta_x-np.min(trim_index_max))]
    return trimmed_x, trimmed_y

def find_zero_loss_peak(x, y, method='max'):
    '''
    Identify the zero loss peak
    max method: use the global maximum in the spectrum
    '''
    check_spectrum(x,y)
    max_location = np.argmax(y)
    if method=='max':
        ZLP_location = max_location
        if np.count_nonzero(y==y[ZLP_location]) != 1:
            raise Warning('Two possible ZLPs found')
            print('Returning the first ZLP, found at {x[ZLP_location]} eV')
        else:
            print(f'ZLP found at {x[ZLP_location]} eV')
        return ZLP_location, x[ZLP_location]
#        ZLP = int(stats.mode(np.argmax(data, axis = -1), axis=None)[0])
    elif method=='gaussian_fit':
    # TODO: find the FWHM and input it into stddev
    # TODO: calculate fit statistics and use them to judge if the fit was successful
        model_zlp = models.Gaussian1D(amplitude = y[max_location], mean=max_location, stddev=0.01)
        fit_zlp = fitting.LevMarLSQFitter()
        zlp_fit_range = range(max_location - 2, max_location + 2)
        zlp_fitted = fit_zlp(model_zlp, x[zlp_fit_range], y[zlp_fit_range])
        print(f'ZLP found at {fit_zlp.mean}')
        return fit_zlp
    else:
        raise NotImplementedError


#def fit_zlp_maximum(self, data, data_range):
#        #model_zlp = models.Lorentz1D(amplitude = np.max(data), x_0=0, fwhm=0.01)
#        model_zlp = models.Gaussian1D(amplitude = np.max(data), mean=0, stddev=0.01)
#        fit_zlp = fitting.LevMarLSQFitter()
#        zlp_location = self.find_ZLP(data)
#        zlp_fit_range = range(zlp_location - 2, zlp_location + 2)
#        zlp_fitted = fit_zlp(model_zlp, data_range[zlp_fit_range], data[zlp_fit_range])
#        print(fit_zlp.fit_info)
#        print(dir(fit_zlp))
#        #plt.figure()
#        #plt.plot(data_range, data, marker='x')
#        #plt.plot(np.linspace(-0.01, 0.01, 100), zlp_fitted(np.linspace(-0.01, 0.01, 100)), ls='--')
#        return zlp_fitted

def find_baseline(y, indices):
        '''
        Find a value for the baseline 
        (to compensate for poor dark/gain reference on the camera)
        Input
        - y: the y-data/intensity data for the spectrum
        - indices: the indices over which to derive the baseline
        '''
        check_spectrum_one_axis(y)
        baseline = np.average(y[indices])
        return baseline
        
def subtract_value(y, value):
    '''
    Subtract a value from the spectral intensity (DC offset)
    '''
    if np.isnan(value):
        raise ValueError('Input value should not be NaN')
    new_y = y - value
    return new_y

def integrate_spectrum(x, y, indices=None):
    '''
    Integrate a spectrum or slice from a spectrum
    indices: a (start, stop) value pair of indices over which to integrate 
    (eg, integrating only a slice). If None, integrate the whole spectrum.
    '''
    check_spectrum(x, y)
    if indices is not None:
        integral = np.trapz(y[indices[0]:indices[1]], x[indices[0]:indices[1]])
    else:
        integral = np.trapz(y, x)
    return integral
