import CLAngleResolvedPolarPlotter as CLARPP
import matplotlib.pyplot as plt

SiN_samples = ['SiN_TR', 'SiN_TL', 'SiN_C', 'SiN_BR', 'SiN_BL', 'SiNSi',
    'AuSiNSi', 'AuSiN']

for ss in SiN_samples:
	filename = '/home/isobel/Documents/McMaster/CL/2016-06-03/T8-1_Sq3_Angular_30keV_Ap3Spot4_10s_' + ss + '_poldata.csv'
	filenameout = '/home/isobel/Documents/McMaster/CL/2016-06-03/T8-1_Sq3_Angular_30keV_Ap3Spot4_10s_' + ss

	plot = CLARPP.PolarPlotter(filename, filenameout)
	plot.SavePlot()
plt.show()
