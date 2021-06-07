#Chlorophyll vs pH trend specific stations

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats

rws_file = 'C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws = pd.read_parquet(rws_file, engine='auto')

stations = [
    "ROTTMPT20",
    "ROTTMPT70",
    "ROTTMPT100",
    "TERSLG10",
    "TERSLG30",
    "TERSLG50",
    "TERSLG175",
    "CALLOG30",
    "NOORDWK50",
    "GOERE70",
    "SCHOUWN30",
    "SCHOUWN50",
    "WALCRN20",
    "WALCRN30",
    "WALCRN50",
    "WALCRN70"]

for stationcode in stations:
    L = (~np.isnan(rws.xs(stationcode, level='station')['pH']))
    L2 = ~np.isnan(rws.xs(stationcode, level='station')['chlorophyll'])
    x = rws.xs(stationcode, level='station')['datetime']
    y = rws.xs(stationcode, level = 'station')['pH']
    z = rws.xs(stationcode, level = 'station')['chlorophyll']
    fig,ax = plt.subplots()
    ax.plot(x[L], y[L], c='blue', label='pH')
    ax.set_xlabel('year')
    ax.set_ylabel('pH')
    ax2=ax.twinx()
    ax2.plot(x[L2], z[L2], c='red', label='chlorophyll')
    ax2.set_ylabel('chlorophyll')
    # interp_linear = interpolate.interp1d(x, y, kind='linear')
    # interp2_linear = interpolate.interp1d(x, z, kind='linear')
    # x_interp = np.linspace(np.min(x), np.max(x), num = 800)
    # pH_linear = interp_linear(x_interp)
    # chlorophyll_linear = interp2_linear(x_interp)
    ax.set_title(stationcode.upper())
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1.02))
    plt.show()


