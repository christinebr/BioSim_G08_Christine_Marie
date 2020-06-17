# -*- coding: utf-8 -*-

"""
Taken directly from:https://github.com/heplesser/nmbu_inf200_june2020/blob/7240186b0a97b24a325fa68280be344e5e49a9da/examples/randvis_project/randvis/simulation.py#L234

todo: MUST MAKE SOME CHANGES HERE!!! made some changed -> more or not?

:mod:`biosim.simulation` provides the user interface to the package.
Each simulation is represented by a :class:`BioSim` instance. On each
instance, the :meth:`BioSim.simulate` method can be called as often as
you like to simulate a given number of years.
The state of the system is visualized as the simulation runs, at intervals
that can be chosen. The graphics can also be saved to file at regular
intervals. By calling :meth:`BioSim.make_movie` after a simulation is complete,
individual graphics files can be combined into an animation.
.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<http://ffmpeg.org>` and `<http://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.
Example
--------
::
    sim = BioSim(island_map, ini_pop, seed, ymax_animals, cmax_animals,
                 hist_specs, img_base, img_fmt='png')
    sim.simulate(num_years, vis_years, img_years)
    sim.make_movie()

This code
#. creates a island according to the ``island_map``, which contain different
   types of landscape. the initial population is placed on the island, and it
   can consist of two types of animals: herbivores and carnivores. the random
   number generator uses the seed given.;
#. performs a simulation of the ecosystem on the island for ``num_years``
   years. the graphics is updated after number of years given to ``vis_years``,
   and the figure are saved after every ``img_years``;
#. creates a movie from the individual figures saved.
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
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif

# https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
# Set fontsize for text, axes title and tick labels
plt.rc('font', size=8)
plt.rc('axes', titlesize=8)
plt.rc('xtick', labelsize=5)
plt.rc('ytick', labelsize=5)


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
        self.width = 0
        self.height = 0
        if ymax_animals is None:
            self.ymax_animals = 5000
        else:
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
            self._set_hist_specs(hist_specs)

        self._img_base = img_base
        self._img_fmt = img_fmt

        self._year = 0
        self._final_year = None
        self._img_no = 0

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
        Setting maximum value and the bin width for histograms if provided
        in hist_specs. Init calls this method for sorting out this.

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
        img_years : int
            years between visualizations saved to files (default: vis_years)

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

            if self._year % img_years == 0:
                self._save_graphics()
            self._isl.annual_cycle()
            self._year += 1

    def _setup_graphics(self):
        """
        Creates the figure with different subplots. Subplots are:
            - Map of island
            - Counting years
            - Plot of number of animals on the island
            - Heatmaps for distribution of herbivores and carnivores
            - Histograms showing distribution of animals fitness, age and weight.
        """
        # Create figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add subplot for creating plot of island
        if self._map_ax is None:
            self._map_ax = self._fig.add_axes([0.1, 0.63, 0.3, 0.3])
            self._img_ax = None

        # Add count for years
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

        # Add subplots for heatmaps
        if self._herb_ax is None and self._carn_ax is None:
            self._herb_ax = self._fig.add_axes([0.15, 0.26, 0.34, 0.3])
            self._carn_ax = self._fig.add_axes([0.6, 0.26, 0.34, 0.3])
            self._img_ax_heat1 = None
            self._img_ax_heat2 = None
            self._herb_ax.set_title('Herbivore distribution')
            self._carn_ax.set_title('Carnivore distribution')

        # Add subplots for histograms
        if self._fitness_ax is None and self._age_ax is None and self._weight_ax is None:
            self._fitness_ax = self._fig.add_axes([0.1, 0.08, 0.23, 0.1])
            self._age_ax = self._fig.add_axes([0.4, 0.08, 0.23, 0.1])
            self._weight_ax = self._fig.add_axes([0.7, 0.08, 0.23, 0.1])

    def _plot_island(self):
        """
        Plots a map of the island.
        Initial code for this function was taken from Hans Ekkehard Plesser
        from nmbu_inf200_june2020 repository inside the directories examples->plotting
        filename: mapping.py
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
        already made, it makes sure it's updated. It also makes the axes follow
        specifications.
        """
        if self._line_h is None and self._line_c is None:
            line_h = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'b-')
            line_c = self._line_ax.plot(np.arange(0, self._final_year),
                                        np.full(self._final_year, np.nan),
                                        'r-')
            self._line_ax.legend(['Herbivore', 'Carnivore'],
                                 loc='upper left', fontsize=4)

            self._line_h = line_h[0]
            self._line_c = line_c[0]
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
        self._axt.cla()
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
        """
        if self._img_ax_heat1 is not None:
            self._img_ax_heat1.set_data(herbi_map)
        else:
            self._img_ax_heat1 = self._herb_ax.imshow(herbi_map,
                                                      interpolation='nearest',
                                                      vmin=0, vmax=self.vmax_h)
            plt.colorbar(self._img_ax_heat1, ax=self._herb_ax,
                         shrink=0.7, orientation='vertical')
            self._herb_ax.set_xticks(range(self.width))
            self._herb_ax.set_xticklabels(range(1, 1 + self.width))
            self._herb_ax.set_yticks(range(self.height))
            self._herb_ax.set_yticklabels(range(1, 1 + self.height))

        if self._img_ax_heat2 is not None:
            self._img_ax_heat2.set_data(carni_map)
        else:
            self._img_ax_heat2 = self._carn_ax.imshow(carni_map,
                                                      interpolation='nearest',
                                                      vmin=0, vmax=self.vmax_c)
            plt.colorbar(self._img_ax_heat2, ax=self._carn_ax,
                         shrink=0.7, orientation='vertical')
            self._carn_ax.set_xticks(range(self.width))
            self._carn_ax.set_xticklabels(range(1, 1 + self.width))
            self._carn_ax.set_yticks(range(self.height))
            self._carn_ax.set_yticklabels(range(1, 1 + self.height))

    def _update_histograms(self, herb_prop, carn_prob):
        """
        Remakes histograms. Makes sure axes follows specifications.
        """
        self._fitness_ax.cla()
        self._fitness_ax.set_xlim([0, self._fit_max])
        self._fitness_ax.set_ylim([0, 2000])
        self._fitness_ax.set_title('Fitness')
        self._age_ax.cla()
        self._age_ax.set_xlim([0, self._age_max])
        self._age_ax.set_ylim([0, 2000])
        self._age_ax.set_title('Age')
        self._weight_ax.cla()
        self._weight_ax.set_xlim([0, self._weight_max])
        self._weight_ax.set_ylim([0, 2000])
        self._weight_ax.set_title('Weight')

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
        """
        ydata_h = self._line_h.get_ydata()
        ydata_h[self._year] = num_herb
        self._line_h.set_ydata(ydata_h)

        ydata_c = self._line_c.get_ydata()
        ydata_c[self._year] = num_carn
        self._line_c.set_ydata(ydata_c)
        if num_herb > self.ymax_animals or num_carn > self.ymax_animals:
            new_ymax = max(num_herb, num_carn) + 2000
            self._line_ax.set_ylim(0, round(new_ymax, -3))

    def _update_graphics(self):
        """
        Updates graphics each year. Uses the methods for updating plots. Makes
        a pause so that the plot are visible between updates.
        """
        _, h, c = self._isl.total_num_animals_on_island()
        self._update_line_graph(num_herb=h, num_carn=c)
        h_map, c_map = self._isl.herbis_and_carnis_on_island()
        self._update_heatmaps(herbi_map=h_map, carni_map=c_map)
        herb_properties = self._isl.collect_fitness_age_weight_herbi()
        carn_properties = self._isl.collect_fitness_age_weight_carni()
        self._update_histograms(herb_prop=herb_properties,
                                carn_prob=carn_properties)
        self._update_count()
        plt.pause(1e-3)

    def _save_graphics(self):
        """Saves the figure/graphics to file."""

        if self._img_base is None:
            return

        plt.savefig('{}_{:05d}.{}'.format(self._img_base, self._img_no, self._img_fmt))
        self._img_no += 1

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : list of dicts
            List of dictionaries specifying population
        """
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
            Number of animals per species in island, as dictionary."""
        herbis = self._isl.total_num_animals_on_island()[1]
        carnis = self._isl.total_num_animals_on_island()[2]
        return {'Herbivore': herbis, 'Carnivore': carnis}

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
