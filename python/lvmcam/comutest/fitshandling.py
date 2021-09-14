from astropy.io import fits


with fits.open("/home/mgjeon/lvmcam/python/lvmcam/assets/2459471/sci.agw-00000001.fits") as hdul:
    # print(hdul[0].header['EXPTIME'])
    # print(hdul[0].header.comments['EXPTIME'])
    # print(hdul[0].header.set('EXAMPLE', 'This is example header [s]'))
    hdrs = hdul[0].header
    with open("./hdr.txt", "w") as f:
        for hdr in hdrs:
            f.write(f"* - {hdr}\n")
            f.write(f"  - {hdrs[hdr]}\n")
            f.write(f"  - {hdrs.comments[hdr]}\n")
            # print("* - ", hdr)
            # print("  - ", hdrs[hdr])
            # print("  - ", hdrs.comments[hdr])
    # print(repr(hdr))
    # print(list(hdr))
