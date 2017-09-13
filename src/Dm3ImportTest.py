import Dm3Import as DM3
import SpectrumImagePlotter as SIPl
import SpectrumImage
import re
import numpy as np

def make_dict_from_tags(iterables):
	d = {}
	for ii in iterables:
		tempD = d
		for tt in ii:
			tempD = tempD.setdefault(tt, {})
	return d

#filename = '/home/isobel/Documents/McMaster/EELS/Sam/EELS Spectrum Image (dark ref corrected)_aligned_calibrated.dm3'
filename = '/home/isobel/Documents/McMaster/EELS/2017-03-31 - inverse Sierpinskis/SI2/EELS Spectrum Image (dark ref corrected).dm3'

data = DM3.DM3(filename)

tagdata = []
for ii in data._storedTags:
	splitted = ii.split(' = ')
	keys = list(splitted[:-1][0].split('.'))
	value = splitted[-1]
	keys.append(value)
	tagdata.append(keys)

tags = make_dict_from_tags(tagdata)


eels = SpectrumImage.EELSSpectrumImage.LoadFromDM3(filename, spectrum_calibrated=True)
plot = SIPl.SpectrumImagePlotter(eels)
plot.ShowPlot()
