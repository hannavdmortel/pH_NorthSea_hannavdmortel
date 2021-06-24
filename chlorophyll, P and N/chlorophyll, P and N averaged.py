import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

x=pd.DataFrame()

locations = {
    1: 'WaddenSea',
    2: 'Nearshore1',
    3: 'Nearshore2',
    4: 'Offshore'}

#Choose years
startyear = '1975'
endyear = '1985'

#Choose variables for Redfield calculation
P = 'tp'
N = 'tn'

#Choose location
location = locations[4]
    
#Wadden Sea
if location == 'WaddenSea':
    station_codes = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

#Nearshore <20km
if location == 'Nearshore1':
    station_codes = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]

#Nearshore 20-50 km
if location == 'Nearshore2':
    station_codes = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]

#Offshore 70+ km
if location == 'Offshore':
    station_codes = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]
    

#Choose variables
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "phosphate_seasonal"
var2 = "tn_seasonal"
var3 = "chlorophyll_seasonal"
var4 = "pH_seasonal"

    
#%%
#Select specific stations listed above:
for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x = x.append(dfL, ignore_index=True)

#%% Grouped per year for averages

#Plot average trend
grouped = x.groupby('datetime').mean()

#Add column and make sure column is in datetime format
grouped['dates'] = mdates.num2date(grouped.datenum)
grouped['dates'] = pd.to_datetime(grouped.dates)

#%%
fig, ax = plt.subplots(3, dpi=300)
ax[0].scatter(x.datetime, x[var1], c='xkcd:pink purple', alpha=0.2, s=10, edgecolor='none')
ax[0].plot(grouped.dates, grouped[var1], c='xkcd:pink purple', label='Phosphate')
ax[0].set_ylabel('Phosphate')

ax2 = ax[0].twinx()
ax2.scatter(x.datetime, x[var2], c='xkcd:bluish grey', alpha=0.2, s=10, edgecolor='none')
ax2.plot(grouped.dates, grouped[var2], c='xkcd:bluish grey', label='TN')
ax2.set_ylabel('TN')

ax[1].scatter(x.datetime, x[var4], c='royalblue', alpha=0.2, s=10, edgecolor='none')
ax[1].plot(grouped.dates, grouped[var4], c='royalblue')
ax[1].set_ylabel('pH')

ax[2].scatter(x.datetime, x[var3], c='xkcd:teal green', alpha=0.2, s=10, edgecolor='none')
ax[2].plot(grouped.dates, grouped[var3], c='xkcd:teal green')
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
    ax[i].set_xlim([datetime(int(startyear), 1, 1), datetime(int(endyear), 1, 1)])

#Removing nan & outliers for RR calculation
L_RR = ~np.isnan(x[P]) & ~np.isnan(x[N])
xRR = x[L_RR]
xRR['z_score_P'] = stats.zscore(xRR[P])
xRR['z_score_N'] = stats.zscore(xRR[N])
L2 = (xRR['z_score_P'].abs()<=3) & (xRR['z_score_N'].abs()<=3)
xL = xRR[L2]

#Plotting RR on top
RR = ((xL.nitrate/xL.phosphate).mean())
#Formatting
fig.suptitle(location + ' ' + startyear + '-' + endyear)
fig.legend(loc='upper right', bbox_to_anchor=(0.96, 1.03))
fig.savefig("figures/seasonal/"+ location + "_" + startyear + "-" + endyear + "_nutrients_chlorophyll_pH"  + ".png",
            bbox_inches='tight')
