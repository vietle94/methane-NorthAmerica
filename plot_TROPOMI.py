#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:17:29 2020

@author: tenkanen
"""

import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors



# open data
datadir = '/media/tenkanen/My Passport/MethaneHotSpots/h5/'
time_deGouw = pd.date_range(start='2018-12-01', end='2019-03-31', freq='1D')
files = [f'{datadir}{date.strftime("%Y%m%d")}_TROPOMI_xch4_filtered_gridded_lat_01_lon_0125.h5'\
         for date in time_deGouw]
data = xr.open_mfdataset(files, combine='nested', concat_dim='time')
data['phony_dim_0'] = data['latitude'][0]
data['phony_dim_1'] = data['longitude'][0]
data = data.rename({'phony_dim_0':'lat', 'phony_dim_1':'lon'})

# select wanted variable and lat and lon coords
var = 'xch4_biascorrected_qa_surf_albedo_filtered'
data = data[var].sel(lat=slice(20,50), lon=slice(-130,-60))

# calculate average
data_mean = data.where(data>0).mean(dim='time')
xch4 = xr.DataArray(data_mean.values, 
                    coords=[data_mean.lat.values, data_mean.lon.values], 
                    dims=['lat','lon'])
levels = np.arange(1820,1900.1,0.1)
projection = ccrs.PlateCarree(central_longitude = 0.0)

colors1 = plt.cm.Blues_r(np.linspace(0., 0.9, 128))
colors2 = plt.cm.hot_r(np.linspace(0., 0.9, 150))
colors = np.vstack((colors1, colors2))
cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
# cmap = plt.get_cmap('jet')

label = r'CH$_4$ Column Average Mixing Ratio [ppb]'
figsize = (14,6)

plt.figure(figsize=figsize)
# plt.figure()
ax = plt.subplot(111, projection=projection)
# plot image
im = xch4.plot(x='lon', y='lat',
                    transform=ccrs.PlateCarree(),
                    ax=ax, levels=levels,
                    cmap=cmap, add_colorbar=False)
ax.set_ylim(xch4.lat.min(), xch4.lat.max())
# plot features
ax.coastlines()
ax.add_feature(feature.BORDERS)
ax.add_feature(feature.OCEAN, color='lightgrey')
ax.add_feature(feature.LAND, color='lightgrey')
ax.add_feature(feature.STATES, lw=0.5)
cbar = plt.colorbar(im, ax=ax, orientation='horizontal', fraction=0.075)
cbar.set_label(label)   
plt.savefig('Figures/tropomi_deGouw.png', dpi=150, bbox_inches='tight')
plt.show()

