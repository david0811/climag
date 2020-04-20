import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Import Scientific Colormaps
cm_data = np.loadtxt("/Users/davidlafferty/Projects/misc/ScientificColourMaps5/cork/cork.txt")[::-1]
cork_map = LinearSegmentedColormap.from_list("Cork", cm_data)
cm_data = np.loadtxt("/Users/davidlafferty/Projects/misc/ScientificColourMaps5/batlow/batlow.txt")
batlow_map = LinearSegmentedColormap.from_list("Batlow", cm_data)
cm_data = np.loadtxt("/Users/davidlafferty/Projects/misc/ScientificColourMaps5/berlin/berlin.txt")
berlin_map = LinearSegmentedColormap.from_list("Berlin", cm_data)

# Import plotting shapefiles
county_shp = gp.read_file('../../data/conus_shp/conus_plot/final/counties_contig_plot.shp')
county_shp["GEOID"] = county_shp["GEOID"].astype(str).str.zfill(5)

states = gp.read_file('../../data/conus_shp/conus_plot/final/states_contig_plot.shp')
coast = gp.read_file('../../data/conus_shp/conus_plot/final/coast_contig_plot.shp')


def PlotAgVar(data, model, agvar, title, vmin, vmax, cmap, save=False):
    """
    Plots the county-level map of a pre-calculated verification metric for one models

    Inputs:
        - data: Pandas DataFrame of pre-calculated verification metric for all models
        - model: String of model name to be plotted
        - agvar: Agricultural variable to be plotted ('gdd', 'egdd', 'prcp')
        - metric: String of metric (to be used in plot asthetics)
        - vmin/vmax : Min/Max values to be plotted
        - cmap: Colormap to use in plot ('batlow' or 'broc')
        - save: Boolean, savefig or not
    """
    # Select Ag variable
    data = data.reset_index()
    data = data[data.AgVar == agvar]
    # Merge county-level shapefile with data
    data['GEOID'] = data["GEOID"].astype(str).str.zfill(5)
    data.set_index(['GEOID'], inplace=True)
    data_shp = pd.merge(county_shp, data.filter([model]), on="GEOID", how="outer", copy=False)
    # Do the plot!
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cax.tick_params(labelsize=20)
    data_shp.dropna().plot(column=model, ax=ax, cax=cax, legend=True, cmap=globals()[cmap + '_map'], vmin=vmin, vmax=vmax)
    states.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    coast.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=20)
    plt.tight_layout()
    plt.show()


def PlotYield(data, model, title, vmin, vmax, cmap, save=False):
    """
    Plots the county-level map of a pre-calculated verification metric for one model

    Inputs:
        - data: Pandas DataFrame of pre-calculated verification metric for all models
        - model: String of model name to be plotted
        - metric: String of metric (to be used in plot asthetics)
        - vmin/vmax : Min/Max values to be plotted
        - cmap: Colormap to use in plot ('batlow' or 'broc')
        - save: Boolean, savefig or not
    """
    # Merge county-level shapefile with data
    data = data.reset_index()
    data['GEOID'] = data["GEOID"].astype(str).str.zfill(5)
    data.set_index(['GEOID'], inplace=True)
    data_shp = pd.merge(county_shp, data.filter([model]), on="GEOID", how="outer", copy=False)
    # Do the plot!
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cax.tick_params(labelsize=20)
    data_shp.dropna().plot(column=model, ax=ax, cax=cax, legend=True, cmap=globals()[cmap + '_map'], vmin=vmin, vmax=vmax)
    data_shp[data_shp[model].isna()].plot(ax=ax, color="lightgray")
    states.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    coast.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=20)
    plt.tight_layout()
    plt.show()


def PlotRatio(data, model, vmin, vmax, cmap, title, agvar=False, save=False):
    """
    Plots the county-level map of a pre-calculated verification metric for one models

    Inputs:
        - data: Pandas DataFrame of pre-calculated verification metric for all models
        - model: String of model name to be plotted
        - agvar: Agricultural variable to be plotted ('gdd', 'egdd', 'prcp')
        - vmin/vmax : Min/Max values to be plotted
        - cmap: Colormap to use in plot ('batlow' or 'broc')
        - save: Boolean, savefig or not
    """
    # Select Ag variable
    if agvar == False:
        data = data.reset_index()
    else:
        data = data.reset_index()
        data = data[data.AgVar == agvar]
    # Merge county-level shapefile with data
    data['GEOID'] = data["GEOID"].astype(str).str.zfill(5)
    data.set_index(['GEOID'], inplace=True)
    data_shp = pd.merge(county_shp, data.filter([model]), on="GEOID", how="outer", copy=False)
    # Do the plot!
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cax.tick_params(labelsize=20)
    data_shp.dropna().plot(column=model, ax=ax, cax=cax, legend=True, cmap=globals()[cmap + '_map'], vmin=vmin, vmax=vmax)
    states.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    coast.geometry.boundary.plot(ax=ax, linewidth=0.5, edgecolor="black", color=None)
    if agvar == False:
        data_shp[data_shp[model].isna()].plot(ax=ax, color="lightgray")
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=20)
    plt.tight_layout()
    plt.show()
