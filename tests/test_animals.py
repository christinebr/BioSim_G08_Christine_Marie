# -*- coding: utf-8 -*-

from biosim.animals import Herbivores


class TestHerbivores:

    def test_constructor_default(self):
        """ Test that the class Herbivores creates an instance."""
        h = Herbivores()
        assert isinstance(h, Herbivores)

    def test_if_raises_keyerror(self):
        """
        Tests that the Herbivores class raises a KeyError if default parameter names are not used.

        Todo: Denne skal teste at programmet blir avbrutt hvis man gir inn feil key
        """
        pass

    def test_default_value_for_age(self):
        """Testing default value for age"""
        h = Herbivores()
        assert h.age == 0
        h = Herbivores(age=3)
        assert h.age != 0

    def test_age_setter_cant_be_negative(self):
        pass

    def test_fitness_between_0_and_1(self):
        """Testing if value of fitness is between 0 and 1"""
        h = Herbivores()
        assert 0 <= h.fitness() <= 1

    def test_fitness_0_if_zero_weight(self):
        """Test if value of fitness is 0 when weight is zero or less"""
        h = Herbivores()
        h.weight = 0
        assert h.fitness() == 0

