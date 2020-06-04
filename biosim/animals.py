# -*- coding: utf-8 -*-


class Animal:
    """This class will represent an animal."""
    pass


class Herbivores:
    """This class will represent herbivores."""

    # Default parameters for herbivores:
    default_params_herbi = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                            'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                            'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4,
                            'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, age=0):
        """Create a herbivore with age 0"""
        self._age = age

    @property
    def age(self):
        """A getter-method for age-property."""
        return self._age

    @age.setter
    def age(self, new_age):
        """A setter-method for age."""
        if new_age >= 0 and isinstance(new_age, int):
            self._age = new_age
        else:
            raise ValueError("Age need to be a positive integer")

    def update_age(self):
        """Updating the age by 1 when one year has passed."""
        self._age += 1

    def fitness(self):
        pass

    def set_params(self):
        pass

    def get_params(self):
        pass


class Carnivores:
    """This class will represent carnivores."""
    pass
