# -*- coding: utf-8 -*-

from biosim.cell import Highland, Lowland, Desert, Water
import textwrap

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

class TheIsland:
    """ This class will represent an island. """

    def __init__(self, landscape_of_cells, animals_on_island=None):
        """
        Create an island consisting of cells with attributes decided by
        the type of landscape.

        Parameters
        ----------
        landscape_of_cells : str
            multiline python string representing the landscape of the island.
        animals_on_island : list of dicts
            list of dictionaries with location of cell and population of
            animals in that cell.
        """
        # Check conditions for geography of island
        self.check_if_island_legal(landscape_of_cells)

        # Make landscape into list of lists
        self.landscape = self.landscape_to_list_of_lists(landscape_of_cells)
        self.row, self.col = len(self.landscape), len(self.landscape[0])

        # Create empty island, then construction of cells
        self.island_cells = None
        self.construct_island_with_cells()

        if animals_on_island:
            self.animals_on_island = animals_on_island
        else:
            self.animals_on_island = []

        self.add_animals_on_island(self.animals_on_island)

    @staticmethod
    def check_if_island_legal(geogr):
        """
        Checks if the landscape of the island follows the specifications.
            - only have 'W' around edges
            - no other characters than 'L', 'H', 'D' and 'W'
            - all lines in the string must have equal length, be aware that
              trailing whitespace will disrupt this.

        Raises
        -------
        ValueError
            if any of the specifications is violated.
        """
        geogr = textwrap.dedent(geogr)
        geogr_split = geogr.split('\n')
        len_first_line = len(geogr_split[0])
        for line in geogr_split:
            if len(line) != len_first_line:
                raise ValueError("All lines must have the same length.")

        for top, bottom in zip(geogr_split[0], geogr_split[-1]):
            if top != 'W' or bottom != 'W':
                raise ValueError("North or south of island is not only water.")

        for line in geogr_split:
            if line[0] != 'W' or line[-1] != 'W':
                raise ValueError("West or east side of island is not only water.")

        for line in geogr_split:
            for element in line:
                if element not in ['W', 'D', 'L', 'H']:
                    raise ValueError("Forbidden character, only 'W', 'D', 'L' and 'H' allowed.")

    @staticmethod
    def landscape_to_list_of_lists(landscape):
        """
        Makes a landscape string into a nested list (list of lists).

        Parameters
        ----------
        landscape : str
            multiline string representing the landscape of the island

        Returns
        -------
        list of lists
            an inner list is a row and an element of an inner list is the
            landscape of that cell.
        """
        landscape = textwrap.dedent(landscape)
        landscape_split = landscape.split('\n')
        return [list(line) for line in landscape_split]

    def construct_island_with_cells(self):
        """
        Construction the island by initialising a class for each of the
        landscape types. For each cell the class is initialized without
        animals.
        """
        self.island_cells = [[] for _ in range(self.row)]
        for x, row in enumerate(self.landscape):
            for cell in row:
                if cell == 'W':
                    self.island_cells[x].append(Water(animals_list=[]))
                elif cell == 'L':
                    self.island_cells[x].append(Lowland(animals_list=[]))
                elif cell == 'H':
                    self.island_cells[x].append(Highland(animals_list=[]))
                elif cell == 'D':
                    self.island_cells[x].append(Desert(animals_list=[]))

    def add_animals_on_island(self, new_animals):
        """
        Insert animals on island by adding animals to specified cells.

        Parameters
        ----------
        new_animals : list of dicts
            list of dictionaries with location of cell and population of
            animals in that cell.

        Raises
        ------
        ValueError
            if animals are being placed in water cells where they can't stay
        """
        for dictionary in new_animals:
            x, y = dictionary['loc']  # Location of a cell
            landscape_type = self.landscape[x-1][y-1]  # Landscape type of cell
            if landscape_type == 'W':
                raise ValueError("Animals can't stay in water")
            else:
                self.island_cells[x-1][y-1].add_animals_to_cell(dictionary['pop'])
                # add new animals to cell

    def all_animals_eat(self):
        """
        Letting the animals on the island eat.
        Looping through the cells of the island and letting the animals in
        each cell eat.
        """
        for row in self.island_cells:
            for cell in row:
                cell.animals_in_cell_eat()

    def animals_procreate(self):
        """
        Letting animals on the island procreate
        Looping through the cells of the island and giving the animals in the
        cells the change to procreate.
        """
        for row in self.island_cells:
            for cell in row:
                cell.birth()

    def where_can_animals_migrate_to(self, row, col):
        """
        Check if any of the neighboring adjacent cells are water, and
        returns the directions animals can migrate.

        Parameters
        ----------
        row : int
            row number as python uses it
        col : int
            column number as python uses it

        Returns
        -------
        directions : list
            list with possible directions
                - can move in all directions: ``['North', 'East', 'South', 'West']``
                - can only move to east and south: ``['East', 'South']``
        """
        directions = []
        if self.landscape[row-1][col] != 'W':
            directions.append('North')

        if self.landscape[row][col+1] != 'W':
            directions.append('East')

        if self.landscape[row+1][col] != 'W':
            directions.append('South')

        if self.landscape[row][col-1] != 'W':
            directions.append('West')

        return directions

    def migration(self):
        """
        Makes migration happen, by creating a ghost island where migrating
        animals makes a 'pit-stop' to a cell before getting added to that
        cell later in the 'real' island. This is to avoid animals migrating
        more than once.
        """
        # Make ghost island to store migrating animals
        ghost_island = [[[] for _ in range(self.col)] for _ in range(self.row)]

        # Placing migrating animals on the ghost island
        for x, row in enumerate(self.island_cells):
            for y, cell in enumerate(row):
                if self.landscape[x][y] != 'W':
                    pos_dir = self.where_can_animals_migrate_to(x, y)
                    # Finding animals wanting to migrate
                    north, east, south, west = cell.animals_migrate()
                    # Adding animals to ghost island
                    ghost_island = self.relocated_animals(x, y, pos_dir, north,
                                                          east, south, west,
                                                          ghost_island)
        # Adding migrating animals to cells
        for x, row in enumerate(self.island_cells):
            for y, cell in enumerate(row):
                cell.add_animals_after_migration(ghost_island[x][y])

    @staticmethod
    def relocated_animals(x, y, pos_dir, north, east, south, west, ghost_island):
        """
        Checks if animals can move or not for every direction. If the animals
        are allowed to move, these are added to that adjacent cell in the
        ghost island. Otherwise the animals are added to the original cell,
        which means that they do not migrate.

        Parameters
        ----------
        x : int
            row of original cell
        y : int
            column of original cell
        pos_dir : list
            possible directions animals can move along
        north : list
            animals wanting to move north
        east : list
            animals wanting to move east
        south : list
            animals wanting to move south
        west : list
            animals wanting to move west
        ghost_island : list of lists
            a replicate of the island, with lists of animals in each position.

        Returns
        -------
        ghost_island : list of lists
            updated ghost island with the animals added to cells for which
            they were allowed to move to.
        """
        if 'North' in pos_dir:
            ghost_island[x - 1][y] += north
        else:
            ghost_island[x][y] += north

        if 'East' in pos_dir:
            ghost_island[x][y + 1] += east
        else:
            ghost_island[x][y] += east

        if 'South' in pos_dir:
            ghost_island[x + 1][y] += south
        else:
            ghost_island[x][y] += south

        if 'West' in pos_dir:
            ghost_island[x][y - 1] += west
        else:
            ghost_island[x][y] += west

        return ghost_island

    def all_animals_age(self):
        """
        All animals on the island age.
        Looping through the cells of the island and letting the animals in the
        cells age.
        """
        for row in self.island_cells:
            for cell in row:
                cell.aging_of_animals()

    def all_animals_losses_weight(self):
        """
        All animals on the island losses weight (end of year).
        Looping through the cells of the island and letting the animals in the
        cells lose weight.
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.weight_loss_end_of_year()

    def animals_die(self):
        """
        Letting animals on the island die.
        Looping through the cells of the island and giving the animals in the
        cells a change to die.
        """
        for row in self.island_cells:
            for cell in row:
                cell.death()

    def annual_cycle(self):
        """
        The annual cycle on the island:
            1. Animals eats
            2. Animals procreates
            3. Animals migrates
            4. Animals age
            5. Animals looses weight
            6. Animals die
        """
        self.all_animals_eat()
        self.animals_procreate()
        self.migration()
        self.all_animals_age()
        self.all_animals_losses_weight()
        self.animals_die()

    def give_animals_in_cell(self, row, col):
        """
        Give lists of herbivores and carnivores in a given cell

        Parameters
        ----------
        row : int
            row number for cell
        col : int
            column number for cell

        Returns
        -------
        herbis : list
            list of herbivores in cell
        carnis : list
            list of carnivores in cell
        """
        herbis = self.island_cells[row-1][col-1].herbi_list
        carnis = self.island_cells[row-1][col-1].carni_list
        return herbis, carnis

    def herbis_and_carnis_on_island(self):
        """
        Make two islands, one for herbivores and one for carnivores.
        In each cell the number of herbivores/carnivores are stored. This is
        used to make heatmaps.

        Returns
        -------
        herbi_island : list
            island with number of herbivores in each cell
        carni_island : list
            island with number of carnivores in each cell
        """
        herbi_island = [[] for _ in range(self.row)]
        carni_island = [[] for _ in range(self.row)]
        for x, row in enumerate(self.island_cells):
            for cell in row:
                herbi_island[x].append(len(cell.herbi_list))
                carni_island[x].append(len(cell.carni_list))
        return herbi_island, carni_island

    def total_num_animals_on_island(self):
        """
        Calculates the total number of
            - animals on the island
            - herbivores on the island
            - carnivores on the island

        Returns
        -------
        tot_animal : int
            total number of animals on the island
        tot_herbi : int
            total number of herbivores on the island
        tot_carni : int
            total number of carnivores on the island
        """
        tot_herbi = 0
        tot_carni = 0
        for row in self.island_cells:
            for cell in row:
                tot_herbi += len(cell.herbi_list)
                tot_carni += len(cell.carni_list)
        tot_animal = tot_herbi + tot_carni
        return tot_animal, tot_herbi, tot_carni

    def collect_fitness_age_weight_herbi(self):
        """
        Collect the fitness, age and weight of all herbivores on the island in
        three lists.

        Returns
        -------
        fitness_herbi : list
            fitness for all herbivores on the island
        age_herbi : list
            age for all herbivores on the island
        weight_herbi : list
            weight for all herbivores on the island
        """
        fitness_herbi = []
        age_herbi = []
        weight_herbi = []
        for row in self.island_cells:
            for cell in row:
                fitness, age, weight = cell.collect_fitness_age_weight_herbi()
                fitness_herbi += fitness
                age_herbi += age
                weight_herbi += weight

        return fitness_herbi, age_herbi, weight_herbi

    def collect_fitness_age_weight_carni(self):
        """
        Collect the fitness, age and weight of all carnivores on the island in
        three lists.

        Returns
        -------
        fitness_carni : list
            fitness for all carnivores on the island
        age_carni : list
            age for all carnivores on the island
        weight_carni : list
            weight for all carnivores on the island
        """
        fitness_carni = []
        age_carni = []
        weight_carni = []
        for row in self.island_cells:
            for cell in row:
                fitness, age, weight = cell.collect_fitness_age_weight_carni()
                fitness_carni += fitness
                age_carni += age
                weight_carni += weight

        return fitness_carni, age_carni, weight_carni
