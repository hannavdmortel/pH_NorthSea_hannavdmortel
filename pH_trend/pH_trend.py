import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator)
from datetime import datetime
import seaborn as sns

df=pd.DataFrame()
df1=pd.DataFrame()
df2=pd.DataFrame()
df3=pd.DataFrame()
df4=pd.DataFrame()
df5=pd.DataFrame()

fpath = "C:/Users/hanna/Documents/GitHub/"
northsea = pd.read_csv(
    fpath + "pH-North-Sea/Maps/data/coordinates_stations.csv")

# #Wadden
station_codes_1 = [
    "BLAUWSOT", 
    "DANTZGT", 
    "EILDBG", 
    "HOLWDBG", 
    "MALZN", 
    "VLIESZD", 
    "WESTMP", 
    "ZOUTKPLZGT", 
    "ZUIDOLWNOT", 
    "DOOVBWT"
    ]

#Nearshore <20km
station_codes_2 = [
    "CALLOG4", 
    "CALLOG10", 
    "EGMAZE4", 
    "EGMAZE10", 
    "GOERE6", 
    "GOERE10", 
    "NOORDWK4", 
    "NOORDWK10", 
    "ROTTMPT20", 
    "SCHOUWN1", 
    "SCHOUWN4", 
    "SCHOUWN10", 
    "TERSLG10", 
    "WALCRN4", 
    "WALCRN10"
    ]

#Intermediate 20-50 km
station_codes_3 = [
    "CALLOG30", 
    "CALLOG50", 
    "EGMAZE20", 
    "EGMAZE30", 
    "EGMAZE50", 
    "GOERE20", 
    "GOERE30", 
    "GOERE50", 
    "NOORDWK20", 
    "NOORDWK30", 
    "NOORDWK50", 
    "ROTTMPT30", 
    "ROTTMPT50", 
    "SCHOUWN20", 
    "SCHOUWN30", 
    "TERSLG30",  
    "TERSLG50", 
    "WALCRN20", 
    "WALCRN30", 
    "WALCRN50"
    ]

#Offshore 70+ km
station_codes_4 = [
    "CALLOG70", 
    "EGMAZE70", 
    "GOERE70", 
    "NOORDWK70", 
    "ROTTMPT70", 
    "ROTTMPT100", 
    "SCHOUWN50", 
    "SCHOUWN70", 
    "TERHDE70", 
    "TERSLG70", 
    "TERSLG100", 
    "TERSLG135", 
    "TERSLG175",
    "WALCRN70"
    ]

for stationcode in station_codes_1:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df1 = df1.append(df, ignore_index=True)

for stationcode in station_codes_2:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df2 = df2.append(df, ignore_index=True)
    
for stationcode in station_codes_3:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df3 = df3.append(df, ignore_index=True)

for stationcode in station_codes_4:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df4 = df4.append(df, ignore_index=True) 
    
for stationcode in northsea.station_code:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df5 = df5.append(df, ignore_index=True)
    
#Create extra datetime column
df1['YEAR'] = mdates.num2date(df1.datenum)
df1['YEAR'] = pd.to_datetime(df1.YEAR)
df2['YEAR'] = mdates.num2date(df2.datenum)
df2['YEAR'] = pd.to_datetime(df2.YEAR)
df3['YEAR'] = mdates.num2date(df3.datenum)
df3['YEAR'] = pd.to_datetime(df3.YEAR)
df4['YEAR'] = mdates.num2date(df4.datenum)
df4['YEAR'] = pd.to_datetime(df4.YEAR)
df5['YEAR'] = mdates.num2date(df5.datenum)
df5['YEAR'] = pd.to_datetime(df5.YEAR)

#Plot average trend
grouped1 = df1.groupby('YEAR').mean()
grouped2 = df2.groupby('YEAR').mean()
grouped3 = df3.groupby('YEAR').mean()
grouped4 = df4.groupby('YEAR').mean()
grouped5 = df5.groupby('YEAR').mean()

fig, ax = plt.subplots(figsize=(5, 3), dpi=300)

ax.plot(grouped1.datenum, grouped1.pH_trend, c='xkcd:light orange', linewidth=2.2, label='Wadden Sea', alpha=0.9)
ax.plot(grouped2.datenum, grouped2.pH_trend, c='royalblue', linewidth=2.2, label='Nearshore (<20 km)', alpha=0.9)
ax.plot(grouped3.datenum, grouped3.pH_trend, c='xkcd:teal', linewidth=2.2, label='Intermediate (20-50 km)', alpha=0.9)
ax.plot(grouped4.datenum, grouped4.pH_trend, c='xkcd:pink', linewidth=2.2, label='Offshore (≥70 km)', alpha=0.9)
#ax.scatter(df5.YEAR, df5.pH, alpha=0.2, s=8, c='grey', edgecolor='none')
sns.regplot(x=df5.datenum, y=df5.pH, ax=ax, fit_reg = False, 
            x_jitter=0.1, y_jitter=0.1, 
            color='grey',
            scatter_kws={'alpha':0.12, 's':8, 'edgecolor':'none'}
            ).set(xlabel=None, ylabel=None)
#Formatting
ax.xaxis.set_minor_locator(MultipleLocator(365.25))
ax.grid(axis='both')
ax.grid(axis='both', which='minor', linestyle=':', linewidth='0.5')
ax.set_xlim([datetime(1973, 1, 1), datetime(2020, 1, 1)])
ax.set_xticks([datetime(1980, 1, 1), datetime(1990, 1, 1), datetime(2000, 1, 1), datetime(2010, 1, 1)])
ax.set_xticklabels(['1980', '1990', '2000', '2010'])
ax.set_ylim([7.2, 9])
ax.set_xlabel('Years')
ax.set_ylabel('pH')

fig.suptitle('pH trends Dutch coastal zone')
fig.legend(loc='upper left', bbox_to_anchor=(0.16, -0.02), fontsize=8, ncol=2)
plt.savefig("figures/pH trend together.png", bbox_inches='tight')



