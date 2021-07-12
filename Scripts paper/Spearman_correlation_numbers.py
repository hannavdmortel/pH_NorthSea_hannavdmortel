import numpy as np
import pyarrow.parquet as pq
import pandas as pd
from scipy.stats.stats import spearmanr

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "pH_seasonal"
var2 = "spm_seasonal"

station = []
correlation = []
corrdict = {}

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()

    L = ~np.isnan(df[var1]) & ~np.isnan(df[var2])    
    _var1 = df[var1][L]
    _var2 = df[var2][L]
    
    corr, _ = spearmanr(_var1, _var2)
    corr = "%.1f" % corr
    
    station.append(stationcode)
    correlation.append(corr)

for i in range(60):
    corrdict[station[i]] = correlation[i]
    
data = list(corrdict. items())
corr_array = np.array(data)

