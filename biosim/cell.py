# -*- coding: utf-8 -*-
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
        animals_list: [list] List of animals, default-value is None

        Returns
        -------
        None
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
        Adding animals to the cell and sorting them into lists of herbivores
        and carnivores, by appending the correct animal-class to the lists.

        Parameters
        ----------
        animals: [list] List of animals that shall be added to the cell.

        Returns
        -------
        None
        """
        for animal in animals:
            if animal['species'] == 'Herbivore':
                self.herbi_list.append(Herbivores(age=animal['age'], weight=animal['weight']))
            if animal['species'] == 'Carnivore':
                self.carni_list.append(Carnivores(age=animal['age'], weight=animal['weight']))

        self.animals_list = self.herbi_list + self.carni_list

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.
        Raises a KeyError if given an invalid parameter name, i.e. a key that's
        not present in the dictionary.
        Raises a ValueError if given invalid value for key.

        Parameters
        ----------
        new_params: [dict]
            Dictionary with new parameter values

        Returns
        -------
        None

        Raises
        ------
        KeyError if given an invalid parameter name.
        """
        for key in new_params:
            if key not in cls._params:
                raise KeyError(f"Invalid parameter name + {key}")
            else:
                cls._params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Makes it possible to get the parameter values

        Returns
        -------
        _params: [dict] Dictionary of parameter values.
        """
        return cls._params

    def sort_animals_after_fitness(self):
        """
        Sorting the animals after fitness
            - herbivores are sorted from lowest to highest fitness.
            - carnivores are sorted from highest to lowest fitness.
        Returns
        -------
        sorted_herbis: [list of class-instances]
            List of herbivores sorted from lowest to highest fitness.
        sorted_carnis: [list of class-instances]
            List of herbivores sorted from highest to lowest fitness.
        """
        # Sorting the herbivores
        # finding the fitness of each herbi and placing them in a list
        fitness_herbi = [herbi.fitness() for herbi in self.herbi_list]
        # the first element is the herbi with the lowest fitness
        zip_fitness_herbis = zip(fitness_herbi, self.herbi_list)
        sorted_herbi_after_fitness = sorted(zip_fitness_herbis, key=itemgetter(0))
        sorted_herbis = [herb for _, herb in sorted_herbi_after_fitness]

        # Sorting the carnivores
        # finding the fitness of each herbi and placing them in a list
        fitness_carni = [carni.fitness() for carni in self.carni_list]
        # sorting the self.carni_list after the fitness_carni
        # the first element is the carni with the highest fitness
        zip_fitness_carnis = zip(fitness_carni, self.carni_list)
        sorted_carni_after_fitness = sorted(zip_fitness_carnis, key=itemgetter(0), reverse=True)
        sorted_carnis = [carn for _, carn in sorted_carni_after_fitness]

        return sorted_herbis, sorted_carnis

    def animals_in_cell_eat(self):
        """
        First the herbivores eat, they eat in random order. Shuffle the
        herbivores list, then let the first animal eat and gain weigh. This
        goes on until there are no fodder left in the cell.

        Then the carnivores eat. The fittest carnivore eats first, it tries to
        kill the least fit herbivores until it is filled or there are no more
        herbivores that's week enough for it to kill. Then the next carnivore
        kills and eat, and so on until there are no more herbivores week enough
        to be killed by the hungry carnivores or all carnivores are stuffed. If
        a carnivore kills a herbivore that weights more than what the carnivore
        wants to eat, the remainders of the herbivore are lost.

        The surviving herbivores are stored in a list that's in the end used
        to update the herbivore list in init. Carnivores in init are also updated.

        Todo: This is a little to long.

        Returns
        -------
        None
        """
        # Herbivores eats
        random.shuffle(self.herbi_list)  # Shuffles the herbivores, they eat in random order
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
        self.carni_list = sorted_carni  # carnis after eating

    def birth(self):
        """
        Decides if animals are born and updates the animal_list.
        Makes sure the mother loses weight and assigns a weight and specie to
        the newborn animals.

        Returns
        -------
        None
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
        Check if animals stay in a cell or migrate to another cell. The method
        also updates lists of herbivores and carnivores in the init.

        Returns
        -------
        animals_move: [list]
            list of animals that moves out of the cell
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
        Sorts animals that wants to move in list showing the direction they
        wants to move in.

        Returns
        -------
        north: [list] Animals who wants to move to the north.
        east: [list] Animals who wants to move to the east.
        south: [list] Animals who wants to move to the south.
        west: [list] Animals who wants to move to the west.
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

        Returns
        _______
        None

        """
        for animal in animals_migrated:
            if isinstance(animal, Herbivores):
                self.herbi_list.append(animal)
            if isinstance(animal, Carnivores):
                self.carni_list.append(animal)

    def aging_of_animals(self):
        """
        Makes sure animals ages. Updates the attributes of the class.

        Returns
        -------
        None
        """
        for herbi in self.herbi_list:
            herbi.update_age()

        for carni in self.carni_list:
            carni.update_age()

    def weight_loss_end_of_year(self):
        """
        Makes all the animals loose weight according to their start-weight and
        the constant eta. Updates the class attributes.

        Returns
        -------
        None
        """
        for herbi in self.herbi_list:
            herbi.update_weight()
        for carni in self.carni_list:
            carni.update_weight()

    def death(self):
        """
        Decides which of the animals that dies and updates the animal_list
        accordingly.

        Returns
        -------
        None
        """
        survived_herbis = []
        for herbi in self.herbi_list:
            if random.random() > herbi.probability_death():
                # Tests if the animal survives, not if it dies. That's why we use > instead of <
                survived_herbis.append(herbi)

        survived_carnis = []
        for carni in self.carni_list:
            if random.random() > carni.probability_death():
                # Testing if the animal survives, not if it dies. That's why we use > instead of <
                survived_carnis.append(carni)

        self.herbi_list = survived_herbis
        self.carni_list = survived_carnis

    def collect_fitness_age_weight_herbi(self):
        """
        Collects the fitness, age and weight for all herbivores and returns
        it in three lists, one with fitness, one with age and one with weight.

        Returns
        -------
        fitness: [list] fitness of herbivores in cell
        age:     [list] age of herbivores in cell
        weight:  [list] weight of herbivores in cell
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
        fitness: [list] fitness of carnivores in cell
        age:     [list] age of carnivores in cell
        weight:  [list] weight of carnivores in cell
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
