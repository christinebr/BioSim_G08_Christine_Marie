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
                   {'loc': (3, 3),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20} for _ in range(200)]
                    + [{'species': 'Carnivore',
                        'age': 5,
                        'weight': 20} for _ in range(20)]
                    }
                   ]

    island = TheIsland(geogr, ini_animals)
    # Makes the island
    years = list(range(num_of_years))
    # Makes list of years
    herbi_count = []
    # List with total number of herbivores each year
    carni_count = []
    # Ditto for carnivores
    for year in years:
        _, total_herbis, total_carnis = island.total_num_animals_on_island()
        # Number of herbivores and carnivores on the island
        herbi_count.append(total_herbis)
        carni_count.append(total_carnis)
        island.annual_cycle()

    plt.figure()

    plt.plot(years, herbi_count, label='Herbivores')
    plt.plot(years, carni_count, label='Carnivores')
    plt.legend()

    plt.xlabel('Years')
    plt.ylabel('Number of animals')

    plt.show()
