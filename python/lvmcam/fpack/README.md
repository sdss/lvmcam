# fpack & funpack FITS image compression programs
This programs are made by C source code from https://heasarc.gsfc.nasa.gov/fitsio/fpack/.

## Usage
```
$ ls -al                               
3528000 input.fits

$ fpack -O output.fits.fz input.fits 
3528000 input.fits
2180160 output.fits.fz

$ funpack output.fits.fz            
$ ls -al
3528000 input.fits
3528000 output.fits
2180160 output.fits.fz
```