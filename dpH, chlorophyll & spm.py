import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#CALCULATE dPH
for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    
    #RIGHT NOW THIS GOES THROUGH ALL DATA
    #NEED TO SELECT min & max FOR ONE YEAR USING A LOGICAL
    L_year = (df.datenum > mdates.date2num('1977-01-01')) & (df.datenum < mdates.date2num('1978-01-01'))
    df_L_year = df[L] #THIS DOESNT WORK
    #Calculate min and max pH
    min_pH = df_L_year.pH.min()
    max_pH = df_L_year.pH.max()
    
    #Interpolate between these two values
    dpH = np.linspace(min_pH, max_pH, num = 500)
    
    #Create logical to select time spring bloom (from min_pH to max_pH)
    L_start = (df.pH == min_pH)
    L_peak = (df.pH == max_pH)
    
    #Selecting datenum using logical
    start_spring_bloom = df.datenum[L_start]
    peak_spring_bloom = df.datenum[L_peak]
    
    #Plotting against spm
    fig, ax = plt.subplots(dpi=300)
    ax.scatter(dpH, df.spm., s=20, c='xkcd:red')
    
#     ax.scatter(df[var1], df[var2]., s=20, c='xkcd:red')
#     ax.set_title(stationcode.upper())
#     ax.set_xlabel(var1)
#     ax.set_ylabel(var2)
