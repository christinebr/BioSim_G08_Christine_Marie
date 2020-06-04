# -*- coding: utf-8 -*-

from biosim.animals import Herbivores
import pytest


class TestHerbivores:

    @pytest.fixture()
    def initial_herbivore_class(self):
        self.h = Herbivores(weight=20)
        return self.h

    def test_constructor_default(self, initial_herbivore_class):
        """ Test that the class Herbivores creates an instance."""
        assert isinstance(initial_herbivore_class, Herbivores)

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

    def test_increase_weight_when_eating(self, initial_herbivore_class):
        old_weight = self.h.weight
        self.h.update_weight2(amount_fodder_eaten=8)
        assert self.h.weight > old_weight

    def test_decrease_weight_not_eating(self, initial_herbivore_class):
        old_weight = self.h.weight
        self.h.update_weight2(amount_fodder_eaten=None)
        assert self.h.weight < old_weight


    def test_fitness_between_0_and_1(self, initial_herbivore_class):
        """Testing if value of fitness is between 0 and 1"""
        fitness = self.h.fitness()
        assert 0 <= fitness <= 1

    def test_fitness_0_if_zero_weight(self, initial_herbivore_class):
        """Test if value of fitness is 0 when weight is zero or less"""
        self.h.weight = 0
        assert self.h.fitness() == 0

    def test_death_when_zero_weight(self, initial_herbivore_class):
        self.h.weight = 0
        assert self.h.death() == True

    def test_prob_of_death_when_fitness_is_one(self, initial_herbivore_class):
        # Age 0 and weight 100 gives fitness 0.999...
        self.h.weight = 100
        assert self.h.death() < 0.1

    def test_no_birth_when_n_is_1(self, initial_herbivore_class):
        assert self.h.birth(N=1) == 0

    def test_no_birth_when_small_weight(self, initial_herbivore_class):
        assert self.h.birth(N=2) == 0

    def test_not_eating_and_feeding_at_once(self, initial_herbivore_class):
        """
        This test checks that the update_weight method does not run if an animal tries to eat and
        get a child at the same moment
        """
        h = self.h
        weight = h.get_weight()
        h.update(weight_of_newborn=10, amount_fodder_eaten=3)
        assert weight == h.get_weight()

    def test_fitness_update_whith_weight(self, initial_herbivore_class):
        """Tests that the fitness of the animal updates automatically when the weight changes"""
        h = self.h
        fitness1 = h.fitness()
        h.update_weight2(amount_fodder_eaten=50)
        fitness2 = h.fitness()
        assert fitness1 != fitness2
