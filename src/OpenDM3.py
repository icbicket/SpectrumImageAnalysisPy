from __future__ import print_function
import struct

filename = '/home/isobel/Documents/McMaster/EELS/2016-07-21/SI3/EELS Spectrum Image (dark ref corrected).dm3'
filename2 = '/home/isobel/Documents/McMaster/EELS/2016-07-21/SI3/Analog 0.dm3'


f = open(filename)
f2 = open(filename2)
print(struct.unpack('>1s', f.read(1)))
