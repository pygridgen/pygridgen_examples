from glob import glob

import numpy as np
import matplotlib.pyplot as plt

import pygridgen
import cartopy.crs as ccrs

beta, lonbry, latbry = np.loadtxt('grd_bry_test.dat', unpack=True)
ul_idx = 1

proj = ccrs.LambertConformal(central_longitude=lonbry.mean(), central_latitude=latbry.mean())

# focus the grid near the estuary mouth (parameters were determined
# by trial-and-error)
def focus(x, y, xo=0.6, yo=0.5):
    xf = np.tan((x - xo)*2.0)
    yf = np.tan((y - yo)*2.0)
    xf -= xf.min()
    xf /= xf.max()
    yf -= yf.min()
    yf /= yf.max()
    return xf, yf

shp = (259, 515)        # shape of the large grid

# get the points in a projected coordinate system
xbry, ybry, _ = proj.transform_points(ccrs.PlateCarree(), lonbry, latbry).T

# run pygridgen
grd = pygridgen.grid.Gridgen(xbry, ybry, beta, shp, 
                            focus=focus, ul_idx=ul_idx, verbose=True)
							
# mask the grid using existing polygons that represent land
for maskfile in glob('*.mask'):
    lon, lat = np.loadtxt(maskfile, unpack=True)
    x, y, _ = proj.transform_points(ccrs.PlateCarree(),lon, lat).T
    grd.mask_polygon(np.vstack((x, y)).T)

# An extra masked region, done by hand to fix the grid
lon = np.array([-70.809356641927451,
                -70.807724158705241,
                -70.80674047240781 ,
                -70.807340045005887,
                -70.809260613502616])
lat = np.array([42.811496540734552,
                42.811989712803737,
                42.816295717852896,
                42.816240386352455,
                42.815277526598322])
x, y, _ = proj.transform_points(ccrs.PlateCarree(),lon, lat).T

grd.mask_polygon(np.vstack((x, y)).T)

# plot the grid
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(grd.x, grd.y, '-k')
ax.plot(grd.x.T, grd.y.T, '-k')
ax.set_aspect(1.0)
ax.set_title('The full grid for the Merrimack domain')

# plot the mask
fig = plt.figure()
ax = fig.add_subplot(111)
ax.pcolor(grd.x.filled(np.nan), grd.y.filled(np.nan), grd.mask, 
          cmap=plt.cm.Blues, vmin=-0.2)
ax.set_aspect(1.0)
ax.set_title('The masked grid for the Merrimack domain')


## TODO: add bathymetric interpolation


