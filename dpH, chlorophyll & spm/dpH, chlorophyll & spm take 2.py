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

#%%
#Create list
data = []

#List of stations without a negative seasonal correlation between spm & chlorophyll
stationcodes = [
    'ZUIDOLWNOT',
    'EILDBG',
    'HOLWDBG',
    'WESTMP',
    'VLIESZD',
    'MALZN',
    'ROTTMPT20',
    'ROTTMPT30',
    'TERSLG10',
    'TERSLG30',
    'TERSLG50',
    'TERSLG70',
    'TERSLG100',
    'TERSLG135',
    'TERSLG175',
    'CALLOG10',
    'CALLOG50',
    'EGMAZE4',
    'EGMAZE10',
    'EGMAZE20',
    'EGMAZE30',
    'EGMAZE50',
    'EGMAZE70',
    'NOORDWK4',
    'NOORDWK10',
    'NOORDWK20',
    'NOORDWK30',
    'NOORDWK50',
    'NOORDWK70',
    'TERHDE70',
    'GOERE6',
    'GOERE30',
    'GOERE70',
    'SCHOUWN30',
    'SCHOUWN70',
    'WALCRN20',
    'WALCRN50'
    ]
#Loop through station data files
for stationcode in stationcodes:
#for stationcode in northsea.station_code:    
    #Read station specific files
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
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

            
            # #Plotting against chlorophyll
            # ax2 = ax.twinx()
            # ax2.scatter(dpH, df_L_year.chlorophyll, s=60, 
            #             marker='x', c='seagreen', label = 'Chlorophyll')
            
            
            #Add linear regressions for SPM & Chlorophyll
            # L_spm = ~np.isnan(df_L_year.spm)
            # slope, intercept, rv, pv, se = stats.linregress(dpH, df_L_year.spm[L_spm])
            # ax.plot(dpH, intercept + slope * dpH,
            #         c='royalblue', label='Linear regression SPM')
    
            # L_chlorophyll = ~np.isnan(df_L_year.chlorophyll)
            # slope2, intercept2, rv2, pv2, se2 = stats.linregress(dpH, df_L_year.chlorophyll[L_chlorophyll])
            # ax2.plot(dpH, intercept2 + slope2 * dpH,
            #         c='seagreen', label='Linear regression Chlorophyll')
            
            #Pearson 
            # L_pearson = df_L_year.spm.notnull()
            # df_L_pearson = df_L_year.spm[L_pearson]
            # dpH_pearson = np.linspace(min_pH, max_pH, num = len(df_L_pearson))
            # pearson_coef, p_value = stats.pearsonr(dpH_pearson, df_L_pearson)
            # ax.text(0, 0, f"Pearson coefficient = {pearson_coef}")
            
            #Formatting
            # ax.set_title(f"{stationcode} {year}")
            # ax.set_xlabel('\u0394' + 'pH')
            # ax.set_ylabel('SPM')
            # ax2.set_ylabel('Chlorophyll')
            # fig.legend(loc='upper right', bbox_to_anchor=(1.25, 0.55))
           
            #Saving
            #plt.savefig(f"figures/{stationcode} {year}.png")

#Compile all data into one dataframe
df2 = pd.DataFrame(data, columns = ['station', 'year', 'dpH', 'spm', 'chlorophyll'])

#%%
#Plot all spm vs dpH data
fig, (ax1, ax2) = plt.subplots(figsize = (12, 4), ncols=2,  dpi=300)
ax1.scatter(df2.spm, df2.dpH, s=60, marker='o', c='royalblue', alpha=0.4, edgecolor='none')

#Pearson 
L_pearson = df2.spm.notnull()
df2_L_pearson = df2.spm[L_pearson]
dpH_pearson = np.linspace(df2.dpH.min(), df2.dpH.max(), num = len(df2_L_pearson))
# pearson_coef, p_value = stats.pearsonr(dpH_pearson, df2_L_pearson)
# ax.text(30, 0, f"Pearson coefficient = {pearson_coef}")
           
# Spearman
corr, _ = spearmanr(dpH_pearson, df2_L_pearson)
ax1.set_xscale("log")
ax1.text(15, 2.3, 'Spearmans correlation: %.3f' % corr)
 
#Formatting
ax1.set_title('\u0394' + 'pH vs SPM')
ax1.set_xlabel('SPM')
ax1.set_ylabel('\u0394' + 'pH')
#fig.legend(loc='upper right', bbox_to_anchor=(1.25, 0.55))
   
#Saving
#plt.savefig("figures/dpH vs spm not all stations per year.png")


#Plot all chlorophyll vs dpH data
ax2.scatter(df2.chlorophyll, df2.dpH, s=60, marker='o', c='seagreen', alpha=0.4, edgecolor='none')

#Pearson 
L_pearson = df2.chlorophyll.notnull()
df2_L_pearson = df2.chlorophyll[L_pearson]
dpH_pearson = np.linspace(df2.dpH.min(), df2.dpH.max(), num = len(df2_L_pearson))
# pearson_coef, p_value = stats.pearsonr(dpH_pearson, df2_L_pearson)
# ax.text(10, 0, f"Pearson coefficient = {pearson_coef}")

# Spearman
corr, _ = spearmanr(dpH_pearson, df2_L_pearson)
ax2.set_xscale("log")
ax2.text(2.8, 2.3, 'Spearmans correlation: %.3f' % corr)

#Formatting
ax2.set_title('\u0394' + 'pH vs chlorophyll')
ax2.set_xlabel('chlorophyll')
ax2.set_ylabel('\u0394' + 'pH')
#fig.legend(loc='upper right', bbox_to_anchor=(1.25, 0.55))
   
#Saving
plt.savefig("figures/dpH vs chlorophyll BOTH.png")
