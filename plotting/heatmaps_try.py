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
    for col in range(island.colon):
        herbis, carnis = island.give_animals_in_cell(row, col)
        herbis_row += len(herbis)
        carnis_row += len(carnis)
    herbis_lists += herbis_row
    carnis_lists += carnis_row

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