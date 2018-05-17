from __future__ import division
import numpy as np

def check_image(im):
    if im.ndim != 2:
        raise ValueError(
            'Your image is not 2D! Please check the number of dimensions '
            'in the input!')
    else: 
        return

def quadrant_sum(im):
    check_image(im)
    x_half = np.int(np.ceil(np.shape(im)[0]/2))
    y_half = np.int(np.ceil(np.shape(im)[1]/2))
    Q1 = np.sum(im[:x_half, :y_half])
    Q2 = np.sum(im[:x_half, y_half:])
    Q3 = np.sum(im[x_half:, :y_half])
    Q4 = np.sum(im[x_half:, y_half:])
    return np.array([[Q1, Q2], [Q3, Q4]])
