# -*- coding: utf-8 -*-

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

from biosim.animals import Herbivores, Carnivores
import random
from itertools import zip_longest
from operator import itemgetter


class SingleCell:
    """
    Keeps control of the number of animals of both species,the amount of
    fodder, and landscape-type.
    """
    _params = None

    def __init__(self, animals_list=None):
        """
        Parameters
        ----------
        animals_list : list
            List of animals, default-value is None
        """
        if animals_list:
            self.animals_list = animals_list
        else:
            self.animals_list = []

        self.carni_list = []
        self.herbi_list = []
        self.add_animals_to_cell(self.animals_list)

    def add_animals_to_cell(self, animals):
        """
        Receives list of animals and sorts them into lists of herbivores and
        carnivores by appending to self.herbi_list and self.carni_list.

        Parameters
        ----------
        animals : list
            List of animals that shall be added to the cell.
        """
        for animal in animals:
            if animal['species'] == 'Herbivore':
                self.herbi_list.append(Herbivores(age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carni_list.append(Carnivores(age=animal['age'], weight=animal['weight']))

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.

        Parameters
        ----------
        new_params : dict
            Dictionary with parameter name as keys and parameter value as value.

            ``new_params = {'key': value}``

        Raises
        ------
        KeyError
            if given an invalid parameter name
        ValueError
            if given an invalid parameter value
        """
        for key in new_params:
            if key not in cls._params:
                raise KeyError(f"Invalid parameter name + {key}")
            else:
                cls._params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Makes it possible to get the parameter dictionary.

        Returns
        -------
        _params : dict
            Dictionary of the parameters.
        """
        return cls._params

    def sort_animals_after_fitness(self):
        """
        Sorting the animals after fitness
            - herbivores are sorted from lowest to highest fitness.
            - carnivores are sorted from highest to lowest fitness.

        Returns
        -------
        sorted_herbis : list of class-instances
            List of herbivores sorted from lowest to highest fitness.
        sorted_carnis : list of class-instances
            List of herbivores sorted from highest to lowest fitness.
        """
        # Sorting the herbivores from low to high fitness
        fitness_herbi = [herbi.fitness() for herbi in self.herbi_list]
        zip_fitness_herbis = zip(fitness_herbi, self.herbi_list)
        sorted_herbi_after_fitness = sorted(zip_fitness_herbis, key=itemgetter(0))
        sorted_herbis = [herb for _, herb in sorted_herbi_after_fitness]

        # Sorting the carnivores from high to low fitness
        fitness_carni = [carni.fitness() for carni in self.carni_list]
        zip_fitness_carnis = zip(fitness_carni, self.carni_list)
        sorted_carni_after_fitness = sorted(zip_fitness_carnis, key=itemgetter(0), reverse=True)
        sorted_carnis = [carn for _, carn in sorted_carni_after_fitness]

        return sorted_herbis, sorted_carnis

    def animals_in_cell_eat(self):
        """
        Animals in the cell eats, first herbivores and then carnivores.
        """
        # If there are herbivores in the cell, they eat
        if self.herbi_list:
            self.herbivores_eats()

        # If there are herbivores and carnivores in the cell, the carnivores
        # eats by trying to kill herbivores
        if self.herbi_list and self.carni_list:
            self.carnivores_eats()

    def herbivores_eats(self):
        """
        The herbivores eat in random order and each herbivore wants to eat a
        fixed amount of fodder. The herbivores eats as long as there is
        available fodder in the cell. Each time a herbivore eats, the weight
        of that herbivore is updated.
        """
        # Shuffles the herbivores, they eat in random order
        random.shuffle(self.herbi_list)
        fodder_in_cell = self._params['f_max']
        for herbi in self.herbi_list:
            fodder = herbi.get_params()['F']
            if fodder_in_cell >= fodder:
                herbi.update_weight(amount_fodder_eaten=fodder)
                fodder_in_cell -= fodder
            elif fodder_in_cell > 0:
                herbi.update_weight(amount_fodder_eaten=fodder_in_cell)
                fodder_in_cell = 0

    def carnivores_eats(self):
        """
        The carnivores eats by killing herbivores. The carnivores and
        herbivores are sorted after fitness. The fittest carnivore eats first
        and each carnivore tries to eat the herbivore with lowest fitness. One
        carnivore eats at a time and it stops to eat when the desired amount of
        fodder is reached. Each time a carnivore eats, the weight of that
        carnivore is updated.

        The surviving herbivores are stored in a list which in the end is used
        to update the herbivore list.
        """
        sorted_herbi, sorted_carni = self.sort_animals_after_fitness()
        for carni in sorted_carni:  # first carni has the highest fitness
            appetite = carni.get_params()['F']
            not_killed_herbis = []
            for herbi in sorted_herbi:  # first herbi has the lowest fitness
                prob_kill = carni.probability_of_killing_herbivore(fitness_herbi=herbi.fitness())
                if random.random() < prob_kill and appetite > 0:  # carni kills herbi
                    carni.update_weight_after_kill(weight_herbi=herbi.weight)
                    appetite -= herbi.weight
                else:
                    not_killed_herbis.append(herbi)
            sorted_herbi = not_killed_herbis

        self.herbi_list = sorted_herbi  # the herbis remaining are the not_killed_herbis
        self.carni_list = sorted_carni  # carnis after eating

    def birth(self):
        """
        Decides if animals are born and updates lists of herbivores and
        carnivores. The animal giving birth, the mother, loses weight and a
        new animal (herbivore or carnivore) is added.
        """
        num_herbi = len(self.herbi_list)
        num_carni = len(self.carni_list)

        newborn_herbi, newborn_carni = [], []
        for herbi, carni, in zip_longest(self.herbi_list, self.carni_list):
            if herbi:  # needs this because herbi is None if num_carni > num_herbi
                prob_birth_herbi, birth_weight_herbi = herbi.birth(num_herbi)
                if random.random() < prob_birth_herbi:
                    newborn_herbi.append(Herbivores(age=0, weight=birth_weight_herbi))
                    herbi.update_weight(weight_of_newborn=birth_weight_herbi)
                    # This updates the weight of the mother according to the weight of the newborn

            if carni:  # need this because carni is None if num_herbi > num_carni
                prob_birth_carni, birth_weight_carni = carni.birth(num_carni)
                if random.random() < prob_birth_carni:
                    newborn_carni.append(Carnivores(age=0, weight=birth_weight_carni))
                    carni.update_weight(weight_of_newborn=birth_weight_carni)

        # Adds the newborn animals to the list of animals
        self.herbi_list.extend(newborn_herbi)
        self.carni_list.extend(newborn_carni)

    def animals_stay_or_move(self):
        """
        Check if animals stay in a cell or wants migrate to another cell.
        The method updates the list of herbivores and carnivores to only
        include the animals wanting to stay in the cell.

        Returns
        -------
        animals_move : list
            list of animals that wants to migrate from the cell
        """
        animals_stay = []
        animals_move = []
        self.animals_list = self.herbi_list + self.carni_list

        for animal in self.animals_list:
            prob_migrate = animal.probability_of_migration()
            if random.random() < prob_migrate:  # check if animal migrate
                animals_move.append(animal)
            else:
                animals_stay.append(animal)

        # Separate animals_stay into self.herbi_list and self.carni_list
        self.herbi_list = []
        self.carni_list = []
        for animal in animals_stay:
            if isinstance(animal, Herbivores):
                self.herbi_list.append(animal)
            elif isinstance(animal, Carnivores):
                self.carni_list.append(animal)
        
        return animals_move

    def animals_migrate(self):
        """
        Sorts animals that wants to migrate from the cell in lists
        representing the direction they wants to move in.

        Returns
        -------
        north : list
            Animals who wants to move to the north.
        east : list
            Animals who wants to move to the east.
        south : list
            Animals who wants to move to the south.
        west : list
            Animals who wants to move to the west.
        """
        animals_move = self.animals_stay_or_move()
        north = []
        east = []
        south = []
        west = []
        for animal in animals_move:
            move_to = random.choice(['North', 'East', 'South', 'West'])
            if move_to == 'North':
                north.append(animal)
            elif move_to == 'East':
                east.append(animal)
            elif move_to == 'South':
                south.append(animal)
            elif move_to == 'West':
                west.append(animal)

        return north, east, south, west

    def add_animals_after_migration(self, animals_migrated):
        """
        Adds animals to cell after migration. Updates the attributes of the
        class in the end.

        Parameters
        ----------
        animals_migrated : list
            list with animals to be added to either herbivore or carnivore list
        """
        for animal in animals_migrated:
            if isinstance(animal, Herbivores):
                self.herbi_list.append(animal)
            if isinstance(animal, Carnivores):
                self.carni_list.append(animal)

    def aging_of_animals(self):
        """
        Makes sure animals ages. Updates the age attribute of each animals.
        """
        for herbi in self.herbi_list:
            herbi.update_age()

        for carni in self.carni_list:
            carni.update_age()

    def weight_loss_end_of_year(self):
        """
        Makes all the animals loose weight at the end of a year. Updates the
        weight attribute of each animal.
        """
        for herbi in self.herbi_list:
            herbi.update_weight()

        for carni in self.carni_list:
            carni.update_weight()

    def death(self):
        """
        Decides which of the animals that dies and updates the herbi_list and
        carni_list accordingly.
        """
        survived_herbis = []
        for herbi in self.herbi_list:
            if random.random() > herbi.probability_death():
                # Tests if the animal survives, not if it dies.
                # That's why we use > instead of <
                survived_herbis.append(herbi)

        survived_carnis = []
        for carni in self.carni_list:
            if random.random() > carni.probability_death():
                # Testing if the animal survives, not if it dies.
                # That's why we use > instead of <
                survived_carnis.append(carni)

        self.herbi_list = survived_herbis
        self.carni_list = survived_carnis

    def collect_fitness_age_weight_herbi(self):
        """
        Collects the fitness, age and weight for all herbivores and returns
        it in three lists, one with fitness, one with age and one with weight.

        Returns
        -------
        fitness : list
            fitness of herbivores in cell
        age : list
            age of herbivores in cell
        weight : list
            weight of herbivores in cell
        """
        fitness = []
        age = []
        weight = []
        for herbi in self.herbi_list:
            fitness.append(herbi.fitness())
            age.append(herbi.age)
            weight.append(herbi.weight)

        return fitness, age, weight

    def collect_fitness_age_weight_carni(self):
        """
        Collects the fitness, age and weight for all carnivores and returns
        it in three lists, one fitness, one for age and one for weight.

        Returns
        -------
        fitness : list
            fitness of carnivores in cell
        age : list
            age of carnivores in cell
        weight : list
            weight of carnivores in cell
        """
        fitness = []
        age = []
        weight = []
        for carni in self.carni_list:
            fitness.append(carni.fitness())
            age.append(carni.age)
            weight.append(carni.weight)

        return fitness, age, weight


class Water(SingleCell):
    """Represents the water-landscape."""
    _params = {'f_max': 0.0}

    def __init__(self, animals_list=None):
        super().__init__(animals_list)


class Desert(SingleCell):
    """Represents the desert-landscape."""
    _params = {'f_max': 0.0}

    def __init__(self, animals_list=None):
        super().__init__(animals_list)


class Lowland(SingleCell):
    """Represents the lowland-landscape."""
    _params = {'f_max': 800.0}

    def __init__(self, animals_list=None):
        super().__init__(animals_list)


class Highland(SingleCell):
    """Represents the highland_landscape."""

    _params = {'f_max': 300.0}

    def __init__(self, animals_list=None):
        super().__init__(animals_list)
