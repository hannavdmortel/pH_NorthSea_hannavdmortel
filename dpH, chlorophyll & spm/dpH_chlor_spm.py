import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats.stats import spearmanr
import matplotlib.dates as mdates
from matplotlib.ticker import (AutoMinorLocator)

fpath = "C:/Users/hanna/Documents/GitHub/"

#%%
#Create list
data = []

#Create figure
fig, (ax1, ax2) = plt.subplots(figsize = (12, 4), ncols=2,  dpi=300)

#List of stations without a negative seasonal correlation between spm & chlorophyll
stationcodes = [
    'CALLOG30',
    'DOOVBWT',
    'EGMAZE10',
    'EGMAZE20',
    'EGMAZE30',
    'EGMAZE50',
    'GOERE30',
    'GOERE70',
    'NOORDWK20',
    'NOORDWK30',
    'NOORDWK50',
    'NOORDWK70',
    'ROTTMPT20',
    'ROTTMPT30',
    'SCHOUWN70',
    'TERHDE70',
    'TERSLG30',
    'TERSLG70',
    'TERSLG100',
    'TERSLG135',
    'WALCRN50',
    'WALCRN70']

#Loop through station data files
for stationcode in stationcodes:    
    #Read station specific files
    filename = fpath + "rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    
    #Create datetime column
    df['datetime'] = mdates.num2date(df.datenum)
    
    #Calculate min and max year per station
    min_year = df['datetime'].dt.year.min()
    max_year = df['datetime'].dt.year.max()
        
    #Loop through years
    for year in range(min_year, max_year):
        #Select year
        L_year = (df.datenum > mdates.datestr2num('{}-01-01'.format(year))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(year+1)))
        df_L_year = df[L_year]
        
        #Calculate min and max pH per year
        min_pH = df_L_year.pH.min()
        max_pH = df_L_year.pH.max()
        dpH = max_pH - min_pH
                
        #Average spm
        L_month = (df.datenum > mdates.datestr2num('{}-02-01'.format(year))) & (df.datenum < mdates.datestr2num('{}-05-01'.format(year)))
        spm_avg = df_L_year.spm[L_month].mean()
            
        #Average spm
        chlorophyll_avg = df_L_year.chlorophyll[L_month].mean()
        
        #Compile data into list
        data.append((stationcode, year, dpH, spm_avg, chlorophyll_avg))

#Compile all data into one dataframe
df2 = pd.DataFrame(data, columns = ['station', 'year', 'dpH', 'spm', 'chlorophyll'])

#%% SPM
ax1.scatter(df2.spm, df2.dpH, s=60, marker='o', c='royalblue', alpha=0.4, edgecolor='none')

#Spearman
L1 = ~np.isnan(df2.spm) & ~np.isnan(df2.dpH)
corr, _ = spearmanr(df2.dpH[L1], df2.spm[L1])

L2 = df2.spm > 10
corr2, _ = spearmanr(df2.dpH[L2], df2.spm[L2])

# Linear regression
slope1, intercept1, rv, pv, se = stats.linregress(10**df2.spm[L1], df2.dpH[L1])
spm_interp = np.linspace(np.min(df2.spm[L1]), np.max(df2.spm[L1]), num=500)
ax1.plot(spm_interp, intercept1 + slope1 * spm_interp, 
         c='xkcd:pink', linestyle='--', linewidth=2)
 
#Formatting
ax1.set_xscale("log")
#ax1.set_xlim(10**-0.1, 10**1.65)
ax1.yaxis.set_minor_locator(AutoMinorLocator(4))
ax1.text(8.9, 1.9, 'Spearman correlation: %.2f' % corr)
ax1.set_title('\u0394' + 'pH vs SPM')
ax1.set_xlabel('SPM ($\mathregular{mg^{-L}}$)')
ax1.set_ylabel('\u0394' + 'pH')

#%% Chlorophyll
ax2.scatter(df2.chlorophyll, df2.dpH, s=60, marker='o', c='xkcd:teal green', alpha=0.4, edgecolor='none')

#Spearman
L3 = ~np.isnan(df2.chlorophyll) & ~np.isnan(df2.dpH)
corr3, _ = spearmanr(df2.dpH[L3], df2.chlorophyll[L3])
L4 = df2.spm > 6
corr4, _ = spearmanr(df2.dpH[L4], df2.spm[L4])

# Linear regression
slope2, intercept2, rv, pv, se = stats.linregress(10**df2.chlorophyll[L3], df2.dpH[L3])
chlor_interp = (np.linspace(np.min(df2.chlorophyll[L3]), np.max(df2.chlorophyll[L3]), num=500))
ax2.plot(chlor_interp, intercept2 + slope2 * chlor_interp, 
         c='xkcd:light orange', linestyle='--', linewidth=2)

#Formatting
ax2.set_xscale("log")
#ax2.set_ylim(0,2)
ax2.set_xlim(10**(-0.4), 10**1.35)
ax2.yaxis.set_minor_locator(AutoMinorLocator(4))
ax2.text(3.1, 1.9, 'Spearman correlation: %.2f' % corr)
ax2.set_title('\u0394' + 'pH vs Chlorophyll')
ax2.set_xlabel('Chl (\u03BC$\mathregular{g^{-L}}$)')
ax2.set_ylabel('\u0394' + 'pH') 
#%% Save
plt.savefig("figures/dpH vs chlorophyll BOTH log.png")
