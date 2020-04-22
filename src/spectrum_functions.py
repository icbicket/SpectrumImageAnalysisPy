from __future__ import division
import numpy as np

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

def normalize(x, ind=None):
    '''Normalize data to value of x at the given index or the sum of x 
    between the given indices or if ind is None, over the whole spectrum'''
    if isinstance(ind, int):
        normfactor = x[ind]
    elif ind is None:
        normfactor = np.sum(x, keepdims=True)
    elif np.size(ind) == 2:
        normfactor = np.sum(x[ind[0]:ind[1]], keepdims=True)
    else:
        raise ValueError('ind is not right: it should be a single integer or '
        'a list of two integers, or None')
    
    x_norm = x/normfactor
    return x_norm

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
