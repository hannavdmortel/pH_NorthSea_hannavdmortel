import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from cartopy import crs as ccrs, feature as cfeature
import xarray as xr
import cmocean

fpath = "C:/Users/hanna/Documents/GitHub/"

#IMPORT STATION DATA
northsea = pd.read_csv(fpath + "pH-North-Sea/Maps/data/coordinates_stations.csv")

#IMPORT BATHYMETRY DATA
gebco = xr.open_dataset(fpath + "python-tutorials/data/gebco_2020_noordzee.nc")

#CREATE FIGURE
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson())
ax.set_extent([2.3, 7.3, 51.3, 54.9], crs=ccrs.PlateCarree())

#STATION CODES PER REGION
station_codes_wadden = ["BLAUWSOT", "DANTZGT", "EILDBG", 'HOLWDBG', 'MALZN', 'VLIESZD', 'WESTMP', 'ZOUTKPLZGT', 'ZUIDOLWNOT', 'DOOVBWT']
station_codes_nearshore = ["CALLOG4", "CALLOG10", "EGMAZE4", "EGMAZE10", "GOERE6", "GOERE10", "IJMDN3", "NOORDWK4", "NOORDWK10", "ROTTMPT20", "SCHOUWN1", "SCHOUWN4", "SCHOUWN10", "TERSLG10", "WALCRN4", "WALCRN10"]
station_codes_intermediate = ["CALLOG30", "CALLOG50", "EGMAZE20", "EGMAZE30", "EGMAZE50", "GOERE20", "GOERE30", "GOERE50", "NOORDWK20", "NOORDWK30", "NOORDWK50", "ROTTMPT30", "ROTTMPT50", "SCHOUWN20", "SCHOUWN30", "SCHOUWN50", "TERSLG30",  "TERSLG50", "WALCRN20", "WALCRN30", "WALCRN50"]
station_codes_offshore = ["CALLOG70", "EGMAZE70", "GOERE70", "NOORDWK70", "ROTTMPT70", "ROTTMPT100", "SCHOUWN70", "TERHDE70", "TERSLG70", "TERSLG100", "TERSLG135", "TERSLG175","WALCRN70"]

#ADD LOCATION LABELS
labels = {
    'BLAUWSOT': {'lon': 5.3, 'lat': 53.08},
    'DANTZGT': {'lon': 5.22, 'lat':53.49},
    'DOOVB': {'lon': 4.55, 'lat': 53.1},
    'EILDBG': {'lon': 6.3, 'lat': 53.3},
    'HOLWDBG': {'lon': 5.4, 'lat': 53.665},
    'MALZN':  {'lon': 4.95, 'lat': 52.92},
    'VLIES': {'lon': 4.73, 'lat': 53.2621},
    'WESTMP': {'lon': 5.35, 'lat': 53.26},
    'ZOUTKPLZGT': {'lon': 5.4, 'lat': 53.84},
    'ZUIDOLWNOT': {'lon': 6.52, 'lat': 53.45},
    
    'CALLOG': {'lon': 4.70187, 'lat': 52.77},
    'EGMAZE': {'lon': 4.63, 'lat': 52.59},
    'GOERE': {'lon': 3.94, 'lat': 51.8},
    'IJMDN': {'lon': 4.58, 'lat': 52.43},
    'NOORDWK': {'lon': 4.45413, 'lat': 52.23},
    'ROTTMPT': {'lon': 6.58, 'lat': 53.7},
    'SCHOUWN': {'lon': 3.67, 'lat': 51.64},
    'TERHDE': {'lon': 3.4, 'lat': 52.3},
    'TERSLG': {'lon': 4.3, 'lat': 53.58},
    'WALCRN': {'lon': 3.5, 'lat': 51.5}
    }

#Loop through dict
for key in labels:
    ax.text(labels[key]['lon'], labels[key]['lat'], key, 
            fontsize='xx-small',
            bbox ={'fc':'white', 'ec':'none','alpha':0.7, 'pad':1},
            transform=ccrs.PlateCarree()) 
    
