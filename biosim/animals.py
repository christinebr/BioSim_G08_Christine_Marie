# -*- coding: utf-8 -*-
import numpy as np
import random


class Animal:
    """This class will represent an animal."""
    _params = None

    def __init__(self, weight, age=0):
        """
        Parameters
        ----------
        weight: [float]
            the weight of an animal
        age: [int]
            the age of an animal, default value is zero (the age at birth)
        """
        self.weight = weight
        self.age = age

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.
        Raises a KeyError if given an invalid parameter name, invalid key used
        in the dictionary.

        Parameters
        ----------
        new_params: [dict]
            Dictionary with new parameter values

        todo: all parameters shall be positive (>=0)
              DeltaPhiMax shall be strictly positive (>0)
              required that eta <= 1
              Implement this and raise ValueError if conditions not met?
        """
        for key in new_params:
            if key not in cls._params:
                raise KeyError(f"Invalid parameter name + {key}")
            else:
                cls._params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        return cls._params

    # @property
    # def age(self):
    #     """A getter-method for age-property."""
    #     return self._age
    #
    # @age.setter
    # def age(self, new_age):
    #     """A setter-method for age."""
    #     if new_age >= 0 and isinstance(new_age, int):
    #         self._age = new_age
    #     else:
    #         raise ValueError("Age need to be a positive integer")

    # @property
    # def weight(self):
    #     """A getter-method for weight-property."""
    #     return self.weight

    # @weight.setter
    # def weight(self, new_weight):
    #     """A setter-method for weight."""
    #     if new_weight >= 0:
    #         self.weight = new_weight
    #     else:
    #         raise ValueError("Weight need to be a positive number")


    def update_age(self):
        """
        Updating the age by 1 when one year has passed.
        Todo: Is this necessary?
              Seems like we could do everything in SingleCell?
        """
        self.age += 1

    def update_weight(self, amount_fodder_eaten=None, weight_of_newborn=None):
        """
        Update the weight of an animal under certain conditions:
            - the weight increases if the animal have eaten, by the amount of
              fodder eaten by the animal times the animal-parameter 'beta'.
            - the weight decreases if the animal have given birth, by the
              weight of the newborn animal.
            - the weight decreases for every animal at the end of the year,
              this happens when the default values of both parameters is used.
              The weight then decreases by the weight of the animal times
              the animal-parameter 'eta'.

        Parameters
        ----------
        amount_fodder_eaten: [None] or [float]
            the amount of fodder eaten by an animal
        weight_of_newborn: [None] or [float]
            the weight of a newborn to be subtracted from the weight of the mother

        Raises
        -------
        ValueError: if both parameters are given as a number, because an
                    animal can't eat and give birth at the same time
        """
        if weight_of_newborn and amount_fodder_eaten:
            raise ValueError('No animal could give birth and eat at the same time')
        elif amount_fodder_eaten:
            self.weight += self._params['beta']*amount_fodder_eaten
        elif weight_of_newborn:
            self.weight -= self._params['xi'] * weight_of_newborn
        else:
            self.weight -= self._params['eta'] * self.weight

    @staticmethod
    def _q(sign, x, x_half, phi):
        """ Static method of function used in fitness-method """
        return 1.0 / (1.0 + np.exp(sign * phi * (x - x_half)))

    def fitness(self):
        """
        Calculates the value of fitness for an animal, which says something
        about the overall condition of the animal.
        The value of fitness is between 0 and 1.
            - If the weight of the animal is less than or equal to zero
              the values of fitness is zero
            - Otherwise the value of fitness is calculated from the age, the
              weight and the other parameters of the animal.

        Returns
        -------
        [float] The value of fitness for an animal.
        """
        age = self.age
        weight = self.weight
        if weight <= 0:
            return 0.
        else:
            return (self._q(+1, age, self._params['a_half'], self._params['phi_age']))\
                      * (self._q(-1, weight, self._params['w_half'], self._params['phi_weight']))

    def probability_of_migration(self):
        """
        Finds the probability of migration based on the animals fitness.

        Returns
        -------
        [float] The animals probability of migrating
        """
        return self._params['mu'] * self.fitness()

    def birth(self, num):
        """
        Calculates the probability that an animal gives birth.
        The probability of birth lies between 0 and 1.
            - If num=1 (only one animal) the probability of giving birth is 0.
            - If the weight of an animal is less that a weight limit, the
              probability of giving birth is also 0.

        todo: if num=0 we will get a negative probability
              maybe not a problem because we won't calculate probability
              of birth when there is no animals?

        Parameters
        ----------
        num: [int]
            the number of animals of the same species in one cell

        Returns
        -------
        [float] the probability that an animal will give birth.
        """
        weight_limit = self._params['zeta'] * (self._params['w_birth']
                                               + self._params['sigma_birth'])
        if num == 1:
            return 0.
        elif self.weight < weight_limit:
            return 0.
        else:
            return min(1, self._params['gamma'] * self.fitness() * (num - 1))

    def birth_weight(self):
        """
        Uses a Gaussian distribution with mean and standard deviation as
        specified in the animal-parameters to find the weight of a newborn.

        Returns
        -------
        [float] The weight of a newborn
        """
        return random.gauss(self._params['w_birth'],
                            self._params['sigma_birth'])

    def death(self):
        """
        The probability of death for an animal lies between 0 and 1
            - If the animals weight is zero, the probability of death is 1
            - Otherwise the probability of death is calculated from the weight
              and the fitness of the animal.

        Returns
        -------
        [float] the probability that an animal will die.

        todo: maybe change == to <=
              or maybe not possible to get negative weight?

        """
        if self.weight == 0:
            return 1.0  # the animal is dead
        else:
            # Probability of death:
            return self.weight*(1-self.fitness())


class Herbivores(Animal):
    """This class will represent herbivores."""

    # Default parameters for herbivores:
    _params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
               'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
               'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
               'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
               'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, weight, age=0):
        """Create a herbivore with age 0"""
        super().__init__(weight, age)


class Carnivores(Animal):
    """This class will represent carnivores."""
    # Default parameters for carnivores:
    _params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
               'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
               'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
               'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1, 'omega': 0.8,
               'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, weight, age):
        """ Initialise the carnivore """
        super().__init__(weight, age)

    def probability_of_killing_herbivore(self, fitness_herbi):
        """

        Parameters
        ----------
        fitness_herbi: [float]
            the fitness of a herbivore that a carnivore is preying on.

        Returns
        -------
        [float] the probability that a carnivore kills the herbivore.

        todo: carnivore weight increases with beta*weight_herbi when it
              kills the herbivore, where should this happen? in SingleCell?
              Added a update_weight_after_kill below, is this ok?
              NB! fitness of carnivore should be re-evaluated each time it
              kills a herbivore, is this ok when using self.fitness()?
        """
        fitness_carni = self.fitness()
        max_diff_fitness = self._params['DeltaPhiMax']
        if fitness_carni <= fitness_herbi:
            return 0.
        elif 0 < fitness_carni - fitness_herbi < max_diff_fitness:
            return (fitness_carni - fitness_herbi)/max_diff_fitness
        else:
            return 1.

    def update_weight_after_kill(self, weight_herbi):
        """
        Updates the weight of a carnivore with the weight of the herbivore
        killed and eaten time the carnivore-parameter 'beta'.

        Parameters
        ----------
        weight_herbi: [float]
            the weight of the herbivore killed
        """
        self.weight += self._params['beta']*weight_herbi


if __name__ == "__main__":

    h3 = Herbivores(weight=80, age=16)
    print(h3.fitness())
    old_param = h3.get_params()
    print(old_param)
    h3.set_params({'w_half': 2.0, 'beta': 0.8})
    new_param = h3.get_params()
    print(new_param)

    herbis = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
              {'species': 'Herbivore', 'age': 8, 'weight': 29},
              {'species': 'Herbivore', 'age': 3, 'weight': 15},
              {'species': 'Herbivore', 'age': 3, 'weight': 10}]

    carnis = [{'species': 'Carnivore', 'age': 10, 'weight': 40},
              {'species': 'Carnivore', 'age': 8, 'weight': 29},
              {'species': 'Carnivore', 'age': 3, 'weight': 18}]

    print("HERBIVORES")
    for herb in herbis:
        h = Herbivores(weight=herb['weight'], age=herb['age'])
        print(f"Weight:        {h.weight}")
        print(f"Age:           {h.age}")
        print(f"Fitness:       {h.fitness():.3f}")
        print(f"Prob of birth: {h.birth(num=9)}")
        print(f"Prob of death: {h.death():.3f}\n")

    print("CARNIVORES")
    for carb in carnis:
        c = Carnivores(weight=carb['weight'], age=carb['age'])
        print(f"Weight:        {c.weight}")
        print(f"Age:           {c.age}")
        print(f"Fitness:       {c.fitness():.3f}")
        print(f"Prob of birth: {c.birth(num=9)}")
        print(f"Prob of death: {c.death():.3f}\n")



