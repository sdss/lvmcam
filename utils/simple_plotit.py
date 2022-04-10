# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)



import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.patches import Ellipse, Rectangle
from matplotlib import use as plt_use

from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage.filters import gaussian_filter, gaussian_gradient_magnitude
import scipy.ndimage
import sep


from sdsstools.logger import get_logger

class PlotIt:
    def __init__(self, title=["west, east"], logger=get_logger("plotit")):
        self.log = logger
        
#        plt_use('TkAgg')
        plt_use('Qt5Agg')
        self.fig = plt.figure(figsize=(8, 10))
        self.ax = [None, None]
        self.ax_img = [None, None]

        for i in [0,1]:
            self.ax[i] = plt.subplot2grid((2, 1), (i, 0))
            self.ax[i].set_title(title[i], fontweight ="bold")
            self.ax[i].tick_params(labelbottom=False, labelleft=False)
        
        self.fig.tight_layout()
        plt.pause(.5)

    def update(self, num, data):

        mean, sigma = np.mean(data), np.std(data)
        lperc, uperc = np.percentile(data, 0.5), np.percentile(data, 99.8)
        
        if self.ax_img[num]:
            self.ax_img[num].set_data(data)
        else:
            ax_divider = make_axes_locatable(self.ax[num])
            cax = ax_divider.append_axes('right', size='3%', pad=0.05)
            self.ax_img[num] = self.ax[num].imshow(data, vmin=mean-sigma, vmax=mean+sigma, interpolation='nearest', origin='lower')
            self.fig.colorbar(self.ax_img[num], cax=cax, orientation='vertical')

        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(0.001)

    def start_event_loop(self, time):
        self.fig.canvas.start_event_loop(time)
