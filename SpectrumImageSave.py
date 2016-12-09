import h5py
import numpy as np

def SaveCL_SI(SI, filename, survey=None, SEM=None):
	print 'Saving to...', filename
	with h5py.File(filename, 'w') as hf:
		if survey:
			g0_1 = hf.create_group('Acquisition0/ImageData') # survey image
			g0_1.create_dataset('Image', 
							data=survey.data.reshape(np.append([1,1,1], survey.size)),
							compression='gzip', compression_opts=9)
			g0_1.create_dataset('DimensionScaleX', data=survey.calibration)
			g0_1.create_dataset('DimensionScaleY', data=survey.calibration)
		if SEM:
			g1_1 = hf.create_group('Acquisition1/ImageData') # SEM image
			g1_1.create_dataset('Image', 
							data=SEM.data.reshape(np.append([1,1,1], SEM.size)),
							compression='gzip', compression_opts=9)
			g1_1.create_dataset('DimensionScaleX', data=SEM.calibration)
			g1_1.create_dataset('DimensionScaleY', data=SEM.calibration)

		g2_1 = hf.create_group('Acquisition2/ImageData') # SI
		g2_1.create_dataset('Image', 
				            data=SI.data.reshape(np.append([1,1], SI.size)).transpose(4,0,1,2,3),
				            compression='gzip', compression_opts=9)
		g2_1.create_dataset('DimensionScaleC', data=SI.SpectrumRange*1e-9)
		g2_1.create_dataset('DimensionScaleX', data=SI.calibration)
		g2_1.create_dataset('DimensionScaleY', data=SI.calibration)
