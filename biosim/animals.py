# -*- coding: utf-8 -*-
import numpy as np
import random


class Animal:
    """This class will represent an animal."""
    _params = None

    def __init__(self, weight, age=0):
        """
        Create an animal with weight and age.

        Parameters
        ----------
        weight: [float] the weight of an animal
        age: [int] the age of an animal
                   default value is zero (the age at birth)
        """
        if weight < 0:
            raise ValueError("Weight can't be negative")
        else:
            self.weight = round(weight, 2)

        if age < 0:
            raise ValueError("Age can't be negative")
        else:
            self.age = age

    @classmethod
    def set_params(cls, new_params):
        """
        Set parameters for class.

        todo: DeltaPhiMax shall be strictly positive (>0)
              required that eta <= 1
              Should we implement this?

        Parameters
        ----------
        new_params: [dict] dictionary with new parameter values

        Raises
        ------
        KeyError: if invalid parameter name
        ValueError: if invalid parameter value
        """
        for key, value in new_params.items():
            if key not in cls._params:
                raise KeyError(f"Invalid parameter name: {key}")
            if value <= 0:
                raise ValueError(f"Parameter value for {key} must be positive")

        cls._params.update(new_params)

    @classmethod
    def get_params(cls):
        """
        Get class parameters

        Returns
        -------
        _params: [dict] dictionary with class parameters
        """
        return cls._params

    def update_age(self):
        """
        Updating the age of the animal by 1.
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
            self.weight += round(self._params['beta']*amount_fodder_eaten, 2)
        elif weight_of_newborn:
            self.weight -= round(self._params['xi'] * weight_of_newborn, 2)
        else:
            self.weight -= round(self._params['eta'] * self.weight, 2)

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
        if self.weight <= 0:
            return 0.
        else:
            return (self._q(+1, self.age,
                            self._params['a_half'],
                            self._params['phi_age']))\
                      * (self._q(-1, self.weight,
                                 self._params['w_half'],
                                 self._params['phi_weight']))

    def probability_of_migration(self):
        """
        Finds the probability of migration based on the animals fitness and
        the parameter 'mu'.

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

        Parameters
        ----------
        num: [int]
            the number of animals of the same species in one cell

        Returns
        -------
        [float] the probability that an animal will give birth.
        [float] weight of the newborn animal
        """
        weight_limit = self._params['zeta'] * (self._params['w_birth']
                                               + self._params['sigma_birth'])
        if num == 1:  # only one animal
            return 0., 0.
        elif self.weight < weight_limit:
            return 0., 0.
        else:
            birth_weight_newborn = self.birth_weight()
            if self.weight <= birth_weight_newborn:
                return 0., 0.
            else:
                return min(1, self._params['gamma'] * self.fitness() * (num - 1)),\
                       round(birth_weight_newborn, 2)

    def birth_weight(self):
        """
        Uses a Gaussian distribution with mean and standard deviation as
        specified in the animal-parameters to find the weight of a newborn.

        Returns
        -------
        [float] the weight of a newborn animal
        """
        return round(random.gauss(self._params['w_birth'],
                                  self._params['sigma_birth']), 2)

    def probability_death(self):
        """
        The probability of death for an animal lies between 0 and 1
            - If the animals weight is zero, the probability of death is 1
            - Otherwise the probability of death is calculated from the weight
              and the fitness of the animal.

        Returns
        -------
        [float] the probability that an animal will die.
        """
        if self.weight <= 0:
            return 1.0  # the animal is dead
        else:
            # Probability of death:
            return self._params['omega'] * (1 - self.fitness())


class Herbivores(Animal):
    """This class will represent herbivores."""

    # Default parameters for herbivores:
    _params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
               'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
               'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
               'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
               'F': 10.0}

    def __init__(self, weight, age=0):
        """Create a herbivore with age 0."""
        super().__init__(weight, age)


class Carnivores(Animal):
    """This class will represent carnivores."""

    # Default parameters for carnivores:
    _params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
               'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
               'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
               'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1, 'omega': 0.8,
               'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, weight, age=0):
        """Create a carnivore with age 0."""
        super().__init__(weight, age)

    def probability_of_killing_herbivore(self, fitness_herbi):
        """
        Calculating the probability that a carnivore kills a herbivore,
        depending on the fitness of the herbivores and the carnivore, and
        also the 'DeltaPhiMax' parameter for a carnivore.

        Parameters
        ----------
        fitness_herbi: [float] the fitness of the herbivore that the carnivore
                               is trying to kill.

        Returns
        -------
        [float] the probability that a carnivore kills the herbivore.
        """
        fitness_carni = self.fitness()
        if fitness_carni <= fitness_herbi:
            return 0.
        elif 0 < fitness_carni - fitness_herbi < self._params['DeltaPhiMax']:
            return (fitness_carni - fitness_herbi)/self._params['DeltaPhiMax']
        else:
            return 1.

    def update_weight_after_kill(self, weight_herbi):
        """
        Updates the weight of a carnivore with the weight of the herbivore
        killed, and eaten, times the 'beta' parameter.

        Parameters
        ----------
        weight_herbi: [float] the weight of the herbivore killed
        """
        self.weight += round(self._params['beta']*weight_herbi, 2)
