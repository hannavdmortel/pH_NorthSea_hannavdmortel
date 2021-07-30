import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import interpolate, stats
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.ticker import (AutoMinorLocator)

fpath = "C:/Users/hanna/Documents/GitHub/"

x=pd.DataFrame()

locations = {
    1: 'WaddenSea',
    2: 'Nearshore',
    3: 'Intermediate',
    4: 'Offshore'}

#Choose years
startyear = '1975'
endyear = '1985'

#Choose location
location = locations[1]
    
#Wadden Sea
if location == 'WaddenSea':
    station_codes = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

#Nearshore <20km
if location == 'Nearshore':
    station_codes = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]

#Nearshore 20-50 km
if location == 'Intermediate':
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
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
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

#Remove outliers
L = ~np.isnan(x[var1]) & ~np.isnan(x[var2])
xL = x[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL = xL[L2]

#For adding extra Jan on x-axis
xL['months13'] = xL.index.month.to_numpy()
xL_Jan = xL[xL.index.month == 1].copy()
xL_Jan['months13'] = 13
xL = xL.append(xL_Jan)

#Monthly averages
monthly_avg_var1 = xL.groupby('months13')[var1].mean()
monthly_avg_var2 = xL.groupby('months13')[var2].mean()
monthly_avg_var3 = xL.groupby('months13')[var3].mean()
monthly_avg_var4 = xL.groupby('months13')[var4].mean()
monthly_avg_var5 = xL.groupby('months13')[var5].mean()

#Interpolation for smooth line
months_interp = np.linspace(1, 13, num=100)
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

#Calculating RR of reproduction
RR = (var2_pchip.max()-var2_pchip.min())/(var1_pchip.max()-var1_pchip.min())

#Plotting RR on top
axs[0,0].set_title('RR = %.0f' % RR, fontsize=8, loc='right', pad=1)

#Plot interpolated trends
axs[0,0].plot(months_interp, var1_pchip*RR, 
        zorder=10, c='xkcd:light orange', linewidth=2)
axs[0,0].plot(months_interp, var2_pchip, 
        zorder=10, c='royalblue', linewidth=2)
axs[0,1].plot(months_interp, var3_pchip, 
        zorder=10, c='xkcd:teal green', linewidth=2)
axs[1,0].plot(months_interp, var4_pchip, 
        zorder=10, c='xkcd:pink', linewidth=2)
axs[1,1].plot(months_interp, var5_pchip, 
        zorder=10, c='xkcd:coral', linewidth=2)

#Formatting
axs[0,0].set_ylabel('Nutrients (\u03BCmol $\mathregular{L^{-1}}$)', fontsize=8)
axs[0,0].set_ylim(bottom=0)
axs[0,0].tick_params(axis='y', labelsize=7)

axs[0,0].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[0,0].set_xticks(np.arange(0, 13, 2))
axs[0,0].set_xticklabels(['', 'Feb', 'April', 'June', 'Aug', 'Oct', 'Dec'], fontsize=7)

axs[0,1].set_ylabel('Chl (\u03BC$\mathregular{g^{-L}}$)', fontsize=8)
axs[0,1].tick_params(axis='y', labelsize=7)
axs[0,1].set_ylim(bottom=0)
axs[0,1].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[0,1].set_xticks(np.arange(0, 13, 2))
axs[0,1].set_xticklabels(['', 'Feb', 'April', 'June', 'Aug', 'Oct', 'Dec'], fontsize=7)
axs[0,1].yaxis.set_label_position("right")
axs[0,1].yaxis.tick_right()

axs[1,0].set_ylabel('pH', fontsize=8)
axs[1,0].tick_params(axis='y', labelsize=7)
axs[1,0].set_ylim(bottom=7.71, top=8.5)
axs[1,0].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[1,0].set_xticks(np.arange(0, 13, 2))
axs[1,0].set_xticklabels(['', 'Feb', 'April', 'June', 'Aug', 'Oct', 'Dec'], fontsize=7)

axs[1,1].set_ylabel('SPM ($\mathregular{mg^{-L}}$)', fontsize=8)
axs[1,1].tick_params(axis='y', labelsize=7)
axs[1,1].set_ylim(bottom=0)
axs[1,1].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[1,1].set_xticks(np.arange(0, 13, 2))
axs[1,1].set_xticklabels(['', 'Feb', 'April', 'June', 'Aug', 'Oct', 'Dec'], fontsize=7)
axs[1,1].yaxis.set_label_position("right")
axs[1,1].yaxis.tick_right()

#Formatting
fig.suptitle('Monthly averages Offshore (≥70 km) '+ startyear + '-' + endyear, fontsize=11, x=0.5, y=0.96)
fig.tight_layout()

#Grid
axs[0,0].set_xlim(1,13)
axs[0,0].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[0,0].grid(axis='x')
axs[0,0].grid(axis='x', which='minor', linestyle=':', linewidth='0.5')

axs[0,1].set_xlim(1,13)
axs[0,1].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[0,1].grid(axis='x')
axs[0,1].grid(axis='x', which='minor', linestyle=':', linewidth='0.5')     

axs[1,0].set_xlim(1,13)
axs[1,0].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[1,0].grid(axis='x')
axs[1,0].grid(axis='x', which='minor', linestyle=':', linewidth='0.5')

axs[1,1].set_xlim(1,13)
axs[1,1].xaxis.set_minor_locator(AutoMinorLocator(2))
axs[1,1].grid(axis='x')
axs[1,1].grid(axis='x', which='minor', linestyle=':', linewidth='0.5')

#Create legend
patch1 = mpatches.Patch(color='xkcd:light orange', label='DIP × RR')
patch2 = mpatches.Patch(color='royalblue', label='DIN')
patch3 = mpatches.Patch(color='xkcd:teal green', label= 'Chlorophyll')
patch4 = mpatches.Patch(color='xkcd:pink', label= 'pH')
patch5 = mpatches.Patch(color='xkcd:coral', label= 'SPM')

plt.legend(handles=[patch1, patch2, patch3, patch4, patch5], 
           bbox_to_anchor=(1.16, -0.2), fontsize=8, ncol=5)

fig.savefig("figures/seasonal/"+ location + "_" + startyear + "-" + endyear + ".png",
            bbox_inches='tight')
