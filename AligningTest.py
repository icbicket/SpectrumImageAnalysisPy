import AlignPair
import Image
import ImageAligner
from skimage import data

p1 = Image.Image(data.camera())
p2 = Image.Image(data.coins())
p3 = Image.Image(data.chelsea()[:, :, 0])
p4 = Image.Image(data.astronaut()[:, :, 0])
Ap = ImageAligner.ImageAligner((p1, p2, p3, p4))
plotter = AlignPair.AlignPlot(Ap)
