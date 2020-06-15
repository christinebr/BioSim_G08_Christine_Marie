# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
The checkerboard test 
Check to see if migration of animals works as intended.
"""
if __name__ == '__main__':
    plt.ion()

    geogr = """\
                WWWWWWWWW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    initial_a = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore',
                           'age': 5, 'weight': 20}
                          for _ in range(1000)]
                 + [{'species': 'Carnivore',
                     'age': 5, 'weight': 20}
                    for _ in range(1000)]
                  }
                 ]

    sim = BioSim(island_map=geogr, ini_pop=initial_a,
                 seed=123456,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                              'age': {'max': 60.0, 'delta': 2},
                              'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters('Herbivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})
    sim.set_animal_parameters('Carnivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'F': 0, 'a_half': 1000})

    sim.simulate(num_years=20, vis_years=1, img_years=2000)

    plt.savefig('check_sim.pdf')

    input('Press ENTER')
