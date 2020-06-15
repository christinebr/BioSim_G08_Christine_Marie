# -*- coding: utf-8 -*-
from biosim.animals import Herbivores, Carnivores
from biosim.cell import Water, Desert, Lowland, Highland
from biosim.island import TheIsland
import random
import matplotlib.pyplot as plt
import numpy as np
from biosim.plotting import Plotting


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png'):
        """

        Parameters
        ----------
        island_map: Multi-line string specifying island geography
        ini_pop: List of dictionaries specifying initial population
        seed: Integer used as random number seed
        ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        cmax_animals: Dict specifying color-code limits for animal densities
        hist_specs: Specifications for histograms, see below
        img_base: String with beginning of file name for figure, including path
        img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automtically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
            {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self._isl = TheIsland(landscape_of_cells=island_map,
                              animals_on_island=ini_pop)
        self.island_map = island_map
        random.seed(seed)
        self.ymax_animals = ymax_animals
        if cmax_animals is None:
            self.vmax_h = 200
            self.vmax_c = 50
        else:
            self.vmax_h = cmax_animals['Herbivore']
            self.vmax_c = cmax_animals['Carnivore']

        if hist_specs is None:
            self._fit_max = 1.0
            self._fit_bins = int(self._fit_max/0.05)
            self._age_max = 60
            self._age_bins = int(self._age_max/2)
            self._weight_max = 60
            self._weight_bins = int(self._weight_max/2)
        else:
            if 'fitness' in hist_specs.keys():
                self._fit_max = hist_specs['fitness']['max']
                self._fit_bins = int(self._fit_max/hist_specs['fitness']['delta'])
            else:
                self._fit_max = 1.0
                self._fit_bins = int(self._fit_max/0.05)
            if 'age' in hist_specs.keys():
                self._age_max = hist_specs['age']['max']
                self._age_bins = int(self._age_max/hist_specs['age']['delta'])
            else:
                self._age_max = 60
                self._age_bins = int(self._age_max/2)
            if 'weight' in hist_specs.keys():
                self._weight_max = hist_specs['weight']['max']
                self._weight_bins = int(self._weight_max/hist_specs['weight']['delta'])
            else:
                self._weight_max = 60
                self._weight_bins = int(self._weight_max / 2)

        self.hist_specs = hist_specs  # should we check that only weight, age and fitness are given?
        self._img_base = img_base
        self._img_fmt = img_fmt

        self._year = 0
        self._final_year = None
        self._img_counter = 0

        self._fig = None
        self._map_ax = None
        self._img_ax = None
        self._line_ax = None
        self._line_h = None
        self._line_c = None
        self._herb_ax = None
        self._carn_ax = None
        self._img_ax_heat1 = None
        self._img_ax_heat2 = None
        self._fitness_ax = None
        self._age_ax = None
        self._weight_ax = None
        self._axt = None

        # General stuff for the plot
        # Fontsizes to be used on the titles of all plots
        self.font = 8
        # Fontsizes to be used on the axes of all plots
        self.font_axes = 8

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species: String, name of animal species
        params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivores.set_params(params)
        elif species == "Carnivore":
            Carnivores.set_params(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type

        Parameters
        ----------
        landscape: String, code letter for landscape
        params: Dict with valid parameter specification for landscape
        """
        if landscape == 'L':
            Lowland.set_params(params)
        elif landscape == 'H':
            Highland.set_params(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulations while visualizing the result.

        Parameters
        ----------
        num_years: number of years to simulate
        vis_years: years between visualization updates
        img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()
        self._plot_island()

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self._update_graphics()

            # if self._year % img_years == 0:
                # self._save_graphics()
            self._isl.annual_cycle()
            self._year += 1

    def _setup_graphics(self):
        """Creates subplots."""
        # Create figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add subplot for creating plot of island with imshow()
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            self._img_ax = None

        # Add count for years
        if self._axt is None:
            self._axt = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
            self._axt.axis('off')  # turn off coordinate system
        
        # Add subplot for animal count plot
        if self._line_ax is None:
            self._line_ax = self._fig.add_subplot(3, 3, 3)
            self._line_ax.set_ylim(0, 10000)
        
        self._line_ax.set_xlim(0, self._final_year + 1)
        self._line_setup_graph()

        # Add subplots for heatmaps
        if self._herb_ax is None and self._carn_ax is None:
            self._herb_ax = self._fig.add_subplot(3, 3, 4)
            self._carn_ax = self._fig.add_subplot(3, 3, 6)
            self._img_ax_heat1 = None
            self._img_ax_heat2 = None
        
        # Add subplots for histograms
        if self._fitness_ax is None and self._age_ax is None and self._weight_ax is None:
            self._fitness_ax = self._fig.add_subplot(3, 3, 7)
            self._fitness_ax.set_xlim([0, self._fit_max])
            self._fitness_ax.set_ylim([0, 2000])
            self._age_ax = self._fig.add_subplot(3, 3, 8)
            self._age_ax.set_xlim([0, self._age_max])
            self._age_ax.set_ylim([0, 2000])
            self._weight_ax = self._fig.add_subplot(3, 3, 9)
            self._weight_ax.set_xlim([0, self._weight_max])
            self._weight_ax.set_ylim([0, 2000])

    def _plot_island(self):
        """Create a map of the island."""
        """
        Plotting a map of the island.
        Initial code for this function was taken from Hans Ekkehard Plesser
        from nmbu_inf200_june2020 repository inside the directories examples->plotting
        filename: mapping.py

        Parameters
        ----------
        geogr: [str] Multiline string representing the landscape on the island.
        """
        island_map = self.island_map.replace(' ', '') + '\n'
        # Colors to be used for the different landscapes on the island
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        geogr_rgb = [[rgb_value[column] for column in row]
                     for row in island_map.splitlines()]

        self._img_ax = self._map_ax.imshow(geogr_rgb)
        self._map_ax.set_xticks(range(len(geogr_rgb[0])))
        self._map_ax.set_xticklabels(range(1, 1 + len(geogr_rgb[0])), fontsize=self.font_axes)
        self._map_ax.set_yticks(range(len(geogr_rgb)))
        self._map_ax.set_yticklabels(range(1, 1 + len(geogr_rgb)), fontsize=self.font_axes)

        self._map_ax.set_title('The island', fontsize=self.font)

    def _line_setup_graph(self):
        """Create the line graph/the animal count graph setup."""
        if self._line_h is None and self._line_c is None:
            line_h = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'b-')
            line_c = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'r-')
            self._line_h = line_h[0]
            self._line_c = line_c[0]
        else:
            xdata_h, ydata_h = self._line_h.get_data()
            xdata_c, ydata_c = self._line_c.get_data()
            xnew = np.arange(xdata_h[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._line_h.set_data(np.hstack((xdata_h, xnew)),
                                      np.vstack((ydata_h, ynew)))
                self._line_c.set_data(np.hstack((xdata_c, xnew)),
                                      np.vstack((ydata_c, ynew)))

    def _update_count(self):
        """Updates the counter."""
        self._axt.cla()
        self._axt.axis('off')
        template = '\n\nYear: {:5d}\n\nHerbivores - blue\nCarnivores - red'
        txt = self._axt.text(0.5, 0.5, template.format(0),
                             horizontalalignment='center',
                             verticalalignment='center',
                             transform=self._axt.transAxes)  # relative coordinates

        txt.set_text(template.format(self._year))

    def _update_heatmaps(self, herbi_map, carni_map):
        """Updates heatmaps of island."""
        if self._img_ax_heat1 is not None:
            self._img_ax_heat1.set_data(herbi_map)
        else:
            self._img_ax_heat1 = self._herb_ax.imshow(herbi_map,
                                                      interpolation='nearest',
                                                      vmin=0,
                                                      vmax=self.vmax_h)
            plt.colorbar(self._img_ax_heat1, ax=self._herb_ax, orientation='vertical')

        if self._img_ax_heat2 is not None:
            self._img_ax_heat2.set_data(carni_map)
        else:
            self._img_ax_heat2 = self._carn_ax.imshow(carni_map,
                                                      interpolation='nearest',
                                                      vmin=0,
                                                      vmax=self.vmax_c)
            plt.colorbar(self._img_ax_heat2, ax=self._carn_ax, orientation='vertical')

    def _update_histograms(self, herb_prop, carn_prob):
        """Update histograms."""
        self._fitness_ax.cla()
        self._age_ax.cla()
        self._weight_ax.cla()
        self._fitness_ax.hist(herb_prop[0], bins=self._fit_bins,
                              fill=False, edgecolor='blue')
        self._age_ax.hist(herb_prop[1], bins=self._age_bins,
                          fill=False, edgecolor='blue')
        self._weight_ax.hist(herb_prop[2], bins=self._weight_bins,
                             fill=False, edgecolor='blue')

        self._fitness_ax.hist(carn_prob[0], bins=self._fit_bins,
                              fill=False, edgecolor='red')
        self._age_ax.hist(carn_prob[1], bins=self._age_bins,
                          fill=False, edgecolor='red')
        self._weight_ax.hist(carn_prob[2], bins=self._weight_bins,
                             fill=False, edgecolor='red')

    def _update_line_graph(self, num_herb=0, num_carn=0):
        """Update the line graph/the animal count graph."""
        ydata_h = self._line_h.get_ydata()
        ydata_h[self._year] = num_herb
        self._line_h.set_ydata(ydata_h)

        ydata_c = self._line_c.get_ydata()
        ydata_c[self._year] = num_carn
        self._line_c.set_ydata(ydata_c)

    def _update_graphics(self):
        """Updates graphics each year."""
        _, h, c = self._isl.total_num_animals_on_island()
        self._update_line_graph(num_herb=h, num_carn=c)
        h_map, c_map = self._isl.herbis_and_carnis_on_island()
        self._update_heatmaps(herbi_map=h_map, carni_map=c_map)
        herb_properties = self._isl.collect_fitness_age_weight_herbi()
        carn_properties = self._isl.collect_fitness_age_weight_carni()
        self._update_histograms(herb_prop=herb_properties,
                                carn_prob=carn_properties)
        self._update_count()
        plt.pause(1e-6)

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population: List of dictionaries specifying population
        """
        self._isl.add_animals_on_island(new_animals=population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self._isl.total_num_animals_on_island()[0]

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        herbis = self._isl.total_num_animals_on_island()[1]
        carnis = self._isl.total_num_animals_on_island()[2]
        return {'Herbivore': herbis, 'Carnivore': carnis}

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass
