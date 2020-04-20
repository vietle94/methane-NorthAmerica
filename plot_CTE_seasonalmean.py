#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:10:37 2020

@author: tenkanen
"""

import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt



def plot_seasonal_averages(ds, levels, cmap, label, figsize, projection):
    plt.figure(figsize=figsize)
    for i, season in enumerate(ds.season):
        # choose the axis
        ax = plt.subplot(np.ceil(len(ds.season)/2), 2, i+1,
                         projection=projection)
        # select data
        ch4 = ds.sel(season=season)
        # drop small values (mainly the ocean)
        # ch4 = ch4.where(ch4>0.01)
        # plot image
        im = ch4.plot(x='lon', y='lat',
                      transform=ccrs.PlateCarree(),
                      ax=ax, levels=levels,
                      cmap=cmap, add_colorbar=False)
        # plot features
        ax.coastlines()
        ax.add_feature(feature.BORDERS)
        ax.add_feature(feature.OCEAN, color='lightgrey')
        # colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(label)  



# open data
# file = 'esticc_USA'
file = 'GOSAT_2x2'
data = xr.open_dataset(f'{file}.nc')
if file== 'esticc_USA':
    var = 'posterior_tot'
    data = data[var]*1e9 # mol m⁻² s⁻¹ ->  nmol m⁻² s⁻¹
    levels = np.arange(-3,50,0.01)
    label = r'CH$_4$ flux [nmol m$^{-2}$ s$^{-1}$]'
    
if file.split('_')[0]=='GOSAT':
    var = 'xch4_biascorrected'
    data = data[var].sel(lat=slice(20,50), lon=slice(-130,-60), time=slice('2017','2018'))
    levels = np.arange(1.77,1.9,0.001)
    label = r'CH$_4$ mole fraction [ppm]'
     

# calculte weighted seasonal average

# example with 3 month averages
ds = data.resample(time='3MS').mean(dim='time')
ds = ds.rename({'time':'season'})

# plot 3-month averages of total posterior methane fluxes
projection = ccrs.PlateCarree(central_longitude = 0.0)
cmap = plt.get_cmap('jet')
figsize = (14,10)
plot_seasonal_averages(ds, levels, cmap, label, figsize, projection)
# save image
plt.savefig(f'Figures/{file}_3month_average.png', dpi=150, bbox_inches='tight')
plt.show()
