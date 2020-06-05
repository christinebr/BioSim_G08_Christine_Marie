# -*- coding: utf-8 -*-
import numpy as np


class Animal:
    """This class will represent an animal."""
    _params = None

    def __init__(self, weight, age=0):
        """Create an animal with age 0"""
        self.weight = weight
        self.age = age


class Herbivores:
    """This class will represent herbivores."""

    # # Default parameters for herbivores:
    # _params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
    #            'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
    #            'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
    #            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
    #            'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, weight, age=0):
        """Create a herbivore with age 0"""
        self.weight = weight
        self.age = age
        self._params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                        'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                        'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                        'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
                        'F': 10.0, 'DeltaPhiMax': None}

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

    def update_weight2(self, weight_of_newborn=None, amount_fodder_eaten=None):
        """
        amount_fodder_eaten: amount of fodder eaten by a herbivore
        The method updated the weight of a herbivore:
                - the weight increases if the herbivore have eaten
                - the weight decreases if amount_fodder_eaten=None
                - the weight neither decreases nor increases if amount_fodder_eaten=0

        In the spring animals will eat, then amount of fodder will be 0 or more, in the autumn
        animals will loss weigth, i.e. amount_of_fodder=None

        If an animal gives birth, it will loose weight accordingly.
        No animal should give birth and eat at the same time.
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
        return 1.0 / (1.0 + np.exp(sign * phi * (x - x_half)))

    def fitness(self):
        """
        Calculates the value of fitness. Note that the value of fitness should be between 0 and 1.
        :return: Value of fitness
        """
        age = self.age
        weight = self.weight
        if weight <= 0:
            return 0.
        else:
            return (self._q(+1, age, self._params['a_half'], self._params['phi_age']))\
                      * (self._q(-1, weight, self._params['w_half'], self._params['phi_weight']))

    def set_params(self, new_params):
        """

        Parameters
        ----------
        new_params: dict
                New parameter values

        Returns
        -------

        """
        for key in new_params:
            if key not in self._params:
                raise KeyError(f"Invalid parameter name + {key}")
            else:
                self._params[key] = new_params[key]

    def get_params(self):
        return self._params

    def birth(self, N):
        """
        N: the number of herbivores in the same place.
        Returns the probability for a herbivore to give birth.
        Gender of animal is not important
        If N=1 -> the probability of giving birth is zero
        If the weight of a herbivore is less than zeta*(w_birth+sigma_birth) -> the probability of
        giving birth is also zero
        """
        weight_limit = self._params['zeta']*(self._params['w_birth']+self._params['sigma_birth'])
        if N == 1:
            return 0
        elif self.weight < weight_limit:
            return 0
        else:
            # Probability of giving birth (maximum value is 1)
            prob_birth = min(1, self._params['gamma'] * self.fitness() * (N - 1))
            return prob_birth

    def death(self):
        """
        Returns True if the herbivores weight is zero, hence the herbivore is dead.
        Returns the probability that the herbivore dies otherwise.
        """
        if self.weight == 0:
            return True  # the herbivore is dead
        else:
            # A herbivore dies with the probability:
            prob_death = self.weight*(1-self.fitness())
            return prob_death


class Carnivores:
    """This class will represent carnivores."""
    # Default parameters for carnivores:
    _params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
               'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
               'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
               'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1, 'omega': 0.8,
               'F': 50.0, 'DeltaPhiMax': 10.0}
    pass


if __name__ == "__main__":
    h1 = Herbivores(weight=40, age=5)
    print(f"Weight:{h1.weight:17}")
    print(f"Age:{h1.age:20}")
    print(f"Fitness:{h1.fitness():20.3f}")

    print(f"Prob of birth:{h1.birth(N=9):10}")
    print(f"Prob of death:{h1.death():14.3f}\n")

    h2 = Herbivores(weight=60, age=0)
    print(h2.fitness())
    h3 = Herbivores(weight=80, age=0)
    print(h3.fitness())
    h4 = Herbivores(weight=100, age=0)
    print(h4.fitness())
    print(h4.death())
    h4.update_weight2(amount_fodder_eaten=3)
    print(h4.get_weight())
    print(h4.fitness())
    h4.update_weight2(weight_of_newborn=10)
    print(h4.get_weight())
    print(h4.fitness())
    #h4.update_weight2(weight_of_newborn=20, amount_fodder_eaten=50)
    #print(h4.get_weight())
    old_param = h3.get_params()
    print(old_param)
    h3.set_params({'w_half': 2.0, 'beta': 0.8})
    new_param = h3.get_params()
    print(new_param)
