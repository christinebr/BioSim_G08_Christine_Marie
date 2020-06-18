# -*- coding: utf-8 -*-

"""
Initial code taken from:
https://github.com/heplesser/nmbu_inf200_june2020/blob/master/examples/
randvis_project/randvis/simulation.py
and the project descriptions. These are written by Hans Ekkehard Plesser.

The initial specifications for ffmpeg are still unchanged. We've done a lot of
modifications else.
"""

from biosim.animals import Herbivores, Carnivores
from biosim.cell import Lowland, Highland
from biosim.island import TheIsland
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import subprocess
import os

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
# _CONVERT_BINARY/magick is only needed if you want to create animated GIFs.
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif

# Set fontsize for text, axes title and tick labels
plt.rc('font', size=8)
plt.rc('axes', titlesize=8)
plt.rc('xtick', labelsize=5)
plt.rc('ytick', labelsize=5)


class BioSim:
    """"
    This is the class for simulation of the island. It also takes care of the
    graphics.
    """

    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt='png'):
        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        ymax_animals : int or None
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict or None
            Dictionary specifying color-code limits for animal densities
        hist_specs : dict or None
            Specifications for histograms, see below
        img_base : str
            String with beginning of file name for figure, including path
        img_fmt : str
            String with file type for figures, e.g. 'png'


        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
            {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a
        histogram shall be shown. For each property, a dictionary providing the
        maximum value and the bin width must be given, e.g.,
            {'weight': {'max': 80, 'delta': 2},
             'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        # Initialize the island
        self._isl = TheIsland(landscape_of_cells=island_map,
                              animals_on_island=ini_pop)
        self.island_map = island_map

        # Initialize a pseudo-random number generator
        random.seed(seed)

        self.width = 0  # will later be set to the width of the island
        self.height = 0  # will later be set to the height of the island

        # Setting the y-axis limit for the animal count plot
        if ymax_animals is None:
            self.ymax_animals = 5000
        else:
            self.ymax_animals = ymax_animals

        # Setting the max value for the colorbars of the heatmaps
        if cmax_animals is None:
            self.cmax_h = 200  # for herbivores distribution
            self.cmax_c = 50  # for carnivores distribution
        else:
            self.cmax_h = cmax_animals['Herbivore']
            self.cmax_c = cmax_animals['Carnivore']

        # Setting the max value and number of bins for the histograms
        if hist_specs is None:
            self._fit_max = 1.0
            self._fit_bins = int(self._fit_max / 0.05)
            self._age_max = 60
            self._age_bins = int(self._age_max / 2)
            self._weight_max = 60
            self._weight_bins = int(self._weight_max / 2)
        else:
            self._set_hist_specs(hist_specs)

        self._img_base = img_base  # beginning of filename for saving image
        self._img_fmt = img_fmt  # file type of image

        self._year = 0  # year count, updating this for each year
        self._final_year = None  # final year, will be set later
        self._img_no = 0  # count for image, updating for every file saved

        # Creating all axes used for plotting
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

    def _set_hist_specs(self, hist_specs):
        """
        Setting maximum value and the bin width (calculation number of bins)
        for histograms if provided in hist_specs. Init uses this method.

        Parameters
        ----------
        hist_specs : dict
            Specifications for histograms, for more information, see the
            general documentation for the class.
        """
        if 'fitness' in hist_specs.keys():
            self._fit_max = hist_specs['fitness']['max']
            self._fit_bins = int(self._fit_max / hist_specs['fitness']['delta'])
        else:
            self._fit_max = 1.0
            self._fit_bins = int(self._fit_max / 0.05)
        if 'age' in hist_specs.keys():
            self._age_max = hist_specs['age']['max']
            self._age_bins = int(self._age_max / hist_specs['age']['delta'])
        else:
            self._age_max = 60
            self._age_bins = int(self._age_max / 2)
        if 'weight' in hist_specs.keys():
            self._weight_max = hist_specs['weight']['max']
            self._weight_bins = int(self._weight_max / hist_specs['weight']['delta'])
        else:
            self._weight_max = 60
            self._weight_bins = int(self._weight_max / 2)

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of animal species, 'Herbivore' or 'Carnivore'
        params : dict
            Dictionary with valid parameter specification for species
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
        landscape : str
            Code letters for landscape, 'L' or 'H'
        params : dict
            Dictionary with valid parameter specification for landscape
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
        num_years : int
            number of years to simulate
        vis_years : int
            years between visualization updates
        img_years : int or None
            years between visualizations saved to files (default: vis_years)


        Image files will be numbered consecutively
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()  # setting up the graphics
        self._plot_island()  # plotting the map of the island

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self._update_graphics()  # updating the graphics

            if self._year % img_years == 0:
                self._save_graphics()  # saving the graphics

            self._isl.annual_cycle()  # letting one year on the island pass
            self._year += 1  # updating the year count

    def _setup_graphics(self):
        """
        Creates the figure with different subplots. Subplots are:
            - Map of island
            - Counting years
            - Plot of number of animals on the island
            - Heatmaps for distribution of herbivores and carnivores
            - Histograms showing distribution of animals fitness, age and
              weight.
        """
        # Create figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add axes for creating plot of island
        if self._map_ax is None:
            self._map_ax = self._fig.add_axes([0.1, 0.63, 0.3, 0.3])
            self._img_ax = None

        # Add axes count for years
        if self._axt is None:
            self._axt = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
            self._axt.axis('off')  # turn off coordinate system

        # Add subplot for animal count plot
        if self._line_ax is None:
            self._line_ax = self._fig.add_subplot(3, 3, 3)
            self._line_ax.set_ylim(0, self.ymax_animals)

        self._line_ax.set_xlim(0, self._final_year + 1)
        self._line_setup_graph()
        self._line_ax.set_title('Animal count')

        # Add axes for heatmaps for herbivore and carnivore distribution
        if self._herb_ax is None and self._carn_ax is None:
            self._herb_ax = self._fig.add_axes([0.15, 0.26, 0.34, 0.3])
            self._carn_ax = self._fig.add_axes([0.6, 0.26, 0.34, 0.3])
            self._img_ax_heat1 = None
            self._img_ax_heat2 = None
            self._herb_ax.set_title('Herbivore distribution')
            self._carn_ax.set_title('Carnivore distribution')

        # Add axes for histograms of fitness, age and weight
        if self._fitness_ax is None and self._age_ax is None and self._weight_ax is None:
            self._fitness_ax = self._fig.add_axes([0.1, 0.08, 0.23, 0.1])
            self._age_ax = self._fig.add_axes([0.4, 0.08, 0.23, 0.1])
            self._weight_ax = self._fig.add_axes([0.7, 0.08, 0.23, 0.1])

    def _plot_island(self):
        """
        Plots a map of the island.
        Initial code for this function was taken from Hans Ekkehard Plesser:
        https://github.com/heplesser/nmbu_inf200_june2020/blob/master/examples
        /plotting/mapping.py
        """
        island_map = self.island_map.replace(' ', '') + '\n'
        # Colors to be used for the different landscapes on the island
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        labels = {'W': 'Water', 'L': 'Lowland', 'H': 'Highland', 'D': 'Desert'}
        # create patches as legend
        patches = [mpatches.Patch(color=rgb_value[key], label=labels[key])
                   for key in rgb_value.keys()]

        geogr_rgb = [[rgb_value[column] for column in row]
                     for row in island_map.splitlines()]
        self.width = len(geogr_rgb[0])
        self.height = len(geogr_rgb)
        self._img_ax = self._map_ax.imshow(geogr_rgb)
        self._map_ax.set_xticks(range(self.width))
        self._map_ax.set_xticklabels(range(1, 1 + self.width))
        self._map_ax.set_yticks(range(self.height))
        self._map_ax.set_yticklabels(range(1, 1 + self.height))
        self._map_ax.set_title('The island')
        self._map_ax.legend(handles=patches, loc=4, borderaxespad=0.,
                            fontsize=4)

    def _line_setup_graph(self):
        """
        Creates the line graph/the animal count graph setup. If this graph are
        already made, it makes sure it's updated by updating the xdata and
        ydata.
        """
        if self._line_h is None and self._line_c is None:
            line_h = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'b-')
            line_c = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'r-')
            self._line_h = line_h[0]
            self._line_c = line_c[0]

            self._line_ax.legend(['Herbivore', 'Carnivore'],
                                 loc='upper left', fontsize=4)
        else:
            xdata_h, ydata_h = self._line_h.get_data()
            xdata_c, ydata_c = self._line_c.get_data()
            xnew = np.arange(xdata_h[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._line_h.set_data(np.hstack((xdata_h, xnew)),
                                      np.hstack((ydata_h, ynew)))
                self._line_c.set_data(np.hstack((xdata_c, xnew)),
                                      np.hstack((ydata_c, ynew)))

    def _update_count(self):
        """
        Updates the counter that keeps track of which year of the simulation we
        are looking at.
        """
        self._axt.cla()  # clear axes
        self._axt.axis('off')
        template = '\n\nYear: {:5d}\n\nHerbivores - blue\nCarnivores - red'
        txt = self._axt.text(0.5, 0.5, template.format(0),
                             horizontalalignment='center',
                             verticalalignment='center',
                             transform=self._axt.transAxes)  # relative coordinates

        txt.set_text(template.format(self._year))

    def _update_heatmaps(self, herbi_map, carni_map):
        """
        Remakes heatmas of herbivores and carnivores. Makes sure axes
        follows specifications.

        Parameters
        ----------
        herbi_map : list of lists
            represent the number of herbivores in each cell of the island
        carni_map : list of lists
            represent the number of carnivores in each cell of the island
        """
        # Update heatmap for herbivore distribution
        if self._img_ax_heat1 is not None:
            self._img_ax_heat1.set_data(herbi_map)
        else:
            self._img_ax_heat1 = self._herb_ax.imshow(herbi_map,
                                                      interpolation='nearest',
                                                      vmin=0, vmax=self.cmax_h)
            plt.colorbar(self._img_ax_heat1, ax=self._herb_ax,
                         shrink=0.8, orientation='vertical')
            self._herb_ax.set_xticks(range(self.width))
            self._herb_ax.set_xticklabels(range(1, 1 + self.width))
            self._herb_ax.set_yticks(range(self.height))
            self._herb_ax.set_yticklabels(range(1, 1 + self.height))

        # Update heatmap for carnivore distribution
        if self._img_ax_heat2 is not None:
            self._img_ax_heat2.set_data(carni_map)
        else:
            self._img_ax_heat2 = self._carn_ax.imshow(carni_map,
                                                      interpolation='nearest',
                                                      vmin=0, vmax=self.cmax_c)
            plt.colorbar(self._img_ax_heat2, ax=self._carn_ax,
                         shrink=0.8, orientation='vertical')
            self._carn_ax.set_xticks(range(self.width))
            self._carn_ax.set_xticklabels(range(1, 1 + self.width))
            self._carn_ax.set_yticks(range(self.height))
            self._carn_ax.set_yticklabels(range(1, 1 + self.height))

    def _update_histograms(self, herb_prop, carn_prob):
        """
        Remakes histograms. Makes sure axes follows specifications.

        Parameters
        ----------
        herb_prop : list of lists
            lists of herbivores properties, first list is for fitness, second
            for age and third for weight
        carn_prob : list of lists
            lists of carnivores properties, first list is for fitness, second
            for age and third for weight
        """
        self._fitness_ax.cla()  # clear axes
        self._fitness_ax.set_xlim([0, self._fit_max])
        self._fitness_ax.set_ylim([0, 2000])
        self._fitness_ax.set_title('Fitness')
        self._age_ax.cla()  # clear axes
        self._age_ax.set_xlim([0, self._age_max])
        self._age_ax.set_ylim([0, 2000])
        self._age_ax.set_title('Age')
        self._weight_ax.cla()  # clear axes
        self._weight_ax.set_xlim([0, self._weight_max])
        self._weight_ax.set_ylim([0, 2000])
        self._weight_ax.set_title('Weight')

        # Plot histograms for herbivores properties
        self._fitness_ax.hist(herb_prop[0], bins=self._fit_bins,
                              range=(0, self._fit_max),
                              histtype='stepfilled', fill=False,
                              edgecolor='blue')
        self._age_ax.hist(herb_prop[1], bins=self._age_bins,
                          histtype='stepfilled', fill=False,
                          range=(0, self._age_max),
                          edgecolor='blue')
        self._weight_ax.hist(herb_prop[2], bins=self._weight_bins,
                             histtype='stepfilled', fill=False,
                             range=(0, self._weight_max),
                             edgecolor='blue')

        # Plot histograms for carnivores properties
        self._fitness_ax.hist(carn_prob[0], bins=self._fit_bins,
                              histtype='stepfilled', fill=False,
                              range=(0, self._fit_max),
                              edgecolor='red')
        self._age_ax.hist(carn_prob[1], bins=self._age_bins,
                          histtype='stepfilled', fill=False,
                          range=(0, self._age_max),
                          edgecolor='red')
        self._weight_ax.hist(carn_prob[2], bins=self._weight_bins,
                             histtype='stepfilled', fill=False,
                             range=(0, self._weight_max),
                             edgecolor='red')

    def _update_line_graph(self, num_herb=0, num_carn=0):
        """
        Update the line graph/the animal count graph.

        Parameters
        ----------
        num_herb : int
            total number of herbivores on the island
        num_carn : int
            total number of carnivores on the island
        """
        # Updating the ydata for herbivores
        ydata_h = self._line_h.get_ydata()
        ydata_h[self._year] = num_herb
        self._line_h.set_ydata(ydata_h)

        # Updating the ydata for carnivores
        ydata_c = self._line_c.get_ydata()
        ydata_c[self._year] = num_carn
        self._line_c.set_ydata(ydata_c)

        # Updating the y-axis limit for the animal count plot if number of
        # either herbivores or carnivores exceed the self.ymax_animals
        if num_herb > self.ymax_animals or num_carn > self.ymax_animals:
            self.ymax_animals = max(num_herb, num_carn) + 2000
            self._line_ax.set_ylim(0, round(self.ymax_animals, -3))

    def _update_graphics(self):
        """
        Updates graphics each year. Uses the methods for updating plots. Makes
        a pause so that the plot are visible between updates.
        """
        # Get number of herbivores and carnivores, and update animal count plot
        _, num_h, num_c = self._isl.total_num_animals_on_island()
        self._update_line_graph(num_herb=num_h, num_carn=num_c)

        # Get herbivores and carnivores distribution, and update the heatmaps
        h_map, c_map = self._isl.herbis_and_carnis_on_island()
        self._update_heatmaps(herbi_map=h_map, carni_map=c_map)

        # Get herbivores and carnivores properties, and update the histograms
        herb_properties = self._isl.collect_fitness_age_weight_herbi()
        carn_properties = self._isl.collect_fitness_age_weight_carni()
        self._update_histograms(herb_prop=herb_properties,
                                carn_prob=carn_properties)
        # Update the year count
        self._update_count()

        plt.pause(1e-3)

    def _save_graphics(self):
        """Saves the figure/graphics to file."""

        if self._img_base is None:
            return

        plt.savefig('{}_{:05d}.{}'.format(self._img_base,
                                          self._img_no,
                                          self._img_fmt))

        self._img_no += 1  # updating image number/count

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : list of dicts
            List of dictionaries specifying population
        """
        # Adding the population to the island
        self._isl.add_animals_on_island(new_animals=population)

    @property
    def year(self):
        """
        Makes it possible to get the last year simulated.

        Returns
        -------
        int
            Last year simulated.
        """

        return self._year

    @property
    def num_animals(self):
        """
        Makes it possible to get the number of animals on the island.

        Returns
        --------
        int
            Total number of animals on island.
        """

        return self._isl.total_num_animals_on_island()[0]

    @property
    def num_animals_per_species(self):
        """
        Makes it possible to get the number of animals on the island by specie.

        Returns
        -------
        dict
            Number of animals per species in island, as dictionary.
        """

        num_herbis = self._isl.total_num_animals_on_island()[1]
        num_carnis = self._isl.total_num_animals_on_island()[2]

        return {'Herbivore': num_herbis, 'Carnivore': num_carnis}

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Create MPEG4 movie from visualization images saved.

        Note
        ----
        Requires ffmpeg


        The movie is stored as img_base + movie_fmt
        """
        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(f"ERROR: ffmpeg failed with: {err}")
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(f"ERROR: convert failed with: {err}")
        else:
            raise ValueError(f"Unknown movie format: {movie_fmt}")
