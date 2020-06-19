# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
This is an easy form for making the simulation run.
"""

if __name__ == '__main__':
    plt.ion()

    geogr = """\
               WWWW
               WLHW
               WLDW
               WWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                          for _ in range(150)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)

    # Simulate first 100 years with only herbivores
    sim.simulate(num_years=100, vis_years=1, img_years=1)

