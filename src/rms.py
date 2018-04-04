import numpy as np

def rms(data, reference):
    rms = np.sqrt(np.sum(np.ndarray.flatten(np.square(data - reference)))/np.size(data))
    return rms
    
def rms_array(data, reference):
    rms_array = rms(data, reference)
    rms_array = np.average(np.ndarray.flatten(rms_array))
    return rms_array
