import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import interpolate, stats
import pandas as pd
import matplotlib.dates as mdates

x=pd.DataFrame()

locations = {
    1: 'WaddenSea',
    2: 'Nearshore1',
    3: 'Nearshore2',
    4: 'Offshore'}

#Choose location
location = locations[1]

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
    
#Choose time range
startyear = '1973'
endyear = '2019'

#Choose variables
#(+ _irregular, _seasonal or _trend)
var1 = "phosphate_seasonal"
var2 = "tp_seasonal"

#%%
#Select specific stations listed above:
for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x = x.append(dfL, ignore_index=False)
    
#%% 
#Remove outliers
L = ~np.isnan(x['phosphate']) & ~np.isnan(x['tp'])
xL = x[L]
xL['z_score_phosphate'] = stats.zscore(xL['phosphate'])
xL['z_score_tp'] = stats.zscore(xL['tp'])
L2 = (xL['z_score_phosphate'].abs()<=2) & (xL['z_score_tp'].abs()<=2)
xL = xL[L2]

#Monthly averages P and TP
months = xL.index.month
monthly_avg_phosphate = xL.groupby(months).phosphate.mean()
monthly_avg_tp = xL.groupby(months).tp.mean()

#Interpolation for smooth line
months_interp = np.linspace(np.min(months), np.max(months), num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_phosphate.index, monthly_avg_phosphate)
phosphate_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_tp.index, monthly_avg_tp)
tp_pchip = interp_pchip2(months_interp)

#Plot
fig, ax = plt.subplots(4, figsize=(4,5), dpi=300)
#Scatter all raw data minus outliers
ax.scatter(months, xL.phosphate, 
           alpha=0.1, edgecolor='none', c='teal')
ax.scatter(months, xL.tp, 
           alpha=0.1, edgecolor='none', c='pink')

#Plot interpolated phosphate and tp trend
ax.plot(months_interp, phosphate_pchip, 
        label='Phosphate', zorder=10, c='teal', linewidth=3)
ax.plot(months_interp, tp_pchip, 
        label='TP', zorder=10, c='pink', linewidth=3)

#Formatting
ax.set_ylabel('P concentrations', fontsize=8)
#ax.set_ylim([0, 1.3])
ax.tick_params(axis='y', labelsize=7)
ax.set_xticklabels(['Jan', 'Feb', 'April', 'June', 'Aug', 'Oct', 'Dec'], fontsize=7)
ax.set_title('Monthly averaged phosphate and TP for Wadden Sea', fontsize=9)
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.88), fontsize=8)

#Saving
#plt.savefig("figures/phosphate_tp_"+ location + ".png", bbox_inches='tight')
