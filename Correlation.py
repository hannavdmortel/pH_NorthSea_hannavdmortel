import numpy as np
import pyarrow.parquet as pq
from matplotlib import pyplot as plt
from scipy import stats

#CHOOSE STATION
#Case insensitive
stationcode = "terhde70"

filename = "C:/Users/hanna/Documents/Marine Sciences/NIOZ/CO2 flux and acidification North Sea/rws-the-olden-days/data/x13/"+ stationcode.upper() + ".parquet"
df = pq.read_table(source=filename).to_pandas()

#CHOOSE VARIABLES
#(+ _irregular, _seasonal or _trend, or datenum for time)
var1 = "pH_trend"
var2 = "spm_trend"

fig, ax = plt.subplots(dpi=300)

ax.scatter(df[var1], df[var2], s=20, c='xkcd:navy')
ax.set_title(stationcode.upper())
ax.set_xlabel(var1)
ax.set_ylabel(var2)

#LINEAR REGRESSION
#Convert to np array to use logical and drop nan for both
var1_np = df[var1].to_numpy()
var2_np = df[var2].to_numpy()
L = (~np.isnan(var1_np) & ~np.isnan(var2_np))
x = var1_np[L]
y = var2_np[L]

slope, intercept, rv, pv, se = stats.linregress(x, y)
var1_interp = np.linspace(np.min(x), np.max(x))
ax.plot(var1_interp, intercept + slope * var1_interp, c='red', label = 'linear')
