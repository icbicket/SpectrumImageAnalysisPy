import CLAngleResolvedPolarPlotter as CLARPP
import matplotlib.pyplot as plt

SiN_samples = ['SiN_TR', 'SiN_TL', 'SiN_C', 'SiN_BR', 'SiN_BL', 'SiNSi',
    'AuSiNSi', 'AuSiN']

filename = '/home/isobel/Documents/McMaster/CL/T8-1_Sq3E_(8,2)/2016-06-03/Processed_Angular/T8-1_Sq3(8,2)_Angular_30keV_Ap3Spot4_10s_AuNrbubble_poldata.csv'
filenameout = '/home/isobel/Documents/McMaster/CL/T8-1_Sq3E_(8,2)/2016-06-03/Processed_Angular/T8-1_Sq3_Angular_30keV_Ap3Spot4_10s_test'

plot = CLARPP.PolarPlotter(filename, filenameout)
plot.SavePlot()
plt.show()
