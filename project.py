import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import h5py
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader

# %%
# List all data files path
files_list = glob('TROPOMI_daily_gridded_XCH4_in_h5/h5/*.h5')
files_list

# %%
df = h5py.File(files_list[0], 'r')
date = df.filename.split('\\')[1].split('_')[0]

# list all keys
list(df.keys())

# apprently she did not put any attributes in the data file
try:
    next(df.attrs.__iter__())
except StopIteration:
    print('No attributes')

# Look at data structure
for x in list(df.keys()):
    print(x)
    print(df[x].shape)

# %% plot
fig, ax = plt.subplots(2, 3, figsize=(16, 9))
for ax, var in zip(ax.flatten(),
                   [key for key in list(df.keys()) if 'tude' not in key]):
    ax.hist(df[var][:].flatten())
    ax.set_title(var)
    ax.set_yscale('log')
fig.subplots_adjust(hspace=0.3)

# %% Plot map
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

ax.set_extent([-130, -60, 24, 52], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.coastlines()
ax.set_title(date, size=22, weight='bold', y=1.1)
# Add grid lines
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
# Change format of grid label
gl.yformatter = LATITUDE_FORMATTER
gl.xformatter = LONGITUDE_FORMATTER

shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m',
                                     category='cultural', name=shapename)
oilproduction = {
    'New Jersey':  438.00,
    'Rhode Island':   387.35,
    'Utah': 9999
}

cmap = plt.cm.jet

facecolor = {key: cmap(value/10000) for key, value in oilproduction.items()}
for astate in shpreader.Reader(states_shp).records():
    state_name = astate.attributes['name']
    if state_name in oilproduction:
        ax.add_geometries([astate.geometry], ccrs.PlateCarree(),
                          facecolor=facecolor[state_name], alpha=0.5)

vmin = 1500  # exclude all value <1500, but the aim is to exclude 0
vmax = 2000
levels = np.linspace(vmin, vmax, 20)
contourf_ = ax.contourf(df['longitude'],
                        df['latitude'],
                        df['xch4_biascorrected_qa_surf_albedo_filtered'],
                        cmap='jet', vmin=vmin, vmax=vmax, levels=levels)
# cbar = fig.colorbar(contourf_, ax=ax, orientation='horizontal', fraction=0.05)
# %% Close file
df.close()
