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

    def __init__(self, message=None):

        message = "There has been an error" if not message else message

        super(LvmcamError, self).__init__(message)


class LvmcamNotImplemented(LvmcamError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = "This feature is not implemented yet." if not message else message

        super(LvmcamNotImplemented, self).__init__(message)


class LvmcamAPIError(LvmcamError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = "Error with Http Response from Lvmcam API"
        else:
            message = "Http response error from Lvmcam API. {0}".format(message)

        super(LvmcamAPIError, self).__init__(message)


class LvmcamApiAuthError(LvmcamAPIError):
    """A custom exception for API authentication errors"""

    pass


class LvmcamMissingDependency(LvmcamError):
    """A custom exception for missing dependencies."""

    pass


class LvmcamWarning(Warning):
    """Base warning for Lvmcam."""


class LvmcamUserWarning(UserWarning, LvmcamWarning):
    """The primary warning class."""

    pass


class LvmcamSkippedTestWarning(LvmcamUserWarning):
    """A warning for when a test is skipped."""

    pass


class LvmcamDeprecationWarning(LvmcamUserWarning):
    """A warning for deprecated features."""

    pass
