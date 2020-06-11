# -*- coding: utf-8 -*-
import numpy as np
from biosim.cell import SingleCell, Highland, Lowland, Desert, Water
import textwrap


class TheIsland:
    """
    Keeps control of the island.

    Takes a matrix with the landscape types of each cell.
    """

    def __init__(self, landscape_of_cells, animals_on_island=None):
        """
        Parameters
        ----------
        landscape_of_cells: multiline python string
        animals_on_island: list of dictionaries
        """
        # Check conditions for geography of island
        self.check_if_island_legal(landscape_of_cells)
        # Turn into numpy array
        self.landscape = self.landscape_to_array(land=landscape_of_cells)
        self.row, self.colon = len(self.landscape), len(self.landscape[0])

        self.island_cells = []

        if animals_on_island:
            self.animals_on_island = animals_on_island
        else:
            self.animals_on_island = []

        self.construct_island_with_cells()
        self.add_animals_on_island(self.animals_on_island)

    def set_cell_params(self, landscape, new_params=None):
        """
        Update the parameters for each cell-type on the island
        Parameters
        ----------
        landscape: [str] landscape type: 'L', 'H', 'D' (or 'W')
        new_params: [dict] parameters for landscape
        """
        if landscape == 'L':
            Lowland.set_params(new_params)
        elif landscape == 'H':
            Highland.set_params(new_params)
        elif landscape == 'D':
            Desert.set_params(new_params)
        elif landscape == 'W':
            Water.set_params(new_params)

    def set_animal_params(self, speci, new_params=None):
        """
        Parameters
        ----------
        speci: [str] type of animal: Herbivore or Carnivore
        new_params: [dict] parameters for animals
        todo: is this ok? parameters for all animals will change?
        """
        for cell_type in [Lowland, Highland, Desert, Water]:
            cell_type.set_animals_params(speci, new_params)

    @staticmethod
    def check_if_island_legal(geogr):
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
        Takes in a multiline string and turns it into a nested list
        """
        land = textwrap.dedent(land)
        land_split = land.split('\n')
        return [list(line) for line in land_split]

    def construct_island_with_cells(self):  # RENAME THIS ONE
        """
        Sorting animals by location on the island
        """
        self.island_cells = [[[] for _ in range(self.colon)] for _ in range(self.row)]
        for x, row in enumerate(self.landscape):
            for y, col in enumerate(row):
                if col == 'W':
                    self.island_cells[x][y] = Water(animals_list=None)
                elif col == 'L':
                    self.island_cells[x][y] = Lowland(animals_list=None)
                elif col == 'H':
                    self.island_cells[x][y] = Highland(animals_list=None)
                elif col == 'D':
                    self.island_cells[x][y] = Desert(animals_list=None)

    def add_animals_on_island(self, new_animals):
        """
        Parameters
        ----------
        new_animals: list of dict ->
                    [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 25}, ... ]
        """
        for place in new_animals:
            x, y = place['loc']
            landscape_type = self.landscape[x-1][y-1]
            if landscape_type == 'W':
                # island_cells[x-1, y-1] = Water(animals_list=None)
                raise ValueError("Animals can't stay in water")
            else:
                self.island_cells[x-1][y-1].add_new_animals_to_cell(place['pop'])
                # add new animals to cell

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

    def all_animals_losses_weight(self):
        """
        Animals in each cell losses weight (end of year)
        """
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.weight_loss_end_of_year()

    def animals_die(self):
        for row in self.island_cells:
            for cell in row:
                if cell:  # nothing happens in water cell
                    cell.death()

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
        self.all_animals_eat()
        self.animals_procreate()
        # self.migration()
        self.all_animals_age()
        self.all_animals_losses_weight()
        self.animals_die()

    def total_num_animals_on_island(self):
        """Returns total number of animals on the island

        Returns:
        ----------
        Total number of animals on the island
        """
        tot_herbi = 0
        tot_carni = 0
        for row in self.island_cells:
            for cell in row:
                tot_herbi += len(cell.herbi_list)
                tot_carni += len(cell.carni_list)
        tot_animal = tot_herbi + tot_carni
        return tot_animal, tot_herbi, tot_carni


if __name__ == "__main__":
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 25}
                          for _ in range(10)]}]
    # Simplest island possible
    land = """\
                WWW
                WLW
                WWW"""
    isl = TheIsland(landscape_of_cells=land, animals_on_island=ini_herbs)
    print("Original landscape given in:\n", isl.landscape)
    isl.construct_island_with_cells()
    print("Landscape used in TheIsland-class\n", isl.island_cells)
    isl.add_animals_on_island(ini_herbs)
    print(isl.island_cells[1][1].get_params())

    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    isl.all_animals_eat()
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)

    print("Animals in cell before birth:", len(isl.island_cells[1][1].herbi_list))
    isl.animals_procreate()
    print("Animals in cell after birth:", len(isl.island_cells[1][1].herbi_list))

    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)
    isl.all_animals_age()
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    isl.all_animals_losses_weight()
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)

    print("Animals in cell before death:", len(isl.island_cells[1][1].herbi_list))
    isl.animals_die()
    print("Animals in cell after death:", len(isl.island_cells[1][1].herbi_list))

    # Start of year:
    print("\nBEFORE ANNUAL CYCLE")
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    print("Animals in cell:", len(isl.island_cells[1][1].herbi_list))
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    isl.annual_cycle()
    print("\nAFTER ANNUAL CYCLE")
    print("Weight of one herbivore:", isl.island_cells[1][1].herbi_list[0].weight)
    print("Animals in cell:", len(isl.island_cells[1][1].herbi_list))
    print("Age of one herbivore:", isl.island_cells[1][1].herbi_list[0].age)

    new = [{'loc': (2, 2),
            'pop':[{'species': 'Herbivore', 'age': 10, 'weight': 10},
                   {'species': 'Herbivore', 'age': 8, 'weight': 25},
                   {'species': 'Herbivore', 'age': 5, 'weight': 15},
                   {'species': 'Carnivore', 'age': 6, 'weight': 10},
                   {'species': 'Carnivore', 'age': 3, 'weight': 8},
                   {'species': 'Carnivore', 'age': 43, 'weight': 8}]
            }
           ]

    print("\nAnimals in cell before:",
          len(isl.island_cells[1][1].herbi_list+isl.island_cells[1][1].carni_list))
    isl.add_animals_on_island(new_animals=new)
    print("Animals in cell after:",
          len(isl.island_cells[1][1].herbi_list+isl.island_cells[1][1].carni_list))

    bigger_island = """\
                        WWWWW
                        WLLLW
                        WHWHW
                        WLDLW
                        WWWWW"""
    isl2 = TheIsland(landscape_of_cells=bigger_island)
    print("Original landscape given in:\n", isl2.landscape)
    isl2.construct_island_with_cells()
    print("Landscape used in TheIsland-class\n", isl2.island_cells)
