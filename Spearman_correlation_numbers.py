import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
from scipy.stats.stats import spearmanr

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "pH_seasonal"
var2 = "nitrxte_seasonal"

station = []
correlation = []
corrdict = {}

for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()

    L = ~np.isnan(df[var1]) & ~np.isnan(df[var2])    
    pH = df[var1][L]
    P = df[var2][L]
    
    corr, _ = spearmanr(pH, P)
    corr = "%.1f" % corr
    #ax.text(3.5, 0, 'Spearmans correlation: %.3f' % corr)

    station.append(stationcode)
    correlation.append(corr)
    #L = (~np.isnan(correlation))
    #correlation = [int(float(i)) for i in correlation]
    

for i in range(60):
    corrdict[station[i]] = correlation[i]

