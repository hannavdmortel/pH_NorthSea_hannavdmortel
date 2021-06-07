import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "chlorophyll_seasonal"
var2 = "phosphate_seasonal"

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    fig, ax = plt.subplots(dpi=300)
    
    ax.scatter(df[var1], df[var2], s=20, c='xkcd:red')
    ax.set_title(stationcode.upper())
    ax.set_xlabel(var1)
    ax.set_ylabel(var2)
