# -*- coding: utf-8 -*-

from biosim.cell import Lowland
import matplotlib.pyplot as plt

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
Our second test run on plotting both herbivores and carnivores in a cell. No
migration. Since we only use the cell class, we have to do the annual cycle 
using a for loop.
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
    herbi_count = []
    carni_count = []
    years = list(range(300))
    for year in years:
        if year == 50:
            low.add_animals_to_cell(ini_carns)  # Adding carnivores after 50 years
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
