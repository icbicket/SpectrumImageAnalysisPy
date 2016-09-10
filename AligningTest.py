import AlignPair
import numpy as np
from skimage import data

p1 = data.camera()
p2 = data.coins()
Ap = AlignPair.AlignPair(p1, p2)
plotter = AlignPair.AlignPlot(Ap)
