import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#On to offshore
stationcodes = [
    "SCHOUWN1",
    "SCHOUWN4",
    "SCHOUWN10",
    "SCHOUWN20",
    "SCHOUWN30",
    "SCHOUWN50",
    "SCHOUWN70"]

#Over time
# stationcodes = [    
#     "ZOUTKPLZGT",
#     "WALCRN20",
#     "NOORDWK10"]    

#Choose variables
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "phosphate_seasonal"
var2 = "tn_seasonal"
var3 = "chlorophyll_seasonal"
var4 = "pH_seasonal"

#Choose years
startyear = '1976'
endyear = '1983'

#Choose variables for Redfield calculation
P = 'phosphate'
N = 'nitrate'
    
#%%

#Select all stations:
#for stationcode in northsea.station_code:
    
#Select specific stations listed above:
for stationcode in stationcodes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    x=df[L]
    fig, ax = plt.subplots(3, dpi=300)
    ax2 = ax[0].twinx()
    ax2.plot(x.datetime, x[var2], c='xkcd:bluish grey', label='TN')
    ax2.set_ylabel('TN')
    ax[0].set_ylabel('Phosphate')
    ax[0].plot(x.datetime, x[var1], c='xkcd:pink purple', label='Phosphate')
    ax[1].plot(x.datetime, x[var4], c='royalblue')
    ax[2].plot(x.datetime, x[var3], c='xkcd:teal green')
    ax[1].set_ylabel('pH')
    ax[2].set_ylabel('Chlorophyll')
    ax[2].set_xlabel('Years')
    
    #Formatting
    for i in [0, 1]:
        ax[i].tick_params(
            axis='x',
            which='both',
            bottom=False,
            top=False,
            labelbottom=False)
    for i in [0, 1, 2]:
        ax[i].xaxis.get_ticklocs(minor=True)
        ax[i].minorticks_on()
        ax[i].grid(axis='both')
        ax[i].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')
        ax[i].set_xlim([datetime(1976, 1, 1), datetime(1983, 1, 1)])
    
    #Removing outliers for RR calculation
    x['z_score_P'] = stats.zscore(x[P])
    x['z_score_N'] = stats.zscore(x[N])
    L2 = (x['z_score_P'].abs()<=3) & (x['z_score_N'].abs()<=3)
    xL = x[L2]

    #Plotting RR on top
    RR = ((xL.nitrate/xL.phosphate).mean())
    ax[1].set_title('N:P = %.2f' % RR, fontsize=8, loc='right', pad=1)
    
    #Formatting
    fig.suptitle(stationcode.upper() + ' ' + startyear + '-' + endyear)
    fig.legend(loc='upper right', bbox_to_anchor=(0.96, 1.03))
    fig.savefig("figures/seasonal/1976-1983/" + stationcode + '_' + startyear + '-' + endyear +"_nutrients_chlorophyll_pH"  + ".png",
                bbox_inches='tight')
