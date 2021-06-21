import xarray as xr, numpy as np
from matplotlib import pyplot as plt
from cartopy import crs as ccrs, feature as cfeature
import cmocean

gebco = xr.open_dataset("C:/Users/hanna/Documents/GitHub/python-tutorials/data/gebco_2020_noordzee.nc")

#%% Visualise the dataset
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection=ccrs.Robinson())

vmin = -50
vmax = 0
cmap = cmocean.cm.gray
#cmap = cmocean.tools.crop(cmap, vmin, vmax, 0)
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

# Add land areas
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
    facecolor="none", zorder=10)

ax.add_feature(cfeature.BORDERS, edgecolor='darkgrey')

#Adding labels
ax.text(4.92, 53.05, "Wadden Sea", fontsize='x-small',
        rotation = 30,
        transform=ccrs.PlateCarree())

ax.text(5.15, 52.53, "IJssel", fontsize='x-small',
        rotation = 30,
        transform=ccrs.PlateCarree())

ax.text(2.7, 52.5, "Southern Bight", fontsize='small',
        transform=ccrs.PlateCarree())

ax.text(4.3, 52.05, "Rhine-Meuse-Scheldt Delta", fontsize='x-small',
        transform=ccrs.PlateCarree())
# ax.text(4.49, 52, "Rotterdam", fontsize='small',
#         transform=ccrs.PlateCarree())

# ax.scatter(4.4777, 51.9244,
#         s=10, c='black', linewidth=0.4, edgecolor='black',
#         zorder=20, transform=ccrs.PlateCarree())

# Axis settings
ax.set_extent([2.2, 7.2, 51.48, 54.58])
gl = ax.gridlines(alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False

plt.savefig("figures/Map-with-bathymetry.png")
