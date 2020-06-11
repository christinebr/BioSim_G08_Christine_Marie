# -*- coding: utf-8 -*-
from biosim.animals import Herbivores, Carnivores
from biosim.cell import Water, Desert, Lowland, Highland


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
        pass

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
        elif landscape == 'D':
            Desert.set_params(params)
        elif landscape == 'W':
            Water.set_params(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulations while visualizing the result.

        Parameters
        ----------
        num_years: number of years to simulate
        vis_years: years between visualization updates
        img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered conseccutively
        """
        pass

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population: List of dictionaries specifying population
        """
        pass

    @property
    def year(self):
        """Last year simulated."""
        pass

    @property
    def num_animals(self):
        """Total number of animals on island."""
        pass

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass
