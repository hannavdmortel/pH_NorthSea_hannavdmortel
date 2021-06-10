import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from scipy import interpolate, stats
from scipy.stats.stats import pearsonr
import matplotlib.dates as mdates

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#%%
#Loop through stations
for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    
    #Create datetime column
    df['datetime'] = mdates.num2date(df.datenum)
    
    #Calculate min and max year per station
    min_year = df['datetime'].dt.year.min()
    max_year = df['datetime'].dt.year.max()
    
    #Loop through years
    for year in range(min_year, max_year):
        L_year = (df.datenum > mdates.date2num('{}-01-01'.format(year))) & (df.datenum < mdates.date2num('{}-01-01'.format(year+1)))
        df_L_year = df[L_year]
        
        #Calculate min and max pH per year
        min_pH = df_L_year.pH.min()
        max_pH = df_L_year.pH.max()
        
        #Create logical to select timing onset spring bloom (from min_pH to max_pH)
        L_start = (df.pH == min_pH)
        L_peak = (df.pH == max_pH)
        
        #Selecting datenum using logical
        start_spring_bloom = df.datenum[L_start]
        peak_spring_bloom = df.datenum[L_peak]
        
        #Interpolate between min and max pH
        dpH = np.linspace(min_pH, max_pH, num = len(df_L_year))

        #Plotting against spm
        fig, ax = plt.subplots(dpi=300)
        ax.scatter(dpH, df_L_year.spm, s=60, 
                   marker='o', c='royalblue', label = 'SPM')
        
        #Plotting against chlorophyll
        ax2 = ax.twinx()
        ax2.scatter(dpH, df_L_year.chlorophyll, s=60, 
                    marker='x', c='seagreen', label = 'Chlorophyll')
        
        #PROBLEM: there are nan values, but if you remove these there are missing values
        #How do I ignore nan and missing values?
        
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
        ax.set_title(f"{stationcode} {year}")
        ax.set_xlabel('\u0394' + 'pH')
        ax.set_ylabel('SPM')
        ax2.set_ylabel('Chlorophyll')
        fig.legend(loc='upper right', bbox_to_anchor=(1.25, 0.55))
       
        #Saving
        #plt.savefig(f"figures/{stationcode} {year}.png")

