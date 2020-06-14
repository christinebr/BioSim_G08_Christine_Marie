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