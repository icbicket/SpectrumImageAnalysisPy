import numpy as np
import matplotlib.pyplot as plt

def snr(array, ref_array):
    snr = np.sum(np.ndarray.flatten(ref_array))/np.sum(np.ndarray.flatten(np.abs(array - ref_array)))
    return snr
