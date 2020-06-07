# -*- coding: utf-8 -*-
from biosim.island import TheIsland
import numpy as np
import matplotlib.pyplot as plt

"""
First try on a simulation
Having the simplest island: W W W
                            W L W
                            W W W
Only having herbivores
No migration
"""


if __name__ == '__main__':
    # Simplest island possible
    landscape = np.array([['W', 'W', 'W'],
                          ['W', 'L', 'W'],
                          ['W', 'W', 'W']])

    # Initial herbivores on island (only in one cell -> 'L')
    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(10)]
                  }]

    # Initialize the island
    isl = TheIsland(landscape_of_cells=landscape, herbis=ini_herbs)
    print(isl.herbis)
    plt.figure()
    for year in range(20):
        num_start_of_year = len(isl.herbis[0]['pop'])
        isl.all_animals_eat(landscape)   # eating
        isl.animals_procreate()          # giving birth
        num_after_birth = len(isl.herbis[0]['pop'])
        # migration
        isl.all_animals_age()            # aging
        isl.all_animals_losses_weight()  # weight loss
        isl.animals_die()                # dying
        num_end_of_year = len(isl.herbis[0]['pop'])
        print(year, num_start_of_year, num_after_birth, num_end_of_year)

        # Calculating average weight
        tot_weight = 0
        for herb in isl.herbis[0]['pop']:
            tot_weight += herb['weight']
        avg_weight = tot_weight/len(isl.herbis[0]['pop'])
        print(avg_weight)

        print(isl.herbis)

        # Plotting
        plt.plot(year, num_end_of_year, '.')
        plt.plot(year, avg_weight, '*')
    plt.show()
