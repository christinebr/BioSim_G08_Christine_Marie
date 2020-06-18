# -*- coding: utf-8 -*-

from biosim.animals import Herbivores, Carnivores
import pytest
from scipy.stats import normaltest

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

alpha = 0.01  # Significant level for statistical tests


class TestHerbivores:

    @pytest.fixture()
    def initial_herbivore_class(self):
        """Makes a  single herbivore, to be used in tests."""
        self.herb = Herbivores(age=5, weight=20)

    def test_constructor_default(self, initial_herbivore_class):
        """Test that the class Herbivores creates an instance."""
        assert isinstance(self.herb, Herbivores)

    def test_set_params_raises_keyerror(self, initial_herbivore_class):
        """
        Tests that the Herbivores class raises a KeyError if default parameter
        names are not used.
        """
        with pytest.raises(KeyError):
            self.herb.set_params({'weight': 10, 'a_half': 5.0})

    def test_set_params_raises_valueerror(self, initial_herbivore_class):
        """
        Test that Animal class raises ValueError when trying to update
        parameters to negative value.
        """
        with pytest.raises(ValueError):
            self.herb.set_params({'gamma': -0.8})

    def test_invalid_value_eta(self, initial_herbivore_class):
        """
        Test that Animal class raises ValueError when trying to update
        eta with a value higher than 1.
        """
        with pytest.raises(ValueError):
            self.herb.set_params({'eta': 1.2})

    def test_update_parameters(self):
        """Test if parameters is updated correctly."""
        h1 = Herbivores(weight=20)
        param = h1.get_params()
        assert param['beta'] == 0.9  # The default parameter values
        assert param['w_half'] == 10.0
        h1.set_params({'w_half': 2.0, 'beta': 0.8})
        assert param['beta'] == 0.8
        assert param['w_half'] == 2.0

    def test_default_value_for_age(self):
        """
        Testing default value for age and that it is possible to assign
        a different value for age.
        """
        h1 = Herbivores(weight=20)
        assert h1.age == 0
        h2 = Herbivores(age=3, weight=20)
        assert h2.age != 0

    def test_age_not_negative(self):
        """
        Check that the class raises a ValueError if the given age is negative.
        """
        with pytest.raises(ValueError):
            Herbivores(age=-1, weight=20)

    def test_update_age(self, initial_herbivore_class):
        """Check that an animals age can be updated."""
        age_before = self.herb.age
        self.herb.update_age()
        assert age_before < self.herb.age

    def test_weight_not_negative(self):
        """
        Check that the class raises a ValueError if the assigned weight is
        negative.
        """
        with pytest.raises(ValueError):
            Herbivores(age=3, weight=-20)

    def test_increase_weight_when_eating(self, initial_herbivore_class):
        """"
        Test that a herbivore gain weight when eating an amount of fodder.
        """
        old_weight = self.herb.weight
        self.herb.update_weight_after_eating(amount_fodder_eaten=8)
        assert self.herb.weight > old_weight

    def test_decrease_weight_not_eating(self, initial_herbivore_class):
        """
        Tests that a herbivore losses weight when the method
        update_weight_end_of_year is called.
        """
        old_weight = self.herb.weight
        self.herb.update_weight_end_of_year()
        assert self.herb.weight < old_weight

    def test_decrease_weight_after_given_birth(self):
        """
        Check if animal losses weight after giving birth.
        """
        h = Herbivores(weight=35, age=5)
        prob, newborn_weight = h.birth(num=10)
        assert prob != 0
        assert newborn_weight != 0
        h.update_weight_after_birth(weight_of_newborn=newborn_weight)
        assert h.weight < 35

    def test_fitness_between_0_and_1(self, initial_herbivore_class):
        """Testing if value of fitness is between 0 and 1."""
        fitness = self.herb.fitness()
        assert 0 <= fitness <= 1

    def test_fitness_0_if_zero_weight(self, initial_herbivore_class):
        """Test if value of fitness is 0 when weight is zero or less."""
        self.herb.weight = 0
        assert self.herb.fitness() == 0

    def test_probability_of_migration(self, initial_herbivore_class):
        """Test that probability of migration is between 0 and 1."""
        prob_migration = self.herb.probability_of_migration()
        assert 0 <= prob_migration <= 1

    def test_death_when_zero_weight(self, initial_herbivore_class):
        """
        Test that a herbivore dies if it has zero weight.
        """
        self.herb.weight = 0
        assert self.herb.probability_death() == 1.0

    def test_prob_of_death_when_fitness_is_one(self, initial_herbivore_class):
        """
        Test that probability of death is less than 0.1 when fitness is nearly
        equal to 1.
        Age 0 and weight 100 shall give fitness 0.999...
        """
        self.herb.weight = 100
        assert self.herb.probability_death() < 0.1

    def test_no_birth_when_n_is_1(self, initial_herbivore_class):
        """
        Check that one animal can't give birth alone.
        """
        assert self.herb.birth(num=1)[0] == 0

    def test_no_birth_when_small_weight(self, initial_herbivore_class):
        """
        Check that an animal can't give birth if it's weight is below the
        weight limit.
        """
        assert self.herb.birth(num=2)[0] == 0

    def test_stat_birth_weight(self, initial_herbivore_class):
        """
        Tests if the birth weight of a herbivore is drawn from a normal
        distribution.
        """
        num_of_runs = 300
        array_birth_weight = []
        for _ in range(num_of_runs):
            array_birth_weight.append(self.herb.birth_weight())
        assert normaltest(array_birth_weight)[1] > alpha


