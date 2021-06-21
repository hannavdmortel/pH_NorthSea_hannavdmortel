import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

stationcodes = [
    "ZOUTKPLZGT",
    "WALCRN70",
    "WALCRN20",
    "TERSLG50",
    "TERSLG175",
    "TERSLG135",
    "TERSLG10",
    "TERSLG100",
    "SCHOUWN10",
    "NOORDWK70",
    "NOORDWK20",
    "NOORDWK10",
    "GOERE6",
    "DOOVBWT",
    "DANTZGT"]
#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "phosphate_trend"
var2 = "tn_trend"
var3 = "chlorophyll_trend"
var4 = "pH_trend"

startyear = '2010'
endyear = '2020'

for stationcode in northsea.station_code:
#for stationcode in stationcodes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()

    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    x=df[L]
    fig, ax = plt.subplots(3, dpi=300)
    ax[0].plot(x.index, x[var1], c='xkcd:royal blue', label='Phosphate')
    ax[0].set_ylabel('Phosphate')
    ax2 = ax[0].twinx()
    ax2.plot(x.index, x[var2], c='xkcd:electric pink', label='TN')
    ax2.set_ylabel('TN')
    ax[1].plot(x.index, x[var4], c='crimson', label ='pH')
    ax[2].plot(x.index, x[var3], c='xkcd:green', label='Chlorophyll')
    #ax[1].set_ylabel('Chlorophyll')
    #ax[2].set_ylabel('pH')
    ax[2].set_xlabel('Years')
    
    ax[0].tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)
    ax[1].tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)
    ax[0].grid(axis='x')
    ax[0].set_xlim([startyear, endyear])
    ax[1].grid(axis='x')
    ax[1].set_xlim([startyear, endyear])
    ax[2].grid(axis='x')
    ax[2].set_xlim([startyear, endyear])
    fig.suptitle(stationcode.upper() + ' ' + startyear + '-' + endyear)
    fig.legend(loc='upper right', bbox_to_anchor=(1.15, 0.6))
    fig.savefig("figures/trend/2010-2020/" + stationcode + '_' + startyear + '-' + endyear +"_nutrients_chlorophyll_pH"  + ".png",
                bbox_inches='tight')
