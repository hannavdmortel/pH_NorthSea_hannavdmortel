import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

df=pd.DataFrame()

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

#Wadden
station_codes = [
    ]

#Offshore
station_codes = [
    ]

#Nearshore
station_codes = [
    ]

for stationcode in northsea.station_code:    
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df2 = pq.read_table(source=filename).to_pandas()
    df = df.append(df2)
    
fig, ax = plt.subplots(figsize=(15,6), dpi=300)

#Create extra datetime column
df['YEAR'] = mdates.num2date(df.datenum)
df['YEAR'] = pd.to_datetime(df.YEAR)

#Scatter ALL
#ax.scatter(df.YEAR, df.pH_trend, alpha=0.3, s=8, c='grey')

#Plot average trend
grouped = df.groupby('YEAR').mean()
ax.plot(grouped.index, grouped.pH_trend, c='royalblue', linewidth=3.5, label='pH')
ax2 = ax.twinx()

ax2.plot(grouped.index, grouped.chlorophyll_trend, c='red', linewidth=3.5, label='Phosphate')
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))

#Formatting
ax.set_xlim([df.YEAR.min(), df.YEAR.max()])
ax.set_ylabel('pH')
ax.minorticks_on()
ax.grid(axis='x')

#plt.savefig("figures/pH trend ALL.png")



