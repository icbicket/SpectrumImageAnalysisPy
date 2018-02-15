from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector
from matplotlib.ticker import FuncFormatter, MaxNLocator
import collections
from matplotlib.lines import Line2D
import Spectrum
from constants import *
from matplotlib import transforms as mtransforms
import matplotlib.ticker as mticker
import matplotlib.axes
from mpl_toolkits.axes_grid1 import host_subplot

class SpectrumPlotter(object):
    def __init__(self, spectrum, axis=None, ax_transform=None, colour='red'):
        '''Line plot with span selector
           Input: matplotlib axis object, Spectrum object to plot
        '''
        self.spectrum = spectrum
        self.ax_transform = self.choose_ax_transform(ax_transform)
            
        if hasattr(axis, 'twin'):
            self.main_axis = axis
            self.linked_axis = self.setup_linked_axis()
        elif hasattr(axis, 'plot'):
            self.main_axis = axis
        elif axis is None:
            self.main_axis = host_subplot(1,1,1)
            self.linked_axis = self.setup_linked_axis()
        else:
            raise TypeError("Your axis input was not an acceptable axis type! It must be a subplot or a host_subplot!")
        self.line_colour = colour

        self.label = ''
        self.main_axis.set_xlabel(r"%s (%s)" % (spectrum.unit_label, spectrum.units))
        self.main_axis.set_ylabel(r"Intensity (a.u.)")
        plt.gcf().canvas.draw()

    def choose_ax_transform(self, ax_transform):
        if ax_transform is None:
            return
        if ax_transform[0] == 'eV' and ax_transform[1] == 'nm':
            return eV2nmTransform()
        elif ax_transform[0] == 'nm' and ax_transform[1] == 'eV':
            return nm2eVTransform()
        else:
            raise ValueError('We do not have a transform for that yet, sorry!')

    def setup_linked_axis(self):
        transform = mtransforms.BlendedGenericTransform(
                eV2nmTransform(),
                mtransforms.IdentityTransform()
                )
        linked_axis = self.main_axis.twin(transform)
        linked_axis.set_viewlim_mode("transform")
        linked_axis.axis["right"].toggle(ticklabels=False) 
        linked_axis.xaxis.set_major_locator(nmTickLocator(self.main_axis, numticks=5))
        linked_axis.set_xlabel(r"%s (%s)" % (self.spectrum.secondary_unit_label, self.spectrum.secondary_units))
        return linked_axis

    def add_spectrum(self, spectrum, label=''):
        self.label = label
        plotted_spectrum = self.main_axis.plot(spectrum.SpectrumRange, 
                spectrum.intensity, label=self.label)
        return plotted_spectrum

    def update_spectrum(self, line, spectrum):
        line[0].remove()
        plotted_spectrum = self.main_axis.plot(spectrum.SpectrumRange, 
            spectrum.intensity, label=self.label)
        return plotted_spectrum

def eVtonm(eV, pos=None):
    nm = PLANCK*LIGHTSPEED/(COULOMB*np.abs(eV))*1e9
    if np.isfinite(nm): nm = int(nm)
    if np.abs(nm/1e4) > 1:
        value = "%.0f" % nm
    else:
        value = "%.1f" %nm
    return value

def eVtonm_array(eV, pos=None):
    nm = PLANCK*LIGHTSPEED/(COULOMB*eV)*1e9
    return nm

def nmtoeV(nm, pos=None):
    eV = PLANCK*LIGHTSPEED/(COULOMB*nm)*1e9
    if np.abs(eV/1e4) > 1:
        value = "%.3g" % eV
    elif np.abs(eV/1e3) > 1:
        value = "%.4g" % eV
    else:
        value = "%.3g" % eV
    return value
    
def nmtoeV_array(nm):
    eV = PLANCK*LIGHTSPEED/(COULOMB * np.abs(nm)) * 1e9
    return eV

class SpectrumManager(object):
    def __init__(self, spectrum, axis=None, ax_transform = ('eV', 'nm'), cmap=plt.get_cmap('cool'), currentID=0):
        self.currentID = currentID
        self.ax_transform = ax_transform
        self.cmap = cmap
        self.axis = axis
        self.spectrumDict = collections.OrderedDict()
        self.spectrumDict[self.currentID] = spectrum
        self.lineDict = collections.OrderedDict()
        self.SpectrumPlot = SpectrumPlotter(self.spectrumDict[self.currentID], 
            self.axis, ax_transform=self.ax_transform, colour=self.cmap)
        self.lineDict[self.currentID] = self.SpectrumPlot.add_spectrum(
            self.spectrumDict[self.currentID], label=str(self.currentID))
        self.colourDict = collections.OrderedDict()
        self.colourDict[self.currentID] = self.cmap(0)

    def make_colour_list(self):
        colour_callers = np.linspace(0, 1, len(self.lineDict.keys()))
        for cc, ll in zip(colour_callers, self.lineDict.keys()):
            self.colourDict[ll] = self.cmap(cc)

