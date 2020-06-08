# -*- coding: utf-8 -*-
import numpy as np
from biosim.cell import SingleCell, Highland, Lowland, Desert  # , Water
import textwrap


class TheIsland:
    """
    Keeps control of the island.

    Takes a matrix with the landscape types of each cell.
    """

    def __init__(self, landscape_of_cells, animals_on_island=None):
        # Check conditions for geography of island
        self.test_if_island_legal(landscape_of_cells)
        # Turn into numpy array
        self.landscape = self.landscape_to_array(land=landscape_of_cells)
        self.row, self.colon = len(self.landscape), len(self.landscape[0])

        self.island_cells = []

        if animals_on_island:
            self.animals_on_island = animals_on_island
        else:
            self.animals_on_island = []

    @staticmethod
    def test_if_island_legal(geogr):
        """
        Test if the island follows the specifications.
        The string tha specify the island must only contain legal letters, i.e. L, H, W and D
        All the outermost cells must be of the water type.

        Returns
        -------
        Raises ValueError if any of the specifications is violated.

        Todo: This might be better to do in the __init__ section, and/or in biosim
        """
        geogr = textwrap.dedent(geogr)
        geogr_split = geogr.split('\n')
        len_first_line = len(geogr_split[0])
        for line in geogr_split:
            if len(line) != len_first_line:
                raise ValueError("All lines must have same length")

        for top, bottom in zip(geogr_split[0], geogr_split[-1]):
            if top != 'W' or bottom != 'W':
                raise ValueError("North and south of island is not only water")

        for line in geogr_split:
            if line[0] != 'W' or line[-1] != 'W':
                raise ValueError("West or east side of island is not only water")

        for line in geogr_split:
            for element in line:
                if element not in ['W', 'D', 'L', 'H']:
                    raise ValueError("Forbidden character, only 'W', 'D', 'L' and 'H' allowed")

    @staticmethod
    def landscape_to_array(land):
        """
        Takes in a multiline string and turns it into a np.array
        """
        land = textwrap.dedent(land)
        land_split = land.split('\n')
        return [list(line) for line in land_split]

    def sort_animals_by_cell(self):
        """
        Sorting animals by location on the island
        """
        self.island_cells = [[[] for _ in range(self.colon)] for _ in range(self.row)]

        for place in self.animals_on_island:
            x, y = place['loc']
            landscape_type = self.landscape[x-1][y-1]
            if landscape_type == 'W':
                # island_cells[x-1, y-1] = Water(animals_list=None)
                raise ValueError("Animals can't stay in water")
            if landscape_type == 'D':
                self.island_cells[x-1][y-1] = Desert(animals_list=place['pop'])
            if landscape_type == 'L':
                self.island_cells[x-1][y-1] = Lowland(animals_list=place['pop'])
            if landscape_type == 'H':
                self.island_cells[x-1][y-1] = Highland(animals_list=place['pop'])

    def all_animals_eat(self):
        """
        Params
        ------
        herbis: [list]
            list of dictionaries containing location of a cell and the
            population of herbivores in that cell
        carnis: [list]
            list of dictionaries containing location of a cell and the
            population of carnivores in that cell
        landscape: [narray]
            numpy array of the landscape of the island

        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # if cell = [] it is a water cell, no animals eat
                    cell.animals_in_cell_eat()

        # # All herbivores on the island eat
        # for dictionary in self.herbis:
        #     row, col = dictionary['loc']  # getting the location of the cell
        #     landscape_type = landscape[row, col]  # the landscape in the cell
        #     if landscape_type == 'L':
        #         low = Lowland(animals_list=dictionary['pop'], f_max=800.0)
        #         # don't put in 800.0 directly here?
        #         low.animals_eat()  # animals eat -> use Cell-method directly?
        #     elif landscape_type == 'H':
        #         high = Highland(animals_list=dictionary['pop'], f_max=300.0)
        #         # don't put in 300.0 directly here?
        #         high.animals_eat()  # animals eat -> use Cell-method directly?
        #
        # # All carnivores on the island eat
        # for dictionary in self.carnis:
        #     row, col = dictionary['loc']  # getting the location of the cell
        #     landscape_type = landscape[row, col]  # the landscape in the cell
        #     if landscape_type == 'L':
        #         low = Lowland(animals_list=dictionary['pop'], f_max=800.0)
        #         # don't put in 800.0 directly here?
        #         low.animals_eat()  # animals eat -> use Cell-method directly?
        #     elif landscape_type == 'H':
        #         high = Highland(animals_list=dictionary['pop'], f_max=300.0)
        #         # don't put in 300.0 directly here?
        #         high.animals_eat()  # animals eat -> use Cell-method directly?

    def animals_procreate(self):
        """
        Loops trough populated cells and animals in all cells have the change to procreate
        Parameters
        ----------
        herbis
        carnis

        todo: carnis and herbis have same structure as described in the method above

        Returns
        -------

        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.birth()

        # for dictionary in self.herbis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     updated_pop_list = cell.birth()
        #     dictionary['pop'] = updated_pop_list
        #
        # for dictionary in self.carnis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     updated_pop_list = cell.birth()
        #     dictionary['pop'] = updated_pop_list

    def migration(self):
        """
        Makes migration happen, updates amount of animals in each cell
        Returns
        -------

        todo: think that we should make list of choices like moving = ['L', 'R', 'T', 'B']
              for left, right, top and bottom, must use random.choice to pick a random, and use
              method form cell to get the probability for migration

        """
        pass

    def all_animals_age(self):
        """
        Animals in each cell age
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.aging_of_animals()
        # for dictionary in self.herbis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     cell.aging_of_animals()
        #
        # for dictionary in self.carnis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     cell.aging_of_animals()

    def all_animals_losses_weight(self):
        """
        Animals in each cell losses weight (end of year)
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.weight_loss_end_of_year()
        # for dictionary in self.herbis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     cell.weight_loss_end_of_year()
        #
        # for dictionary in self.carnis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     cell.weight_loss_end_of_year()

    def animals_die(self):
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.death()
        # for dictionary in self.herbis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     dictionary['pop'] = cell.death()
        #
        # for dictionary in self.carnis:
        #     cell = SingleCell(animals_list=dictionary['pop'])
        #     dictionary['pop'] = cell.death()

    def annual_cycle(self):
        """
        Makes the year happen.
        1. Animals eats, first herbivores, then carnivores
        2. Animals procreates
        3. Animals migrates
        4. Animals age
        5. Animals looses weight
        6. Animals die

        Returns
        -------
        Updates the list of animals for the two species at the end of the year.
        """
        self.all_animals_eat(landscape=self.landscapes)
        self.animals_procreate()
        # self.migration()
        self.all_animals_age()
        self.all_animals_losses_weight()
        self.animals_die()
        
if __name__ == "__main__":
    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(10)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]
    # Simplest island possible
    l = np.array([['W', 'W', 'W'], ['W', 'L', 'W'], ['W', 'W', 'W']])
    i = TheIsland(landscape_of_cells=l, herbis=ini_herbs)
    i.all_animals_eat(l)
    print(i.herbis)


    # A big but small island (only Lowland and Highland)
    ll = np.array([['W','W','W','W'],
                   ['W','L','L','W'],
                   ['W','H','H','W'],
                   ['W','L','L','W'],
                   ['W','W','W','W']])

    # landscape in cell 1,1:
    l[1,1]

    # only testing
    for r in l[1:-1]:
        for c in r[1:-1]:
            print(c)