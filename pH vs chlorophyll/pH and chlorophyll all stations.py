import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "pH_trend"
var2 = "chlorophyll_trend"

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    L = ((df.datenum > mdates.date2num('1990-01-01')) & (df.datenum < mdates.date2num('2000-01-01')))
    x=df[L]
    fig, ax = plt.subplots(dpi=300)
    ax.plot(x.index, x[var1], c='xkcd:strawberry', label='pH')
    ax.set_title(stationcode.upper())
    ax.set_xlabel('Time')
    ax.set_ylabel('pH trend')
    ax2=ax.twinx()
    ax2.plot(x.index, x[var2], c='xkcd:lime green', label='chlorophyll')
    ax2.set_ylabel('Chlorophyll trend')
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1.02))
    #plt.show()
    fig.savefig("figures/trend/" + stationcode + "_pH_vs_chlorophyll"  + ".png")
