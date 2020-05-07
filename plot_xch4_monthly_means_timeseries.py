#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:26:08 2020

@author: tenkanen
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import matplotlib.ticker as mticker

# %%

def caclulat_monthly_means(region):
    from plot_TROPOMI_seasonal_variable import open_data_season

    # TROPOMI
    var = 'xch4_biascorrected_qa_surf_albedo_filtered'
    timerange =  pd.date_range(start='2017-11-28',
                                end='2019-10-01',
                                freq='1D')
    
    xch4 = open_data_season(timerange,
                            region=region)
    print('done')
    xch4_monthly_mean = xch4.where(xch4!=0).resample(time='MS').mean(dim=xr.ALL_DIMS)
    xch4_monthly_mean = xr.DataArray(xch4_monthly_mean[var])
    print('done')
    xch4_monthly_mean.to_netcdf(f'TROPOMI_XCH4_monthly_mean_{region}.nc')
    
    
    # GOSAT 
    gosat_datadir = '/home/tenkanen/OneDrive/Jatko-opinnot/Satellite Remote Sensing Methods in Aerosols Science/MethaneHotSpots/methane-NorthAmerica/'
    xch4_gosat = xr.open_dataset(f'{gosat_datadir}/GOSAT_1x1.nc')
    xch4_gosat = xch4_gosat['xch4_biascorrected'].sel(time=slice(timerange[0], timerange[-1]))
    
    if region=='usa':
        xch4_gosat = xch4_gosat.sel(lat=slice(15,55), lon=slice(-135,-55))
    elif region=='permianbasin':
        xch4_gosat = xch4_gosat.sel(lat=slice(26.5,36.5), lon=slice(-108.5,-97.5))
    elif region=='uintahbasin':
        xch4_gosat = xch4_gosat.sel(lat=slice(35.5,43), lon=slice(-114,-105)) 
        
    xch4_gosat_monthly_mean = xch4_gosat.resample(time='MS').mean(dim=xr.ALL_DIMS)*1000 # ppm -> ppb
    
    return xch4_monthly_mean, xch4_gosat_monthly_mean



# %%

regions = ['permianbasin', 'uintahbasin']

    #%%
for region in regions:
    xch4_tropomi_monthly_mean = xr.open_dataarray(f'TROPOMI_XCH4_monthly_mean_{region}.nc')
    xch4_tropomi_monthly_mean = xch4_tropomi_monthly_mean.sel(time=slice('2017-12-01', '2019-09-30'))
    xch4_gosat_monthly_mean = xr.open_dataarray(f'GOSAT_XCH4_monthly_mean_{region}.nc')
    xch4_gosat_monthly_mean = xch4_gosat_monthly_mean.sel(time=slice('2017-12-01', '2019-09-30'))
    
    xch4_tropomi_season = xch4_tropomi_monthly_mean.resample(time='3MS').mean()
    xch4_gosat_season = xch4_gosat_monthly_mean.resample(time='3MS').mean()
    
    # %%
    cmap = plt.get_cmap('tab10')
    
    fig, ax = plt.subplots(figsize=(9, 6))
    xch4_tropomi_monthly_mean.plot(ax=ax, c=cmap(0), marker='.', label='TROPOMI')
    xch4_gosat_monthly_mean.plot(ax=ax, c=cmap(1), marker='.', label='GOSAT')
    ax.set_ylabel('XCH4 Column Average Mixing Ratio [ppb]')
    if region=='permianbasin':
        ax.set_title(f'Permian basin', size=22, weight='bold')
    elif region=='uintahbasin':
        ax.set_title(f'Uintah basin', size=22, weight='bold')
    ax.legend()
    fig.savefig(f'Figures/XCH4_TROPOMI_GOSAT_{region}_trend.png', bbox_inches='tight')
    plt.show()
    
    
    fig, ax = plt.subplots(figsize=(9, 6))
    
    xch4_tropomi_season.plot(ax=ax, c=cmap(2), marker='.', label='TROPOMI seasonal mean')
    xch4_gosat_season.plot(ax=ax, c=cmap(3), marker='.', label='GOSAT seasonal mean')
    
    ax.set_ylabel('XCH4 Column Average Mixing Ratio [ppb]')
    if region=='permianbasin':
        ax.set_title(f'Permian basin', size=22, weight='bold')
    elif region=='uintahbasin':
        ax.set_title(f'Uintah basin', size=22, weight='bold')
    ax.legend()
    fig.savefig(f'Figures/XCH4_TROPOMI_GOSAT_{region}_trend_seasonal.png', bbox_inches='tight')
    plt.show()



