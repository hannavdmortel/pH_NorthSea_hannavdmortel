import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from cartopy import crs as ccrs, feature as cfeature
import seaborn as sns

#IMPORT DATA
northsea = pd.read_csv(
    "data/coordinates_stations.csv")

northsea["lon_radians"] = np.deg2rad(northsea.lon_dd)
northsea["lat_radians"] = np.deg2rad(northsea.lat_dd)

#CREATE FIGURE
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson())
#ax.set_extent([2.3, 7.3, 51.3, 54.9], crs=ccrs.PlateCarree())

#ADD LOCATION LABELS
# (Put into dict for simplification)
# ax.text(5.3, 53.08, "BLAUWSOT", fontsize='xx-small',
#         bbox ={'fc':'red', 'ec':'none',
#                 'alpha':0.5, 'pad':1},
#         transform=ccrs.PlateCarree())
ax.text(4.70187, 52.77, "CALLOG", fontsize='xx-small',
        bbox ={'fc':'chocolate', 'ec':'none',
                'alpha':0.5, 'pad':1},
        transform=ccrs.PlateCarree()) 
ax.text(5.22, 53.49, "DANTZGT", fontsize='xx-small', 
        bbox ={'fc':'goldenrod', 'ec':'none',
                'alpha':0.5, 'pad':1},
          transform=ccrs.PlateCarree())
# ax.text(4.55, 53.1, "DOOVB", fontsize='xx-small', 
#         bbox ={'fc':'gold', 'ec':'none',
#                'alpha':0.5, 'pad':1},
#         transform=ccrs.PlateCarree())
# ax.text(4.63, 52.59, "EGMAZE", fontsize='xx-small', 
#         bbox ={'fc':'yellowgreen', 'ec':'none',
#                'alpha':0.5, 'pad':1},
#         transform=ccrs.PlateCarree())
# ax.text(6.3, 53.3, "EILDBG", fontsize='xx-small', 
#          bbox ={'fc':'greenyellow', 'ec':'none',
#                'alpha':0.6, 'pad':1},
#         transform=ccrs.PlateCarree())
ax.text(3.94, 51.8, "GOERE", fontsize='xx-small', 
        bbox ={'fc':'lightgreen', 'ec':'none',
                'alpha':0.7, 'pad':1},
        transform=ccrs.PlateCarree())
# ax.text(5.4, 53.665, "HOLWDBG", fontsize='xx-small',
#          bbox ={'fc':'lime', 'ec':'none',
#                'alpha':0.4, 'pad':1},
#         transform=ccrs.PlateCarree())
# ax.text(4.58, 52.43, "IJMDN", fontsize='xx-small',
#         bbox ={'fc':'deeppink', 'ec':'none',
#                'alpha':0.6, 'pad':1},
#         transform=ccrs.PlateCarree())
# ax.text(4.95, 52.93, "MALZN", fontsize='xx-small', 
#         bbox ={'fc':'mediumspringgreen', 'ec':'none',
#                'alpha':0.5, 'pad':1},
#         transform=ccrs.PlateCarree())
ax.text(4.45413, 52.23, "NOORDWK", fontsize='xx-small',
        bbox ={'fc':'turquoise', 'ec':'none',
                'alpha':0.6, 'pad':1},
        transform=ccrs.PlateCarree())
ax.text(5.65, 53.95, "ROTTMPT", fontsize='xx-small',
        bbox ={'fc':'darkturquoise', 'ec':'none',
                'alpha':0.4, 'pad':1},
        transform=ccrs.PlateCarree())
ax.text(3.67, 51.64, "SCHOUWN", fontsize='xx-small', 
        bbox ={'fc':'cornflowerblue', 'ec':'none',
                'alpha':0.7, 'pad':1},
        transform=ccrs.PlateCarree())
# ax.text(3.4, 52.3, "TERHDE", fontsize='xx-small', 
#         bbox ={'fc':'navy', 'ec':'none',
#                'alpha':0.35, 'pad':1},
#         transform=ccrs.PlateCarree())
ax.text(4.3, 53.58, "TERSLG", fontsize='xx-small',
        bbox ={'fc':'mediumblue', 'ec':'none',
                'alpha':0.4, 'pad':1},
        transform=ccrs.PlateCarree())
