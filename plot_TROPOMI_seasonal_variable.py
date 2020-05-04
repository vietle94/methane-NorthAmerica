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
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from datetime import datetime
from dateutil.relativedelta import relativedelta


def open_data_season(timerange, region):
    datadir = '/media/tenkanen/My Passport/MethaneHotSpots/h5/'
    files = [f'{datadir}{date.strftime("%Y%m%d")}_TROPOMI_xch4_filtered_gridded_lat_01_lon_0125.h5'\
         for date in timerange]
    data = xr.open_mfdataset(files, combine='nested', concat_dim='time')
    data['phony_dim_0'] = data['latitude'][0]
    data['phony_dim_1'] = data['longitude'][0]
    data = data.rename({'phony_dim_0':'lat', 'phony_dim_1':'lon'})
    data['time'] = timerange
    
    if region=='usa':
        data = data.sel(lat=slice(15,55), lon=slice(-135,-55))
    elif region=='permianbasin':
        data = data.sel(lat=slice(26.5,36.5), lon=slice(-108.5,-97.5))
    elif region=='uintahbasin':
        data = data.sel(lat=slice(35.5,43), lon=slice(-114,-105))        
        
    return data


def calculate_timeaverage(data):
    data_mean = data.where(data!=0).mean(dim='time')
    
    return data_mean


def calculate_sum_over_time(data):
    data_sum = data.sum(dim='time')
    
    return data_sum


def basemap(ax, extent, base):
    ax.set_ylim(*extent[2:])
    ax.set_xlim(*extent[:2])
    # plot features
    ax.coastlines()
    ax.add_feature(feature.BORDERS)
    ax.add_feature(feature.OCEAN, color='lightgrey')
    ax.add_feature(feature.LAND, color='lightgrey')
    ax.add_feature(feature.STATES, lw=0.5)
    
    ax.set_xticks(np.arange(myround(extent[0], base), 
                            extent[1]+1, base), 
                  crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(myround(extent[2], base), 
                            extent[3]+1, base),
                  crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_ylabel('Latitude')
    ax.set_xlabel('Longitude')
    

def plot_seasonal_variable(xch4, ax, levels, cmap, label, title,
                           start, end):
    im = xch4.plot(x='lon', y='lat',
                    transform=ccrs.PlateCarree(),
                    ax=ax, levels=levels,
                    cmap=cmap, add_colorbar=False)
    
    start_date = datetime.strftime(start, '%Y-%m-%d')

    end_date = datetime.strftime(end, '%Y-%m-%d')
    ax.set_title(f'{title} {start_date} - {end_date}')
    
    return im


def myround(x, base=5):
    return base * round(x/base)




var = 'xch4_biascorrected_qa_surf_albedo_filtered'
# var = 'xch4_biascorrected_qa_filtered'
label = r'CH$_4$ Column Average Mixing Ratio [ppb]'
title = 'Time average'
levels = np.arange(1820,1871.1,0.1)

regions = ['usa', 'permianbasin', 'uintahbasin']
# regions = [regions[1]]
for region in regions:
    # extent = [min lon, max lon, min lat, max lat]
    if region=='usa':
        extent = [-130, -60, 20, 50]
        base = 10
    elif region=='permianbasin':
        extent = [-106.5, -99.5, 28.5, 34.5]
        base = 1
    elif region=='uintahbasin':
        extent = [-113,-106, 36, 42]
        base = 1
    else:
        raise Exception('!!! Region should be \'usa\', \'permianbasin\' or \'uintahbasin\' !!!')
    
    
    # var = 'number_of_observations_qa_surf_albedo_filtered'
    # label = 'Number of observations'
    # title = 'Number of observations'
    # levels = np.arange(0,120.1,0.1)
    
    # start_dates = pd.date_range(start='2017-12', end='2019-07', freq='3MS')
    # end_dates = pd.date_range(start='2018-02', end='2019-09', freq='3M')
    
    start_dates = pd.date_range(start='2018-01', end='2018-12', freq='YS')
    end_dates = pd.date_range(start='2018-12', end='2019-01', freq='Y')
    
    seasonal_vars = []
    for ind, timerange_start in enumerate(start_dates):
        timerange = pd.date_range(start=timerange_start,
                                  end=end_dates[ind],
                                  freq='1D')
        xch4 = open_data_season(timerange, region)
        if var.split('_')[0]=='number':
            seasonal_var = calculate_sum_over_time(xch4) 
        else:
            seasonal_var = calculate_timeaverage(xch4)
    
        seasonal_vars.append(seasonal_var)
    
        
    xch4_seasonal_var = xr.concat(seasonal_vars, dim='time')
    xch4_seasonal_var
    xch4_seasonal_var['time'] = start_dates
    
    projection = ccrs.PlateCarree(central_longitude = 0.0)
    
    # colors1 = plt.cm.Blues_r(np.linspace(0., 0.95, 128))
    # colors2 = plt.cm.hot_r(np.linspace(0., 0.9, 150))
    # colors = np.vstack((colors1, colors2))
    # cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    cmap = plt.get_cmap('jet')
    
    # figsize = (20,18)
    # plt.figure(figsize=figsize)
    for ind,season in enumerate(xch4_seasonal_var.time):
        if region=='usa':
            figsize = (14,4)
        else:
            figsize = (12,5)
        plt.figure(figsize=figsize)
        # ax = plt.subplot(np.ceil(len(xch4_seasonal_average.time)/2), 2, ind+1, 
        #                  projection=projection)
        ax = plt.axes(projection=projection)
        im = plot_seasonal_variable(xch4_seasonal_var[var].sel(time=season), ax, 
                                    levels, cmap, label, title,
                                    start_dates[ind], end_dates[ind])
        basemap(ax, extent, base)
        # if ind==len(xch4_seasonal_average.time)-1:
        #     cbar = plt.colorbar(im, ax=ax, orientation='vertical', fraction=0.075)
        #     cbar.set_label(label)   
    
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(label)   
        
        start_date = datetime.strftime(start_dates[ind], '%Y%m%d')
        end_date = datetime.strftime(end_dates[ind], '%Y%m%d')
        if var.split('_')[0]=='number':
            plt.savefig(f'Figures/tropomi_3month_numberofobs_{start_date}_{end_date}_{region}.png', dpi=150, bbox_inches='tight')
        else:
            plt.savefig(f'Figures/tropomi_3month_average_{start_date}_{end_date}_{region}.png', dpi=150, bbox_inches='tight')
    
        plt.show()
