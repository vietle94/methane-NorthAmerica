#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:35:18 2020

@author: tenkanen
"""

import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from datetime import datetime
from dateutil.relativedelta import relativedelta


def open_data_season(timerange):
    datadir = '/media/tenkanen/My Passport/MethaneHotSpots/h5/'
    files = [f'{datadir}{date.strftime("%Y%m%d")}_TROPOMI_xch4_filtered_gridded_lat_01_lon_0125.h5'\
         for date in timerange]
    data = xr.open_mfdataset(files, combine='nested', concat_dim='time')
    data['phony_dim_0'] = data['latitude'][0]
    data['phony_dim_1'] = data['longitude'][0]
    data = data.rename({'phony_dim_0':'lat', 'phony_dim_1':'lon'})
    data['time'] = timerange
    
    data = data.sel(lat=slice(20,50), lon=slice(-130,-60))
    
    return data


def calculate_timeaverage(data):
    data_mean = data.where(data!=0).mean(dim='time')
    
    return data_mean


def plot_seasonal_average(xch4, ax, levels, cmap, label):
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
    
    start_date = datetime.strftime(pd.Timestamp(xch4_seasonal_average[var].sel(time=season).time.values),
                                   '%Y-%m-%d')
    end_date = datetime.strftime(pd.Timestamp(start_date)+relativedelta(months=+3)-pd.Timedelta('1 day'),
                                 '%Y-%m-%d')
    ax.set_title(f'Time average {start_date} - {end_date}')
    
    return im


start_dates = pd.date_range(start='2017-12', end='2019-07', freq='3MS')
end_dates = pd.date_range(start='2018-02', end='2019-09', freq='3M')

means = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    xch4 = open_data_season(timerange)
    xch4_mean = calculate_timeaverage(xch4)

    means.append(xch4_mean)

    
xch4_seasonal_average = xr.concat(means, dim='time')
xch4_seasonal_average
xch4_seasonal_average['time'] = start_dates

var = 'xch4_biascorrected_qa_surf_albedo_filtered'
# var = 'xch4_biascorrected_qa_filtered'
# var = 'number_of_observations_qa_surf_albedo_filtered'
label = r'CH$_4$ Column Average Mixing Ratio [ppb]'

levels = np.arange(1820,1900.1,0.1)
projection = ccrs.PlateCarree(central_longitude = 0.0)

colors1 = plt.cm.Blues_r(np.linspace(0., 0.95, 128))
colors2 = plt.cm.hot_r(np.linspace(0., 0.9, 150))
colors = np.vstack((colors1, colors2))
cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
# cmap = plt.get_cmap('jet')

# figsize = (20,18)
# plt.figure(figsize=figsize)
for ind,season in enumerate(xch4_seasonal_average.time):
    figsize = (14,4)
    plt.figure(figsize=figsize)
    # ax = plt.subplot(np.ceil(len(xch4_seasonal_average.time)/2), 2, ind+1, 
    #                  projection=projection)
    ax = plt.axes(projection=projection)
    im = plot_seasonal_average(xch4_seasonal_average[var].sel(time=season), ax, levels, cmap, label)
    # if ind==len(xch4_seasonal_average.time)-1:
    #     cbar = plt.colorbar(im, ax=ax, orientation='vertical', fraction=0.075)
    #     cbar.set_label(label)   

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(label)   
    
    start_date = datetime.strftime(start_dates[ind], '%Y%m%d')
    end_date = datetime.strftime(end_dates[ind], '%Y%m%d')
    plt.savefig(f'Figures/tropomi_3month_average_{start_date}_{end_date}.png', dpi=150, bbox_inches='tight')
    plt.show()
