# -*- coding: utf-8 -*-

from biosim.animals import Herbivores
import pytest


class TestHerbivores:

    @pytest.fixture
    def initial_herbivore_class(self):
        self.h = Herbivores(weight=20)

    def test_constructor_default(self, initial_herbivore_class):
        """ Test that the class Herbivores creates an instance."""
        assert isinstance(self.h, Herbivores)

    def test_if_raises_keyerror(self):
        """
        Tests that the Herbivores class raises a KeyError if default parameter names are not used.

        Todo: Denne skal teste at programmet blir avbrutt hvis man gir inn feil key
        """
        pass

    def test_default_value_for_age(self, initial_herbivore_class):
        """Testing default value for age"""
        assert self.h.age == 0
        h = Herbivores(age=3, weight=20)
        assert h.age != 0

    def test_age_setter_cant_be_negative(self):
        pass

    def test_fitness_between_0_and_1(self, initial_herbivore_class):
        """Testing if value of fitness is between 0 and 1"""
        assert 0 <= self.h.fitness() <= 1

    def test_fitness_0_if_zero_weight(self, initial_herbivore_class):
        """Test if value of fitness is 0 when weight is zero or less"""
        self.h.weight = 0
        assert self.h.fitness() == 0

