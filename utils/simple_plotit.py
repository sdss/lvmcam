# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import math

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, PowerNorm
from matplotlib.patches import Ellipse, Rectangle, Arrow
from matplotlib import use as plt_use

from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage.filters import gaussian_filter, gaussian_gradient_magnitude
import scipy.ndimage
import sep

from sdsstools.logger import get_logger

from lvmtipo.site import Site
from lvmtipo.siderostat import Siderostat
from lvmtipo.fiber import Fiber
from lvmtipo.target import Target

from astropy.coordinates import SkyCoord
import astropy.units as u


class PlotIt:
    def __init__(self, title=["west, east"], site='LCO', logger=get_logger("plotit")):
        self.log = logger
        
#        plt_use('TkAgg')
        plt_use('Qt5Agg')
        self.fig = plt.figure(figsize=(8, 10))
        self.ax = [None, None]
        self.ax_img = [None, None]

        for i in [0, 1]:
            self.ax[i] = plt.subplot2grid((2, 1), (i, 0))
            self.ax[i].set_title(title[i], fontweight ="bold")
            self.ax[i].tick_params(labelbottom=False, labelleft=False)
        
        self.fig.tight_layout()
        plt.pause(.5)
        
        self.annoN = [None, None]
        self.annoE = [None, None]

        self.site = site
        self.sid = Siderostat()
        self.geoloc = Site(name = self.site)
        
        self.imgsize = [None, None]
        self.mean, self.sigma , self.lperc, self.uperc = [0,0], [0,0], [0,0], [0,0]

    def update(self, num, data, radec, kmangle):

        mean, sigma, min, max = np.mean(data), np.std(data), np.min(data), np.max(data)
        lperc, uperc = np.percentile(data, 5), np.percentile(data, 99.95)
        gamma=0.6
        vmin, vmax = mean-sigma, uperc
        
        self.log.debug(f"m/s {mean}/{sigma} {lperc}/{uperc} ")        
        self.imgshape = data.shape
        if self.ax_img[num]:
            # we have to set clim to vmax first, otherwise the real values later will be ignored.
            if self.mean[num] > mean + sigma or self.mean[num] < mean - sigma:
                self.ax_img[num].set_clim(vmin=min, vmax=max)
            self.ax_img[num].set_data(data)
            if self.mean[num] > mean + sigma or self.mean[num] < mean - sigma:
#                self.ax_img[num].set_norm(LogNorm(vmin=mean-sigma, vmax=mean+sigma))
#                self.ax_img[num].set_norm(LogNorm(vmin=mean-sigma,vmax=mean+sigma))
#                self.ax_img[num].set_norm(PowerNorm(gamma, vmin=mean-sigma, vmax=uperc))
                self.ax_img[num].set_clim(vmin=vmin, vmax=vmax)
                self.mean[num], self.sigma[num], self.lperc[num], self.uperc[num] = mean, sigma, lperc, uperc
        else:
            ax_divider = make_axes_locatable(self.ax[num])
            cax = ax_divider.append_axes('right', size='3%', pad=0.05)
            self.ax_img[num] = self.ax[num].imshow(data, vmin=vmin, vmax=vmax, interpolation='nearest', origin='lower')
#            self.ax_img[num] = self.ax[num].imshow(data, norm=LogNorm(vmin=vmin, vmax=vmax), interpolation='nearest', origin='lower')
#            self.ax_img[num] = self.ax[num].imshow(data, norm=LogNorm(vmin=vmin, vmax=vmax ), interpolation='nearest', origin='lower')
#            self.ax_img[num] = self.ax[num].imshow(data, norm=PowerNorm(gamma, vmin=vmin, vmax=vmax), interpolation='nearest', origin='lower')
            self.fig.colorbar(self.ax_img[num], cax=cax, orientation='vertical')
            self.mean[num], self.sigma[num], self.lperc[num], self.uperc[num] = mean, sigma, lperc, uperc

        if radec and kmangle:
            self.drawNE(num, radec, kmangle)
            return

        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(0.001)
        

    def drawNE(self, num, tcs_coord, km_angle):
        def rotate(deg, point):
            theta = np.radians(deg)
            c, s = np.cos(theta), np.sin(theta)
            t = np.array(((c, -s), (s, c)))
            return np.dot(point, t)

        mathar_angle = math.degrees(self.sid.fieldAngle(self.geoloc, Target(tcs_coord), None))
        sky_angle = km_angle - mathar_angle
        print(f"kmirror/mathar/sky angle (deg): {km_angle}/{mathar_angle}/{sky_angle}")

        if self.annoN[num]: self.annoN[num].remove()
        if self.annoE[num]: self.annoE[num].remove()
        
        l = self.imgshape[0]/10
        x,y, = l+20, self.imgshape[0]-l-20
        print(f"{self.imgshape} {x} {y} {l}")
        lx, ly = rotate(sky_angle, (0, l))
        self.annoN[num] = self.ax[num].annotate('N', xy=(x, y), xytext=(x+lx, y+ly), size="large", color="w", ha='center', va="center", weight="bold", arrowprops=dict(arrowstyle='<-', lw=2, color="w"))
        lx, ly = rotate(sky_angle, (l, 0))
        self.annoE[num] = self.ax[num].annotate('E', xy=(x, y), xytext=(x-lx, y-ly), size="large", color="w", ha='center', va="center", weight="bold", arrowprops=dict(arrowstyle='<-', lw=2, color="w"))
        
        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(0.01)
        


    def start_event_loop(self, time):
        self.fig.canvas.start_event_loop(time)
