#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:35:18 2020

@author: tenkanen
"""
#
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
from datetime import datetime
from plot_TROPOMI_seasonal_average import open_data_season, plot_seasonal_average


def sd_timeaverage(data):
    data_filtered = data.where(data != 0)
    variance = data_filtered.stddev_xch4_biascorrected_qa_surf_albedo_filtered**2
    sd = np.sqrt(variance)
    sd_average = sd.mean(dim='time')
    return sd_average


start_dates = pd.date_range(start='2017-12', end='2019-07', freq='3MS')
end_dates = pd.date_range(start='2018-02', end='2019-09', freq='3M')

sd = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    xch4 = open_data_season(timerange,
                            datadir='TROPOMI_daily_gridded_XCH4_in_h5/h5/')
    sd.append(sd_timeaverage(xch4))

# %%
xch4_seasonal_sd = xr.concat(sd, dim='time')
xch4_seasonal_sd['time'] = start_dates

# %%
label = 'Standard deviation of \n CH$_4$ Column Average Mixing Ratio [ppb]'
projection = ccrs.PlateCarree(central_longitude=0.0)

colors1 = plt.cm.Blues_r(np.linspace(0., 0.95, 128))
colors2 = plt.cm.hot_r(np.linspace(0., 0.9, 150))
colors = np.vstack((colors1, colors2))
cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

for ind, season in enumerate(xch4_seasonal_sd.time):
    figsize = (14, 4)
    plt.figure(figsize=figsize)
    ax = plt.axes(projection=projection)
    im = plot_seasonal_average(xch4_seasonal_sd.sel(time=season), ax=ax,
                               vmax=10, vmin=0, cmap=cmap, label=label)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(label)

    start_date = datetime.strftime(start_dates[ind], '%Y%m%d')
    end_date = datetime.strftime(end_dates[ind], '%Y%m%d')
    plt.savefig(
        f'Figures/tropomi_3month_sd_{start_date}_{end_date}.png',
        dpi=150, bbox_inches='tight')
    plt.show()
