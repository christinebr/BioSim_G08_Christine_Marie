# -*- coding: utf-8 -*-
from biosim.animals import Herbivores, Carnivores
import random


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

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.
        Raises a KeyError if given an invalid parameter name, invalid key used
        in the dictionary.
        Raises a ValueError if given invalid value for key.

        todo: change 800.0 and 300.0 with parameters that we can change the value off

        Parameters
        ----------
        new_params: [dict]
            Dictionary with new parameter values
        """
        for key in new_params:
            if key not in cls.f_max:
                raise KeyError(f"Invalid parameter name + {key}")
            elif key == 'W':
                raise ValueError("There is no food in water-cells")
            elif key == 'D':
                raise ValueError("There is no food in dessert-cells")
            else:
                if key == 'L' and new_params[key] <= 800.0:
                    cls.f_max[key] = new_params[key]
                elif key == 'H' and new_params[key] <= 300.0:
                    cls.f_max[key] = new_params[key]
                else:
                    raise ValueError("To much fodder placed in cell")

    @classmethod
    def get_params(cls):
        return cls.f_max

    def get_animals(self):
        """Just making it 'legal' to get information about the animals."""
        return self.animals_list

    def sort_animals_by_species(self):
        """
        Sorting the animals in herbivores and carnivores in two lists
        Returns
        -------
        [list] herbivore and carnivore list
        """
        herbi_list, carni_list = [], []
        for animal in self.animals_list:
            if animal['species'] == 'Herbivore':
                herbi_list.append(animal)
            else:
                carni_list.append(animal)

        return herbi_list, carni_list

    def animals_in_cell_eat(self, start_value_fodder):
        """
        shuffles the animals, loops through all the animals in self.animal_list
        call the function animal.update_weight()

        todo: add eating for carnivores

        """
        herbis, carnis = self.sort_animals_by_species()

        # Herbivore eats
        random.shuffle(herbis)  # Shuffles the herbivore, they eat in random order
        fodder_in_cell = start_value_fodder
        for herbi in herbis:
            h = Herbivores(weight=herbi['weight'], age=herbi['age'])
            fodder = h.get_params()['F']
            if fodder <= fodder_in_cell:
                h.update_weight(amount_fodder_eaten=fodder)
                herbi['weight'] = h.weight
                fodder_in_cell -= fodder
            elif fodder_in_cell > 0:
                h.update_weight(amount_fodder_eaten=fodder_in_cell)
                herbi['weight'] = h.weight
                fodder_in_cell = 0

        # Carnivores eats
        # ...
        self.animals_list = herbis + carnis

    def birth(self):
        """
        Decides if animals are born and updates the animal_list
        """

        herbis, carnis = self.sort_animals_by_species()
        num_herbi = len(herbis)
        num_carni = len(carnis)

        newborn_animals = []
        for animal in self.animals_list:
            w = animal['weight']
            a = animal['age']
            if animal['species'] == 'Herbivore':
                herbi = Herbivores(weight=w, age=a)  # make herbivore (mother)
                prob_birth, birth_weight = herbi.birth(num_herbi)
                # probability of giving birth for mother and weight of newborn
                speci = 'Herbivore'
                if random.random() < prob_birth:  # check if herbivore gives birth
                    new_animal = {'species': speci, 'age': 0, 'weight': birth_weight}
                    newborn_animals.append(new_animal)  # add newborn to list of newborns

                    # update weight of herbivore (mother)
                    herbi.update_weight(weight_of_newborn=birth_weight)

                    # update weight of herbivore (mother) in animal list
                    animal['weight'] = herbi.weight
            else:
                carni = Carnivores(weight=w, age=a)  # make carnivore (mother)
                prob_birth, birth_weight = carni.birth(num_carni)
                # probability of giving birth for mother and weight of newborn
                speci = 'Carnivore'
                if random.random() < prob_birth:  # check if carnivore gives birth
                    new_animal = {'species': speci, 'age': 0, 'weight': birth_weight}
                    self.animals_list.append(new_animal)  # add newborn to list of newborns

                    # update weight of carnivore (mother)
                    carni.update_weight(weight_of_newborn=birth_weight)

                    # update weight of carnivore (mother) in animal list
                    animal['weight'] = carni.weight

        # Adds the newborn animals to the list of animals
        self.animals_list.extend(newborn_animals)

    def migration(self):
        pass

    def aging_of_animals(self):
        """Makes sure animals ages"""
        for animal in self.animals_list:
            animal['age'] += 1

    def weight_loss_end_of_year(self):
        """
        Makes all the animals looses weight according to their start-weight and the constant eta
        """
        for animal in self.animals_list:
            w = animal['weight']
            a = animal['age']
            if animal['species'] == 'Herbivore':
                herbi = Herbivores(weight=w, age=a)
                herbi.update_weight()
                animal['weight'] = herbi.weight
            else:
                carni = Carnivores(weight=w, age=a)
                carni.update_weight()
                animal['weight'] = carni.weight
        
        # list_herbi, list_carni = self.sort_animals_by_species()
        # for herbi in list_herbi:
        #     her = Herbivores(weight=herbi['weight'], age=herbi['age'])
        #     her.update_weight()
        #     herbi['weight'] = her.weight
        # for carni in list_carni:
        #     car = Carnivores(weight=carni['weight'], age=carni['age'])
        #     car.update_weight()
        #     carni['weight'] = car.weight
        #

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

            if random.random() < prob_death:
                survived_animals.append(animal)

        self.animals_list = survived_animals


class Water(SingleCell):
    """
    Represents the water-landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)


class Desert(SingleCell):
    """
    Represents the desert-landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)


class Lowland(SingleCell):
    """
    Represents the lowland-landscape.
    """
    def __init__(self, animals_list, f_max=800.0):
        super().__init__(animals_list)
        self.f_max = f_max

    def animals_eat(self):
        self.animals_in_cell_eat(start_value_fodder=self.f_max)


class Highland(SingleCell):
    """
    Represents the highland_landscape.
    """
    def __init__(self, animals_list, f_max=300.0):
        super().__init__(animals_list)
        self.f_max = f_max

    def animals_eat(self):
        self.animals_in_cell_eat(start_value_fodder=self.f_max)


if __name__ == "__main__":
    animals = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
               {'species': 'Herbivore', 'age': 8, 'weight': 29},
               {'species': 'Herbivore', 'age': 3, 'weight': 50}]
    cell1 = SingleCell(animals)
    print(f"Number of animals: {len(cell1.get_animals())}")
    print(cell1.get_animals())
    cell1.birth()
    print(f"Number of animals after birth: {len(cell1.get_animals())}")
    print(cell1.get_animals())

    c = SingleCell(animals)
    print(c.sort_animals_by_species())

    high = Highland(animals)
    print(f"Before eating")
    print(high.get_animals())
    high.animals_eat()
    print(f"After eating")
    print(high.get_animals())
