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
var1 = "nitrxte_seasonal"
var2 = "phosphate_seasonal"

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    fig, ax = plt.subplots(dpi=300)
    #df = df.set_index(df['M'])
    #x=df.loc['1990-01-31':'2000-12-31']
    x=df.index
    ax.plot(x, df[var1], c='xkcd:royal blue', label='nitrxte')
    ax.set_title(stationcode.upper())
    ax.set_xlabel('Time')
    ax.set_ylabel('Seasonal nitrxte trend')
    ax2=ax.twinx()
    ax2.plot(x, df[var2], c='xkcd:green', label='phosphate')
    ax2.set_ylabel('Seasonal phosphate trend')
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 1.02))
    #plt.show()
    fig.savefig("figures/seasonal/" + stationcode + "_nitrxte_vs_phosphate"  + ".png")
