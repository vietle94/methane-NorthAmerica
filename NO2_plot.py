import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plot_TROPOMI_seasonal_average import calculate_timeaverage, open_data_season, plot_seasonal_average
import glob
import cartopy.crs as ccrs
import cartopy.feature as feature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
# %%
# Calculate montly mean
start_dates = pd.date_range(start='2017-12', end='2019-09', freq='1MS')
end_dates = pd.date_range(start='2017-12', end='2019-10', freq='1M')

mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    xch4 = open_data_season(timerange,
                            datadir='TROPOMI_daily_gridded_XCH4_in_h5/h5/',
                            region='uintah')
    mean.append(calculate_timeaverage(xch4))

xch4_uintah = xr.concat(mean, dim='time')
xch4_uintah['time'] = start_dates

# %%
uintah_xch4 = np.zeros(len(xch4_uintah.time))
var = 'xch4_biascorrected_qa_surf_albedo_filtered'
for ind, season in enumerate(xch4_uintah.time):
    uintah_xch4[ind] = xch4_uintah[var].sel(
        time=season).mean().values

# %%
mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    xch4 = open_data_season(timerange,
                            datadir='TROPOMI_daily_gridded_XCH4_in_h5/h5/',
                            region='permian')
    mean.append(calculate_timeaverage(xch4))

xch4_permian = xr.concat(mean, dim='time')
xch4_permian['time'] = start_dates

# %%
permian_xch4 = np.zeros(len(xch4_permian.time))
var = 'xch4_biascorrected_qa_surf_albedo_filtered'
for ind, season in enumerate(xch4_permian.time):
    permian_xch4[ind] = xch4_permian[var].sel(
        time=season).mean().values


# %%


def open_data_season_NO2(timerange, region, datadir='NO2/'):
    files_list = glob.glob('NO2/*.nc4')
    files = []
    for time in timerange:
        for file in files_list:
            if time.strftime("%Ym%m%d") in file:
                files.append(file)
    data = xr.open_mfdataset(files, combine='nested', concat_dim='time')
    data['time'] = timerange

    if region == 'usa':
        data = data.sel(lat=slice(15, 55), lon=slice(-135, -55))
    elif region == 'permian':
        data = data.sel(lat=slice(26.5, 36.5), lon=slice(-108.5, -97.5))
    elif region == 'uintah':
        data = data.sel(lat=slice(35.5, 43), lon=slice(-114, -105))

    return data


# %%
# Calculate montly mean
start_dates = pd.date_range(start='2017-12', end='2019-09', freq='1MS')
end_dates = pd.date_range(start='2017-12', end='2019-10', freq='1M')

mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    no2 = open_data_season_NO2(timerange,
                               region='uintah')
    mean.append(calculate_timeaverage(no2))

no2_uintah = xr.concat(mean, dim='time')
no2_uintah['time'] = start_dates

# %%
uintah_no2 = np.zeros(len(no2_uintah.time))
var = 'ColumnAmountNO2TropCloudScreened'
for ind, season in enumerate(no2_uintah.time):
    uintah_no2[ind] = no2_uintah[var].sel(
        time=season).mean().values

# %%
mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    no2 = open_data_season_NO2(timerange,
                               region='permian')
    mean.append(calculate_timeaverage(no2))

no2_permian = xr.concat(mean, dim='time')
no2_permian['time'] = start_dates

# %%
permian_no2 = np.zeros(len(no2_permian.time))
var = 'ColumnAmountNO2TropCloudScreened'
for ind, season in enumerate(no2_permian.time):
    permian_no2[ind] = no2_permian[var].sel(
        time=season).mean().values

# %%
cmap = plt.get_cmap('tab10')
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(no2_uintah.time, uintah_no2, c=cmap(1))
ax.set_ylabel('NO2-OMI', color=cmap(1))
ax1 = ax.twinx()
ax1.plot(xch4_uintah.time, uintah_xch4, c=cmap(0))
ax1.set_ylabel('XCH4 Column Average Mixing Ratio [ppb]', color=cmap(0))
ax.set_ylabel('NO2 Total Column 1/cm2')
ax.set_title('Uintah basin', size=22, weight='bold')
fig.savefig('Figures/NO2-CH4_uintah_trend.png')

