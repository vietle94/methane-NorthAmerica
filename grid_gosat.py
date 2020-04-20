#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 17:10:37 2020

@author: tenkanen
"""


import xarray as xr
from datetime import datetime
import h5py
import pandas as pd
import numpy as np


def to_datetime(x):
    return datetime.strptime(str(x.values),'%Y-%m-%d %H:%M:%S.%f')

def sort_data_to_bins(data, bins):
    categorical_object = pd.cut(data, bins, right=False)
    return categorical_object

def calculate_daily_mean(xch4, day, res=1):
    timedelta = pd.Timedelta('P0DT23H59M59.599999999S')
    xch4_day = xch4.sel(time=slice(day, day+timedelta))
    xch4_df = pd.DataFrame([xch4_day['xch4_biascorrected'].values,
                            xch4_day['xch4_uncertainty'].values, 
                            xch4_day['lat'].values, 
                            xch4_day['lon'].values]).T
    xch4_df.columns = variables
    
    lat_bins = np.arange(-90,91, res)
    data_lat_bins = sort_data_to_bins(xch4_df['lat'], lat_bins)
    xch4_df['lat_bin'] = data_lat_bins
    lon_bins = np.arange(-180,181, res)
    data_lon_bins = sort_data_to_bins(xch4_df['lon'], lon_bins)
    xch4_df['lon_bin'] = data_lon_bins
    
    mean = xch4_df.groupby(['lat_bin','lon_bin']).mean()
    freq = xch4_df.groupby(['lat_bin','lon_bin']).size().unstack()

    xch4_mean = mean['xch4_biascorrected'].unstack().values
    xch4_ds = xr.Dataset({'xch4_biascorrected':(['lat','lon'], xch4_mean),
                          'freq':(['lat','lon'], freq)},
                         coords={'lat':np.arange(-90+res/2,90, res), 'lon':np.arange(-180+res/2,180, res)})
    
    return xch4_ds
    

res = 2
filename = 'GOSAT_NIES_XCH4_v02.75.h5'
xch4 = xr.open_dataset(filename, drop_variables='time')
# time = list(map(to_datetime, xch4['time']))
time = xr.open_dataarray('GOSAT_datetime.nc')
xch4['phony_dim_0'] = time.values
xch4 = xch4.rename({'phony_dim_0':'time'})
time_daily = pd.date_range(pd.to_datetime(xch4['time'][0].values).date(),
                           pd.to_datetime(xch4['time'][-1].values).date())

variables = ['xch4_biascorrected','xch4_uncertainty', 'lat', 'lon']
mean_daily = []

for i,day in enumerate(time_daily):
    data = calculate_daily_mean(xch4, day, res)
    mean_daily.append(data)
    
    if i%10==0:
        print(i)
        
        
xch4_mean = xr.concat(mean_daily, dim='time')
xch4_mean['time'] = time_daily
xch4_mean.to_netcdf(f'GOSAT_NIES_XCH4_daily_{res}x{res}.nc')