#    def RecolourSpectra(self):
#        colours = self.cmap(i) for i in np.linspace(0, 1, len(self.spectrumDict))
##        cmaps = []
##        for ii in self.spectrumDict.keys():
##            cmaps.append(self.cmap(i/len(self.spectrumDict)))
#        self.SpectrumPlot.colour_spectra(colours)
##        for (i, g) in self.polyDict.items():
##            g.colour_spectrum(self.cmap(i/len(self.polyDict)))
#        
        
#    def AddSpectrum(self, spectrum):
#        '''Adds spectrum to spectrum dictionary to be plotted'''
#        self.currentID = (self.currentID + step) % (max(self.spectrumDict.keys()) + 1)
#        print("I added a new spectrum for you!")
#        self.spectrumDict[self.currentID] = spectrum

    def update_spectrum(self, spectrum, ID):
        self.currentID = ID
        if self.SpectrumPlot.main_axis.get_xlabel() != r"%s (%s)" % (spectrum.unit_label, spectrum.units):
            print('oh no!', spectrum.units)
            if spectrum.units == 'nm':
                spectrum_rangemod = nmtoeV_array(spectrum.SpectrumRange)            
                spectrum_match = Spectrum.Spectrum(spectrum.intensity, units='eV', SpectrumRange=spectrum_rangemod)
            elif spectrum.units == 'eV':
                spectrum_rangemod = eVtonm_array(spectrum.SpectrumRange)
                spectrum_match = Spectrum.Spectrum(spectrum.intensity, units='nm', SpectrumRange=spectrum_rangemod)
        else:
            spectrum_match = spectrum
        self.spectrumDict[ID] = spectrum_match
            
        if self.currentID in self.lineDict.keys():
            self.lineDict[self.currentID] = self.SpectrumPlot.update_spectrum(
                self.lineDict[self.currentID], self.spectrumDict[self.currentID])
            self.lineDict[self.currentID][0].set_color(self.colourDict[self.currentID])
        else:
            self.lineDict[self.currentID] = add_function = self.SpectrumPlot.add_spectrum(
                self.spectrumDict[self.currentID], label=str(self.currentID))
            self.make_colour_list()
            for ll in self.lineDict.keys():
                self.lineDict[ll][0].set_color(self.colourDict[ll])

    def make_visible(self, ID):
        self.lineDict[ID][0].set_visible(True)
#        self.lineDict[ID][0].set_color('r')
        
    def make_invisible(self, ID):
        self.lineDict[ID][0].set_visible(False)
    
    def add_legend(self):
        legend = self.axis.legend(loc='best', framealpha=0.5)
        if legend:
            legend.draggable(state=True)
            
    def ShowPlot(self):
        plt.show()

class eV2nmTransform(mtransforms.Transform):
    input_dims = 1
    output_dims = 1
    is_separable = False
    has_inverse = True
    
    def __init__(self):
        mtransforms.Transform.__init__(self)
        
    def transform_non_affine(self, eV):
        return LIGHTSPEED * PLANCK / (COULOMB * eV * 1e-9)
        
    def inverted(self):
        return nm2eVTransform()

class nm2eVTransform(mtransforms.Transform):
    input_dims = 1
    output_dims = 1
    is_separable = False
    has_inverse = True
    
    def __init__(self):
        mtransforms.Transform.__init__(self)
        
    def transform_non_affine(self, nm):
        return LIGHTSPEED * PLANCK / (COULOMB * nm * 1e-9)
        
    def inverted(self):
        return eV2nmTransform()

class nmTickLocator(mticker.MaxNLocator):
    def __init__(self, other_axis, numticks=None):
        self.numticks = numticks
        self.other_axis = other_axis
        self.set_params(**self.default_params)

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def _raw_ticks(self, vmin, vmax):
        if self._nbins == 'auto':
            if self.axis is not None:
                nbins = np.clip(self.axis.get_tick_space(),
                                max(1, self._min_n_ticks - 1), 9)
            else:
                nbins = 9
        else:
            nbins = self._nbins
        scale, offset = mticker.scale_range(vmin, vmax, nbins)
        _vmin = vmin - offset
        _vmax = vmax - offset
        raw_step = 1/(1/vmax - 1/vmin) / nbins
        steps = self._extended_steps * scale
        if self._integer:
            # For steps > 1, keep only integer values.
            igood = (steps < 1) | (np.abs(steps - np.round(steps)) < 0.001)
            steps = steps[igood]
        self.numticks = len(self.other_axis.get_xticks())
        ticks = 1/np.linspace(1/vmin, 1/vmax, self.numticks)
        for step in steps:
            best_vmin = (_vmin//step) * step
            low = np.round(mticker.Base(step).le(_vmin - best_vmin) / step)
            high = np.round(mticker.Base(step).ge(_vmax - best_vmin) / step)
        return ticks
