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
        
        #Interpolate between min and max pH
        dpH = np.linspace(min_pH, max_pH, num = len(df_L_year))
        
        #Create logical to select timing onset spring bloom (from min_pH to max_pH)
        L_start = (df.pH == min_pH)
        L_peak = (df.pH == max_pH)
        
        #Selecting datenum using logical
        start_spring_bloom = df.datenum[L_start]
        peak_spring_bloom = df.datenum[L_peak]
        
        #Plotting against spm
        fig, ax = plt.subplots(dpi=300)
        ax.scatter(dpH, df_L_year.spm, s=20, c='xkcd:red')
        
        #Add linear regression
        # interp_linear = interpolate.interp1d(dpH, , kind='linear')
        # slope, intercept, rv, pv, se = stats.linregress(volume, emf)
        # volume_interp = np.linspace(np.min(volume), np.max(volume), num=500)
        # emf_linear = interp_linear(volume_interp)
        # ax.plot(volume_interp, emf_linear, label="interp1d linear",
        # linestyle="--")
        
        #Spearman
        pearson_coef, p_value = stats.pearsonr(dpH, df_L_year) #define the columns to perform calculations on
        ax.text(0, 0, f"Pearson coefficient = {pearson_coef}"
        
        #Formatting
        ax.set_title(f"{stationcode} {year}")
        ax.set_xlabel('\u0394' + 'pH')
        ax.set_ylabel('SPM')
        
        #Saving to separate station folders
        plt.savefig(f"/dpH vs spm/figures/{stationcode}/{year} {stationcode}.png")

