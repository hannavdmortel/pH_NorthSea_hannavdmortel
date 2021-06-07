import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats

rws_file = 'C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws = pd.read_parquet(rws_file, engine='auto')

#%%
#Group by datetime
grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="M")).mean()

#%% spm

chosen_stations = [
    "CALLOG70",
    "EGMAZE70",
    "NOORDWK20",
    "NOORDWK50",
    "ROTTMPT20",
    "ROTTMPT30",
    "ROTTMPT50",
    "ROTTMPT70",
    "SCHOUWN20",
    "TERSLG30",
    "TERSLG135",
    "TERHDE70",
    "WALCRN4"]

#rws.xs('BLAUWSOT', level='station')

for chosen_stations in rws.xs(key=chosen_stations, level='station'):
    fig, ax = plt.subplots(dpi=300)
    ax.scatter(x = grouped_month.index, y = grouped_month.spm, s=0)
    
    x = grouped_month
    interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.spm, kind='linear')
    interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.spm, s = 1000)
    
    datenum_interp = np.linspace(np.min(grouped_month.datenum), np.max(grouped_month.datenum), num = 500)
    spm_linear = interp_linear(datenum_interp)
    spm_spline = interp_spline(datenum_interp)
    
    ax.plot(datenum_interp, spm_linear)
    ax.plot(datenum_interp, spm_spline, zorder=10)
    ax.set_xlabel('Year')
    ax.set_ylabel('spm')
    ax.set_title('North Sea spm over time (annual averages)')

#%% pH
fig, ax = plt.subplots(dpi=300)
ax.scatter(x = grouped_month.index, y = grouped_month.pH, s=0)

interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.pH, kind='linear')
interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.pH, s = 1000)

datenum_interp = np.linspace(np.min(grouped_month.datenum), np.max(grouped_month.datenum), num = 800)
pH_linear = interp_linear(datenum_interp)
pH_spline = interp_spline(datenum_interp)

ax.plot(datenum_interp, pH_linear)
ax.plot(datenum_interp, pH_spline)
ax.set_xlabel('Year')
ax.set_ylabel('pH')
ax.set_title('North Sea pH over time (annual averages)')

#%% chlorophyll
chlorophyll_years = rws.xs['1980-01-01' : '2016-01-01', 'ymd']


grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="M")).mean()

fig, ax = plt.subplots(dpi=300, figsize=(8,2))
ax.scatter(x = grouped_month.index, y = grouped_month.chlorophyll, s=0)

interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.chlorophyll, kind='linear')
interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.chlorophyll, s = 1000)

datenum_interp = np.linspace(np.min(grouped_month.datenum), np.max(grouped_month.datenum), num = 800)
chlorophyll_linear = interp_linear(datenum_interp)
chlorophyll_spline = interp_spline(datenum_interp)

ax.plot(datenum_interp, chlorophyll_linear)
ax.plot(datenum_interp, chlorophyll_spline)
ax.set_xlabel('Year')
ax.set_ylabel('Chlorophyll')
ax.set_title('North Sea chlorophyll over time (annual averages)')
