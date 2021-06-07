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
var1 = "temperature_raw"
var2 = "spm_raw"

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    fig, ax = plt.subplots(dpi=300)
    x = df.index
    ax.plot(x, df[var1], c='xkcd:teal', label='Temperature')
    ax.set_title(stationcode.upper())
    ax.set_xlabel('Time')
    ax.set_ylabel('Raw temperature variation')
    ax2=ax.twinx()
    ax2.plot(x, df[var2], c='xkcd:magenta', label='SPM')
    ax2.set_ylabel('Raw SPM variation')
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1.02))
    #plt.show()
    fig.savefig("figures/raw/" + stationcode + "_temp_vs_spm"  + ".png")
