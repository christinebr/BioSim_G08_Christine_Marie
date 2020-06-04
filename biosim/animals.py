# -*- coding: utf-8 -*-
import numpy as np

# Default parameters for herbivores:
default_params_herbi = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                        'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                        'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                        'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
                        'F': 10.0, 'DeltaPhiMax': None}


class Animal:
    """This class will represent an animal."""

    def __init__(self, weight, age=0):
        """Create a herbivore with age 0"""
        self.weight = weight
        self.age = age


class Herbivores:
    """This class will represent herbivores."""

    def __init__(self, weight, age=0):
        """Create a herbivore with age 0"""
        self.weight = weight
        self.age = age

    def get_weight(self):
        return self.weight

    def set_weight(self, new_weight):
        self.weight = new_weight

    def get_age(self):
        return self.age

    def set_age(self, new_age):
        self.age = new_age

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

    def update_age(self):
        """Updating the age by 1 when one year has passed."""
        self.age += 1

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

    def update_weight(self, delta_weight):
        """Updating the weight."""
        self.weight += delta_weight

    @staticmethod
    def _q(sign, x, x_half, phi):
        return 1./(1.+np.exp(sign*phi*(x-x_half)))

    def fitness(self):
        """
        Calculates the value of fitness. Note that the value of fitness should be between 0 and 1.
        :return: Value of fitness
        """
        age = self.age
        weight = self.weight
        params = default_params_herbi

        if weight <= 0:
            return 0.
        else:
            (self._q(+1, age, params['a_half'], params['phi_age']))\
                * (self._q(-1, weight, params['w_half'], params['phi_weight']))

    def set_params(self):
        pass

    def get_params(self):
        pass


class Carnivores:
    """This class will represent carnivores."""
    pass


if __name__ == "__main__":
    h1 = Herbivores(weight=20, age=0)
    print(h1.weight)
    print(h1.age)
    print(h1.fitness())
