import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import interpolate, stats
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.patches as mpatches


x1=pd.DataFrame()
x2=pd.DataFrame()
x3=pd.DataFrame()
x4=pd.DataFrame()

fig, axs = plt.subplots(2, 2, figsize=(6,7), dpi=300)

locations = {
    1: 'WaddenSea',
    2: 'Nearshore',
    3: 'Intermediate',
    4: 'Offshore'}

#Choose time range
startyear = '1973'
endyear = '2019'

#Choose variables
#(+ _irregular, _seasonal or _trend)
var1 = "phosphate"
var2 = "tp"

# fpath = "C:/Users/hanna/Documents/GitHub/"
fpath = '/home/matthew/github/'

#%% Wadden Sea
#Choose location
location = locations[1]

if location == 'WaddenSea':
    station_codes = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

for stationcode in station_codes:
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x1 = x1.append(dfL, ignore_index=False)

#Remove outliers
L = ~np.isnan(x1[var1]) & ~np.isnan(x1[var2])
xL = x1[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL = xL[L2]

#For adding extra Jan on x-axis
L_Jan = (xL.index.month == 1)
xL1 = xL.append(xL[L_Jan])

# #Create months list
months = xL1.index.month
L3 = months > len(xL)
Jan_13 = months[L3] 

#Monthly averages
monthly_avg_var1 = xL1.groupby(xL1.index.month)[var1].mean()
monthly_avg_var2 = xL1.groupby(xL1.index.month)[var2].mean()
monthly_avg_pH = xL1.groupby(xL1.index.month)['pH'].mean()

#Interpolation for smooth line
months_interp = np.linspace(1, 12, num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_var1.index, monthly_avg_var1)
var1_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_var2.index, monthly_avg_var2)
var2_pchip = interp_pchip2(months_interp)
interp_pchip3 = interpolate.PchipInterpolator(monthly_avg_pH.index, monthly_avg_pH)
pH_pchip = interp_pchip3(months_interp)

#Scatter all raw data minus outliers, with jitter
sns.regplot(x=months, y=xL1[var1], ax=axs[0,0], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:teal',
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)
sns.regplot(x=months, y=xL1[var2], ax=axs[0,0], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:light orange', 
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)

#Plot interpolated phosphate and tp trend
axs[0,0].plot(months_interp, var1_pchip, 
        label='Phosphate', zorder=10, c='xkcd:teal', linewidth=2)
axs[0,0].plot(months_interp, var2_pchip, 
        label='TP', zorder=10, c='xkcd:light orange', linewidth=2)
axs[0,0].plot(months_interp, (var2_pchip-var1_pchip), 
              c='xkcd:coral', linewidth=2, zorder=10)

#Plot pH
ax2 = axs[0,0].twinx()
ax2.plot(months_interp, pH_pchip, 
        label='pH', zorder=5, c='grey', linewidth=2, linestyle='--')

#Formatting
axs[0,0].set_ylabel('P (\u03BCmol $\mathregular{L^{-1}}$)', fontsize=8)
axs[0,0].set_ylim(bottom=0, top=6)
ax2.set_ylim(7.8, 8.45)
ax2.yaxis.set_major_formatter(plt.NullFormatter())
axs[0,0].tick_params(axis='y', labelsize=7)
axs[0,0].set_xticks(np.arange(0, 11, 2))
axs[0,0].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[0,0].set_title('Wadden Sea', fontsize=10)

#%% Nearshore <20km
location = locations[2]

if location == 'Nearshore':
    station_codes = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]

for stationcode in station_codes:
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x2 = x2.append(dfL, ignore_index=False)

#Remove outliers
L = ~np.isnan(x2[var1]) & ~np.isnan(x2[var2])
xL = x2[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL = xL[L2]

#Monthly averages
months = xL.index.month
monthly_avg_var1 = xL.groupby(months)[var1].mean()
monthly_avg_var2 = xL.groupby(months)[var2].mean()
monthly_avg_pH = xL.groupby(months)['pH'].mean()

#Interpolation for smooth line
months_interp = np.linspace(np.min(months), np.max(months), num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_var1.index, monthly_avg_var1)
var1_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_var2.index, monthly_avg_var2)
var2_pchip = interp_pchip2(months_interp)
interp_pchip3 = interpolate.PchipInterpolator(monthly_avg_pH.index, monthly_avg_pH)
pH_pchip = interp_pchip3(months_interp)

