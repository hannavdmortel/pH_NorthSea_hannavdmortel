import pandas as pd
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

df=pd.DataFrame()

northsea = pd.read_csv(
    "C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/data/coordinates_stations.csv")

# #Wadden
station_codes = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

#Nearshore <20km
#station_codes = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]

#Nearshore 20-50 km
#station_codes = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]

# #Offshore 70+ km
#station_codes = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]


#for stationcode in northsea.station_code: 
for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df2 = pq.read_table(source=filename).to_pandas()
    df = df.append(df2)

#Create extra datetime column
df['YEAR'] = mdates.num2date(df.datenum)
df['YEAR'] = pd.to_datetime(df.YEAR)

start = 2000 
end = 2020

L_year = (df.datenum > mdates.datestr2num('{}-01-01'.format(start))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(end)))
df_year = df[L_year]
maximum = df_year.pH_seasonal.max()
minimum = df_year.pH_seasonal.min()

