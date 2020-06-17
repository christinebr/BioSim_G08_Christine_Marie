# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from biosim.island import TheIsland


class Plotting:

    def __init__(self, num_years):

        # Initialising figure with subplots
        self.fig = plt.figure()
        grid = self.fig.add_gridspec(ncols=3, nrows=3, wspace=0.2, hspace=0.4)
        self.ax1 = self.fig.add_subplot(grid[0, 0])
        self.ax3 = self.fig.add_subplot(grid[0, 2])
        self.ax4 = self.fig.add_subplot(grid[1, 0])
        self.ax6 = self.fig.add_subplot(grid[1, 2])
        self.ax7 = self.fig.add_subplot(grid[2, 0])
        self.ax8 = self.fig.add_subplot(grid[2, 1])
        self.ax9 = self.fig.add_subplot(grid[2, 2])
        self.fig.show()

        # General stuff for the plot
        # Fontsizes to be used on the titles of all plots
        self.font = 8
        # Fontsizes to be used on the axes of all plots
        self.font_axes = 8

        self.tot_herbis = []
        self.tot_carnis = []
        self.num_years = num_years

        self.herbis_line = self.ax3.plot(np.arange(self.num_years),
                                         np.full(self.num_years, np.nan), 'b-')[0]
        self.carnis_line = self.ax3.plot(np.arange(self.num_years),
                                         np.full(self.num_years, np.nan), 'r-')[0]

    def map_of_island(self, geogr):
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

        self.ax1.imshow(geogr_rgb)
        self.ax1.set_xticks(range(len(geogr_rgb[0])))
        self.ax1.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=self.font_axes)
        self.ax1.set_yticks(range(len(geogr_rgb)))
        self.ax1.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=self.font_axes)

        self.ax1.set_title('The island', fontsize=self.font)

    def update_animal_count(self, year, tot_herbi, tot_carni):
        """
        Updating plot over total amount of herbivores and carnivores on the island.
        Parameters
        ----------
        year
        tot_herbi
        tot_carni
        """
        y_herbis = self.herbis_line.get_ydata()
        y_carnis = self.carnis_line.get_ydata()

        y_herbis[year] = tot_herbi
        y_carnis[year] = tot_carni

        self.herbis_line.set_ydata(y_herbis)
        self.carnis_line.set_ydata(y_carnis)

    def heatmaps_sepcies_dist(self, herbis_dist, carnis_dist, cmax_animals):
        """
        Makes heatmaps showing the distribution of herbivore and carnivare
        distribution on the island.
        Parameters
        ----------
        herbis_dist: [list of lists]
            Amount of herbivores in each cell.
        carnis_dist: [list of lists]
            Amount of carnivores in each cell.
        cmax_animals: [dict]
            Maximum values for colorbars of herbivores and carnivores.
        """
        width_island = len(herbis_dist[0])
        height_island = len(herbis_dist)
        # Herbivores distribution
        im = self.ax4.imshow(herbis_dist, cmap='viridis')
        self.ax4.set_title('Herbivore distribution', fontsize=self.font)
        self.fig.colorbar(im, ax=self.ax4, orientation='vertical', max=cmax_animals['Herbivore'])
        self.ax4.set_xticks(range(width_island))
        self.ax4.set_xticklabels(range(1, 1 + width_island), fontsize=self.font_axes)
        self.ax4.set_yticks(range(height_island))
        self.ax4.set_yticklabels(range(1, 1 + height_island), fontsize=self.font_axes)

        # Carnivores distribution
        im = self.ax6.imshow(carnis_dist, cmap='viridis')
        self.ax6.set_title('Carnivore distribution', fontsize=self.font)
        self.fig.colorbar(im, ax=self.ax6, orientation='vertical', max=cmax_animals['Carnivore'])
        self.ax6.set_xticks(range(width_island))
        self.ax6.set_xticklabels(range(1, 1 + width_island), fontsize=self.font_axes)
        self.ax6.set_yticks(range(height_island))
        self.ax6.set_yticklabels(range(1, 1 + height_island), fontsize=self.font_axes)

    def histograms(self, herbi_properties, carni_properties, hist_specs):
        """
        Makes histograms for the properties fitness, age and weight for
        herbivores and arnivores.
        Parameters
        ----------
        herbi_properties: [list of lists]
            List of lists with fitness, age and weight for all herbivores.
        carni_properties: [list of list]
            List of list with fitness, age, weight for all carnivores.
        hist_specs: [dict of dict]
            Dictionary with dictionaries, with specifications for the
            histograms.

        Returns
        -------
        Plots histograms
        """
        for prop, specs in hist_specs.items():
            if prop == 'fitness':
                self.ax7.hist(herbi_properties[0], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='blue')
                self.ax7.hist(carni_properties[0], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='red')
                self.ax7.set_title('Fitness', fontsize=self.font)
                xticks = np.linspace(0, specs['max'], 5)
                self.ax7.set_xticks(xticks)
                self.ax7.set_xticklabels(xticks, fontsize=self.font_axes)
            if prop == 'age':
                self.ax8.hist(herbi_properties[1], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='blue')
                self.ax8.hist(carni_properties[1], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='red')
                self.ax8.set_title('Age', fontsize=self.font)
                xticks = np.linspace(0, specs['max'], 4)
                self.ax8.set_xticks(xticks)
                self.ax8.set_xticklabels(xticks, fontsize=self.font_axes)
            if prop == 'weight':
                self.ax9.hist(herbi_properties[2], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='blue')
                self.ax9.hist(carni_properties[2], binwith=specs['delta'], range=(0, specs['max']),
                              histtype='stepfilled', fill=False, edgecolor='red')
                self.ax9.set_title('Weight', fontsize=self.font)
                xticks = np.linspace(0, specs['max'], 4)
                self.ax9.set_xticks(xticks)
                self.ax9.set_xticklabels(xticks, fontsize=self.font_axes)

    def text_axis(self):
        """
        Plots the counter an some informational text.
        """
        pass


if __name__ == '__main__':
    geogr = """WWWWW
    WWLHW
    WDDLW
    WWWWW
    """

    geogr_island = """\
               WWWWW
               WWLHW
               WDDLW
               WWWWW"""

    ini_animals = [{'loc': (2, 4),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20} for _ in range(200)]
                    + [{'species': 'Carnivore',
                        'age': 5,
                        'weight': 20} for _ in range(20)]
                    },
                   {'loc': (3, 3),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20} for _ in range(200)]
                    + [{'species': 'Carnivore',
                        'age': 5,
                        'weight': 20} for _ in range(20)]}
                   ]

    isl = TheIsland(geogr_island)

