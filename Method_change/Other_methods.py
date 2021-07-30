import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.ticker import (AutoMinorLocator)

fpath = "C:/Users/hanna/Documents/GitHub/"

rws_file = fpath + 'rws-the-olden-days/data/old_rws_data/rws_compilation.parquet'
rws_all = pd.read_parquet(rws_file, engine='auto')
rws = rws_all

var = 'spm'

#Choose North Sea stations
rws = rws_all.loc[["CALLOG4", 
                    "CALLOG10", 
                    "CALLOG30", 
                    "EGMAZE4", 
                    "EGMAZE10", 
                    "EGMAZE20", 
                    "EGMAZE30", 
                    "GOERE6", 
                    "GOERE10", 
                    "GOERE20", 
                    "GOERE30", 
                    "NOORDWK4", 
                    "NOORDWK10", 
                    "NOORDWK20", 
                    "NOORDWK30", 
                    "ROTTMPT20", 
                    "ROTTMPT30", 
                    "SCHOUWN1", 
                    "SCHOUWN4", 
                    "SCHOUWN10", 
                    "SCHOUWN20", 
                    "SCHOUWN30", 
                    "TERSLG10", 
                    "TERSLG30", 
                    "WALCRN4", 
                    "WALCRN10", 
                    "WALCRN20", 
                    "WALCRN30", 
                    "CALLOG50", 
                    "CALLOG70", 
                    "EGMAZE50", 
                    "EGMAZE70", 
                    "GOERE50", 
                    "GOERE70", 
                    "NOORDWK50", 
                    "NOORDWK70", 
                    "ROTTMPT50", 
                    "ROTTMPT70", 
                    "ROTTMPT100", 
                    "SCHOUWN50", 
                    "SCHOUWN70", 
                    "TERHDE70", 
                    "TERSLG50", 
                    "TERSLG70", 
                    "TERSLG100", 
                    "TERSLG135", 
                    "TERSLG175", 
                    "WALCRN50", 
                    "WALCRN70"]]

#Group by datetime
grouped_month = rws.groupby(pd.Grouper(key = 'datetime', freq="M")).mean()

#Create logical to ignore nan pH values
L0 = ~np.isnan(grouped_month[var])
gmL_x = grouped_month.datenum[L0]
gmL_y = grouped_month[var][L0]

fig, ax = plt.subplots(dpi=300, figsize=(8,2))

ax.scatter(gmL_x.index, gmL_y,
           alpha=0.5, s=40, c='xkcd:coral', edgecolor='none')
ax.set_yticks
ax.set_xlabel('Year')
ax.set_ylabel(var)
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.set_axisbelow(True)
ax.grid(axis='both')
ax.grid(axis='both', which='minor', linestyle=':', linewidth='0.5')
ax.set_xlim(gmL_x.min()-150, gmL_x.max()+150)
#ax.set_ylim(top=0.1)

ax.set_title('Monthly average {} measurements Dutch Coastal Zone'.format(var))
plt.savefig("figures/{}.png".format(var))