#Scatter all raw data minus outliers, with jitter
sns.regplot(x=months, y=xL[var1], ax=axs[0,1], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:teal',
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)
sns.regplot(x=months, y=xL[var2], ax=axs[0,1], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:light orange', 
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)

#Plot interpolated phosphate and tp trend
axs[0,1].plot(months_interp, var1_pchip, 
        label='Phosphate', zorder=10, c='xkcd:teal', linewidth=2)
axs[0,1].plot(months_interp, var2_pchip, 
        label='TP', zorder=10, c='xkcd:light orange', linewidth=2)
axs[0,1].plot(months_interp, (var2_pchip-var1_pchip), 
              c='xkcd:coral', linewidth=2, zorder=10)

#Plot pH
ax2 = axs[0,1].twinx()
ax2.plot(months_interp, pH_pchip, 
        label='pH', zorder=5, c='grey', linewidth=2, linestyle='--')

#Formatting
axs[0,1].set_ylim(bottom=0, top=3.4)
ax2.set_ylim(7.8, 8.45)
ax2.set_ylabel('pH', fontsize=8)
ax2.tick_params(axis='y', labelsize=7)

axs[0,1].tick_params(axis='y', labelsize=7)
axs[0,1].set_xticks(np.arange(0, 11, 2))
axs[0,1].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[0,1].set_title('Nearshore (<20 km)', fontsize=10)

#%% Intermediate 20-50 km
location = locations[3]

if location == 'Intermediate':
    station_codes = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]

for stationcode in station_codes:
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df['datetime'] = mdates.num2date(df.datenum)
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x3 = x3.append(dfL, ignore_index=False)

#Remove outliers
L = ~np.isnan(x3[var1]) & ~np.isnan(x3[var2])
xL = x3[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL = xL[L2]

#Monthly averages
months = xL.index.month
monthly_avg_var1 = xL.groupby(months)[var1].mean()
monthly_avg_var2 = xL.groupby(months)[var2].mean()
monthly_avg_pH = xL.groupby(months)['pH'].mean()

#Interpolation for smooth line
months_interp = np.linspace(np.min(months), np.max(months), num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_var1.index, monthly_avg_var1)
var1_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_var2.index, monthly_avg_var2)
var2_pchip = interp_pchip2(months_interp)
interp_pchip3 = interpolate.PchipInterpolator(monthly_avg_pH.index, monthly_avg_pH)
pH_pchip = interp_pchip3(months_interp)

#Scatter all raw data minus outliers, with jitter
sns.regplot(x=months, y=xL[var1], ax=axs[1,0], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:teal',
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)
sns.regplot(x=months, y=xL[var2], ax=axs[1,0], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:light orange', 
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)

#Plot interpolated phosphate and tp trend
axs[1,0].plot(months_interp, var1_pchip, 
        label='Phosphate', zorder=10, c='xkcd:teal', linewidth=2)
axs[1,0].plot(months_interp, var2_pchip, 
        label='TP', zorder=10, c='xkcd:light orange', linewidth=2)
axs[1,0].plot(months_interp, (var2_pchip-var1_pchip), 
              c='xkcd:coral', linewidth=2, zorder=10)

#Plot pH
ax2 = axs[1,0].twinx()
ax2.plot(months_interp, pH_pchip, 
        label='pH', zorder=5, c='grey', linewidth=2, linestyle='--')

#Formatting
axs[1,0].set_ylabel('P (\u03BCmol $\mathregular{L^{-1}}$)', fontsize=8)
axs[1,0].set_ylim(bottom=0, top=1.7)
ax2.set_ylim(7.8, 8.45)
ax2.yaxis.set_major_formatter(plt.NullFormatter())
axs[1,0].set_xticks(np.arange(0, 11, 2))
axs[1,0].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[1,0].tick_params(axis='y', labelsize=7)
axs[1,0].set_title('Intermediate (20-50 km)', fontsize=10)
#%% Offshore 70+ km
location = locations[4]

if location == 'Offshore':
    station_codes = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]

