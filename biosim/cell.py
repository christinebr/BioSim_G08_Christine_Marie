# -*- coding: utf-8 -*-
import numpy as np
from .animals import Herbivores, Carnivores
import random


class SingleCell:
    """
    Keeps control of amount of animals of both species and fodder, and landscape
    """
    f_max = {'W': 0.0, 'D': 0.0, 'L': 800.0, 'H': 300.0}

    def __init__(self, animals_list=None):
        if animals_list:
            self.animals_list = animals_list
        else:
            self.animals_list = []

    def animals_in_cell_eat(self):
        """
        shuffles the animals, loops through all the animals in self.animal_list
        call the function animal.update_weight()
        """
        pass

    def migration(self):
        pass

    def birth(self):
        pass

    def death(self):
        """Decides which of the animals that dies and update the animal_list
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

    def weight_loss(self):
        pass

    def fodder_update(self):
        pass


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
