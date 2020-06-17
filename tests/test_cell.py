# -*- coding: utf-8 -*-

__author__ = "Marie Kolvik Valøy, Christine Brinchmann"
__email__ = "mvaloy@nmbu.no, christibr@nmbu.no"

from biosim.cell import SingleCell, Lowland, Desert, Water, Highland
from biosim.animals import Herbivores, Carnivores
import pytest
from scipy.stats import binom_test

alpha = 0.01  # Significant level for statistical tests


class TestSingleCell:

    @pytest.fixture()
    def initial_cell_class(self):
        """
        Makes a single cell with animals to use as test-cell.
        """
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
                   {'species': 'Herbivore', 'age': 40, 'weight': 20},
                   {'species': 'Herbivore', 'age': 2, 'weight': 8},
                   {'species': 'Carnivore', 'age': 30, 'weight': 20},
                   {'species': 'Carnivore', 'age': 3, 'weight': 25},
                   {'species': 'Carnivore', 'age': 37, 'weight': 3.5}
                   ]
        self.cell = SingleCell(animals_list=animals)

    @pytest.fixture()
    def initial_two_herbivore_cell(self):
        """
        Makes a single cell with animals to use as test-cell for statistic tests.
        """
        two_herbivores = [{'species': 'Herbivore', 'age': 5, 'weight': 40}
                          for _ in range(2)]
        self.herbi_cell = SingleCell(animals_list=two_herbivores)

    @pytest.fixture()
    def initial_statistic_cell(self):
        """
        Makes a single cell with animals to use as test-cell for statistic tests.
        """
        self.herbivores = [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                           for _ in range(100)]
        self.stat_cell = SingleCell(animals_list=self.herbivores)

    def test_empty_animal_list(self):
        """
        Check that it's possible to call SingleCell without supplying any
        animals.
        """
        cell = SingleCell()
        assert cell.animals_list == []

    def test_add_animals_after_migration(self, initial_two_herbivore_cell):
        """
        Test that it is possible to add animals to cell. The animals added is
        either a class instance of Herbivores or Carnivores. Check this by
        adding three carnivores to the cell first, and then adding two
        herbivores.
        """
        # Before: 2 herbis and 0 carnis
        assert len(self.herbi_cell.herbi_list) == 2
        assert len(self.herbi_cell.carni_list) == 0
        new_carnis = [Carnivores(age=9, weight=10) for _ in range(3)]
        self.herbi_cell.add_animals_after_migration(new_carnis)
        # After: 2 herbis and 3 carnis
        assert len(self.herbi_cell.herbi_list) == 2
        assert len(self.herbi_cell.carni_list) == 3
        new_herbis = [Herbivores(age=3, weight=20) for _ in range(2)]
        self.herbi_cell.add_animals_after_migration(new_herbis)
        # After: 4 herbis and 3 carnis
        assert len(self.herbi_cell.herbi_list) == 4
        assert len(self.herbi_cell.carni_list) == 3

    def test_that_all_animals_age(self, initial_cell_class):
        """
        Tests that method age makes all animals get one year older.
        The sum of the age in the test-set increases with a number equal to
        the number of animals in the cell.
        """
        sum_old = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_old += animal.age

        self.cell.aging_of_animals()

        sum_new = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_new += animal.age

        assert sum_old + len(self.cell.herbi_list + self.cell.carni_list) == sum_new

    def test_that_give_birth(self, initial_cell_class, mocker):
        """
        Tests that the birth-method makes more animals, both among herbivores
        and carnivores.
        """
        mocker.patch('random.random', return_value=0)
        # Making sure all animals who are able to give birth does so.
        herbis_before = len(self.cell.herbi_list)
        carnis_before = len(self.cell.carni_list)
        self.cell.birth()
        herbis_after = len(self.cell.herbi_list)
        carnis_after = len(self.cell.carni_list)
        assert herbis_before < herbis_after
        assert carnis_before < carnis_after

    def test_that_newborns_weights_something(self, initial_cell_class, mocker):
        """
        Tests that the birth method assigns a weight to the newborn animal.
        Strictly speaking, the test checks all animals, but if no animal has
        weight zero, there are no newborns with this weight either. And we've
        already established that the birth-method makes new animals.
        """
        mocker.patch('random.random', return_value=0)
        # Makes sure there are newborns
        self.cell.birth()
        nonexsistent_newborns = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            if animal.age == 0 and animal.weight <= 0:
                nonexsistent_newborns += 1

        assert nonexsistent_newborns == 0

    def test_that_mother_looses_weight(self, initial_two_herbivore_cell, mocker):
        """
        Tests that the birth method makes the mother loose the correct amount
        of weight.
        The two herbivores in 'initial_two_herbivore_cell' have weight 40,
        which is above the weight limit to give birth for herbivores
            3.5 * (8 + 1.5) = 33.25
        This, in addition to the mocker of random.random(), makes sure that
        both herbivores gives birth.
        """
        # Makes sure that there will be newborns
        mocker.patch('random.random', return_value=0)
        weight_newborn = 7
        correct_weights_after_birth = []
        for herbi in self.herbi_cell.herbi_list:
            correct_weights_after_birth.append(herbi.weight - 1.2 * weight_newborn)

        mocker.patch('random.gauss', return_value=weight_newborn)
        # Makes sure newborns have the right weight.
        self.herbi_cell.birth()
        new_weights = []
        for herbi in self.herbi_cell.herbi_list:
            if herbi.weight != weight_newborn:
                new_weights.append(herbi.weight)

        assert pytest.approx(new_weights) == correct_weights_after_birth

    def test_no_zombies(self, initial_cell_class, mocker):
        """
        Tests that dead animals does not continue to exist (no zombies welcome
        on this island).

        The first test checks that an animal of weight zero disappears. And
        that that the animals that are supposed to survive actually does so.
        The second test checks that when all animals dies, all of them
        disappears.
        """
        mocker.patch('random.random', return_value=1)
        old_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        self.cell.herbi_list[1].weight = 0
        self.cell.carni_list[2].weight = 0
        self.cell.death()
        new_list_of_animals = self.cell.herbi_list + self.cell.carni_list
        assert len(new_list_of_animals) == len(old_list_of_animals) - 2

        mocker.patch('random.random', return_value=0)
        self.cell.death()
        list_of_animals = self.cell.herbi_list + self.cell.carni_list
        assert len(list_of_animals) == 0

    def test_that_newborn_same_speci_as_parent(self, initial_cell_class, mocker):
        """
        Tests that herbivores only gives birth to herbivores and carnivores
        only gives birth to carnivores.
        """
        mocker.patch('random.random', return_value=0)
        mocker.patch('random.gauss', return_value=7)
        self.cell.birth()
        herbis = []
        cars = []
        for herbi in self.cell.herbi_list:
            herbis.append(isinstance(herbi, Herbivores))
        for carni in self.cell.carni_list:
            cars.append(isinstance(carni, Carnivores))

        assert herbis == [True]*len(self.cell.herbi_list) and \
            cars == [True]*len(self.cell.carni_list)

    def test_possible_no_animals(self):
        """
        Checking that there wil be no problems if no animals are given into
        the class.
        """
        animals = []
        empty_cell = SingleCell(animals_list=animals)
        assert len(empty_cell.herbi_list + empty_cell.carni_list) == 0

    def test_sorting_correct(self, initial_cell_class):
        """
        Checks that the sorting of animals_list gives lists with the correct
        numbers of herbivores and carnivores.
        """
        assert len(self.cell.herbi_list) == 3
        assert len(self.cell.carni_list) == 3

    def test_sorting_equal_fitness(self):
        """
        Check that the sorting method for fitness can handle animals with
        equal fitness.
        """
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 40},
                   {'species': 'Herbivore', 'age': 10, 'weight': 40},
                   {'species': 'Carnivore', 'age': 10, 'weight': 40},
                   {'species': 'Carnivore', 'age': 10, 'weight': 40}
                   ]
        cellt = SingleCell(animals_list=animals)
        sorted_herbi, sorted_carni = cellt.sort_animals_after_fitness()
        assert cellt.herbi_list == sorted_herbi
        assert cellt.carni_list == sorted_carni

    def test_weight_loss_end_of_year(self, initial_cell_class):
        """
        Tests that all the method that makes animals loos weight at the end of
        the year does work."""
        sum_old = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_old += animal.weight
        self.cell.weight_loss_end_of_year()

        sum_new = 0
        for animal in self.cell.herbi_list + self.cell.carni_list:
            sum_new += animal.weight
        assert sum_old > sum_new

    def test_all_animals_wants_to_move(self, initial_cell_class, mocker):
        """
        Test that all animals in cell wants to move when mocking
        random.random(). check that no animals are left in cell
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=0)
        moving_animals = self.cell.animals_stay_or_move()
        num_animals_after = len(self.cell.herbi_list+self.cell.carni_list)
        assert len(moving_animals) == num_animals_before
        assert num_animals_after == 0

    def test_no_animals_wants_to_move(self, initial_cell_class, mocker):
        """
        Test that no animals in cell wants to move when mocking
        random.random(). check that no animals are left in cell
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=1)
        moving_animals = self.cell.animals_stay_or_move()
        num_animals_after = len(self.cell.herbi_list+self.cell.carni_list)
        assert len(moving_animals) == 0
        assert num_animals_before == num_animals_after

    def test_animals_migrate_north(self, initial_cell_class, mocker):
        """
        Makes all animals migrate northward, then check that all animals is in
        the list for animals who wants to move to the north, and that no
        animals has magically appeared in any of the other lists.
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='North')
        north, east, south, west = self.cell.animals_migrate()
        assert len(north) == num_animals_before
        assert len(east) == 0
        assert len(south) == 0
        assert len(west) == 0

    def test_animals_migrate_east(self, initial_cell_class, mocker):
        """
        Makes all animals migrate eastward, then check that all animals is in
        the list for animals who wants to move to the east, and that no
        animals has magically appeared in any of the other lists.
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='East')
        north, east, south, west = self.cell.animals_migrate()
        assert len(north) == 0
        assert len(east) == num_animals_before
        assert len(south) == 0
        assert len(west) == 0

    def test_animals_migrate_south(self, initial_cell_class, mocker):
        """
        Makes all animals migrate southward, then check that all animals is in
        the list for animals who wants to move to the south, and that no
        animals has magically appeared in any of the other lists.
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='South')
        north, east, south, west = self.cell.animals_migrate()
        assert len(north) == 0
        assert len(east) == 0
        assert len(south) == num_animals_before
        assert len(west) == 0

    def test_animals_migrate_west(self, initial_cell_class, mocker):
        """
        Makes all animals migrate westward, then check that all animals is in
        the list for animals who wants to move to the west, and that no
        animals has magically appeared in any of the other lists.
        """
        num_animals_before = len(self.cell.herbi_list+self.cell.carni_list)
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='West')
        north, east, south, west = self.cell.animals_migrate()
        assert len(north) == 0
        assert len(east) == 0
        assert len(south) == 0
        assert len(west) == num_animals_before

    def test_stat_probability_of_migration(self, initial_statistic_cell):
        """
        Statistically tests if migration distributes the animals as excepted.
        The number of runs are the number of animals in the initial statistic cell.
        """
        number_of_runs = len(self.herbivores)
        prob_migration = self.stat_cell.herbi_list[0].probability_of_migration()
        # The probability is the same for all animals, because they does not
        # age, nor get hungry.
        num_migrate = len(self.stat_cell.animals_stay_or_move())
        assert binom_test(num_migrate, number_of_runs, prob_migration) > alpha

    def test_stat_probability_of_death(self, initial_statistic_cell):
        """
        Statistically tests if animals dies with the expected probability.
        The number of runs are the number of animals in the initial statistic
        cell.
        """
        number_of_runs = len(self.herbivores)
        prob_death = self.stat_cell.herbi_list[0].probability_death()
        # The probability is the same for all animals, because they does not
        # age, nor get hungry.
        self.stat_cell.death()
        num_dead = number_of_runs - len(self.stat_cell.herbi_list)
        assert binom_test(num_dead, number_of_runs, prob_death) > alpha


class TestLowland:

    @pytest.fixture()
    def initial_lowland(self):
        """
        Makes a single cell with animals to use as test-cell for lowland-class.
        """
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                   {'species': 'Herbivore', 'age': 40, 'weight': 20},
                   {'species': 'Herbivore', 'age': 2, 'weight': 8},
                   {'species': 'Carnivore', 'age': 30, 'weight': 8},
                   {'species': 'Carnivore', 'age': 5, 'weight': 3.5},
                   {'species': 'Carnivore', 'age': 37, 'weight': 5.7}
                   ]
        self.low = Lowland(animals_list=animals)

    def test_no_cannibalism(self, initial_lowland, mocker):
        """
        Test that carnivores only kill and eat herbivores. Does this by checking that
        the number of carnivores are the same after killing as before.
        """
        carni_before = len(self.low.carni_list)
        mocker.patch('random.random', return_value=0)
        self.low.animals_in_cell_eat()
        carni_after = len(self.low.carni_list)
        assert carni_before == carni_after

    def test_if_cell_collect_fitness_for_all_animals(self, initial_lowland):
        """
        Tests if cell can collect fitness for all animals and return them
        in a list.
        """
        num_animals_in_cell = len(self.low.herbi_list + self.low.carni_list)
        fitness_herb_list = self.low.collect_fitness_age_weight_herbi()[0]
        fitness_carn_list = self.low.collect_fitness_age_weight_carni()[0]
        assert len(fitness_herb_list + fitness_carn_list) == num_animals_in_cell
        for fitness_herb in fitness_herb_list:
            assert 0 <= fitness_herb <= 1
        for fitness_carn in fitness_carn_list:
            assert 0 <= fitness_carn <= 1

    def test_if_cell_collect_age_for_all_animals(self, initial_lowland):
        """
        Tests if cell can collect age for all animals and return them in
        a list.
        """
        num_animals_in_cell = len(self.low.herbi_list + self.low.carni_list)
        age_herb_list = self.low.collect_fitness_age_weight_herbi()[1]
        age_carn_list = self.low.collect_fitness_age_weight_carni()[1]
        assert len(age_herb_list + age_carn_list) == num_animals_in_cell
        for age in age_herb_list + age_carn_list:
            assert age >= 0

    def test_if_cell_collect_weight_for_all_animals(self, initial_lowland):
        """
        Test if cell can collect age for all animals and return them in
        a list.
        """
        num_animals_in_cell = len(self.low.herbi_list + self.low.carni_list)
        weight_herb_list = self.low.collect_fitness_age_weight_herbi()[2]
        weight_carn_list = self.low.collect_fitness_age_weight_carni()[2]
        assert len(weight_herb_list + weight_carn_list) == num_animals_in_cell
        for weight in weight_herb_list + weight_carn_list:
            assert weight > 0

    def test_herbivores_eaten(self, initial_lowland, mocker):
        """
        Tests that carnivores eat herbivores by check that the number of
        herbivores are lower after eating.
        """
        mocker.patch('random.random', return_value=0)
        herbi_before = len(self.low.herbi_list)
        self.low.animals_in_cell_eat()
        herbi_after = len(self.low.herbi_list)
        assert herbi_before > herbi_after

    def test_weight_gain_eat(self, initial_lowland, mocker):
        """
        Check that animals weights more after eating. First find the average of weight of
        herbivores and carnivores before eating, then the weight of both after eating.
        The first test checks that herbivores gain weight. The second test checks that
        carnivores gain weight. Thus both species must be able to eat for the test to pass.
        """
        sum_weight_herbi_before = 0
        for herbi in self.low.herbi_list:
            sum_weight_herbi_before += herbi.weight
        av_herbi_before = sum_weight_herbi_before/len(self.low.herbi_list)

        sum_weight_carni_before = 0
        for carni in self.low.carni_list:
            sum_weight_carni_before += carni.weight
        av_carni_before = sum_weight_carni_before/len(self.low.carni_list)

        mocker.patch('random.random', return_value=0.03)
        # Makes sure some herbivores, but not all, are eaten.
        self.low.animals_in_cell_eat()
        sum_weight_herbi_after = 0
        for herbi in self.low.herbi_list:
            sum_weight_herbi_after += herbi.weight
        av_herbi_after = sum_weight_herbi_after/len(self.low.herbi_list)
        sum_weight_carni_after = 0
        for carni in self.low.carni_list:
            sum_weight_carni_after += carni.weight
        av_carni_after = sum_weight_carni_after/len(self.low.carni_list)

        assert av_herbi_before < av_herbi_after
        assert av_carni_before < av_carni_after

    def test_set_params_raises_keyerror(self, initial_lowland):
        """
        Check that the method set_params raises a keyerror when given an
        illegal key.
        """
        with pytest.raises(KeyError):
            self.low.set_params({'g_max': 200.0})

    def test_set_params_cell(self, initial_lowland):
        """Tests that it is possible to update parameters for cell."""
        f_max_before = self.low.get_params()['f_max']
        self.low.set_params({'f_max': 900.0})
        f_max_after = self.low.get_params()['f_max']
        assert f_max_before != f_max_after


class TestDesert:

    @pytest.fixture()
    def initial_desert(self):
        """
        Makes a single cell with animals to use as test-cell for desert-class.
        """
        animals = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                   {'species': 'Herbivore', 'age': 40, 'weight': 20},
                   {'species': 'Herbivore', 'age': 2, 'weight': 8},
                   {'species': 'Carnivore', 'age': 30, 'weight': 8},
                   {'species': 'Carnivore', 'age': 5, 'weight': 3.5},
                   {'species': 'Carnivore', 'age': 37, 'weight': 5.7}
                   ]
        self.desert = Desert(animals_list=animals)

    def test_no_herbs(self, initial_desert, mocker):
        """Tests that herbivores can't find food in the desert.
        """
        sum_weight_before = 0
        for herbi in self.desert.herbi_list:
            sum_weight_before += herbi.weight

        mocker.patch('random.random', return_value=1)  # Makes sure no herbis are killed
        self.desert.animals_in_cell_eat()
        sum_weight_after = 0
        for herbi in self.desert.herbi_list:
            sum_weight_after += herbi.weight
        assert sum_weight_before == sum_weight_after

    def test_only_carnivores_kill(self, initial_desert, mocker):
        """
        Test that only carnivores kill and eat other animals. Does so by
        checking that the number of carnivores stay constant, while the number
        of herbivores decreases.
        """
        herbi_before = len(self.desert.herbi_list)
        carni_before = len(self.desert.carni_list)
        mocker.patch('random.random', return_value=0.01)  # Makes sure some herbis are killed
        self.desert.animals_in_cell_eat()
        herbi_after = len(self.desert.herbi_list)
        carni_after = len(self.desert.carni_list)
        assert carni_before == carni_after
        assert herbi_before > herbi_after


class TestHighland:

    def test_make_highland_instance(self):
        """
        Makes sure it is possible to make a Highland-instance.
        """
        high = Highland()
        assert isinstance(high, Highland)

    def test_default_f_max(self):
        """Test that default value for f_max is 300.0"""
        high = Highland()
        params = high.get_params()
        assert params['f_max'] == 300.0

    def test_animal_eat_rest_of_fodder_in_cell(self):
        """
        Test that herbivore eats the remainder of fodder in cell, even though
        it is less that what it wants to eat.
        Herbivore wants to eat an amount F=10.0.
        Will set f_max in cell to 8.0 and calculate the gain of weight for
        the herbivore when eating fodder=8.0. Weight calculated should be equal
        to the weight of the herbivore.
        """
        animal = [{'species': 'Herbivore', 'age': 2, 'weight': 20}]
        high = Highland(animals_list=animal)
        high.set_params({'f_max': 8.0})
        high.animals_in_cell_eat()
        weight_after_eaten = 20 + 0.9*8.0
        assert high.herbi_list[0].weight == weight_after_eaten


class TestWater:

    def test_make_highland_instance(self):
        """
        Makes sure it is possible to make a Water-instance.
        """
        w = Water()
        assert isinstance(w, Water)
