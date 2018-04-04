import Spectrum
import SpectrumPlotter
import unittest
import numpy as np
import traceback

class SpectrumPlotterTest(unittest.TestCase):
    
    def testLinkedAxisSameDomain(self):
        pass
#        x0 = np.arange(0, 20)
#        y = np.arange(15, 35)
#        spec0 = Spectrum.EELSSpectrum(y, SpectrumRange = x0)
#        x1 = np.arange(0, 20)
#        spec1 = Spectrum.EELSSpectrum(y, SpectrumRange = x1)
#        spec_plot = SpectrumPlotter.SpectrumManager(spec0)
#        spec_plot.update_spectrum(spec1, ID=1)
#        np.testing.assert_almost_equal(
#            spec_plot.SpectrumPlot.main_axis.get_xlim(),
#            spec_plot.SpectrumPlot.linked_axis.get_xlim()
#            )

    def testLinkedAxisDiffDomain(self):
        pass
#        x0 = np.arange(0, 20)
#        y = np.arange(15, 35)
#        spec0 = Spectrum.EELSSpectrum(y, SpectrumRange = x0)
#        x1 = np.arange(10, 30)
#        spec1 = Spectrum.EELSSpectrum(y, SpectrumRange = x1)
#        spec_plot = SpectrumPlotter.SpectrumManager(spec0)
#        print(spec_plot.SpectrumPlot.main_axis.get_xlim(),
#            spec_plot.SpectrumPlot.linked_axis.get_xlim())
#        spec_plot.update_spectrum(spec1, ID=1)
#        print(spec_plot.SpectrumPlot.main_axis.get_xlim(),
#            spec_plot.SpectrumPlot.linked_axis.get_xlim())
#        np.testing.assert_almost_equal(
#            spec_plot.SpectrumPlot.main_axis.get_xlim(),
#            spec_plot.SpectrumPlot.linked_axis.get_xlim()
#            )


if __name__ == '__main__':
    unittest.main()    
