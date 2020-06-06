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

    def all_animals_eat(self, herbis, carnis, landscape):
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
        todo: are we supposed to use this kind of list?
                ini_herbs = [{'loc': (10, 10),
                              'pop': [{'species': 'Herbivore',
                                       'age': 5,
                                       'weight': 20}
                                      for _ in range(150)]}]
                ini_carns = [{'loc': (10, 10),
                              'pop': [ {'species': 'Carnivore',
                                        'age': 5,
                                        'weight': 20}
                                       for _ in range(40) ] }]
              thinking of landscape as:
                  ll = np.array([['W','W','W','W'],
                                 ['W','L','L','W'],
                                 ['W','H','H','W'],
                                 ['W','L','L','W'],
                                 ['W','W','W','W']])

        """
        # All herbivores on the island eat
        for dictionary in herbis:
            row, col = dictionary['loc']  # getting the location of the cell
            landscape_type = landscape[row, col]  # the landscape in the cell
            if landscape_type == 'L':
                low = Lowland(animals_list=dictionary['pop'], f_max=800.0)
                # don't put in 800.0 directly here?
                low.animals_eat()  # animals eat -> use Cell-method directly?
            elif landscape_type == 'H':
                high = Highland(animals_list=dictionary['pop'], f_max=300.0)
                # don't put in 300.0 directly here?
                high.animals_eat()  # animals eat -> use Cell-method directly?

        # All carnivores on the island eat
        for dictionary in carnis:
            row, col = dictionary['loc']  # getting the location of the cell
            landscape_type = landscape[row, col]  # the landscape in the cell
            if landscape_type == 'L':
                low = Lowland(animals_list=dictionary['pop'], f_max=800.0)
                # don't put in 800.0 directly here?
                low.animals_eat()  # animals eat -> use Cell-method directly?
            elif landscape_type == 'H':
                high = Highland(animals_list=dictionary['pop'], f_max=300.0)
                # don't put in 300.0 directly here?
                high.animals_eat()  # animals eat -> use Cell-method directly?


    def animals_procreate(self, herbis, carnis):
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
        for dictionary in herbis:
            cell = SingleCell(animals_list=dictionary['pop'])
            updated_pop_list = cell.birth()
            dictionary['pop'] = updated_pop_list

        for dictionary in carnis:
            cell = SingleCell(animals_list=dictionary['pop'])
            updated_pop_list = cell.birth()
            dictionary['pop'] = updated_pop_list



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

    def all_animals_age(self, herbis, carnis):

        for dictionary in herbis:
            cell = SingleCell(animals_list=herbis)
            cell.aging_of_animals()

        for dictionary in carnis:
            cell = SingleCell(animals_list=herbis)
            cell.aging_of_animals()

    def all_animals_losses_weight(self, herbis, carnis):
        for dictionary in herbis:
            cell = SingleCell(animals_list=herbis)
            cell.weight_loss_end_of_year()

        for dictionary in carnis:
            cell = SingleCell(animals_list=herbis)
            cell.weight_loss_end_of_year()

    def animals_die(self, herbis, carnis):
        for dictionary in herbis:
            cell = SingleCell(animals_list=herbis)
            cell.death()

        for dictionary in carnis:
            cell = SingleCell(animals_list=herbis)
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
        self.all_animals_eat(herbis, carnis)
        self.animals_procreate(herbis, carnis)
        # self.migration()
        self.all_animals_age(herbis, carnis)
        self.all_animals_losses_weight(herbis, carnis)
        self.animals_die(herbis, carnis)
        
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