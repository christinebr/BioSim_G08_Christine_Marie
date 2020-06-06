# -*- coding: utf-8 -*-
import numpy as np
from biosim.cell import SingleCell, Highland, Lowland

class TheIsland:
    """
    Keeps control of the island.

    Takes a matrix with the landscape types of each cell.
    """

    def __init__(self, landscape_of_cells):
        self.landscapes = landscape_of_cells
        self.row, self.colon = landscape_of_cells.shape[0], landscape_of_cells.shape[1]

    def test_if_island_legal(self):
        """
        Test if the island follows the specifications.
        The string tha specify the island must only contain legal letters, i.e. L, H, W and D
        All the outermost cells must be of the water type.

        Returns
        -------
        Raises ValueError if any of the specifications is violated.

        Todo: This might be better to do in the __init__ section, and/or in biosim
        """
        pass

    def all_animals_eat(self):
        """
        todo: are we supposed to use this kind of list?
                ini_herbs = [{'loc': (10, 10),
                              'pop': [{'species': 'Herbivore',
                                       'age': 5,
                                       'weight': 20}
                                      for _ in range(150)]}]
                ini_carns = [{'loc': (10, 10),
                              'pop': [{'species': 'Carnivore',
                                       'age': 5,
                                       'weight': 20}
                                      for _ in range(40)]}]
        """

        pass

    def animals_procreate(self):
        pass


    def migration(self):
        """
        Makes migration happen, updates amount of animals in each cell
        Returns
        -------

        """
        pass

    def all_animals_age(self):
        pass

    def all_animals_losses_weight(self):
        pass

    def animals_die(self):
        pass

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
        
if __name__ == "__main__":
    # Simplest island possible
    l = np.array([['W', 'W', 'W'], ['W', 'L', 'W'], ['W', 'W', 'W']])

    # A big but small island (only Lowland and Highland)
    ll = np.array([['W','W','W','W'],['W','L','L','W'], ['W','H','H','W'],['W','L','L','W'], ['W','W','W','W']])

    # landscape in cell 1,1:
    l[1,1]

    # only testing
    for r in l[1:-1]:
        for c in r[1:-1]:
            print(c)