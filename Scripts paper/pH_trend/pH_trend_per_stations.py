import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

df=pd.DataFrame()
df1=pd.DataFrame()
df2=pd.DataFrame()
df3=pd.DataFrame()
df4=pd.DataFrame()
df5=pd.DataFrame()

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

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

fig, ax = plt.subplots(4, figsize=(4, 5), dpi=300)

ax[0].scatter(df1.YEAR, df1.pH, alpha=0.2, s=10, c='grey', edgecolor='none')
ax[0].plot(grouped1.index, grouped1.pH_trend, c='xkcd:light orange', linewidth=2.5)

ax[1].scatter(df2.YEAR, df2.pH, alpha=0.2, s=10, c='grey', edgecolor='none')
ax[1].plot(grouped2.index, grouped2.pH_trend, c='royalblue', linewidth=2.5)

ax[2].scatter(df3.YEAR, df3.pH, alpha=0.2, s=10, c='grey', edgecolor='none')
ax[2].plot(grouped3.index, grouped3.pH_trend, c='xkcd:teal', linewidth=2.5)

ax[3].scatter(df4.YEAR, df4.pH, alpha=0.2, s=10, c='grey', edgecolor='none')
ax[3].plot(grouped4.index, grouped4.pH_trend, c='xkcd:pink', linewidth=2.5)
ax[3].set_xlabel('Years')
ax[3].set_xticklabels(['', '1980', '', '1990', '', '2000', '', '2010'])

for i in [0, 1, 2]:
    ax[i].tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False)
    ax[i].plot(grouped5.index, grouped5.pH_trend, c='black', linewidth=0.5)

for i in [0, 1, 2, 3]:
    ax[i].xaxis.get_ticklocs(minor=True)
    ax[i].minorticks_on()
    ax[i].grid(axis='both')
    ax[i].grid(axis='both', which='minor', linestyle=':', linewidth='0.5')
    ax[i].set_xlim([datetime(1975, 1, 1), datetime(2019, 1, 1)])
    ax[i].set_ylim([7, 9])
    ax[i].set_yticklabels([' ', '8', '9'])

#Formatting
ax[0].set_title('Wadden Sea', fontsize=9, loc='right', pad=1)
ax[1].set_title('Nearshore (<20 km)', fontsize=9, loc='right', pad=1)
ax[2].set_title('Intermediate (20-50 km)', fontsize=9, loc='right', pad=1)
ax[3].set_title('Offshore (≥70 km)', fontsize=9, loc='right', pad=1)
ax[3].plot(grouped5.index, grouped5.pH_trend, c='black', linewidth=0.5, label='pH trend all stations')
fig.suptitle('pH trends Dutch coastal zone')
fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.945), fontsize=8)
plt.savefig("figures/pH trend ALL.png", bbox_inches='tight')



