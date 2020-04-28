import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plot_TROPOMI_seasonal_average import open_data_season, calculate_timeaverage
import geopandas
from rasterio import features
from affine import Affine

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
                            datadir='TROPOMI_daily_gridded_XCH4_in_h5/h5/')
    mean.append(calculate_timeaverage(xch4))

xch4_seasonal_mean = xr.concat(mean, dim='time')
xch4_seasonal_mean['time'] = start_dates

# %%
# Calculate state mask to extract values in each state in the next step


def transform_from_latlon(lat, lon):
    lat = np.asarray(lat)
    lon = np.asarray(lon)
    trans = Affine.translation(lon[0], lat[0])
    scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
    return trans * scale


def rasterize(shapes, coords, fill=np.nan, **kwargs):
    """Rasterize a list of (geometry, fill_value) tuples onto the given
    xr coordinates. This only works for 1d latitude and longitude
    arrays.
    """
    transform = transform_from_latlon(coords['lat'], coords['lon'])
    out_shape = (len(coords['lat']), len(coords['lon']))
    raster = features.rasterize(shapes, out_shape=out_shape,
                                fill=fill, transform=transform,
                                dtype=float, **kwargs)
    return xr.DataArray(raster, coords=coords, dims=('lat', 'lon'))


# this shapefile is from natural earth data
# http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/
states = geopandas.read_file('ne_10m_admin_1_states_provinces_lakes')
us_states = states.query("admin == 'United States of America'").reset_index(drop=True)
state_ids = {k: i for i, k in enumerate(us_states.woe_name)}
shapes = [(shape, n) for n, shape in enumerate(us_states.geometry)]

# %%
subset = xch4_seasonal_mean.sel(time=xch4_seasonal_mean.time[0])
state_mask = rasterize(shapes, subset.coords)

# %%
# Extract values in each states then take mean of them
chosen_states = ['California', 'New York', 'Texas']
states = pd.DataFrame(np.zeros([len(xch4_seasonal_mean.time),
                                len(chosen_states)]),
                      columns=chosen_states)
number_obs = pd.DataFrame(np.zeros([len(xch4_seasonal_mean.time),
                                    len(chosen_states)]),
                          columns=chosen_states)
var = 'xch4_biascorrected_qa_surf_albedo_filtered'
for ind, season in enumerate(xch4_seasonal_mean.time):
    xch4_season = xch4_seasonal_mean[var].sel(
        time=season)
    number_obs_season = xch4_seasonal_mean['number_of_observations_qa_surf_albedo_filtered'].sel(
        time=season)
    for state in states:
        states.loc[ind, state] = xch4_season.where(state_mask == state_ids[state]).mean().values
        number_obs.loc[ind, state] = number_obs_season.where(
            state_mask == state_ids[state]).mean().values

# %%
fig, axes = plt.subplots(2, 1, figsize=(16, 9))
for ax, data, title in zip(axes.flatten(),
                           [states, number_obs],
                           ['Monthly means of XCH4', 'Monthly number of observation']):
    for state in chosen_states:
        ax.plot(start_dates, data[state], label=state)
    ax.legend()
    ax.set_title(title, size=22, weight='bold')
fig.subplots_adjust(hspace=0.3)
fig.savefig('states_montly_mean.png')

# %%
