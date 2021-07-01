import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import interpolate, stats
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

x=pd.DataFrame()

locations = {
    1: 'WaddenSea',
    2: 'Nearshore1',
    3: 'Nearshore2',
    4: 'Offshore'}

#Choose years
startyear = '2010'
endyear = '2020'

#Choose variables for Redfield calculation
P = 'phosphate'
N = 'DIN'

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
    

#Choose variables
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "phosphate"
var2 = "DIN"
var3 = "chlorophyll"
var4 = "pH"
var5 = "spm"

#%%
#Select specific stations listed above:
for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x = x.append(dfL, ignore_index=False)

#Add DIN column
x['DIN'] = x.nitrxte + x.ammonia

#%%
#Create figure
fig, axs = plt.subplots(2, 2, figsize=(5,4), dpi=300)
ax2 = axs[0,0].twinx()

#Remove outliers
L = ~np.isnan(x[var1]) & ~np.isnan(x[var2])
xL = x[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL = xL[L2]

#Monthly averages
months = xL.index.month
monthly_avg_var1 = xL.groupby(months)[var1].mean()
monthly_avg_var2 = xL.groupby(months)[var2].mean()
monthly_avg_var3 = xL.groupby(months)[var3].mean()
monthly_avg_var4 = xL.groupby(months)[var4].mean()
monthly_avg_var5 = xL.groupby(months)[var5].mean()

#Interpolation for smooth line
months_interp = np.linspace(np.min(months), np.max(months), num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_var1.index, monthly_avg_var1)
var1_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_var2.index, monthly_avg_var2)
var2_pchip = interp_pchip2(months_interp)
interp_pchip3 = interpolate.PchipInterpolator(monthly_avg_var3.index, monthly_avg_var3)
var3_pchip = interp_pchip3(months_interp)
interp_pchip4 = interpolate.PchipInterpolator(monthly_avg_var4.index, monthly_avg_var4)
var4_pchip = interp_pchip4(months_interp)
interp_pchip5 = interpolate.PchipInterpolator(monthly_avg_var5.index, monthly_avg_var5)
var5_pchip = interp_pchip5(months_interp)

#Scatter all raw data minus outliers
# axs[0,0].scatter(months, xL[var1], 
#            alpha=0.1, edgecolor='none', c='royalblue', s=15)
# ax2.scatter(months, xL[var2], 
#            alpha=0.1, edgecolor='none', c='xkcd:pink', s=15)
# axs[0,1].scatter(months, xL[var3], 
#            alpha=0.1, edgecolor='none', c='xkcd:light orange', s=15)
# axs[1,0].scatter(months, xL[var4], 
#            alpha=0.1, edgecolor='none', c='xkcd:teal', s=15)
# axs[1,1].scatter(months, xL[var5], 
#            alpha=0.1, edgecolor='none', c='xkcd:teal green', s=15)

#Plot interpolated trends
axs[0,0].plot(months_interp, var1_pchip, 
        zorder=10, c='xkcd:light orange', linewidth=2)
ax2.plot(months_interp, var2_pchip, 
        zorder=10, c='royalblue', linewidth=2)
axs[0,1].plot(months_interp, var3_pchip, 
        zorder=10, c='xkcd:teal green', linewidth=2)
axs[1,0].plot(months_interp, var4_pchip, 
        zorder=10, c='xkcd:pink', linewidth=2)
axs[1,1].plot(months_interp, var5_pchip, 
        zorder=10, c='xkcd:coral', linewidth=2)

#Formatting
axs[0,0].set_ylabel('[P]', fontsize=8)
ax2.set_ylabel('[N]', fontsize=8)
axs[0,0].tick_params(axis='y', labelsize=7)
ax2.tick_params(axis='y', labelsize=7)
axs[0,0].set_xticks(np.arange(0, 11, 2))
axs[0,0].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)

axs[0,1].set_ylabel('Chlorophyll', fontsize=8)
axs[0,1].tick_params(axis='y', labelsize=7)
axs[0,1].set_xticks(np.arange(0, 11, 2))
axs[0,1].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[0,1].yaxis.set_label_position("right")
axs[0,1].yaxis.tick_right()

axs[1,0].set_ylabel('pH', fontsize=8)
axs[1,0].tick_params(axis='y', labelsize=7)
axs[1,0].set_xticks(np.arange(0, 11, 2))
axs[1,0].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)

axs[1,1].set_ylabel('[SPM]', fontsize=8)
axs[1,1].tick_params(axis='y', labelsize=7)
axs[1,1].set_xticks(np.arange(0, 11, 2))
axs[1,1].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[1,1].yaxis.set_label_position("right")
axs[1,1].yaxis.tick_right()

#Removing nan & outliers for RR calculation
L_RR = ~np.isnan(x[P]) & ~np.isnan(x[N])
xRR = x[L_RR]
xRR['z_score_P'] = stats.zscore(xRR[P])
xRR['z_score_N'] = stats.zscore(xRR[N])
L2_RR = (xRR['z_score_P'].abs()<=3) & (xRR['z_score_N'].abs()<=3)
xL_RR = xRR[L2_RR]

#Plotting RR on top
RR = ((xL_RR[N]/xL_RR[P]).mean())
axs[0,0].set_title('DIN:DIP = %.0f' % RR, fontsize=8, loc='right', pad=1)

#Formatting
fig.suptitle('Monthly averages Wadden Sea '+ startyear + '-' + endyear, fontsize=11, x=0.5, y=0.96)
fig.tight_layout()

#Grid
axs[0,0].set_xlim(1,12)
axs[0,0].minorticks_on()
axs[0,0].grid(axis='both')
axs[0,0].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')

axs[0,1].set_xlim(1,12)
axs[0,1].minorticks_on()
axs[0,1].grid(axis='both')
axs[0,1].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')     

axs[1,0].set_xlim(1,12)
axs[1,0].minorticks_on()
axs[1,0].grid(axis='both')
axs[1,0].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')

axs[1,1].set_xlim(1,12)
axs[1,1].minorticks_on()
axs[1,1].grid(axis='both')
axs[1,1].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')

#Create legend
patch1 = mpatches.Patch(color='xkcd:light orange', label='DIP')
patch2 = mpatches.Patch(color='royalblue', label='DIN')
patch3 = mpatches.Patch(color='xkcd:teal green', label= 'Chlorophyll')
patch4 = mpatches.Patch(color='xkcd:pink', label= 'pH')
patch5 = mpatches.Patch(color='xkcd:coral', label= 'SPM')

plt.legend(handles=[patch1, patch2, patch3, patch4, patch5], 
           bbox_to_anchor=(2.5, -1.4), fontsize=8, ncol=5)

fig.savefig("figures/seasonal/"+ location + "_" + startyear + "-" + endyear + ".png",
            bbox_inches='tight')
