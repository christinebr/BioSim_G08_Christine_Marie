# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
grid = fig.add_gridspec(ncols=3, nrows=3, wspace=0.2, hspace=0.4)
ax1 = fig.add_subplot(grid[0, 0])
ax3 = fig.add_subplot(grid[0, 2])
ax4 = fig.add_subplot(grid[1, 0])
ax6 = fig.add_subplot(grid[1, 2])
ax7 = fig.add_subplot(grid[2, 0])
ax8 = fig.add_subplot(grid[2, 1])
ax9 = fig.add_subplot(grid[2, 2])
fig.show()

# General stuff for the plot
# Fontsizes to be used on the titles of all plots
font = 8
# Fontsizes to be used on the axes of all plots
font_axes = 8


def map_of_island(geogr):
    """
    Plotting a map of the island.
    Initial code for this function was taken from Hans Ekkehard Plesser
    from nmbu_inf200_june2020 repository inside the directories examples->plotting
    filename: mapping.py

    Parameters
    ----------
    geogr: [str] Multiline string representing the landscape on the island.
    """
    # Colors to be used for the different landscapes on the island
    #                   R    G    B
    rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                 'L': (0.0, 0.6, 0.0),  # dark green
                 'H': (0.5, 1.0, 0.5),  # light green
                 'D': (1.0, 1.0, 0.5)}  # light yellow

    geogr_rgb = [[rgb_value[column] for column in row]
                 for row in geogr.splitlines()]

    ax1.imshow(geogr_rgb)
    ax1.set_xticks(range(len(geogr_rgb[0])))
    ax1.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=font_axes)
    ax1.set_yticks(range(len(geogr_rgb)))
    ax1.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=font_axes)

    ax1.set_title('The island', fontsize=font)

def heatmaps_sepcies_dist(herbis_dist, carnis_dist, cmax_animals):
    """
    Makes heatmaps showing the distribution of herbivore and carnivare distribution on the island.
    Parameters
    ----------
    herbis_dist: [list of lists] Amount of herbivores in each cell.
    carnis_dist: [list of lists] Amount of carnivores in each cell.
    cmax_animals: [dict] Maximum values for colorbars of herbivores and carnivores.
    """
    width_island = len(herbis_dist[0])
    height_island = len(herbis_dist)
    # Herbivores distribution
    im = ax4.imshow(herbis_dist, cmap='viridis')
    ax4.set_title('Herbivore distribution', fontsize=font)
    fig.colorbar(im, ax=ax4, orientation='vertical', max=cmax_animals['Herbivore'])
    ax4.set_xticks(range(width_island))
    ax4.set_xticklabels(range(1, 1 + width_island), fontsize=font_axes)
    ax4.set_yticks(range(height_island))
    ax4.set_yticklabels(range(1, 1 + height_island), fontsize=font_axes)

    # Carnivores distribution
    im = ax6.imshow(carnis_dist, cmap='viridis')
    ax6.set_title('Carnivore distribution', fontsize=font)
    fig.colorbar(im, ax=ax6, orientation='vertical', max=cmax_animals['Carnivore'])
    ax6.set_xticks(range(width_island))
    ax6.set_xticklabels(range(1, 1 + width_island), fontsize=font_axes)
    ax6.set_yticks(range(height_island))
    ax6.set_yticklabels(range(1, 1 + height_island), fontsize=font_axes)

def histograms(herbi_properties, carni_properties, hist_specs):
    """
    Makes histograms for the properties fitness, age and weight for herbivores and arnivores.
    Parameters
    ----------
    herbi_properties: [list of lists] List of lists with fitness, age and weight for all herbivores.
    carni_properties: [list of list] List of list with fitness, age, weight for all carnivores.
    hist_specs: [dict of dict] Dictionary with dictionaries, with specifications for the histograms.

    Returns
    -------
    Plots histograms
    """
    for property, specs in hist_specs.items():
        if property == 'fitness':
            ax7.hist(herbi_properties[0], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='blue')
            ax7.hist(carni_properties[0], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='red')
            ax7.set_title('Fitness', fontsize=font)
            xticks = np.linspace(0, specs['max'], 5)
            ax7.set_xticks(xticks)
            ax7.set_xticklabels(xticks, fontsize=font_axes)
        if property == 'age':
            ax8.hist(herbi_properties[1], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='blue')
            ax8.hist(carni_properties[1], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='red')
            ax8.set_title('Age', fontsize=font)
            xticks = np.linspace(0, specs['max'], 4)
            ax8.set_xticks(xticks)
            ax8.set_xticklabels(xticks, fontsize=font_axes)
        if property == 'weight':
            ax9.hist(herbi_properties[2], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='blue')
            ax9.hist(carni_properties[2], binwith=specs['delta'], range=(0, specs['max']),
                     histtype='stepfilled', fill=False, edgecolor='red')
            ax9.set_title('Weight', fontsize=font)
            xticks = np.linspace(0, specs['max'], 4)
            ax9.set_xticks(xticks)
            ax9.set_xticklabels(xticks, fontsize=font_axes)




if __name__ == '__main__':
    geogr = """WWWWW
    WWLHW
    WDDLW
    WWWWW
    """