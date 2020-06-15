# -*- coding: utf-8 -*-
from biosim.animals import Herbivores, Carnivores
from biosim.cell import Water, Desert, Lowland, Highland
from biosim.island import TheIsland
import random
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
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs  # should we check that only weight, age and fitness are given?
        self._img_base = img_base
        self._img_fmt = img_fmt

        self._year = 0
        self._final_year = None
        self._img_counter = 0

        self._fig = None
        self._map_ax = None
        self._ax1 = None
        self._line = None
        self._ax3 = None
        self._ax4 = None
        self._ax6 = None
        self._ax7 = None
        self._ax8 = None
        self._ax9 = None
        self._axt = None

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

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self._update_graphics()

            if self._year % img_years == 0:
                self._save_graphics()

            self._isl.annual_cycle()
            self._year += 1



        # plot = Plotting(num_years)
        # island_map = self.island_map.replace(' ', '') + '\n'
        # plot.map_of_island(island_map)
        # for year in num_years:
        #     herb = self.isl.total_num_animals_on_island[1]
        #     carn = self.isl.total_num_animals_on_island[2]
        #     plot.update_animal_count(num_years, herb, carn)
        #     animals = self.isl.herbis_and_carnis_on_island()
        #     plot.heatmaps_sepcies_dist(animals[0], animals[1], self.cmax_animals)
        #     herbi_prop = self.isl.collect_fitness_age_weight_herbi()
        #     carni_prop = self.isl.collect_fitness_age_weight_carni()
        #     plot.histograms(herbi_prop, carni_prop, self.hist_specs)
        #     plot.text_axis()
        #     self.isl.annual_cycle()

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population: List of dictionaries specifying population
        """
        self.isl.add_animals_on_island(new_animals=population)

    @property
    def year(self):
        """Last year simulated."""
        pass

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.isl.total_num_animals_on_island()[0]

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        herbis = self.isl.total_num_animals_on_island()[1]
        carnis = self.isl.total_num_animals_on_island()[2]
        return {'Herbivore': herbis, 'Carnivore': carnis}

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass
