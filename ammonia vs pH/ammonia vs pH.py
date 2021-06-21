import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "pH_trend"
var2 = "ammonia_trend"

startyear = '1975'
endyear = '1987'

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()

    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    x=df[L]
    fig, ax = plt.subplots(dpi=300)
    ax.plot(x.index, x[var1], c='crimson', label='pH')
    ax.set_ylabel('pH')
    ax2 = ax.twinx()
    ax2.plot(x.index, x[var2], c='mediumorchid', label='Ammonia')
    ax2.set_ylabel('Ammonia')
    ax.set_xlabel('Years')
    
    ax.grid(axis='x')
    ax.set_xlim([startyear, endyear])
    fig.suptitle(stationcode.upper() + ' ' + startyear + '-' + endyear)
    fig.legend(loc='upper right', bbox_to_anchor=(1.15, 0.6))
    fig.savefig("figures/trend/1975-1987/" + stationcode + '_' + startyear + '-' + endyear +"_nutrients_chlorophyll_pH"  + ".png",
                bbox_inches='tight')
