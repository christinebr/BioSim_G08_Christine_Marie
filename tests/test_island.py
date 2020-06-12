# -*- coding: utf-8 -*-

from biosim.island import TheIsland
from biosim.cell import Highland
import pytest


class TestingTheIsland:

    @pytest.fixture()
    def initial_island(self):
        """
        Makes a simple test-model to use in tests
        Returns
        -------
        A simple test-model
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHWHW
                            WLDLW
                            WWWWW"""
        test_animals = [{'loc': (2, 3),
                         'pop': [{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 35} for _ in range(200)]
                        + [{'species': 'Carnivore',
                            'age': 5,
                            'weight': 20} for _ in range(20)]}
                        ]

        self.island = TheIsland(landscape_of_cells=test_island, animals_on_island=test_animals)
        herbis, carnis = self.island.give_animals_in_cell(2,3)
        self.animals = herbis + carnis
        return self.island, self.animals

    @pytest.fixture()
    def start_point_migration(self):
        """
        Makes a simple test-model to use in tests
        Returns
        -------
        A simple test-model
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHDHW
                            WLDLW
                            WWWWW"""
        test_animals = [{'loc': (3, 3),
                         'pop': [{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 35} for _ in range(200)]
                        + [{'species': 'Carnivore',
                            'age': 5,
                            'weight': 20} for _ in range(20)]}
                        ]

        self.isl_mig = TheIsland(landscape_of_cells=test_island,
                                 animals_on_island=test_animals)
        return self.isl_mig

    def test_if_check_size(self):
        """
        Tests if the island class raises a ValueError if given an island with
        different lengths of the lines
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHW
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)

    def test_if_valueerror_if_not_island(self):
        """
        Tests if the island class raises a ValueError if given an island without
        water around the edges
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHWH
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)

    def test_not_possible_give_illegal_lanscape(self):
        """
        Tests if the island class raises a ValueError if given an island with
        a illegal type of landscape.
        """
        test_island = """\
                            WWWWW
                            WLLLW
                            WHHOW
                            WLDLW
                            WWWWW"""

        with pytest.raises(ValueError):
            TheIsland(test_island)

    def test_that_number_of_animals_is_updated(self, initial_island, mocker):
        """
        Tests that number of animals before the year starts is updated by the end of the year.
        """
        mocker.patch('random.random', return_value=0)
        # Makes sure animals are born and killed but do not die
        num_animals_before, h, c = self.island.total_num_animals_on_island()
        self.island.annual_cycle()
        num_animals_after, h, c = self.island.total_num_animals_on_island()
        assert num_animals_after != num_animals_before

    def test_animals_eat(self, initial_island):
        """Check that the class can make the animals gain weight by eating."""
        sum_weight_before = 0
        for animal in self.animals:
            sum_weight_before += animal.weight
        self.island.all_animals_eat()
        sum_weight_after = 0
        for animal in self.animals:
            sum_weight_after += animal.weight
        assert sum_weight_before < sum_weight_after

    def test_animals_procreate(self, initial_island, mocker):
        """Check that animals on island procreate"""
        island = self.island
        num_animals_before = island.total_num_animals_on_island()
        mocker.patch('random.random', return_value=0) # Makes sure animals gives birth
        island.animals_procreate()
        num_animals_after = island.total_num_animals_on_island()
        assert num_animals_before < num_animals_after

    def test_loss_of_weight(self, initial_island):
        """Check that all animals losses weight"""
        sum_weight_before = 0
        for animal in self.animals:
            sum_weight_before += animal.weight
        self.island.all_animals_losses_weight()
        sum_weight_after = 0
        for animal in self.animals:
            sum_weight_after += animal.weight
        assert sum_weight_before > sum_weight_after

    def test_death(self, initial_island, mocker):
        """Tests that animals die."""
        island = self.island
        mocker.patch('random.random', return_value=0.9) # makes sure not all animals die
        self.animals[3].weight = 0 # Makes sure at least one animal dies
        num_animals_before = island.total_num_animals_on_island()
        island.animals_die()
        assert num_animals_before > island.total_num_animals_on_island()

    def test_aging(self, initial_island):
        """Tests that all animals age one year."""
        animals = self.animals
        sum_age_before = 0
        for animal in animals:
            sum_age_before += animal.age
        self.island.all_animals_age()
        sum_age_after = 0
        for animal in animals:
            sum_age_after += animal.age
        assert sum_age_before + len(animals) == sum_age_after

    def test_migration_west(self, start_point_migration, mocker):
        """
        Check that animals migrate westward. Makes everyone migrate westward, then check that the
        original position is empty and all animals has gone to the nwest.
        """
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='West')
        # makes sure they migrate to the same cell
        number_of_animals_before = self.isl_mig.total_num_animals_on_island()[0]
        # All animals are in the first cell at the beginning
        self.isl_mig.migration()
        herbis, carnis = self.isl_mig.give_animals_in_cell(3, 3)
        number_old_cell = len(herbis + carnis)
        herbis, carnis = self.isl_mig.give_animals_in_cell(3, 2)
        number_new_cell = len(herbis + carnis)
        assert number_old_cell == 0
        assert number_new_cell == number_of_animals_before

    def test_migration_east(self, start_point_migration, mocker):
        """
        Check that animals migrate to the east. Makes everyone migrate eastward, then check that
        the original position is empty and all animals has gone to the east.
        """
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='East')  # makes sure they migrate to the same cell
        number_of_animals_before = self.isl_mig.total_num_animals_on_island()[0]
        # All animals are in the first cell at the beginning
        isl = self.isl_mig.migration()
        herbis1, carnis1 = self.isl_mig.give_animals_in_cell(3, 3)
        number_old_cell = len(herbis1 + carnis1)
        herbis, carnis = self.isl_mig.give_animals_in_cell(3, 4)
        number_new_cell = len(herbis + carnis)
        assert number_old_cell == 0
        assert number_new_cell == number_of_animals_before

    def test_migration_south(self, start_point_migration, mocker):
        """
        Check that animals migrate southward. Makes everyone migrate southward, then check that
        the original position is empty and all animals has gone to the south.
        """
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='South')
        # makes sure they migrate to the same cell
        number_of_animals_before = self.isl_mig.total_num_animals_on_island()[0]
        # All animals are in the first cell at the beginning
        isl = self.isl_mig.migration()
        herbis1, carnis1 = self.isl_mig.give_animals_in_cell(3, 3)
        number_old_cell = len(herbis1 + carnis1)
        herbis, carnis = self.isl_mig.give_animals_in_cell(4, 3)
        number_new_cell = len(herbis + carnis)
        assert number_old_cell == 0
        assert number_new_cell == number_of_animals_before

    def test_migration_north(self, start_point_migration, mocker):
        """
        Check that animals migrate northward. Makes everyone migrate northward, then check that
        the original position is empty and all animals has gone to the north. (Yes, it is was
        necessary to test for all directions.)
        """
        mocker.patch('random.random', return_value=0)  # Makes sure all animals migrate
        mocker.patch('random.choice', return_value='North')
        # makes sure they migrate to the same cell
        number_of_animals_before = self.isl_mig.total_num_animals_on_island()[0]
        # All animals are in the first cell at the beginning
        isl = self.isl_mig.migration()
        herbis1, carnis1 = self.isl_mig.give_animals_in_cell(3, 3)
        number_old_cell = len(herbis1 + carnis1)
        herbis, carnis = self.isl_mig.give_animals_in_cell(2, 3)
        number_new_cell = len(herbis + carnis)
        assert number_old_cell == 0
        assert number_new_cell == number_of_animals_before

    def test_not_migrate_water(self, initial_island, mocker):
        """
        Checking that animals are not allowed to migrate into a water-cell.
        Does so by trying to send all animals into the water-cell, then checking that there are no
        animals in the water-cell, and that all animals remain in the old cell.

        Be aware this test will pass if migration is not possible, so try the test that checks that
        migration can happen at al first.
        """
        island = self.island
        mocker.patch('random.random', return_value=0)  # Makes sure all animals tries to migrate
        mocker.patch('random.choice', return_value='North')
        # makes sure all animals tries to migrate to the lake in the middle of the test_island
        number_of_animals_before = len(self.animals)
        # All animals are in the first cell at the beginning
        island.migration()
        herbis, carnis = island.give_animals_in_cell(1,3)
        number_new_cell = len(herbis + carnis)
        herbis, carnis = island.give_animals_in_cell(2,3)
        number_old_cell = len(herbis + carnis)
        assert number_new_cell == 0
        assert number_old_cell == number_of_animals_before

    def test_possible_get_fitness(self, initial_island):
        """
        Tests that it is possible to get a list of the fitnesses of the animals.
        """
        num_animals_in_cell = len(self.animals)
        fitness_herb_list = self.island.collect_fitness_age_weight_herbi()[0]
        fitness_carn_list = self.island.collect_fitness_age_weight_carni()[0]
        assert len(fitness_herb_list + fitness_carn_list) == num_animals_in_cell
        for fitness_herb in fitness_herb_list:
            assert 0 <= fitness_herb <= 1
        for fitness_carn in fitness_carn_list:
            assert 0 <= fitness_carn <= 1

    def test_possible_get_age(self, initial_island):
        """
        Tests that it is possible to get a list of the ages of the animals.
        """
        num_animals_in_cell = len(self.animals)
        age_herb_list = self.island.collect_fitness_age_weight_herbi()[1]
        age_carn_list = self.island.collect_fitness_age_weight_carni()[1]
        assert len(age_herb_list + age_carn_list) == num_animals_in_cell
        for age in age_herb_list + age_carn_list:
            assert age >= 0

    def test_possible_get_weight(self, initial_island):
        """
        Tests that it is possible to get a list of the weights of the animals.
        """
        num_animals_in_cell = len(self.animals)
        age_herb_list = self.island.collect_fitness_age_weight_herbi()[2]
        age_carn_list = self.island.collect_fitness_age_weight_carni()[2]
        assert len(age_herb_list + age_carn_list) == num_animals_in_cell
        for age in age_herb_list + age_carn_list:
            assert age >= 0

    def test_complete_cycle(self, initial_island, mocker):
        """
        Checks that all steps in the annual cycle are made.

        Todo: Do this later, possibly by statistic testing.
        """
        pass