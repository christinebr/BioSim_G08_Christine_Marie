# -*- coding: utf-8 -*-

from biosim.animals import Herbivores
import pytest
from copy import deepcopy


class TestHerbivores:

    @pytest.fixture()
    def initial_herbivore_class(self):
        self.h = Herbivores(weight=20)
        return self.h

    def test_constructor_default(self, initial_herbivore_class):
        """ Test that the class Herbivores creates an instance."""
        assert isinstance(initial_herbivore_class, Herbivores)

    def test_if_raises_keyerror(self, initial_herbivore_class):
        """
        Tests that the Herbivores class raises a KeyError if default parameter names are not used.
        """
        with pytest.raises(KeyError):
            self.h.set_params({'weight': 10, 'a_half': 5.0})

    def test_update_parameters(self):
        """ Test if parameters is updated correctly"""
        h1 = Herbivores(weight=20)
        old_param = deepcopy(h1.get_params())
        h1.set_params({'w_half': 2.0, 'beta': 0.8})
        new_param = h1.get_params()
        assert old_param != new_param
#        assert old_param['beta'] == pytest.approx(new_param['beta'])
 #       assert old_param['w_half'] == pytest.approx(new_param['w_half'])

    def test_default_value_for_age(self, initial_herbivore_class):
        """Testing default value for age"""
        assert self.h.age == 0
        h = Herbivores(age=3, weight=20)
        assert h.age != 0

    def test_age_setter_cant_be_negative(self):
        pass

    def test_increase_weight_when_eating(self, initial_herbivore_class):
        """"
        Test that a herbivore gain weight when eating an amount of fodder
        """
        old_weight = self.h.weight
        self.h.update_weight(amount_fodder_eaten=8)
        assert self.h.weight > old_weight

    def test_decrease_weight_not_eating(self, initial_herbivore_class):
        """
        Test that a herbivore losses weight "at the end of the year"/haven't eaten
        """
        old_weight = self.h.weight
        self.h.update_weight(amount_fodder_eaten=None)
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
        """
        Test that a herbivore dies if it has zero weight
        """
        self.h.weight = 0
        assert self.h.death() == 1.0

    def test_prob_of_death_when_fitness_is_one(self, initial_herbivore_class):
        """
        Test that probability of death is less than 0.1 when fitness is nearly equal to 1.
        Age 0 and weight 100 gives fitness 0.999...
        """
        self.h.weight = 100
        assert self.h.death() < 0.1

    def test_no_birth_when_n_is_1(self, initial_herbivore_class):
        """
        Check that one animal can't give birth alone
        """
        assert self.h.birth(num=1)[0] == 0

    def test_no_birth_when_small_weight(self, initial_herbivore_class):
        """
        Check that an animal can't give birth if it's weight is below the weight limit.
        """
        assert self.h.birth(num=2)[0] == 0

    def test_not_eating_and_feeding_at_once(self, initial_herbivore_class):
        """
        This test checks that the update_weight method does not run if an animal tries to eat and
        get a child at the same moment
        """
        with pytest.raises(ValueError):
            self.h.update_weight(weight_of_newborn=10, amount_fodder_eaten=3)

    def test_fitness_update_with_weight(self, initial_herbivore_class):
        """Tests that the fitness of the animal updates automatically when the weight changes"""
        h = self.h
        fitness1 = h.fitness()
        h.update_weight(amount_fodder_eaten=50)
        fitness2 = h.fitness()
        assert fitness1 != fitness2
