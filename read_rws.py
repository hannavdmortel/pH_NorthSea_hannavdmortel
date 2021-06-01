import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats

rws_file = 'C:/Users/hanna/Documents/Marine Sciences/NIOZ/CO2 flux and acidification North Sea/rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws = pd.read_parquet(rws_file, engine='auto')

#rws.sort_values(by='datetime', inplace=True)
grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="Y")).mean()

fig, ax = plt.subplots(dpi=300)
ax.scatter(x = grouped_month.index, y = grouped_month.spm, s=0)

interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.spm, kind='linear')
interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.spm, s = 1000)

datenum_interp = np.linspace(np.min(grouped_month.datenum), np.max(grouped_month.datenum), num = 800)
spm_linear = interp_linear(datenum_interp)
spm_spline = interp_spline(datenum_interp)

ax.plot(datenum_interp, spm_linear)
ax.plot(datenum_interp, spm_spline)
ax.set_xlabel('Year')
ax.set_ylabel('spm')
ax.set_title('North Sea spm over time (annual averages)')