class TestCarnivores:
    @pytest.fixture()
    def initial_carnivore_class(self):
        """
        Make single carnivore, to be used in tests.
        """
        self.carn = Carnivores(weight=10, age=4)

    def test_to_large_newborn_weight(self, initial_carnivore_class, mocker):
        """
        Test that an animal does not give birth if the weight of the newborn
        is larger that the weight of the mother.
        """
        self.carn.set_params({'zeta': 1})  # make weight limit = 7
        # make newborn weight = 12
        mocker.patch('random.gauss', return_value=12)
        prob, newborn_weight = self.carn.birth(10)
        assert prob == 0.
        assert newborn_weight == 0.

    def test_invalid_value_deltaphimax(self, initial_carnivore_class):
        """Test that DeltaPhiMax is strictly positive (>0)."""
        with pytest.raises(ValueError):
            self.carn.set_params({'DeltaPhiMax': -0.7})
        with pytest.raises(ValueError):
            self.carn.set_params({'DeltaPhiMax': 0})

    def test_prob_kill_0_when_large_herbi_fitness(self):
        """
        Checks that probability of killing a herbivore is 0 when it has high
        fitness
        """
        carni = Carnivores(weight=10, age=2)  # fitness 0.917
        prob_kill = carni.probability_of_killing_herbivore(fitness_herbi=0.999)
        assert prob_kill == 0

    def test_prob_kill_between_0_and_1(self):
        """
        Test that the probability of killing a herbivore is between 0 and 1
        for a carnivore with high enough fitness.
        """
        carni = Carnivores(weight=10, age=2)  # fitness 0.917
        prob_kill = carni.probability_of_killing_herbivore(fitness_herbi=0.5)
        assert 0 <= prob_kill <= 1

    def test_prob_kill_1_otherwise(self):
        """
        Test that probability to kill is 1.
        """
        carni = Carnivores(weight=10, age=2)  # fitness 0.917
        carni.set_params({'DeltaPhiMax': 0.3})  # Makes sure carnivores kills
        prob_kill = carni.probability_of_killing_herbivore(fitness_herbi=0.5)
        assert prob_kill == 1

    def test_update_weight_after_kill(self):
        """
        Test that the weight of a carnivore is being updated after it has
        killed a herbivore.
        """
        carni = Carnivores(weight=25, age=2)  # fitness 0.917
        weight_before = carni.weight
        carni.update_weight_after_kill(weight_herbi=14)
        assert weight_before < carni.weight