#Add arrows
#ZOUTKPLZGT
plt.arrow(x=6.15, y=53.79,
          dx=-0.045, dy=-0.25, 
          length_includes_head=True,
          head_width=0.06, head_length=0.04,
          color='dimgrey', zorder=20,
          transform=ccrs.PlateCarree())
#HOLWDBG
plt.arrow(x=5.9, y=53.62,
          dx=0.035, dy=-0.12, 
          length_includes_head=True,
          head_width=0.06, head_length=0.04,
          color='dimgrey', zorder=20,
          transform=ccrs.PlateCarree())


#PLOT STATIONS
for y in range(60):
    #Wadden Sea
    for x in range(len(station_codes_wadden)):
        if northsea.station_code[y] == station_codes_wadden[x]:
            ax.scatter(northsea.lon_dd[y], northsea.lat_dd[y], 
                s=15, c='xkcd:light orange',
                linewidth=0.4, edgecolor='black', zorder=10,
                transform=ccrs.PlateCarree())
    #Nearshore
    for x in range(len(station_codes_nearshore)):  
        if northsea.station_code[y] == station_codes_nearshore[x]:
            ax.scatter(northsea.lon_dd[y], northsea.lat_dd[y], 
                s=15, c='royalblue',
                linewidth=0.4, edgecolor='black', zorder=10,
                transform=ccrs.PlateCarree())
    #Intermediate
    for x in range(len(station_codes_intermediate)):
        if northsea.station_code[y] == station_codes_intermediate[x]:
            ax.scatter(northsea.lon_dd[y], northsea.lat_dd[y], 
                s=15, c='xkcd:teal', 
                linewidth=0.4, edgecolor='black', zorder=10,
                transform=ccrs.PlateCarree())     
    #Offshore
    for x in range(len(station_codes_offshore)):
        if northsea.station_code[y] == station_codes_offshore[x]:
            ax.scatter(northsea.lon_dd[y], northsea.lat_dd[y], 
                s=15, c='xkcd:pink',
                linewidth=0.4, edgecolor='black', zorder=10,
                transform=ccrs.PlateCarree())


#BATHYMETRY
vmin = -50
vmax = 0
cmap = cmocean.cm.gray
cmap = cmocean.tools.crop_by_percent(cmap, 40, which='min')

# Draw bathymetry data
bathymetry = (
    gebco.elevation
    # .coarsen(lat=10, lon=10, boundary="trim").mean()
    .plot(
        add_colorbar=False,
        ax=ax,
        # cmap="Blues_r",
        cmap=cmap,
        transform=ccrs.PlateCarree(),
        vmin=vmin,
        vmax=vmax,
    )
)
cbar = plt.colorbar(bathymetry)
cbar.set_label("Depth (m)")
ticks = np.array(list(range(vmin, vmax + 1, 10)))
cbar.set_ticks(ticks)
cbar.set_ticklabels(-ticks)

#CARTOPY FEATURES
ax.add_feature(
    cfeature.NaturalEarthFeature(
        "physical", "land", "10m"
    ),
    facecolor=cfeature.COLORS['land'],
    edgecolor="grey",
)
ax.add_feature(
    cfeature.NaturalEarthFeature(
        "physical", "lakes", "10m"
    ),
    facecolor=cmap(1.0),
    edgecolor='grey',
)
ax.add_feature(
    cfeature.NaturalEarthFeature("physical","rivers_lake_centerlines","10m"), 
    edgecolor = 'teal', 
    facecolor="none")

#FIGURE FORMATTING
gl = ax.gridlines(alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False
#ax.set_title('Rijkswaterstaat Stations: North Sea & Wadden Sea')

plt.savefig(fpath +"pH-North-Sea/Maps/figures/all_stations_northsea_with_regions.png")




