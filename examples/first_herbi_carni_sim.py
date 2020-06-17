# -*- coding: utf-8 -*-

from biosim.cell import Lowland
import matplotlib.pyplot as plt

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
Our first test run on plotting both herbivores and carnivores on an island.
Since we are not using the island, we have to do the annual cycle with a for
loop.
"""

if __name__ == "__main__":

    ini_herbs = [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 20}
                 for _ in range(150)]

    ini_carns = [{'species': 'Carnivore',
                             'age': 5,
                             'weight': 20}
                 for _ in range(20)]

    low = Lowland(ini_herbs)
    low.add_animals_to_cell(ini_carns)  # Tests that we can add animals later
    herbi_count = []
    carni_count = []
    years = list(range(300))
    for year in years:
        herbi_count.append(len(low.herbi_list))
        carni_count.append(len(low.carni_list))
        low.animals_in_cell_eat()
        low.birth()
        low.aging_of_animals()
        low.weight_loss_end_of_year()
        low.death()
    plt.figure()

    plt.plot(years, herbi_count)
    plt.plot(years, carni_count)

    plt.show()
