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
               WWWHHHLLLLLWWWWWHHHWW
               WWWHHHLLLLWWWWWHHHWWW
               WWWWHHHLLWWWWWHHHHWWW
               WWWLHHHHWWWWHHHHHWWWW
               WWLLLHHHHHHHHHHHWWWWW
               WLLLLLHHHHHHHHHWWWWWW
               WWLLLWWWHHHHHWWWWWWWW
               WWWLWWWWWWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

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

    sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
                                            'omega': 0.3, 'F': 65,
                                            'DeltaPhiMax': 9.})
    sim.set_landscape_parameters('L', {'f_max': 700})

    sim.simulate(num_years=50, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_years=150, vis_years=1, img_years=2000)

    input('Press ENTER')
