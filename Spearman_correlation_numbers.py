import numpy as np
import pyarrow.parquet as pq
import pandas as pd
from scipy.stats.stats import spearmanr
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "chlorophyll_seasonal"
var2 = "spm_seasonal"

station = []
correlation = []
corrdict = {}

startyear='1973'
endyear='2020'

#With Wadden
station_codes = northsea.station_code

#Without Wadden
# station_codes = [
#     "CALLOG4", 
#     "CALLOG10", 
#     "EGMAZE4", 
#     "EGMAZE10", 
#     "GOERE6", 
#     "GOERE10", 
#     "NOORDWK4", 
#     "NOORDWK10", 
#     "ROTTMPT20", 
#     "SCHOUWN1", 
#     "SCHOUWN4", 
#     "SCHOUWN10", 
#     "TERSLG10", 
#     "WALCRN4", 
#     "WALCRN10",
#     "CALLOG30", 
#     "CALLOG50", 
#     "EGMAZE20", 
#     "EGMAZE30", 
#     "EGMAZE50", 
#     "GOERE20", 
#     "GOERE30", 
#     "GOERE50", 
#     "NOORDWK20", 
#     "NOORDWK30", 
#     "NOORDWK50", 
#     "ROTTMPT30", 
#     "ROTTMPT50", 
#     "SCHOUWN20", 
#     "SCHOUWN30", 
#     "TERSLG30",  
#     "TERSLG50", 
#     "WALCRN20", 
#     "WALCRN30", 
#     "WALCRN50",
#     "CALLOG70", 
#     "EGMAZE70", 
#     "GOERE70", 
#     "NOORDWK70", 
#     "ROTTMPT70", 
#     "ROTTMPT100", 
#     "SCHOUWN50", 
#     "SCHOUWN70", 
#     "TERHDE70", 
#     "TERSLG70", 
#     "TERSLG100", 
#     "TERSLG135", 
#     "TERSLG175",
#     "WALCRN70"
#     ]

for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    L1 = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    df=df[L1]
    L2 = ~np.isnan(df[var1]) & ~np.isnan(df[var2])    
    _var1 = df[var1][L2]
    _var2 = df[var2][L2]
    
    corr, _ = spearmanr(_var1, _var2)
    corr = "%.1f" % corr
    
    station.append(stationcode)
    correlation.append(corr)

for i in range(len(station_codes)):
    corrdict[station[i]] = correlation[i]
    
data = list(corrdict. items())
corr_array = np.array(data)

