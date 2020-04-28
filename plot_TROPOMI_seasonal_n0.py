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


def n0_timeaverage(data):
    data_filtered = data.where(data != 0)
    n0 = data_filtered.number_of_observations_qa_surf_albedo_filtered
    n0 = n0.sum(dim='time')
    return n0


start_dates = pd.date_range(start='2017-12', end='2019-07', freq='3MS')
end_dates = pd.date_range(start='2018-02', end='2019-09', freq='3M')

num_obs = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    xch4 = open_data_season(timerange,
                            datadir='TROPOMI_daily_gridded_XCH4_in_h5/h5/')
    num_obs.append(n0_timeaverage(xch4))

# %%
xch4_seasonal_n0 = xr.concat(num_obs, dim='time')
xch4_seasonal_n0['time'] = start_dates

# %%
label = '# of observation \n CH$_4$ Column Average Mixing Ratio [ppb]'
projection = ccrs.PlateCarree(central_longitude=0.0)

colors1 = plt.cm.Blues_r(np.linspace(0., 0.95, 128))
colors2 = plt.cm.hot_r(np.linspace(0., 0.9, 150))
colors = np.vstack((colors1, colors2))
cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

for ind, season in enumerate(xch4_seasonal_n0.time):
    figsize = (14, 4)
    plt.figure(figsize=figsize)
    ax = plt.axes(projection=projection)
    im = plot_seasonal_average(xch4_seasonal_n0.sel(time=season), ax=ax,
                               cmap=cmap, label=label)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label(label)

    start_date = datetime.strftime(start_dates[ind], '%Y%m%d')
    end_date = datetime.strftime(end_dates[ind], '%Y%m%d')
    plt.savefig(
        f'Figures/tropomi_3month_n0_{start_date}_{end_date}.png',
        dpi=150, bbox_inches='tight')
    plt.show()
