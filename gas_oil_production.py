import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%
permian_df = pd.ExcelFile('production_data/dpr-data.xlsx')
permian = permian_df.parse('Permian Region')

# %%
permian_oil = permian.iloc[1:, 4]
permian_gas = permian.iloc[1:, -1]
permian_month = permian.iloc[1:, 0]

# %%
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(permian_month, permian_oil, c='r')
ax.set_ylabel('Oil production, bbl/day', c='r')
ax1 = ax.twinx()
ax1.plot(permian_month, permian_gas, c='b')
ax1.set_ylabel('Gas production, Mcf/day', c='b')
ax.set_title('Permian region', size=22, weight='bold')
fig.savefig('Figures/Permian_production.png')

# %%
uintah = [10632162, 12146827, 11278096, 10117371]
uintah_year = [2019, 2018, 2017, 2016]
uintah_year = pd.to_datetime(uintah_year, format='%Y')

# %%
years = mdates.YearLocator()
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(uintah_year, uintah)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_title('Uintah region', size=22, weight='bold')
ax.set_ylabel('Oil production, barrel/year')
fig.savefig('Figures/Uintah_production.png')