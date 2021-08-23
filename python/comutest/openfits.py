import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
plt.style.use(astropy_mpl_style)

file = "../lvmcam/assets/test_19283193-0001.fits"

data, header = fits.getdata(file, header=True)
# print(data)
# print(header)

fits_inf = fits.open(file)
print(fits_inf.info())
# print(fits_inf[0].header)
print(fits_inf[0].data[0].shape)

image_data = fits_inf[0].data[0]

plt.figure()

plt.imshow(image_data, cmap='gray')

# plt.axis('off')
# plt.grid(b=None)
plt.colorbar()

plt.show()
