# -*- coding: utf-8 -*-
from biosim.animals import Herbivores, Carnivores
import random


class SingleCell:
    """
    Keeps control of the amount of animals of both species and fodder, and landscape-type.
    """
    _params = None  # = {}, or just an empty dictionary?

    def __init__(self, animals_list=None):
        if animals_list:
            self.animals_list = animals_list
        else:
            self.animals_list = []

        self.carni_list = []
        self.herbi_list = []
        self.sort_animals_by_species()

    def sort_animals_by_species(self):
        """
        Sorting the animals in lists of herbivores and carnivores.
        """
        for animal in self.animals_list:
            if animal['species'] == 'Herbivore':
                self.herbi_list.append(Herbivores(age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carni_list.append(Carnivores(age=animal['age'], weight=animal['weight']))

    def add_new_animals_to_cell(self, new_animals):
        for animal in new_animals:
            if animal['species'] == 'Herbivore':
                self.herbi_list.append(Herbivores(age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carni_list.append(Carnivores(age=animal['age'], weight=animal['weight']))

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.
        Raises a KeyError if given an invalid parameter name, invalid key used
        in the dictionary.
        Raises a ValueError if given invalid value for key.

        Parameters
        ----------
        new_params: [dict]
            Dictionary with new parameter values
        """
        for key in new_params:
            if key not in cls._params:
                raise KeyError(f"Invalid parameter name + {key}")
            else:
                cls._params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        return cls._params

    def get_animals(self):
        """Just making it 'legal' to get information about the animals.
        todo: remove this, shuold not be needed
        """
        return self.animals_list

    def sort_animals_after_fitness(self):
        """
        Sorting the animals after fitness
            - herbivores are sorted from lowest to highest fitness
            - carnivores are sorted from highest to lowest fitness
        """
        # Sorting the herbivores after fitness
        # fining the fitness of each herbi and placing them in a list
        fitness_herbi = [herbi.fitness() for herbi in self.herbi_list]
        # sorting the self.herbi_list after the fitness_herbi
        # the first element is the herbi with lowest fitness
        sorted_herbis = [herb for _, herb in sorted(zip(fitness_herbi, self.herbi_list))]

        # Sorting the carnivores after fitness
        # fining the fitness of each herbi and placing them in a list
        fitness_carni = [carni.fitness() for carni in self.carni_list]
        # sorting the self.carni_list after the fitness_carni
        # the first element is the carni with the highest fitness
        sorted_carnis = [carn for _, carn in sorted(zip(fitness_carni, self.carni_list),
                                                    reverse=True)]
        return sorted_herbis, sorted_carnis

    def animals_in_cell_eat(self):
        """
        shuffles the animals, loops through all the animals in self.animal_list
        call the function animal.update_weight()
        """
        # Herbivore eats
        random.shuffle(self.herbi_list)  # Shuffles the herbivore, they eat in random order
        fodder_in_cell = self._params['f_max']
        for herbi in self.herbi_list:
            fodder = herbi.get_params()['F']
            if fodder <= fodder_in_cell:
                herbi.update_weight(amount_fodder_eaten=fodder)
                fodder_in_cell -= fodder
            elif fodder_in_cell > 0:
                herbi.update_weight(amount_fodder_eaten=fodder_in_cell)
                fodder_in_cell = 0

        # Carnivores eats
        sorted_herbi, sorted_carni = self.sort_animals_after_fitness()
        for carni in sorted_carni:  # first carni has the highest fitness
            not_killed_herbis = []
            for herbi in sorted_herbi:  # first herbi has the lowest fitness
                prob_kill = carni.probability_of_killing_herbivore(fitness_herbi=herbi.fitness())
                if random.random() < prob_kill:  # carni kills herbi
                    carni.update_weight_after_kill(weight_herbi=herbi.weight)
                else:
                    not_killed_herbis.append(herbi)
            sorted_herbi = not_killed_herbis

        self.herbi_list = sorted_herbi  # the herbis remaining are the not_killed_herbis
        self.carni_list = sorted_carni  # the carnis after eating

    def birth(self):
        """
        Decides if animals are born and updates the animal_list
        """
        num_herbi = len(self.herbi_list)
        num_carni = len(self.carni_list)

        newborn_herbi = []
        for herbi in self.herbi_list:
            prob_birth, birth_weight = herbi.birth(num_herbi)
            # probability of giving birth for mother and weight of newborn
            if random.random() < prob_birth:  # check if herbivore gives birth
                newborn_herbi.append(Herbivores(age=0, weight=birth_weight))  # add newborn to list of newborns

                # update weight of herbivore (mother)
                herbi.update_weight(weight_of_newborn=birth_weight)

        newborn_carni = []
        for carni in self.carni_list:
            prob_birth, birth_weight = carni.birth(num_carni)
            # probability of giving birth for mother and weight of newborn
            if random.random() < prob_birth:  # check if herbivore gives birth
                newborn_carni.append(Carnivores(age=0, weight=birth_weight))  # add newborn to list of newborns

                # update weight of herbivore (mother)
                carni.update_weight(weight_of_newborn=birth_weight)

        # Adds the newborn animals to the list of animals
        self.herbi_list.extend(newborn_herbi)
        self.carni_list.extend(newborn_carni)

    def migration(self):
        """
        Check if animals stay in cell or migrate to an other cell

        Returns
        -------
        herbi_stay: [list]
            list of herbivores that stay in the cell
        herbi_move: [list]
            list of herbivores that moves out of the cell
        carni_stay: [list]
            list of carnivores that stay in the cell
        carni_move: [list]
            list of carnivores that moves out of the cell

        """
        # Herbivore migrate
        herbi_stay = []
        herbi_move = []
        for herbi in self.herbi_list:
            prob_migrate = herbi.probability_of_migration()
            if random.random() < prob_migrate:  # check if herbivore migrate
                herbi_move.append(herbi)
            else:
                herbi_stay.append(herbi)

        # Carnivore migrate
        carni_stay = []
        carni_move = []
        for carni in self.carni_list:
            prob_migrate = carni.probability_of_migration()
            if random.random() < prob_migrate:  # check if carnivore migrate
                carni_move.append(carni)
            else:
                carni_stay.append(carni)

        # Animals staying in the cell
        self.herbi_list = herbi_stay
        self.carni_list = carni_stay

        # Returning the animals which want to migrate
        return herbi_move, carni_move

    def aging_of_animals(self):
        """Makes sure animals ages"""
        for herbi in self.herbi_list:
            herbi.update_age()

        for carni in self.carni_list:
            carni.update_age()

    def weight_loss_end_of_year(self):
        """
        Makes all the animals looses weight according to their start-weight and the constant eta
        """
        for herbi in self.herbi_list:
            herbi.update_weight()
        for carni in self.carni_list:
            carni.update_weight()

    def death(self):
        """
        Decides which of the animals that dies and updates the animal_list
        """
        survived_herbis = []
        for herbi in self.herbi_list:
            if random.random() > herbi.probability_death():
                # Testing if the animal survives, not if it dies. That's why we use > instead of <
                survived_herbis.append(herbi)

        survived_carnis = []
        for carni in self.carni_list:
            if random.random() > carni.probability_death():
                # Testing if the animal survives, not if it dies. That's why we use > instead of <
                survived_carnis.append(carni)

        self.herbi_list = survived_herbis
        self.carni_list = survived_carnis


class Water(SingleCell):
    _params = {'f_max': 0.0}
    """
    Represents the water-landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)


class Desert(SingleCell):
    _params = {'f_max': 0.0}
    """
    Represents the desert-landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)


class Lowland(SingleCell):
    _params = {'f_max': 800.0}
    """
    Represents the lowland-landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)


class Highland(SingleCell):
    _params = {'f_max': 300.0}
    """
    Represents the highland_landscape.
    """
    def __init__(self, animals_list):
        super().__init__(animals_list)

    def animals_eat(self):
        return self.animals_in_cell_eat()


if __name__ == "__main__":
    animals = [{'species': 'Herbivore', 'age': 1, 'weight': 5},
               {'species': 'Herbivore', 'age': 8, 'weight': 25},
               {'species': 'Herbivore', 'age': 5, 'weight': 15},
               {'species': 'Carnivore', 'age': 6, 'weight': 15},
               {'species': 'Carnivore', 'age': 3, 'weight': 8},
               {'species': 'Carnivore', 'age': 23, 'weight': 12}]

    low = Lowland(animals_list=animals)

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

