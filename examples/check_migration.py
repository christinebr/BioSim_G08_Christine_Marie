# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
The checkerboard test:

Check to see if migration of animals works as intended. Animals starts in the
middle cell, moves outward in the directions up, down, left and right, but 
not diagonally, with every step. First year they are all in the middle cell, 
next year the heatmaps looks like a cross, then it spreads out until animals 
hits the edges of the island and starts filling every cell. 

This island is sett up sp that animals wont die or give birth nor will the 
herbivores get eaten by carnivores. They will always be fit and want to migrate.
The island have no obstacles, i. e. only one type of landscape (lowland).

This is sett to simulate for 20 years, by then the animals has hit the outer
parts of the island, and the migrating patterns becomes less clearly visible.
"""
if __name__ == '__main__':
    plt.ion()

    geogr = """\
                WWWWWWWWW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    initial_a = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5, 'weight': 20}
                          for _ in range(1000)]
                 + [{'species': 'Carnivore',
                     'age': 5, 'weight': 20}
                    for _ in range(1000)]
                  }
                 ]

    sim = BioSim(island_map=geogr, ini_pop=initial_a,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 )

    # Setting the parameters of animals so that the numbers don't change, and
    # they are fit and wants to migrate as long as the simualtion goes.
    sim.set_animal_parameters('Herbivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})
    sim.set_animal_parameters('Carnivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'F': 0, 'a_half': 1000})

    sim.simulate(num_years=20, vis_years=1, img_years=2000)

    input('Press ENTER, and the plot will disappear. If you dont, it will hunt you forever :)')
