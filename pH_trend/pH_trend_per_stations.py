import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

df=pd.DataFrame()

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

# #Wadden
station_codes_1 = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

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
    "WALCRN10"]

#Nearshore 20-50 km
station_codes_3 = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]

#Offshore 70+ km
station_codes_4 = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]

for stationcode in station_codes_1:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df1 = df.append(df)

for stationcode in station_codes_2:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df2 = df.append(df)
    
for stationcode in station_codes_3:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df3 = df.append(df)

for stationcode in station_codes_4:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df = pq.read_table(source=filename).to_pandas()
    df4 = df.append(df)    
    
#Create extra datetime column
df1['YEAR'] = mdates.num2date(df1.datenum)
df1['YEAR'] = pd.to_datetime(df1.YEAR)
df2['YEAR'] = mdates.num2date(df2.datenum)
df2['YEAR'] = pd.to_datetime(df2.YEAR)
df3['YEAR'] = mdates.num2date(df3.datenum)
df3['YEAR'] = pd.to_datetime(df3.YEAR)
df4['YEAR'] = mdates.num2date(df4.datenum)
df4['YEAR'] = pd.to_datetime(df4.YEAR)

#Plot average trend
grouped1 = df1.groupby('YEAR').mean()
grouped2 = df2.groupby('YEAR').mean()
grouped3 = df3.groupby('YEAR').mean()
grouped4 = df4.groupby('YEAR').mean()

fig, ax = plt.subplots(4, dpi=300)
fig.suptitle = 'pH'

ax[0].scatter(df1.YEAR, df1.pH_raw, alpha=0.3, s=8, c='grey')
ax[0].plot(grouped1.index, grouped1.pH_trend, c='xkcd:pink purple')

ax[1].scatter(df2.YEAR, df2.pH_raw, alpha=0.3, s=8, c='grey')
ax[1].plot(grouped2.index, grouped2.pH_trend, c='royalblue')

ax[2].scatter(df3.YEAR, df3.pH_raw, alpha=0.3, s=8, c='grey')
ax[2].plot(grouped3.index, grouped3.pH_trend, c='xkcd:teal')

ax[3].scatter(df4.YEAR, df4.pH_raw, alpha=0.3, s=8, c='grey')
ax[3].plot(grouped4.index, grouped4.pH_trend, c='xkcd:pink')
ax[3].set_xlabel('Years')

for i in [0, 1, 2]:
    ax[i].tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)

for i in [0, 1, 2, 3]:
    ax[i].xaxis.get_ticklocs(minor=True)
    ax[i].minorticks_on()
    ax[i].grid(axis='both')
    ax[i].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')
    ax[i].set_xlim([datetime(1975, 1, 1), datetime(2019, 1, 1)])
    ax[i].set_ylim([7, 9])

#Formatting
# ax.set_ylabel('pH')
# ax.minorticks_on()
# ax.grid(axis='x')
# ax.set_title('Wadden Sea pH')

plt.savefig("figures/pH trend WADDEN SEA.png")