# ax.text(4.73, 53.2621, "VLIES", fontsize='xx-small',
#         bbox ={'fc':'springgreen', 'ec':'none',
#                'alpha':0.6, 'pad':1},
#         transform=ccrs.PlateCarree())
ax.text(3.5, 51.5, "WALCRN", fontsize='xx-small', 
        bbox ={'fc':'darkviolet', 'ec':'none',
                'alpha':0.4, 'pad':1},
        transform=ccrs.PlateCarree())
ax.text(5.35, 53.26, "WESTMP", fontsize='xx-small', 
        bbox ={'fc':'orchid', 'ec':'none',
                'alpha':0.6, 'pad':1},
        transform=ccrs.PlateCarree())
ax.text(5.5, 53.65, "ZOUTKPLZGT", fontsize='xx-small', 
          bbox ={'fc':'hotpink', 'ec':'none',
                'alpha':0.6, 'pad':1},
        transform=ccrs.PlateCarree())
# ax.text(6.52, 53.45, "ZUIDOLWNOT", fontsize='xx-small', 
#          bbox ={'fc':'indigo', 'ec':'none',
#                'alpha':0.48, 'pad':1},
#         transform=ccrs.PlateCarree())

#COLORS STATION MARKERS
color_labels = northsea.location_code.unique()
rgb_values = sns.color_palette("hls", 21)
color_map = dict(zip(color_labels, rgb_values))

#SELECTING STATIONS
chosen_stations = [
    "ZOUTKPLZGT",
    "DANTZGT",
    "WESTMP",
    "ROTTMPT70",
    "TERSLG50",
    "TERSLG100",
    "TERSLG135",
    "CALLOG4",
    "NOORDWK4",
    "GOERE6",
    "GOERE10",
    "GOERE20",
    "SCHOUWN1",
    "SCHOUWN4",
    "SCHOUWN10",
    "WALCRN4",
    "WALCRN20",
    "WALCRN70"]

#LOGICAL
northsea["chosen_stations"] = False
for i in range(len(northsea.station_code)):
    if northsea.station_code[i] in chosen_stations:
        northsea.chosen_stations[i] = True
L = northsea.chosen_stations
northsea_L = northsea[L]

#SELECTING STATIONS WITHOUT DATA
no_data = [
    "CALLOG10",
    "CALLOG50",
    "MALZN",
    "VLIESZD"]

#LOGICAL
northsea["no_data"] = False
for i in range(len(northsea.station_code)):
    if northsea.station_code[i] in no_data:
        northsea.no_data[i] = True
L2 = northsea.no_data
northsea_L2 = northsea[L2]

#PLOT NON-CHOSEN STATIONS CLEAR
X = ~northsea.chosen_stations
ax.scatter(northsea[X].lon_dd, northsea[X].lat_dd,
           s=10, zorder=10, color='none',
           linewidth=0.2, edgecolor = 'black',
           transform=ccrs.PlateCarree())

#PLOT TRUE STATIONS IN COLOUR
ax.scatter(northsea_L.lon_dd, northsea_L.lat_dd, 
           s=10, c=northsea_L.location_code.map(color_map), 
           linewidth=0.4, edgecolor='black', zorder=10,
           transform=ccrs.PlateCarree())

#PLOT STATIONS WITHOUT DATA
ax.scatter(northsea_L2.lon_dd, northsea_L2.lat_dd, 
           s=10, c='grey', zorder=20, alpha=0.8,
           linewidth=0.2, edgecolor='grey',
           transform=ccrs.PlateCarree())

#CARTOPY FEATURES
ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "land", "10m"), 
    facecolor = cfeature.COLORS['land'], 
    alpha=0.6, 
    edgecolor = "none")

ax.add_feature(
    cfeature.NaturalEarthFeature("physical", "ocean", "10m"), 
    facecolor = cfeature.COLORS['water'], 
    alpha=0.6,
    edgecolor = "none")

ax.add_feature(
    cfeature.NaturalEarthFeature("physical","lakes","10m"), 
    facecolor = cfeature.COLORS['water'], 
    alpha=0.6,
    edgecolor="none")

ax.add_feature(
    cfeature.NaturalEarthFeature("physical","rivers_lake_centerlines","10m"), 
    edgecolor = cfeature.COLORS['water'], 
    facecolor="none")

#FIGURE FORMATTING
gl = ax.gridlines(alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False
ax.set_title('Seasonal: pH vs spm')

plt.savefig("C:/Users/hanna/Documents/GitHub/pH-North-Sea/Maps/figures/seasonal_pH_vs_spm.png")