# %%
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(no2_permian.time, permian_no2, c=cmap(1))
ax.set_ylabel('NO2-OMI', color=cmap(1))
ax1 = ax.twinx()
ax1.plot(xch4_permian.time, permian_xch4, c=cmap(0))
ax1.set_ylabel('XCH4 Column Average Mixing Ratio [ppb]', color=cmap(0))
ax.set_ylabel('NO2 Total Column 1/cm2')
ax.set_title('Permian basin', size=22, weight='bold')
fig.savefig('Figures/NO2-CH4_permian_trend.png')

# %%
# Calculate montly mean
start_dates = pd.date_range(start='2018-01', end='2018-12', freq='YS')
end_dates = pd.date_range(start='2018-12', end='2019-01', freq='Y')

mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    no2 = open_data_season_NO2(timerange,
                               region='uintah')
    mean.append(calculate_timeaverage(no2))

no2_uintah_annual = xr.concat(mean, dim='time')
no2_uintah_annual['time'] = start_dates

# %%
var = 'ColumnAmountNO2TropCloudScreened'
label = 'NO2 Total Column 1/cm2'
projection = ccrs.PlateCarree(central_longitude=0.0)
figsize = (14, 4)
plt.figure(figsize=figsize)
# ax = plt.subplot(np.ceil(len(no2_uintah_annual.time)/2), 2, ind+1,
#                  projection=projection)
ax = plt.axes(projection=projection)
im = no2_uintah_annual[var].plot(x='lon', y='lat',
                                 transform=ccrs.PlateCarree(),
                                 ax=ax, cmap='jet', add_colorbar=False)
ax.set_ylim(no2_uintah_annual.lat.min(), no2_uintah_annual.lat.max())
# plot features
ax.coastlines()
ax.add_feature(feature.BORDERS)
ax.add_feature(feature.OCEAN, color='lightgrey')
ax.add_feature(feature.LAND, color='lightgrey')
ax.add_feature(feature.STATES, lw=0.5)
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_xticks(np.arange(-113, -106, 2), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(36, 42, 1), crs=ccrs.PlateCarree())

ax.set_xlim([-113, -106])
ax.set_ylim([36, 42])
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')

ax.set_title(f'Time average 2018-01-01 - 2018-12-31')

cbar = plt.colorbar(im, ax=ax)
cbar.set_label(label)
plt.savefig(
    f'Figures/NO2-uintah-20180101_20181231.png', dpi=150, bbox_inches='tight')
plt.show()

# %%
mean = []
for ind, timerange_start in enumerate(start_dates):
    timerange = pd.date_range(start=timerange_start,
                              end=end_dates[ind],
                              freq='1D')
    no2 = open_data_season_NO2(timerange,
                               region='permian')
    mean.append(calculate_timeaverage(no2))

no2_permian_annual = xr.concat(mean, dim='time')
no2_permian_annual['time'] = start_dates

# %%
var = 'ColumnAmountNO2TropCloudScreened'
label = 'NO2 Total Column 1/cm2'
projection = ccrs.PlateCarree(central_longitude=0.0)
figsize = (14, 4)
plt.figure(figsize=figsize)
# ax = plt.subplot(np.ceil(len(no2_permian_annual.time)/2), 2, ind+1,
#                  projection=projection)
ax = plt.axes(projection=projection)
im = no2_permian_annual[var].plot(x='lon', y='lat',
                                  transform=ccrs.PlateCarree(),
                                  ax=ax, cmap='jet', add_colorbar=False)
ax.set_ylim(no2_permian_annual.lat.min(), no2_permian_annual.lat.max())
# plot features
ax.coastlines()
ax.add_feature(feature.BORDERS)
ax.add_feature(feature.OCEAN, color='lightgrey')
ax.add_feature(feature.LAND, color='lightgrey')
ax.add_feature(feature.STATES, lw=0.5)
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.set_xticks(np.arange(-106, -98, 2), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(28, 36, 1), crs=ccrs.PlateCarree())

ax.set_xlim([-106.5, -99])
ax.set_ylim([28, 35])
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')

ax.set_title(f'Time average 2018-01-01 - 2018-12-31')

cbar = plt.colorbar(im, ax=ax)
cbar.set_label(label)
plt.savefig(
    f'Figures/NO2-permian_20180101_20181231.png', dpi=150, bbox_inches='tight')
plt.show()
