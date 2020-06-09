# -*- coding: utf-8 -*-

from biosim.cell import Lowland
import matplotlib.pyplot as plt
import textwrap


if __name__ == "__main__":
    geogr = """\
               WWW
               WLW
               WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]

    low = Lowland(ini_herbs[0]['pop'])
    herbi_count = []
    for year in range(100):
        herbi_count.append(len(low.herbi_list + low.carni_list))
        low.animals_in_cell_eat()
        low.birth()
        low.aging_of_animals()
        low.weight_loss_end_of_year()
        low.death()
    plt.figure()
    plt.plot(herbi_count, [year for year in range(100)])
    plt.show()
