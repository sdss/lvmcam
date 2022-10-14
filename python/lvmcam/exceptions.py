# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import absolute_import, division, print_function


class LvmcamError(Exception):
    """A custom core Lvmcam exception"""
    pass

class LvmcamNotConnected(LvmcamError):
    """Camera(s) not connected."""
    pass
