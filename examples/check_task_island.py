# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
Testing our simulation with the island in the task description.


The main setup was copypasted from check_sim.py, a test from the project 
description, which could be found at:
https://github.com/heplesser/nmbu_inf200_june2020/blob/master/project_description/check_sim.py
"""

if __name__ == '__main__':
    plt.ion()

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WWHHLLLLLLLWWLLLLLLLW
               WWHHLLLLLLLWWLLLLLLLW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDWWLLLLLWWW
               WHHHHDDDDDDLLLLLWWWWW
               WWHHHHDDDDDDLWWWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHDDDDDDLLLLLWWWWW
               WWHHHHDDDDDLLLLLWWWWW
               WWWHHHHLLLLLLLLWWWWWW
               WWWHHHHHHWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_pop = [{'loc': (2, 3),
                'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                        for _ in range(150)]
                       + [{'species': 'Carnivore', 'age': 5, 'weight': 20}
                          for _ in range(20)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_pop, seed=654321,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters('Herbivore', {'zeta': 3.5, 'xi': 1.6})
    sim.set_animal_parameters('Carnivore', {'a_half': 65, 'phi_age': 0.55,
                                            'omega': 0.35, 'F': 60,
                                            'DeltaPhiMax': 8.})
    sim.set_landscape_parameters('L', {'f_max': 750})

    sim.simulate(num_years=200, vis_years=1, img_years=2000)

    input('Press ENTER to finish. Then the plot will disappear.')
