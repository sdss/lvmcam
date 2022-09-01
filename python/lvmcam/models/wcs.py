# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-18
# @Filename: models/wcs.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import abc
from math import nan, radians, cos ,sin

from datetime import datetime

from typing import Any, Dict, List, Optional, Tuple, Union

from basecam.exposure import Exposure
from basecam.models import (
    Card,
    CardGroup,
    Extension,
    FITSModel,
    HeaderModel,
    MacroCard,
    WCSCards,
)
from clu.legacy.types.pvt import PVT
from sdsstools.time import get_sjd
from sdsstools import get_logger


# https://learn.astropy.org/tutorials/synthetic-images.html

#exposure.wcs = wcs.WCS()
#exposure.wcs.wcs.cdelt = np.array([1.,1.])
#exposure.wcs.wcs.crval = [exposure.scraper_store.get("ra_h", 0.0)*15, exposure.scraper_store.get("dec_d", 90.0)]
#exposure.wcs.wcs.cunit = ["deg", "deg"]
#exposure.wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]

## The distance from the long edge of the FLIR camera to the center
## of the focus (fiber) is 7.144+4.0 mm according to SDSS-V_0110 figure 6
## and 11.14471 according to figure 3-1 of LVMi-0081
## For the *w or *e cameras the pixel row 1 (in FITS) is that far
## away in the y-coordinate and in the middle of the x-coordinate.
## For the *c cameras at the fiber bundle we assume them to be in the beam center.
#crpix1 = self.width/self.binning[0] / 2
#crpix2 = 11.14471 * 1000.0 / self.pixsize
#exposure.wcs.wcs.crpix = [crpix1, crpix2]




class WcsCards(MacroCard):
    def macro(self, exposure, context={}):
        logger = get_logger("ScraperParamCards")

        ra_d = exposure.scraper_store.get('ra_h', 0.0)*15
        dec_d = exposure.scraper_store.get('dec_d', 90.0)
        kmirr = exposure.scraper_store.get('km_d', 0.0)

        # The distance from the long edge of the FLIR camera to the center
        # of the focus (fiber) is 7.144+4.0 mm according to SDSS-V_0110 figure 6
        # and 11.14471 according to figure 3-1 of LVMi-0081
        # For the *w or *e cameras the pixel row 1 (in FITS) is that far
        # away in the y-coordinate and in the middle of the x-coordinate.
        # For the *c cameras at the fiber bundle we assume them to be in the beam center.
        crpix1 = exposure.camera.image_area.wd / 2 / exposure.camera.binning[0]
        crpix2 = 11.14471 * 1000.0 / exposure.camera.pixsize / exposure.camera.binning[1]
#        logger.warning(f"{crpix1} {crpix2}")

        # field angle: degrees, then radians
        # direction of NCP on the detectors (where we have already flipped pixels
        # on all detectors so fieldrot=kmirr=0 implies North is up and East is left)
        # With right-handed-rule: zero if N=up (y-axis), 90 deg if N=right (x-axis)
        # so the direction is the vector ( sin(f), cos(f)) before the K-mirror.
        # Action of K-mirror is ( cos(2*m), sin(2*m); sin(2*m), -cos(2*m))
        # and action of prism is (-1 0 ; 0 1), i.e. to flip the horizontal coordinate.
        # todo: get starting  value from a siderostat field rotation tracking model
        fieldrot = 0.0

        
        if exposure.camera.name[-1] == 'c' :
            # without prism, assuming center camera placed horizontally
            if exposure.camera.name[:4] == 'spec' :
                # without K-mirror
                pass
            else :
                # with K-mirror
                # in the configuration the y-axis of the image has been flipped,
                # the combined action of (1, 0; 0, -1) and the K-mirror is (cos(2m), sin(2m); -sin(2m), cos(2m))
                # and applied to the input vector this is (sin(2m+f), cos(2m+f))
                fieldrot += 2.*kmirr
        else :
            # with prism
            if exposure.camera.name[:4] == 'spec' :
                # without K-mirror
                # Applied to input beam this gives (-sin(f), cos(f)) but prism effect
                # had been undone by vertical flip in the FLIR image. 
                pass
            else :
                # with K-mirror
                # Combined action of K-mirror and prism is (-cos(2*m), -sin(2*m);sin(2*m), -cos(2*m)).
                # Applied to input beam this gives (-sin(2*m+f), -cos(2*m+f)) = (sin(2*m+f+pi), cos(2*m+f+pi)).
                fieldrot += 2.*kmirr+180.0

            if exposure.camera.name[-1] == 'w' :
                # Camera is vertically,
                # so up in the lab is right in the image
                fieldrot += 90
            else :
                # Camera is vertically,
                # so up in the lab is left in the image
                fieldrot -= 90

        fieldrot = radians(fieldrot)
 
        # pixel scale per arcseconds is focal length *pi/180 /3600
        # = flen * mm *pi/180 /3600
        # = flen * um *pi/180 /3.6, so in microns per arcsec...
        pixscal = radians(exposure.camera.flen) / 3.6

        # degrees per pixel is arcseconds per pixel/3600 = (mu/pix)/(mu/arcsec)/3600
        degperpix =  exposure.camera.pixsize * exposure.camera.binning[0] / exposure.camera.pixscale / 3600.0

        # for the right handed coordinates
        # (pixx,pixy) = (cos f', -sin f'; sin f', cos f')*(DEC,RA) where f' =90deg -fieldrot
        # (pixx,pixy) = (sin f, -cos f; cos f , sin f)*(DEC,RA)
        # (sin f, cos f; -cos f, sin f)*(pixx,pixy) = (DEC,RA)
        # (-cos f, sin f; sin f, cos f)*(pixx,pixy) = (RA,DEC)
        # Note that the det of the WCS matrix is negativ (because RA/DEC is left-handed...)
        cosperpix = degperpix * cos(fieldrot) 
        sinperpix = degperpix * sin(fieldrot) 

        return [
            ("CUNIT1", "deg", "WCS units along axis 1"),
            ("CUNIT2", "deg", "WCS units along axis 2"),
            ("CTYPE1", "RA---TAN", "WCS type axis 1"),
            ("CTYPE2", "DEC--TAN", "WCS type axis 2"),
            ("CRVAL1", ra_d, "[deg] RA at reference pixel"),
            ("CRVAL2", dec_d, "[deg] DEC at reference pixel"),
            ("CRPIX1", crpix1, "[px] RA center along axis 1"),
            ("CRPIX2", -crpix2, "[px] DEC center along axis 2"),
            ("CD1_1", -cosperpix, "[deg/px] WCS matrix diagonal"),
            ("CD2_2", cosperpix, "[deg/px] WCS matrix diagonal"),
            ("CD1_2", sinperpix, "[deg/px] WCS matrix outer diagonal"),
            ("CD2_1", sinperpix, "[deg/px] WCS matrix outer diagonal"),
        ]

