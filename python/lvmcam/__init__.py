# encoding: utf-8

from astropy.utils.iers import conf

from sdsstools import get_logger, get_package_version


# pip package name
NAME = "sdss-lvmcam"


# Inits the logging system as NAME. Only shell logging, and exception and warning
# catching. File logging can be started by calling log.start_file_logger(path).
# Filename can be different than NAME.
log = get_logger(NAME)


# package name should be pip package name
__version__ = get_package_version(path=__file__, package_name=NAME)


# Prevent astropy from downloading data.
conf.auto_max_age = None
conf.iers_degraded_accuracy = "ignore"