for stationcode in station_codes:
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    L = ((df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear))))
    dfL=df[L]
    x4 = x4.append(dfL, ignore_index=False)

#Remove outliers
L = ~np.isnan(x4[var1]) & ~np.isnan(x4[var2])
xL = x4[L]
xL['z_score_var1'] = stats.zscore(xL[var1])
xL['z_score_var2'] = stats.zscore(xL[var2])
L2 = (xL['z_score_var1'].abs()<=2) & (xL['z_score_var2'].abs()<=2)
xL0 = xL[L2]

#For adding extra Jan on x-axis
xL0['months13'] = xL0.index.month.to_numpy()
xL0_Jan = xL0[xL0.index.month == 1].copy()
xL0_Jan['months13'] = 13
xL0 = xL0.append(xL0_Jan)

# #Create months list
# L3 = (months[len(xL1)]-months[len(xL0)::])
# Jan_13 = months[L3]
# months[Jan_13] = 13

#Monthly averages
monthly_avg_var1 = xL0.groupby('months13')[var1].mean()
monthly_avg_var2 = xL.groupby(months)[var2].mean()
monthly_avg_pH = xL.groupby(months)['pH'].mean()

#Interpolation for smooth line
months_interp = np.linspace(np.min(months), np.max(months), num=100)
interp_pchip1 = interpolate.PchipInterpolator(monthly_avg_var1.index, monthly_avg_var1)
var1_pchip = interp_pchip1(months_interp)
interp_pchip2 = interpolate.PchipInterpolator(monthly_avg_var2.index, monthly_avg_var2)
var2_pchip = interp_pchip2(months_interp)
interp_pchip3 = interpolate.PchipInterpolator(monthly_avg_pH.index, monthly_avg_pH)
pH_pchip = interp_pchip3(months_interp)

#Scatter all raw data minus outliers, with jitter
sns.regplot(x=months, y=xL[var1], ax=axs[1,1], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:teal',
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)
sns.regplot(x=months, y=xL[var2], ax=axs[1,1], fit_reg = False, 
            x_jitter=0.2, y_jitter=0.1, 
            color='xkcd:light orange', 
            scatter_kws={'alpha':0.12, 's':15, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)

#Plot interpolated phosphate and tp trend
axs[1,1].plot(months_interp, var1_pchip, 
        label='Phosphate', zorder=10, c='xkcd:teal', linewidth=2)
axs[1,1].plot(months_interp, var2_pchip, 
        label='TP', zorder=10, c='xkcd:light orange', linewidth=2)
axs[1,1].plot(months_interp, (var2_pchip-var1_pchip), 
              c='xkcd:coral', linewidth=2, zorder=10)

#Plot pH
ax2 = axs[1,1].twinx()
ax2.plot(months_interp, pH_pchip, 
        label='pH', zorder=5, c='grey', linewidth=2, linestyle='--')

#Formatting
axs[1,1].set_ylim(bottom=0, top=1.1)
ax2.set_ylim(7.8, 8.45)
ax2.set_ylabel('pH', fontsize=8)
ax2.tick_params(axis='y', labelsize=7)

axs[1,1].set_xticks(np.arange(0, 11, 2))
axs[1,1].set_xticklabels([' ', 'Feb', 'April', 'June', 'Aug', 'Oct'], fontsize=7)
axs[1,1].tick_params(axis='y', labelsize=7)
axs[1,1].set_title('Offshore (>70 km)', fontsize=10)

#%% Formatting and plotting
fig.suptitle('Monthly averaged P surface waters \n 1973-2019', 
             fontsize=12, x=0.36, y=0.97) 

#Create legend
teal_patch = mpatches.Patch(color='xkcd:teal', label='DIP')
orange_patch = mpatches.Patch(color='xkcd:light orange', label='TP')
grey_patch = mpatches.Patch(color='xkcd:grey', label= 'pH')
coral_patch = mpatches.Patch(color='xkcd:coral', label= 'OP')
plt.legend(handles=[teal_patch, orange_patch, grey_patch, coral_patch], 
           bbox_to_anchor=(1.035, 2.5), fontsize=8, ncol=2)

#Saving
plt.savefig("figures/phosphate_tp_with_pH.png", bbox_inches='tight')
