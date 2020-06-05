# -*- coding: utf-8 -*-
import numpy as np
from .animals import Herbivores, Carnivores, Animal
import random
from copy import deepcopy

"""
-----------------------
Todo: Finn ut av importen
"""


class SingleCell:
    """
    Keeps control of the amount of animals of both species and fodder, and landscape-type.
    """
    f_max = {'W': 0.0, 'D': 0.0, 'L': 800.0, 'H': 300.0}

    def __init__(self, animals_list=None):
        if animals_list:
            self.animals_list = animals_list
        else:
            self.animals_list = []
        self.N = len(animals_list)

    def get_animals(self):
        """Just making it 'legal' to get information about the animals."""
        return self.animals_list

    def animals_in_cell_eat(self):
        """
        shuffles the animals, loops through all the animals in self.animal_list
        call the function animal.update_weight()
        """
        pass

    def fodder_update(self):
        pass

    def birth(self):
        """Decides if animals are born and updates the animal_list

        Todo: Gi inn antall dyr, eller endre på birth i animal og kontroller at mer enn ett dyr her.
        Grått var et forsøk på å fikse dette, men løsningen tar for lang tid.
        """
#        n_before = deepcopy(self.N)
        for animal in self.animals_list:
            w = animal['weight']
            a = animal['age']
            if animal['species'] == 'Herbivore':
                herbi = Herbivores(weight=w, age=a)
#                prob_birth = herbi.birth(n_before)
                prob_birth = herbi.birth()
                birth_weight = herbi.birth_weight()
                speci = 'Herbivore'
                if random.random() > prob_birth:
                    new_animal = {'species': speci, 'age': 0, 'weight': birth_weight}
                    self.animals_list.append(new_animal)
                    herbi.update_weight(weight_of_newborn=birth_weight)
                    animal['weight'] = herbi.weight
            else:
                carni = Carnivores(weight=w, age=a)
#                prob_birth = carni.birth(n_before)
                prob_birth = carni.birth()
                birth_weight = carni.birth_weight()
                speci = 'Carnivore'
                if random.random() > prob_birth:
                    new_animal = {'species': speci, 'age': 0, 'weight': birth_weight}
                    self.animals_list.append(new_animal)
                    carni.update_weight(weight_of_newborn=birth_weight)
                    animal['weight'] = carni.weight


    def migration(self):
        pass

    def aging_of_animales(self):
        """Makes sure animals ages"""
        for animal in self.animals_list:
            animal['age'] += 1

    def weight_loss(self):
        pass

    def death(self):
        """Decides which of the animals that dies and updates the animal_list
        todo: We think that animal_list = [{'species': 'Herbivore', 'age': 10, 'weight':40},
                                           {'species': 'Herbivore', 'age': 8, 'weight':29},
                                           {'species': 'Carnivore', 'age': 3, 'weight':50}]
              Is this the right way to think of animal_list??
        """
        survived_animals = []
        for animal in self.animals_list:
            w = animal['weight']
            a = animal['age']
            if animal['species'] == 'Herbivore':
                herbi = Herbivores(weight=w, age=a)
                prob_death = herbi.death()
            else:
                carni = Carnivores(weight=w, age=a)
                prob_death = carni.death()

            if random.random() > prob_death:
                survived_animals.append(animal)

        self.animals_list = survived_animals


class Water(SingleCell):
    """
    Represents the water-landscape.
    """
    pass


class Desert(SingleCell):
    """
    Represents the desert-landscape.
    """
    pass


class Lowland(SingleCell):
    """
    Represents the lowland-landscape.
    """
    pass


class Highland(SingleCell):
    """
    Represents the highland_landscape.
    """
    pass

# class Lowland:
#     def __init__(self, fodder_available=0):
#         self.f_max = 800.0
#         if fodder_available > self.f_max:
#             raise ValueError("To much fodder in lowland")
#         else:
#             self.fodder = fodder_available
#
#     def get_fodder(self):
#         return self.fodder
#
#     def set_fodder(self, new_fodder):
#         self.fodder = new_fodder
#
#
# class Highland:
#     def __init__(self, fodder_available=0):
#         self.f_max = 300.0
#         if fodder_available > self.f_max:
#             raise ValueError("To much fodder in highland")
#         else:
#             self.fodder = fodder_available
#
#     def get_fodder(self):
#         return self.fodder
#
#     def set_fodder(self, new_fodder):
#         self.fodder = new_fodder


if __name__ == "__main__":
    animals = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
               {'species': 'Herbivore', 'age': 8, 'weight': 29},
               {'species': 'Herbivore', 'age': 3, 'weight': 10}]
    cell1 = SingleCell(animals)
    print(cell1.get_animals())
    cell1.birth()
    print(cell1.get_animals())
