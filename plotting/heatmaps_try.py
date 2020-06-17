# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from biosim.island import TheIsland

geogr_island = """\
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
                            'weight': 20} for _ in range(20)]}
                ]

island = TheIsland(geogr_island, ini_animals)

herbis_lists = []
carnis_lists = []
for row in range(island.row):
    herbis_row = []
    carnis_row = []
    for col in range(island.col):
        herbis, carnis = island._give_animals_in_cell(row + 1, col + 1)
        herbis_row.append(len(herbis))
        carnis_row.append(len(carnis))
    herbis_lists.append(herbis_row)
    carnis_lists.append(carnis_row)

plt.imshow(herbis_lists, cmap='viridis')
plt.colorbar()
plt.show()

# def heatmap2d(arr: np.ndarray):
#     plt.imshow(arr, cmap='viridis')
#     plt.colorbar()
#     plt.show()
#
#
# test_array = [[2, 5, 8, 3 ,0, 5], [0, 4, 6, 5, 2, 3]]
# heatmap2d(test_array)