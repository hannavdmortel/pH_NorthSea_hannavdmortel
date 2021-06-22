import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import matplotlib.dates as mdates
df0=pd.DataFrame()

#Choose location
location = 'Offshore'

if location == 'WaddenSea':
    station_codes = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']

#Nearshore <20km
if location == 'Nearshore1':
    station_codes = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]

#Nearshore 20-50 km
if location == 'Nearshore2':
    station_codes = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]

#Offshore 70+ km
if location == 'Offshore':
    station_codes = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]

for stationcode in station_codes:
    filename = "C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/x13/"+ stationcode + ".parquet"
    df2 = pq.read_table(source=filename).to_pandas()
    df0 = df0.append(df2, ignore_index=True,)

#Choose years
startyear = '1975'
endyear = '2020'

#Choose variables
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "phosphate"
var2 = "nitrate"

#Create new dataframe with relevant columns
df = df0[['datenum', var1, var2]]

#Remove nan
var1_np = df[var1].to_numpy()
var2_np = df[var2].to_numpy()
L1 = (~np.isnan(var1_np) & ~np.isnan(var2_np))
df = df[L1]

#Select specified years
L2 = (df.datenum > mdates.datestr2num('{}-01-01'.format(startyear))) & (df.datenum < mdates.datestr2num('{}-01-01'.format(endyear)))

#Remove outliers
df['z_score_var1'] = stats.zscore(df[var1])
df['z_score_var2'] = stats.zscore(df[var2])
L3 = (df['z_score_var1'].abs()<=3) & (df['z_score_var2'].abs()<=3)
dfL = df[L2][L3]

#Scatter
fig, ax = plt.subplots(figsize=(7,5), dpi=300)
ax.scatter(dfL[var1], dfL[var2], s=20, c='xkcd:grey', alpha=0.3)
ax.set_title(location + ' ' + startyear + '-' + endyear)
ax.set_xlabel(var1)
ax.set_ylabel(var2)
plt.xlim(left=0.0)
plt.ylim(bottom=0.0)

#LINEAR REGRESSION
#Convert to np array to use logical and drop nan for both
var1_np = dfL[var1].to_numpy()
var2_np = dfL[var2].to_numpy()
L = (~np.isnan(var1_np) & ~np.isnan(var2_np))
x = var1_np[L]
y = var2_np[L]

#Linear regression
slope, intercept, rv, pv, se = stats.linregress(x, y)
var1_interp = np.linspace(np.min(x), np.max(x))
ax.plot(var1_interp, intercept + slope * var1_interp, c='xkcd:pink', label = 'linear')
ax.text(0.8, 0.9, 'N:P = %.2f' % slope, transform=ax.transAxes)

#plt.savefig("figures/" + location + "_" + startyear + "-" + endyear + ".png")

