# -*- coding: utf-8 -*-
from biosim.cell import Lowland

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

"""
Making sure the method for making carnivores eat works as supposed.
"""

if __name__ == "__main__":
    animals = [{'species': 'Herbivore', 'age': 1, 'weight': 21},
               {'species': 'Herbivore', 'age': 1, 'weight': 27},
               {'species': 'Herbivore', 'age': 1, 'weight': 20},
               {'species': 'Carnivore', 'age': 1, 'weight': 20},
               {'species': 'Carnivore', 'age': 1, 'weight': 20},
               {'species': 'Carnivore', 'age': 1, 'weight': 20}]

    low = Lowland(animals_list=animals)
    hh = low.herbi_list
    cc = low.carni_list
    h, c = low.sort_animals_after_fitness()
    fit_h = [herb.fitness() for herb in h]
    fit_c = [carn.fitness() for carn in c]
    w_before = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight before eating:", w_before)
    # Eating
    low.animals_in_cell_eat()
    w_after = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight after eating:", w_after)

    print("Number of animals before birth:", len(low.herbi_list + low.carni_list))
    low.birth()
    print("Number of animals after birth:", len(low.herbi_list + low.carni_list))

    a_before = [ani.age for ani in (low.herbi_list+low.carni_list)]
    print("Age before:", a_before)
    # Animals aging
    low.aging_of_animals()
    a_after = [ani.age for ani in (low.herbi_list + low.carni_list)]
    print("Age after:", a_after)

    w_before = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight before loss:", w_before)
    low.weight_loss_end_of_year()
    w_after = [ani.weight for ani in (low.herbi_list+low.carni_list)]
    print("Weight after loss:", w_after)

    print("Number of animals before death:", len(low.herbi_list + low.carni_list))
    low.death()
    print("Number of animals after death:", len(low.herbi_list + low.carni_list))

