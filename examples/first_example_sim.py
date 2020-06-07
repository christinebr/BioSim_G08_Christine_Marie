# -*- coding: utf-8 -*-
from biosim.island import TheIsland
import numpy as np
import matplotlib.pyplot as plt

"""
First try on a simulation
"""


if __name__ == '__main__':
    # Simplest island possible
    landscape = np.array([['W', 'W', 'W'],
                          ['W', 'L', 'W'],
                          ['W', 'W', 'W']])

    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                              for _ in range(10)]
                  }]

    isl = TheIsland(landscape_of_cells=landscape, herbis=ini_herbs)
    print(isl.herbis)
    plt.figure()
    for year in range(200):
        num_initial = len(isl.herbis[0]['pop'])
        isl.all_animals_eat(landscape)
        isl.animals_procreate()
        num_after_birth = len(isl.herbis[0]['pop'])
        # migration
        isl.all_animals_age()
        isl.all_animals_losses_weight()
        isl.animals_die()
        num_after_death = len(isl.herbis[0]['pop'])
        print(year, num_initial, num_after_birth, num_after_death)
        print(isl.herbis)
        # Plotting
        plt.plot(year, num_after_death, '.')
    plt.show()



    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    # A big but small island (only Lowland and Highland)
    ll = np.array([['W','W','W','W'],
                   ['W','L','L','W'],
                   ['W','H','H','W'],
                   ['W','L','L','W'],
                   ['W','W','W','W']])