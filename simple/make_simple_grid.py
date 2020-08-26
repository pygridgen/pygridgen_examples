import numpy as np
import matplotlib.pyplot as plt

import pygridgen
import cartopy.crs as ccrs

# create a simple estuary and coast
xbry = [1, 2, 2, 0.5, 1, 0, 0, 1]
ybry = [2.5, 3, 0, 0, 1.25, 1.25, 1.75, 1.75]
beta = [1, 1, 1, 1, -1, 1, 1, -1]

# initialize a focus object
focus = pygridgen.grid.Focus()

# increase focus along the axis of the estuary
focus.add_focus(0.5, 'y', 3.0, 0.5)

shp = (60, 40)

grd = pygridgen.grid.Gridgen(xbry, ybry, beta, shp, 
                            focus=focus, ul_idx=0, verbose=True)
                            
# plot the grid
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(grd.x, grd.y, '-k')
ax.plot(grd.x.T, grd.y.T, '-k')
ax.set_aspect(1.0)
ax.set_title('The grid for the simple domain')
