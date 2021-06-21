import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from scipy import interpolate

rws_file = 'C:/Users/hanna/Documents/GitHub/rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws_all = pd.read_parquet(rws_file, engine='auto')

#%%
#Choose stations
#All
rws = rws_all

#Wadden Sea
#rws = rws_all.loc[["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT]]

#Offshore, >=50km
#rws = rws_all.loc[["CALLOG50", "CALLOG70", "EGMAZE50", "EGMAZE70", "GOERE50", "GOERE70", "NOORDWK50", "NOORDWK70", "ROTTMPT50", "ROTTMPT70", "ROTTMPT100", "SCHOUWN50", "SCHOUWN70", "TERHDE70", "TERSLG50", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175", "WALCRN50", "WALCRN70"]]

#Close to shore, =<30km
#rws = rws_all.loc[["CALLOG4", "CALLOG10", "CALLOG30", "EGMAZE4", "EGMAZE10", "EGMAZE20", "EGMAZE30", "GOERE6", "GOERE10", "GOERE20", "GOERE30", "NOORDWK4", "NOORDWK10", "NOORDWK20", "NOORDWK30", "ROTTMPT20", "ROTTMPT30", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "SCHOUWN20", "SCHOUWN30", "TERSLG10", "TERSLG30", "WALCRN4", "WALCRN10", "WALCRN20", "WALCRN30"]]

#Group by datetime
grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="M")).mean()

#%% spm

L = grouped_month.datenum > mdates.date2num('1976-01-01')
fig, ax = plt.subplots(dpi=300, figsize=(8,2))
gmL = grouped_month[L]
ax.scatter(x = gmL.index, y = gmL.spm, s=0)

interp_linear = interpolate.interp1d(gmL.datenum, gmL.spm, kind='linear')
interp_spline = interpolate.UnivariateSpline(gmL.datenum, gmL.spm, s = 1000)

datenum_interp = np.linspace(np.min(gmL.datenum), np.max(gmL.datenum), num = 800)
phosphate_linear = interp_linear(datenum_interp)

ax.plot(datenum_interp, phosphate_linear, c='seagreen')
ax.set_xlabel('Year')
ax.set_ylabel('SPM')
#ax.set_ylim(-0.01, 0.05)
ax.set_title('Wadden Sea spm concentrations over time (monthly averages)')

#%% pH
fig, ax = plt.subplots(dpi=300)
ax.scatter(x = grouped_month.index, y = grouped_month.pH, s=0)

#Create logical to ignore nan pH values
L = ~np.isnan(grouped_month.pH)
gmL_pH = grouped_month.pH[L]
gmL_datenum = grouped_month.datenum[L]

#Create functions (to create functions)
#interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.pH, kind='linear')
#interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.pH, s = 1000)
interp_pchip = interpolate.PchipInterpolator(gmL_datenum, gmL_pH)

#Interpolate datenum (can change length to length pH)
datenum_interp = np.linspace(np.min(gmL_datenum), np.max(gmL_datenum), num = 1000)

#pH_linear = interp_linear(datenum_interp)
#pH_spline = interp_spline(datenum_interp)
pH_pchip = interp_pchip(datenum_interp)

#ax.plot(datenum_interp, pH_linear, c='black')
#ax.plot(datenum_interp, pH_spline)
ax.plot(datenum_interp, pH_pchip, c='purple')
ax.set_xlabel('Year')
ax.set_ylabel('pH')
#ax.set_title('pH over time (annual averages)')

fig.savefig("pH_trend/figures/ONSHORE_pH_pchip.png")
#%% chlorophyll
chlorophyll_years = rws.xs['1980-01-01' : '2016-01-01', 'ymd']

grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="M")).mean()

fig, ax = plt.subplots(dpi=300, figsize=(8,2))
ax.scatter(x = grouped_month.index, y = grouped_month.chlorophyll, s=0)

interp_linear = interpolate.interp1d(grouped_month.datenum, grouped_month.chlorophyll, kind='linear')
interp_spline = interpolate.UnivariateSpline(grouped_month.datenum, grouped_month.chlorophyll, s = 1000)

datenum_interp = np.linspace(np.min(grouped_month.datenum), np.max(grouped_month.datenum), num = 800)
chlorophyll_linear = interp_linear(datenum_interp)
chlorophyll_spline = interp_spline(datenum_interp)

ax.plot(datenum_interp, chlorophyll_linear)
ax.plot(datenum_interp, chlorophyll_spline)
ax.set_xlabel('Year')
ax.set_ylabel('Chlorophyll')
ax.set_title('North Sea chlorophyll over time (annual averages)')

#%% nutrients
#Try groupby??
# for i in chosen_stations:
#     for rws.xs(key=i, level='station')
#         rws.xs(key='station_name', level='station')
        
L = grouped_month.datenum > mdates.date2num('1976-01-01')
fig, ax = plt.subplots(dpi=300, figsize=(8,2))
gmL = grouped_month[L]
ax.scatter(x = gmL.index, y = gmL.phosphate, s=0)

interp_linear = interpolate.interp1d(gmL.datenum, gmL.phosphate, kind='linear')
interp_spline = interpolate.UnivariateSpline(gmL.datenum, gmL.phosphate, s = 1000)

datenum_interp = np.linspace(np.min(gmL.datenum), np.max(gmL.datenum), num = 800)
phosphate_linear = interp_linear(datenum_interp)

ax.plot(datenum_interp, phosphate_linear, c='royalblue')
ax.set_xlabel('Year')
ax.set_ylabel('Phosphate')
ax.set_ylim(-0.01, 0.05)
ax.set_title('Offshore (>30km) phosphate concentrations over time (monthly averages)')