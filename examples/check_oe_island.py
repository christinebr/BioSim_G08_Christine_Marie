# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
Test how things go with an island with the form of an ø. The circle is higland,
the line is lowland, and there are two lakes. The main point of the island is
to observe how animals migrate around the lakes. 

The main setup was copypasted from check_sim.py, a test from the project 
description, which could be found at:
https://github.com/heplesser/nmbu_inf200_june2020/blob/master/project_description/check_sim.py
"""

if __name__ == '__main__':
    plt.ion()

    # The island
    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWLWWW
               WWWWWWWWHHHHHWWWLLLWW
               WWWWWWHHHHHHHHHLLLLLW
               WWWWWHHHHHHHHHHHLLLWW
               WWWWHHHHWWWWWHHHHLWWW
               WWWHHHHWWWWWLLHHHHWWW
               WWHHHHWWWWLLLLLWHHHWW
               WWHHHWWWWLLLLLWWHHHWW
               WWHHHWWWLLLLLWWWHHHWW
               WWHHHWLLLLLWWWWWHHHWW
               WWWHHHLLLLWWWWWHHHWWW
               WWWWHHHLLWWWWWHHHHWWW
               WWWLHHHHWWWWHHHHHWWWW
               WWLLLHHHHHHHHHHHWWWWW
               WLLLLLHHHHHHHHHWWWWWW
               WWLLLWWWHHHHHWWWWWWWW
               WWWLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    # Adding animals almost in the middle of the island.
    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 )

    # First simulate 50 years without carnivores
    sim.simulate(num_years=50, img_years=2000)

    # Add carnivores and run for 150 years more
    sim.add_population(population=ini_carns)
    sim.simulate(num_years=150, vis_years=1, img_years=2000)

    input('Press ENTER to finish. Then the plot will disappear.')
