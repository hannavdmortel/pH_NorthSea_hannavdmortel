import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

df=pd.DataFrame()

fpath = "C:/Users/hanna/Documents/GitHub/"
northsea = pd.read_csv(
    fpath + "pH-North-Sea/Maps/data/coordinates_stations.csv")

for stationcode in northsea.station_code:    
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df2 = pq.read_table(source=filename).to_pandas()
    df = df.append(df2)
    
fig, ax = plt.subplots(figsize=(15,6), dpi=300)

#Create extra datetime column
df['YEAR'] = mdates.num2date(df.datenum)
df['YEAR'] = pd.to_datetime(df.YEAR)

#Scatter ALL
ax.scatter(df.YEAR, df.pH_trend, alpha=0.3, s=8, c='grey')

#Plot average pH trend
grouped = df.groupby('YEAR').mean()
ax.plot(grouped.index, grouped.pH_trend, c='royalblue', linewidth=3.5, label='pH')

#Plot other variable trend on second axis
# ax2 = ax.twinx()
# ax2.plot(grouped.index, grouped.chlorophyll_trend, c='red', linewidth=3.5, label='Phosphate')
# fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))

#Plot offset from Redfield on second axis
#RR = grouped.nitrate_trend-(16*grouped.phosphate_trend)
ax2 = ax.twinx()
ax2.plot(grouped.index, grouped.temperature_trend, c='xkcd:light red', linewidth=3.5, label='SST')
ax2.set_ylabel('SST')
#ax2.set_ylim([0, 11])
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))



#Formatting
ax.set_ylim([7.4, 8.7])
ax.set_xlim([df.YEAR.min(), df.YEAR.max()])
ax.set_ylabel('pH')
ax.minorticks_on()
ax.grid(axis='x')
ax.set_zorder(1)  # default zorder is 0 for ax and ax2
ax.patch.set_visible(False)  # prevents ax from hiding ax2

plt.savefig("figures/pH trend+SST.png")



