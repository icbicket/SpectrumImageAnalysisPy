from ImageAligner import ImageAligner
from AlignPlot import AlignPlot

def Align(Images):
    model = ImageAligner(Images)
    plotter = AlignPlot(model)
    return model, plotter
