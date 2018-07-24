from __future__ import division
import numpy as np
import imageio as imio

def check_image(im):
    if im.ndim != 2:
        raise ValueError(
            'Your image is not 2D! Please check the number of dimensions '
            'in the input!')
    else: 
        return

def quadrant_sum(im):
    '''
    Sum each quadrant of the input image and output a four-element array
    '''
    check_image(im)
    x_half = np.int(np.ceil(np.shape(im)[0]/2))
    y_half = np.int(np.ceil(np.shape(im)[1]/2))
    Q1 = np.sum(im[:x_half, :y_half])
    Q2 = np.sum(im[:x_half, y_half:])
    Q3 = np.sum(im[x_half:, :y_half])
    Q4 = np.sum(im[x_half:, y_half:])
    return np.array([[Q1, Q2], [Q3, Q4]])

def write_image(im, filename, **kwarg):
    '''
    Write image to png
    im should be image data, can be grayscale (size NxM), RGB, (size NxMx3), 
    or RGBA (size NxMx4)
    '''

    imio.imwrite(
        filename, 
        im, 
        format='png',
        **kwarg
        )
    return

def contrast_stretch(im, s=[0, 255], r=[None, None], bits=8):
    '''
    Stretches (or compresses) contrast of an image such that the image 
    histogram (between the values given in r) goes between the values given
    in s
    For example, given an image going from 0 to 255, using s=[100,150] and 
    r=[50, 200] will make any value in the original image which is greater
    than 200 or less than 50 into 150 and 100 respectively, and linearly
    modify values between 50 and 200 to be between 100 and 150 in the output.
    Using equal values for both elements of r is equivalent to using a 
    threshold.
    '''
    if r[0] is None:
        r[0] = np.min(im)
    if r[1] is None:
        r[1] = np.max(im)
    
    stretched = np.empty(np.shape(im))
    if r[0] == 0:
        stretched[im < r[0]] = 0
    else:
        stretched[im < r[0]] = im[im < r[0]] * s[0] / r[0]
    
    if r[0] == r[1]:
        stretched[im == r[1]] = (
            (2**bits - 1 - s[1]) / (2**bits - 1 - r[1]) * im[im == r[1]] + 
            (2**bits - 1) * (s[1] - r[1]) / (2**bits - 1 - r[1]))
    else:
        stretched[(im >= r[0]) & (im <= r[1])] = (
            (s[1] - s[0]) / (r[1] - r[0]) * im [(im >= r[0]) & (im <= r[1])] + 
            (s[0] * r[1] - s[1] * r[0]) / (r[1] - r[0]))
    
    if r[1] == (2**bits - 1):
        stretched[im > r[1]] = 2**bits - 1
    else:
        stretched[im > r[1]] = (
            (2**bits - 1 - s[1]) / (2**bits - 1 - r[1]) * im[im > r[1]] + 
            (2**bits - 1) * (s[1] - r[1]) / (2**bits - 1 - r[1]))
    return stretched
