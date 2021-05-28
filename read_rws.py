import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns

rws_file = 'C:/Users/hanna/Documents/Marine Sciences/NIOZ/CO2 flux and acidification North Sea/rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws = pd.read_parquet(rws_file, engine='auto')

# fig, ax = plt.subplots(dpi=300)
# spm = rws.spm.to_numpy()
# datetime = rws.datetime.to_numpy()
# L = (~np.isnan(spm))
# spm_L = spm[L]
# datetime_L = datetime[L]

rws['datetime'] = pd.to_datetime(rws['datetime'])
rws['7day_rolling_avg_spm'] = rws.spm.rolling(window=100, on='datetime').mean()
fig, ax = plt.subplots(dpi=300)
ax.scatter(x ='datetime', y = '7day_rolling_avg_spm', data = rws)