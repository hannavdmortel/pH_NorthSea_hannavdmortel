import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats
from scipy.stats.stats import pearsonr, spearmanr
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#%% Create datetime column for each station file
for stationcode in northsea.station_code:    
    #Read station specific files
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    
    #Create datetime column
    df['datetime'] = mdates.num2date(df.datenum)
    
#%% Add data to dict
my_dict = {"Name":[],"Address":[],"Age":[]};

my_dict["Name"].append("Guru")
my_dict["Address"].append("Mumbai")
my_dict["Age"].append(30)

pH_dict ={"Date":[], "pH_trend":[]}

pH_dict["Date"].append()

pH_dict = {pH_trend:  
           for var in ['Y89(LR)', 'Zr90(LR)']}    
pH_dict.append{"Date": df['datetime'], "pH_trend": df['pH_trend']for var in ['Y89(LR)', 'Zr90(LR)']}    
#%% EVERYTHING BELOW IS OLD

#Create dataframe

pH_dict ={"Date":[], "pH_trend":[]}

#Loop through station data files
#for stationcode in stationcodes:
df=[]
for stationcode in northsea.station_code:    
    #Read station specific files
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    
    
    
    #Create datetime column
    df['datetime'] = mdates.num2date(df.datenum)
    df['station_code'] = stationcode
    
pH_dict['Date'].append(df.datetime[:])
pH_dict['pH_trend'].append(df.pH_trend[:])
    
    #pH_dict.append{"Date": df['datetime'], "pH_trend": df['pH_trend']}  

    # station_code = df['station_code']
    # dates = df['datetime']
    # pH_trend = df['pH_trend']
    
    #data.append((df.station_code, df.datetime, df.pH_trend))
    
#df2 = pd.DataFrame(datetime, pH_trend, columns = ['datetime', 'pH_trend'])
#Take average of all trend data per year???????
#Have series within a list... 
fig, ax = plt.subplots(dpi=300)
ax.scatter(pH_dict['Date'], pH_dict['pH_trend'])        


#%%
    #Loop through years
    for year in range(min_year, max_year):
        #Select year
        L_year = (df.datenum > mdates.datestr2num('{}-01-01'.format(year))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(year+1)))
        df_L_year = df[L_year]
        
        #Find average pH
        pH = df_L_year.pH_trend.mean()
        
        #Compile data into list
        data.append((stationcode, year, pH))

#Compile all data into one dataframe
df2 = pd.DataFrame(data, columns = ['station', 'year', 'pH_trend'])

#Scatter all data
fig, ax = plt.subplots(dpi=300)
ax.scatter(df2.year, df2.pH_trend, s=4, c='grey', alpha=0.8)

#Average per year
grouped_year = df2.groupby(pd.Grouper(key = 'year')).mean()

#Interpolate
interp_pchip = interpolate.PchipInterpolator(grouped_year.index, grouped_year.pH_trend)
year_interp = np.linspace(np.min(grouped_year.index), np.max(grouped_year.index), num = 500)
pH_pchip = interp_pchip(year_interp)
ax.plot(year_interp, pH_pchip, c='xkcd:royal blue')

fig.savefig("pH_trend/figures/average_X13")
#ax.plot(grouped_year.index, grouped_year.pH_trend, c='red')