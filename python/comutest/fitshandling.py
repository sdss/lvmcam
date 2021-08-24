from astropy.io import fits 
with fits.open("/home/mgjeon/lvmcam/python/comutest/lab_19283193-0001.fits") as hdul:
    # print(hdul[0].header['EXPTIME'])
    # print(hdul[0].header.comments['EXPTIME'])
    print(hdul[0].header.set('EXAMPLE','This is example header [s]'))
    print(hdul[0].header)
    hdul.