# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from biosim.island import TheIsland

if __name__ == "__main__":
    num_of_years = 100
    geogr = """\
               WWWWW
               WWLHW
               WDDLW
               WWWWW"""

    ini_animals = [{'loc': (2, 3),
                     'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20} for _ in range(200)]
                            + [{'species': 'Carnivore',
                                'age': 5,
                                'weight': 20} for _ in range(20)]
                    },
                   {'loc': (3,3),
                    'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20} for _ in range(200)]
                            + [{'species': 'Carnivore',
                                'age': 5,
                                'weight': 20} for _ in range(20)]
                    }
                    ]

    island = TheIsland(geogr, ini_animals)

    # Just testing
    herbi_fitness = [0.9, 0.3, 0.5, 0.4, 0.6, 0.5, 0.7, 0.3, 0.95, 0.2, 0.3, 0.3]
    carni_fitness = [0.6, 0.4, 0.6, 0.5, 0.6, 0.5, 0.5, 0.5]

    plt.hist(herbi_fitness, bins=5, range=(0, 1), histtype='stepfilled', fill=False, edgecolor='red')
    plt.hist(carni_fitness, range=(0, 1), histtype='stepfilled', fill=False, edgecolor='blue')

    plt.show()